#!/usr/bin/env python3
"""Wiederholbare Kontrasttests; künstliche Daten ausschließlich in TemporaryDirectory.

Kein Zugriff auf ein Unternehmen, keine Netzaufrufe und kein Betriebsnachweis.
Aufruf: python3 09_arbeitsjournal/selbsttest.py
"""
from __future__ import annotations
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('journalpruefer', HERE / 'pruefen.py')
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
START = '11111111-1111-4111-8111-111111111111'
TASK = '22222222-2222-4222-8222-222222222222'
EVENT = '33333333-3333-4333-8333-333333333333'
OTHER = '44444444-4444-4444-8444-444444444444'


def dump(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


class JournalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.old_cwd = Path.cwd()
        self.tmp = tempfile.TemporaryDirectory(prefix='fachjournal_test_')
        os.chdir(self.tmp.name)
        P.git('init', '-q')
        P.git('config', 'user.name', 'Temporäre Prüffigur')
        P.git('config', 'user.email', 'pruefung@example.invalid')
        P.git('config', 'core.fileMode', 'true')
        for version in (1, 2):
            self.write(f'09_arbeitsjournal/schema_v{version}.json', (HERE / f'schema_v{version}.json').read_text())
        self.write('README.md', '# Einstieg\n\n## Ziel\n')
        self.write('arbeit.md', '# Alter Arbeitsstand\n')
        self.initial = {
            'schema_version': 1, 'eintrag_id': START, 'auftrag_id': TASK,
            'uebergeordneter_auftrag': None, 'ereignis': 'beginn',
            'zeitpunkt': '2026-01-01T09:00:00Z',
            'akteur': {'bezeichnung': 'Temporäre Prüffigur', 'typ': 'ki', 'rolle': 'Selbsttest'},
            'vorgaenger': [], 'korrektur_fuer': [],
            'auftrag': {'quelle': 'README.md', 'zusammenfassung': 'Künstlicher Testauftrag',
                        'erlaubter_umfang': ['Lokaler Kontrasttest'], 'ausgeschlossen': ['Echte Facharbeit']},
            'basis': {'commit': 'a' * 40, 'quellen': ['README.md']},
            'taetigkeiten': [], 'ergebnisse': [], 'aenderungen': [], 'pruefungen': [],
            'entscheidungen': [], 'offen': [],
            'fortsetzung': {'verfolgungsort': 'README.md', 'naechste_handlung': 'Testen', 'einstieg': ['README.md']},
            'grenzen': ['Keine echten Daten']}
        self.write(self.path(START), dump(self.initial))
        self.base_commit = self.commit('Künstliche Basis')
        self.base = P.tree(self.base_commit)
        self.entry = copy.deepcopy(self.initial)
        self.entry.update(schema_version=2, eintrag_id=EVENT, ereignis='zwischenstand',
                          zeitpunkt='2026-01-01T10:00:00Z', vorgaenger=[START], taetigkeiten=['Künstlicher Durchlauf'])
        self.entry['basis']['commit'] = self.base_commit
        self.entry['arbeitszeitraum'] = {'von': '2026-01-01T09:10:00Z', 'bis': '2026-01-01T09:59:00Z',
                                        'zeitquelle': 'systemuhr', 'hinweis': 'Künstliche Zeit für die Kontrastprobe'}
        self.entry['pruefungen'] = [{'verfahren': 'Beispielprüfung', 'ergebnis': 'bestanden', 'bezug': ['README.md'],
                                    'grenze': 'Künstliches Ergebnis', 'zeitpunkt': '2026-01-01T09:50:00Z'}]

    def tearDown(self) -> None:
        os.chdir(self.old_cwd)
        self.tmp.cleanup()

    @staticmethod
    def path(eid: str) -> str:
        return f'09_arbeitsjournal/eintraege/2026/{eid}.json'

    @staticmethod
    def write(path: str, text: str) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    @staticmethod
    def commit(message: str) -> str:
        P.git('add', '.')
        P.git('commit', '-q', '-m', message)
        return P.git('rev-parse', 'HEAD').decode().strip()

    def evaluate(self, entry: dict | None = None, raw: str | None = None) -> list[str]:
        entry = entry or self.entry
        self.write(self.path(entry['eintrag_id']), raw if raw is not None else dump(entry))
        P.git('add', '.')
        target = P.tree(P.git('write-tree').decode().strip())
        entries, errors = P.inspect(target, set(target) - set(self.base))
        return errors + P.check_delta(self.base, target, entries, 'HEAD')

    def bad(self, fragment: str) -> None:
        errors = self.evaluate()
        self.assertTrue(any(fragment in e for e in errors), errors)

    def change(self, text: str = '# Neuer Arbeitsstand\n') -> None:
        self.write('arbeit.md', text)
        sha = P.git('hash-object', '-w', 'arbeit.md').decode().strip()
        self.entry['aenderungen'] = [{'pfad': 'arbeit.md', 'vorher': self.base['arbeit.md'][1], 'nachher': sha,
                                     'modus_vorher': '100644', 'modus_nachher': '100644'}]

    def test_01_valid_v2(self): self.assertEqual([], self.evaluate())
    def test_02_legacy_v1_unchanged(self): self.assertEqual([], P.inspect(self.base, set())[1])
    def test_03_exact_before_after(self):
        self.change(); self.assertEqual([], self.evaluate())
    def test_04_wrong_before(self):
        self.change(); self.entry['aenderungen'][0]['vorher'] = 'f' * 40; self.bad('Vorher-Wert')
    def test_05_wrong_after(self):
        self.change(); self.entry['aenderungen'][0]['nachher'] = 'f' * 40; self.bad('Nachher-Wert')
    def test_06_missing_basis(self):
        self.entry['basis']['commit'] = 'f' * 40; self.bad('Herkunft nicht prüfbar')
    def test_07_tree_not_commit(self):
        self.entry['basis']['commit'] = P.git('rev-parse', 'HEAD^{tree}').decode().strip(); self.bad('Basis ist kein')
    def test_08_unreported_change(self):
        self.write('arbeit.md', 'nicht berichtet'); self.bad('Arbeitsbericht')
    def test_09_historic_event_changed(self):
        self.initial['grenzen'] = ['Unzulässige Umschreibung']; self.write(self.path(START), dump(self.initial)); self.bad('verändert/entfernt')
    def test_10_historic_event_deleted(self):
        Path(self.path(START)).unlink(); self.bad('verändert/entfernt')
    def test_11_schema_v1_changed(self):
        f=Path('09_arbeitsjournal/schema_v1.json'); f.write_text(f.read_text()+' '); self.bad('verändert/entfernt')
    def test_12_schema_v2_changed(self):
        f=Path('09_arbeitsjournal/schema_v2.json'); f.write_text(f.read_text()+' '); self.bad('verändert/entfernt')
    def test_13_no_timezone(self):
        self.entry['zeitpunkt']='2026-01-01T10:00:00'; self.bad('Schemafehler')
    def test_14_invalid_calendar(self):
        self.entry['zeitpunkt']='2026-02-30T10:00:00Z'; self.bad('Schemafehler')
    def test_15_unknown_offset(self):
        self.entry['zeitpunkt']='2026-01-01T10:00:00-00:00'; self.bad('Schemafehler')
    def test_16_test_in_future_of_record(self):
        self.entry['pruefungen'][0]['zeitpunkt']='2026-01-01T11:00:00Z'; self.bad('Prüfzeit')
    def test_17_reversed_period(self):
        self.entry['arbeitszeitraum']['bis']='2026-01-01T08:00:00Z'; self.bad('Arbeitsende')
    def test_18_period_after_record(self):
        self.entry['arbeitszeitraum']['bis']='2026-01-01T11:00:00Z'; self.bad('Arbeitszeitraum')
    def test_19_unknown_clock_precise_period(self):
        self.entry['arbeitszeitraum']['zeitquelle']='unbekannt'; self.bad('Unbekannte Zeitquelle')
    def test_20_unknown_period_allowed(self):
        self.entry['arbeitszeitraum'].update(von=None,bis=None,zeitquelle='unbekannt'); self.assertEqual([],self.evaluate())
    def test_21_missing_test_time(self):
        del self.entry['pruefungen'][0]['zeitpunkt']; self.bad('Schemafehler')
    def test_22_duplicate_json_key(self):
        errors=self.evaluate(raw=dump(self.entry).replace('"schema_version": 2','"schema_version": 2, "schema_version": 2'))
        self.assertTrue(any('Doppelter JSON' in e for e in errors),errors)
    def test_23_unknown_version(self):
        self.entry['schema_version']=99; self.bad('Schemafassung')
    def test_24_whitespace_only(self):
        self.entry['auftrag']['zusammenfassung']='  '; self.bad('Leerzeichen')
    def test_25_traversal_path(self):
        self.change(); self.entry['aenderungen'][0]['pfad']='../arbeit.md'; self.bad('Änderungspfad')
    def test_26_credential_url(self):
        self.entry['ergebnisse']=['https://name:secret@example.invalid/a']; self.bad('unsicherer Repository-Verweis')
    def test_27_missing_reference(self):
        self.entry['ergebnisse']=['fehlend.md']; self.bad('fehlender oder unsicherer')
    def test_28_bad_anchor(self):
        self.entry['ergebnisse']=['README.md#fehlt']; self.bad('Abschnittsziel')
    def test_29_good_anchor(self):
        self.entry['ergebnisse']=['README.md#ziel']; self.assertEqual([],self.evaluate())
    def test_30_self_reference(self):
        self.entry['vorgaenger']=[EVENT]; self.bad('Selbstreferenz')
    def test_31_missing_predecessor(self):
        self.entry['vorgaenger']=[OTHER]; self.bad('Ereignis fehlt')
    def test_32_duplicate_change_path(self):
        self.change(); second=copy.deepcopy(self.entry['aenderungen'][0]); second['vorher']='f'*40; self.entry['aenderungen'].append(second); self.bad('mehrfacher Änderungspfad')
    def test_33_false_no_change(self):
        self.change(); self.entry['aenderungen'][0]['nachher']=self.entry['aenderungen'][0]['vorher']; self.bad('Änderung ohne')
    def test_34_mode_only(self):
        Path('arbeit.md').chmod(0o755); h=self.base['arbeit.md'][1]
        self.entry['aenderungen']=[{'pfad':'arbeit.md','vorher':h,'nachher':h,'modus_vorher':'100644','modus_nachher':'100755'}]
        self.assertEqual([],self.evaluate())
    def test_35_mode_false(self):
        self.change(); self.entry['aenderungen'][0]['modus_nachher']='100755'; self.bad('Nachher-Wert')
    def test_36_downgrade(self):
        self.entry['schema_version']=1; del self.entry['arbeitszeitraum']; self.entry['pruefungen']=[]; self.bad('muss Schema v2')
    def test_37_earlier_predecessor_order(self):
        self.entry['zeitpunkt']='2026-01-01T08:00:00Z'; self.entry['arbeitszeitraum'].update(von=None,bis=None,zeitquelle='unbekannt');self.entry['pruefungen']=[];self.bad('liegt nach')
    def test_38_parent_missing(self):
        self.entry['uebergeordneter_auftrag']=OTHER;self.bad('Elternauftrag fehlt')
    def test_39_published_intermediate(self):
        self.change('# Zwischenstand\n'); self.assertEqual([],self.evaluate()); prior=self.commit('Zwischenbericht')
        old=self.entry['aenderungen'][0]['nachher']; self.entry['eintrag_id']=OTHER;self.entry['vorgaenger']=[EVENT];self.entry['basis']['commit']=prior
        self.entry['zeitpunkt']='2026-01-01T11:00:00Z';self.entry['arbeitszeitraum']['bis']='2026-01-01T10:59:00Z'
        self.change('# Endstand\n'); self.entry['aenderungen'][0]['vorher']=old
        self.assertEqual([],self.evaluate())
    def test_40_wrong_year_path(self):
        self.entry['zeitpunkt']='2027-01-01T10:00:00Z';self.bad('Ablagepfad')
    def test_41_unknown_time_string(self):
        self.entry['zeitpunkt']='unbekannt';self.bad('Schemafehler')
    def test_42_missing_required_field(self):
        del self.entry['auftrag'];self.bad('Schemafehler')
    def test_43_invalid_json_constant(self):
        errors=self.evaluate(raw=dump(self.entry).replace('"schema_version": 2','"schema_version": NaN'));self.assertTrue(any('Ungültige Zahl' in e for e in errors),errors)
    def test_44_path_control_character(self):
        self.change();self.entry['aenderungen'][0]['pfad']='arbeit\n.md';self.bad('Änderungspfad')
    def test_45_https_reference(self):
        self.entry['ergebnisse']=['https://example.invalid/keine-netzpruefung'];self.assertEqual([],self.evaluate())
    def test_46_deleted_content_reported(self):
        Path('arbeit.md').unlink();self.entry['aenderungen']=[{'pfad':'arbeit.md','vorher':self.base['arbeit.md'][1],'nachher':None,'modus_vorher':'100644','modus_nachher':None}];self.assertEqual([],self.evaluate())


if __name__ == '__main__':
    unittest.main(verbosity=2)
