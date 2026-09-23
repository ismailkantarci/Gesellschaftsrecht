#!/usr/bin/env python3
"""Prüft das Arbeitsjournal und seine Änderungsspur, nicht die fachliche Wahrheit.

Lesen aus einem Git-Baum (oder dem Index) verhindert, dass ungestagte Dateien
versehentlich als veröffentlichter Kandidat geprüft werden. Keine Netzaufrufe.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError:
    sys.exit('FEHLER: jsonschema fehlt. Benötigt: jsonschema==4.26.0')

PREFIX = '09_arbeitsjournal/eintraege/'
SCHEMA = '09_arbeitsjournal/schema_v1.json'
SUPPORTED_VERSIONS = (1, 2)
SHA = re.compile(r'^[0-9a-f]{40}$')


def git(*args: str, data: bytes | None = None) -> bytes:
    p = subprocess.run(['git', *args], input=data, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=False)
    if p.returncode:
        raise ValueError('Git-Befehl fehlgeschlagen: ' + ' '.join(args[:2]) +
                         ' – ' + p.stderr.decode('utf-8', errors='replace').strip())
    return p.stdout


def tree(ref: str) -> dict[str, tuple[str, str]]:
    result = {}
    for item in git('ls-tree', '-r', '-z', ref).split(b'\0'):
        if not item:
            continue
        meta, raw_path = item.split(b'\t', 1)
        mode, typ, sha = meta.decode().split()
        if typ != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Nicht unterstützter Git-Eintrag im Prüfbaum')
        result[raw_path.decode('utf-8')] = (mode, sha)
    return result


def no_duplicates(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Doppelter JSON-Schlüssel: ' + key)
        result[key] = value
    return result


def read_json(sha: str) -> dict:
    raw = git('cat-file', 'blob', sha)
    if len(raw) > 200_000:
        raise ValueError('JSON-Eintrag überschreitet 200 kB')
    result = json.loads(raw.decode('utf-8'), object_pairs_hook=no_duplicates,
                        parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Ungültige Zahl: ' + x)))
    if not isinstance(result, dict):
        raise ValueError('JSON-Wurzel muss ein Objekt sein')
    return result


def safe_path(value: str) -> bool:
    p = PurePosixPath(value)
    return (bool(value) and value != '.' and not p.is_absolute() and '..' not in p.parts
            and '\\' not in value and str(p) == value
            and not any(ord(char) < 32 or ord(char) == 127 for char in value))


def check_reference(ref: str, files: dict, errors: list[str], label: str) -> None:
    parsed = urlsplit(ref)
    if parsed.scheme == 'https' and parsed.netloc and not parsed.username and not parsed.password:
        return  # Externe Erreichbarkeit und Inhalt werden ausdrücklich nicht geprüft.
    path = unquote(parsed.path)
    if parsed.scheme or parsed.netloc or not safe_path(path) or path not in files:
        errors.append(f'{label}: fehlender oder unsicherer Repository-Verweis {ref!r}')
        return
    if parsed.fragment and path.endswith('.md'):
        text = git('cat-file', 'blob', files[path][1]).decode('utf-8')
        anchors = set()
        seen = {}
        for line in text.splitlines():
            match = re.match(r'^#{1,6}\s+(.+?)\s*#*$', line)
            if not match:
                continue
            anchor = re.sub(r'[^\w\-\s]', '', match.group(1).lower())
            anchor = re.sub(r'\s', '-', anchor)
            n = seen.get(anchor, 0)
            seen[anchor] = n + 1
            anchors.add(anchor if n == 0 else f'{anchor}-{n}')
        if unquote(parsed.fragment) not in anchors:
            errors.append(f'{label}: fehlendes Abschnittsziel {ref!r}')



def parsed_time(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError('Zeitangabe ohne Zeitzone')
    return result


def validate_text(value: object) -> None:
    """Leere Pflichtaussagen verhindern; beurteilt nicht ihren Wahrheitsgehalt."""
    if isinstance(value, str) and not value.strip():
        raise ValueError('Pflichttext besteht nur aus Leerzeichen')
    if isinstance(value, dict):
        for child in value.values():
            validate_text(child)
    elif isinstance(value, list):
        for child in value:
            validate_text(child)


def validate_times(entry: dict) -> None:
    recorded = parsed_time(entry['zeitpunkt'])
    period = entry['arbeitszeitraum']
    begin = parsed_time(period['von']) if period['von'] else None
    end = parsed_time(period['bis']) if period['bis'] else None
    if period['zeitquelle'] == 'unbekannt' and (begin is not None or end is not None):
        raise ValueError('Unbekannte Zeitquelle darf keine genaue Arbeitszeit behaupten')
    if begin and end and end < begin:
        raise ValueError('Arbeitsende liegt vor Arbeitsbeginn')
    if (begin and begin > recorded) or (end and end > recorded):
        raise ValueError('Beobachteter Arbeitszeitraum liegt nach seiner Aufzeichnung')
    if entry['ereignis'] == 'beginn' and end is not None:
        raise ValueError('Beginn behauptet bereits ein Arbeitsende')
    for check in entry['pruefungen']:
        when = parsed_time(check['zeitpunkt'])
        if when > recorded or (begin and when < begin) or (end and when > end):
            raise ValueError('Prüfzeit liegt außerhalb des berichteten Zeitrahmens')


def inspect(files: dict, new_paths: set[str]) -> tuple[dict, list[str]]:
    errors = []
    if SCHEMA not in files:
        return {}, ['Journal-Schema fehlt']
    validators = {}
    for version in SUPPORTED_VERSIONS:
        schema_path = f'09_arbeitsjournal/schema_v{version}.json'
        if schema_path in files:
            schema = read_json(files[schema_path][1])
            Draft202012Validator.check_schema(schema)
            validators[version] = Draft202012Validator(schema, format_checker=FormatChecker())
    entries = {}
    for path, (mode, sha) in sorted(files.items()):
        if not path.startswith(PREFIX):
            continue
        if mode != '100644' or not path.endswith('.json'):
            errors.append(f'Unzulässige Ereignisdatei: {path}')
            continue
        try:
            entry = read_json(sha)
            version = entry.get('schema_version')
            if type(version) is not int or version not in validators:
                raise ValueError('Unbekannte oder fehlende Schemafassung')
            violations = sorted(validators[version].iter_errors(entry), key=lambda e: str(e.path))
            if violations:
                errors.extend(f'{path}: Schemafehler bei {list(e.path)}: {e.message}' for e in violations)
                continue
            eid = entry['eintrag_id']
            time = datetime.fromisoformat(entry['zeitpunkt'].replace('Z', '+00:00'))
            if time.tzinfo is None or time.utcoffset() is None:
                raise ValueError('Zeitpunkt ohne Zeitzone')
            expected = PREFIX + f'{time.year}/{eid}.json'
            if path != expected or eid in entries:
                errors.append(f'Uneindeutige ID oder falscher Ablagepfad: {path}')
                continue
            if entry['uebergeordneter_auftrag'] == entry['auftrag_id']:
                errors.append(f'{path}: Auftrag darf nicht sein eigener Elternauftrag sein')
            if path in new_paths:
                validate_text(entry)
            if version == 2:
                validate_times(entry)
            change_paths = set()
            for change in entry['aenderungen']:
                cp = change['pfad']
                if cp in change_paths:
                    errors.append(f'{path}: mehrfacher Änderungspfad {cp!r}')
                change_paths.add(cp)
                if not safe_path(cp) or cp.startswith(PREFIX):
                    errors.append(f'{path}: unzulässiger Änderungspfad {cp!r}')
                if (change['vorher'] == change['nachher'] and
                        (version == 1 or change['modus_vorher'] == change['modus_nachher'])):
                    errors.append(f'{path}: Änderung ohne geänderten Blobwert')
            refs = ([entry['auftrag']['quelle'], entry['fortsetzung']['verfolgungsort']] +
                    entry['basis']['quellen'] + entry['ergebnisse'] + entry['entscheidungen'] +
                    entry['fortsetzung']['einstieg'])
            refs += [ref for check in entry['pruefungen'] for ref in check['bezug']]
            # Alte Verweise sind historisch; nur neue Berichte gegen den Kandidaten prüfen.
            if path in new_paths:
                for ref in refs:
                    check_reference(ref, files, errors, path)
            entries[eid] = (entry, path)
        except (ValueError, UnicodeError) as exc:
            errors.append(f'{path}: {exc}')
    starts = {}
    for eid, (entry, path) in entries.items():
        if entry['ereignis'] == 'beginn':
            task = entry['auftrag_id']
            if task in starts:
                errors.append(f'{path}: mehrere Beginn-Ereignisse desselben Auftrags')
            starts[task] = eid
    for eid, (entry, path) in entries.items():
        if entry['auftrag_id'] not in starts:
            errors.append(f'{path}: Beginn des Auftrags fehlt')
        parent_task = entry['uebergeordneter_auftrag']
        if parent_task is not None and parent_task not in starts:
            errors.append(f'{path}: Elternauftrag fehlt')
        for prev in entry['vorgaenger'] + entry['korrektur_fuer']:
            if prev not in entries:
                errors.append(f'{path}: referenziertes Ereignis fehlt: {prev}')
                continue
            other = entries[prev][0]
            if prev == eid:
                errors.append(f'{path}: Selbstreferenz')
            if prev in entry['vorgaenger'] and other['auftrag_id'] != entry['auftrag_id']:
                errors.append(f'{path}: Vorgänger gehört zu anderem Auftrag')
            dt = lambda value: datetime.fromisoformat(value.replace('Z', '+00:00'))
            if dt(other['zeitpunkt']) > dt(entry['zeitpunkt']):
                errors.append(f'{path}: Vorgänger/Korrekturziel liegt nach dem Eintrag')
    # Delegationsbeziehungen bilden ebenfalls einen gerichteten, zyklenfreien Graphen.
    parents = {}
    for entry, path in entries.values():
        task = entry['auftrag_id']
        parent = entry['uebergeordneter_auftrag']
        if task in parents and parents[task] != parent:
            errors.append(f'{path}: widersprüchlicher Elternauftrag')
        parents[task] = parent
    for task in parents:
        seen = set()
        current = task
        while current is not None and current in parents:
            if current in seen:
                errors.append('Zyklische Delegation: ' + task)
                break
            seen.add(current)
            current = parents[current]
    visiting, done = set(), set()
    def visit(eid: str) -> None:
        if eid in visiting:
            errors.append('Zyklischer Ereignisbezug: ' + eid)
            return
        if eid in done:
            return
        visiting.add(eid)
        for prev in entries[eid][0]['vorgaenger'] + entries[eid][0]['korrektur_fuer']:
            if prev in entries:
                visit(prev)
        visiting.remove(eid)
        done.add(eid)
    for eid in entries:
        visit(eid)
    return entries, errors


def check_delta(base: dict, target: dict, entries: dict, history_ref: str | None = None) -> list[str]:
    errors = []
    for path, value in base.items():
        if path.startswith(PREFIX) or re.fullmatch(r'09_arbeitsjournal/schema_v\d+\.json', path):
            if target.get(path) != value:
                errors.append('Veröffentlichter Eintrag oder versioniertes Schema verändert/entfernt: ' + path)
    fresh = [(e, p) for e, p in entries.values() if p not in base]
    origins: dict[str, dict] = {}
    for entry, path in fresh:
        if '09_arbeitsjournal/schema_v2.json' in base and entry['schema_version'] != 2:
            errors.append('Neuer Bericht muss Schema v2 verwenden: ' + path)
        if entry['schema_version'] != 2:
            continue
        try:
            origin = entry['basis']['commit']
            if origin not in origins:
                if git('cat-file', '-t', origin).strip() != b'commit':
                    raise ValueError('Basis ist kein erreichbares Commit-Objekt')
                origins[origin] = tree(origin)
            before_files = origins[origin]
            for change in entry['aenderungen']:
                cp = change['pfad']
                old = before_files.get(cp)
                expected = (change['modus_vorher'], change['vorher'])
                if (old or (None, None)) != expected:
                    errors.append(f'{path}: Vorher-Wert/Modus widerspricht Basis: {cp}')
                new = target.get(cp)
                claimed = (change['modus_nachher'], change['nachher'])
                if (new or (None, None)) != claimed:
                    # Ein bereits veröffentlichter Zwischenbericht darf einen früheren
                    # Stand beschreiben. Seine eigene Einführungsfassung muss ihn belegen.
                    proved = False
                    if history_ref:
                        commits = git('log', '--format=%H', '--diff-filter=A', history_ref, '--', path).decode().splitlines()
                        for commit in commits:
                            snapshot = tree(commit)
                            if snapshot.get(path) == target.get(path) and (snapshot.get(cp) or (None, None)) == claimed:
                                proved = True
                                break
                    if not proved:
                        errors.append(f'{path}: Nachher-Wert/Modus weder im Ziel noch im belegten Zwischenstand: {cp}')
        except (ValueError, OSError) as exc:
            errors.append(f'{path}: Herkunft nicht prüfbar: {exc}')
    changed = {p for p in base.keys() | target.keys()
               if base.get(p) != target.get(p) and not p.startswith(PREFIX)}
    for path in sorted(changed):
        after = target[path][1] if path in target else None
        if not any(c['pfad'] == path and c['nachher'] == after
                   for e, _ in fresh if e['ereignis'] != 'beginn'
                   for c in e['aenderungen']):
            errors.append('Neuer Arbeitsbericht mit passendem Ergebnis-Blob fehlt: ' + path)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis', help='Ausgangscommit oder exakt verifizierter Git-Baum')
    parser.add_argument('--ziel', default='HEAD', help='Commit/Tree oder INDEX für gestagte Dateien')
    parser.add_argument('--uebersicht', action='store_true', help='Letzte Ereignisse je Auftrag ausgeben')
    args = parser.parse_args()
    try:
        git('rev-parse', '--show-toplevel')
        target_ref = (git('write-tree').decode().strip() if args.ziel == 'INDEX' else
                      git('rev-parse', '--verify', args.ziel + '^{tree}').decode().strip())
        files = tree(target_ref)
        base = None
        if args.basis:
            base_ref = git('rev-parse', '--verify', args.basis + '^{tree}').decode().strip()
            base = tree(base_ref)
        new_paths = set(files) - set(base) if base is not None else set()
        entries, errors = inspect(files, new_paths)
        if base is not None:
            history_ref = 'HEAD' if args.ziel == 'INDEX' else args.ziel
            # Reine Baumobjekte haben keine beweisbare Elternhistorie.
            try:
                history_ref = git('rev-parse', '--verify', history_ref + '^{commit}').decode().strip()
            except ValueError:
                history_ref = None
            errors += check_delta(base, files, entries, history_ref)
        if errors:
            for error in errors:
                print('FEHLER: ' + error, file=sys.stderr)
            return 1
        if args.uebersicht:
            referenced = {p for e, _ in entries.values() for p in e['vorgaenger']}
            for eid, (e, path) in sorted(entries.items(), key=lambda pair: parsed_time(pair[1][0]['zeitpunkt'])):
                if eid not in referenced:
                    print(f"{e['auftrag_id']} | {e['ereignis']} | {e['zeitpunkt']} | {path}")
                    print('  Nächste Handlung: ' + e['fortsetzung']['naechste_handlung'])
        from datetime import timezone
        print('Prüfzeit UTC: ' + datetime.now(timezone.utc).isoformat(timespec='seconds'))
        print(f'OK: {len(entries)} Einträge; Prüfbaum {target_ref}.')
        print('Änderungs-/Append-only-Prüfung: ' + ('durchgeführt.' if args.basis else 'NICHT durchgeführt (keine Basis).'))
        print('Keine Aussage über fachliche Wahrheit, reale Wirksamkeit oder unbeobachtete Zugriffe.')
        return 0
    except (ValueError, OSError, RecursionError, SchemaError) as exc:
        print('FEHLER: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
