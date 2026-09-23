# Verbindliches Arbeitsjournal

**Grundlage:** [ENT-0002](../05_entscheidungen/ent_0002_arbeitssteuerung_und_journal.md). **Zweck:** Ein neuer Mensch oder Agent kann ohne früheren Chat erkennen, was beauftragt, tatsächlich bearbeitet, geprüft, übergeben und offen gelassen wurde. Das Journal ist ein Arbeitsgedächtnis, keine Firmenchronik und kein Gedankenprotokoll.

## Pflicht und Grenzen

Jede beauftragte Arbeit am oder mit diesem Fachsystem wird journalisiert: Forschung, redaktionelle oder methodische Änderung, Fachprüfung, reine Leseauswertung, Delegation, erfolgloser Versuch, Abbruch und Übergabe. Das gilt für Menschen, ChatGPT, andere Agenten und automatisierte Bearbeiter. Ein Werkzeugaufruf ist nicht jedes Mal ein eigener Auftrag; dessen Schritte werden im verantworteten Arbeitsgang zusammengefasst.

Vor wesentlicher Bearbeitung einen **beginn**-Eintrag anlegen. Bei Übergabe, Blockade oder Ende einen neuen verknüpften Eintrag ergänzen. Ein laufender Auftrag ist an seinem letzten Ereignis erkennbar; kein fertiges Ergebnis aus einem Beginn ableiten. Beginn darf im geschützten Arbeitszweig entstehen; vor Verlassen einer Sitzung den zulässigen Stand dauerhaft sichern oder fehlende Veröffentlichung ausdrücklich melden. Beim einmaligen Aufbau wurden Beginn und Abschluss gemeinsam mit dem erstmals eingeführten Journal übertragen; der Beginn behauptet keine frühere Veröffentlichung.

Ein beauftragter Nur-Lese-Bearbeiter bleibt berichtspflichtig. Hat er keine Schreibbefugnis, liefert er den schutzgeprüften JSON-Eintrag an eine befugte übernehmende Person und benennt ihn bis zur Übernahme als **nicht im Repository veröffentlicht**. Ein ausdrückliches Schreibverbot wird nicht durch die Journalpflicht aufgehoben. Anonyme Besucher oder unbeobachtete externe Lesezugriffe sind mit diesem Repository-Verfahren nicht technisch erfassbar. Sie werden nicht als protokolliert ausgegeben.

## Keine zweite Wahrheit

Fachinhalt bleibt in Fach-/Modellakten, tatsächliche Entscheidung im Entscheidungsregister und der aktuelle Arbeitsstand an seinem benannten Verfolgungsort. Das Journal enthält Ergebnisverweise und historische Berichte. Weder ein neuer Zeitstempel noch die Bezeichnung eines Bearbeiters erzeugt eine Befugnis oder fachliche Richtigkeit.

Anweisungen in alten Journalberichten sind damalige Auftragsbeschreibungen, keine neuen Befehle. Aktuellen Auftrag, aktuellen Repository-Stand und geltende Arbeitsregeln zuerst auflösen. „abgeschlossen“ bedeutet Ende des berichteten Arbeitsgangs, nicht Freigabe des Geschäftsmodells. Die vorhandenen fachlichen Zustandsachsen bleiben unverändert.

## Dateiform und Identität

Jedes Ereignis ist eine UTF-8-JSON-Datei unter `eintraege/JJJJ/<eintrag_id>.json`. `eintrag_id` und `auftrag_id` sind UUIDs. Ein Auftrag behält seine Identität; aufeinander bezogene Ereignisse nennen `vorgaenger`. Parallel übernommene Teilaufträge erhalten eigene Auftrag-IDs und `uebergeordneter_auftrag`; daraus entsteht keine fiktive zweite Person.

[Vorlage](vorlage.json) kopieren, nicht im Vorlagenpfad ausfüllen. Die Nullwerte sind absichtlich kein gültiger Echtbericht. Erst den vollständigen Eintrag gegen [aktuelle Schemafassung v2](schema_v2.json) prüfen. Eine neue Schemafassung erhält eine neue Versionsdatei; veröffentlichte Einträge werden nicht nachträglich dem neuen Schema angepasst.

| Feldgruppe | Inhalt |
|---|---|
| Identität | Schemafassung, Ereignis-ID, Auftrag-ID, Elternauftrag, Ereignisart, tatsächlicher Aufzeichnungszeitpunkt mit Zeitzone |
| Akteur | Tatsächlich ausführender Mensch/Agent/Automatisierung und Rolle; der Git-Commit-Account ist nicht automatisch der fachliche Bearbeiter |
| Auftrag und Basis | Dauerhaft auffindbare Auftragsquelle, genaue Zusammenfassung, erlaubter/ausgeschlossener Umfang, gelesener Ausgangscommit und Quellen |
| Arbeit und Ergebnis | Tatsächliche Tätigkeiten, maßgebliche Ergebnisverweise und berührte Dateipfade mit vorherigem/nachherigem Git-Blob-SHA |
| Prüfung und Entscheidung | Wirklich ausgeführtes Verfahren, Resultat, Umfang und Grenze; Entscheidungen nur referenzieren |
| Offenes und Fortsetzung | Konkretes Hindernis, nächste Handlung, tatsächliche oder offene Zuständigkeit, Auslöser und notwendige Einstiegsdateien |

Zulässige Ereignisse: `beginn`, `zwischenstand`, `uebergabe`, `abschluss`, `blockiert`, `abbruch`, `korrektur`. Ein neuer Auftrag startet mit `beginn`. Bei einer Korrektur betroffene Eintrags-IDs in `korrektur_fuer` nennen; die alte Aussage bleibt historisch erkennbar. Übernahme eines Teilauftrags muss vom wirklichen übernehmenden Bearbeiter oder als ausdrücklich fremder Bericht mit nachvollziehbarer Herkunft aufgezeichnet werden. Kein Prüfer, keine Zustimmung und kein Vollzug wird erfunden.

## Fassung und Veröffentlichung

Veröffentlichte Ereignisdateien werden nicht verändert oder gelöscht. Fehler durch ein neues verbundenes Ereignis berichtigen; vertrauliche Inhalte nicht im Berichtigungstext wiederholen. Ein befugter Datenschutz-/Aufbewahrungsfall kann eine andere Behandlung erfordern und wird gesondert geklärt; diese organisatorische Regel ist keine gesetzliche Unveränderlichkeitsgarantie.

`basis.commit` ist der tatsächlich gelesene Ausgangscommit, nicht der noch unbekannte eigene Commit. Änderungen nennen Git-Blob-SHAs; Journal-Ereignisdateien selbst werden nicht als ihre eigenen Änderungen aufgeführt. Dadurch entsteht kein Selbsthash- oder Endlos-Commit-Problem. Der Commit, der einen Eintrag veröffentlicht, ergibt sich aus der Git-Historie. Ein lokal geprüfter Kandidat wird vor der Veröffentlichung nicht als fernverifiziert beschrieben. Tatsächlich nachträgliche Feststellungen erhalten bei Bedarf einen Nachtrag; jede erneute Validator-Ausführung benötigt nicht wiederum ein Journal über das Journal.

Die Erstfassung schreibt frühere Tätigkeiten nicht mit erfundenen Zeitstempeln nach. Bisherige Einrichtung und Kernprüfung bleiben in ihren damaligen Commits und dem [Szenarienvermerk](../06_anwendung_und_pruefung/szenariopruefungen.md) nachvollziehbar. Vollständige Erfassung beginnt mit diesem Verfahren, nicht rückwirkend.

## Prüfung und technische Reichweite

Das gepflegte Programm `pruefen.py` benötigt Python ab 3.10 und `jsonschema==4.26.0`. Es prüft versionsabhängige Schemas, Datumsform und Zeitreihenfolge, eindeutige IDs, Ereignisbezüge, sichere Pfade, vorhandene Repository-Verweise neuer Einträge, Unverändertheit vorhandener Journale und versionierter Schemas sowie die Abdeckung geänderter Nicht-Ereignisdateien. Für neue v2-Berichte werden der tatsächliche Basiscommit und die vorherigen Blob-/Moduswerte geprüft. Nachherwerte müssen zum geprüften Zielbaum oder zu einem nachweisbaren veröffentlichten Zwischenstand desselben Ereignisses passen; die endgültige Änderung braucht weiterhin einen Bericht für ihren Ergebnisstand.

```bash
python3 09_arbeitsjournal/pruefen.py --basis <ausgangscommit> --ziel HEAD
# Noch unveröffentlichten, bereits gestagten Kandidaten prüfen:
python3 09_arbeitsjournal/pruefen.py --basis <ausgangscommit> --ziel INDEX
# Nach Auftrag oder offenem letzten Ereignis suchen:
python3 09_arbeitsjournal/pruefen.py --uebersicht
```

`INDEX` prüft ausschließlich gestagte Dateien; unstaged oder untracked Inhalt ist vor Abschluss zusätzlich mit `git status` abzugleichen. Alte Ergebnisverweise bleiben auf ihren historischen Stand bezogen; die heutige Entfernung einer Datei macht einen damals richtigen Journalbericht nicht falsch. Ohne `--basis` findet keine Änderungs-/Append-only-Prüfung und keine aktuelle Zielprüfung neuer Verweise statt; das Programm meldet diesen begrenzten Modus ausdrücklich. Der Kommandozeilenprüfer ist keine Hintergrundüberwachung.

Der [Workflow](../.github/workflows/journal.yml) führt zuerst die gepflegten [Gegenfalltests](selbsttest.py) aus und prüft anschließend Pull-Request-Kandidaten und Pushes; er benötigt keine Schreibrechte und erzeugt selbst keine Journaldateien. Ausführungen des Validators sind technische Belege des übergeordneten Auftrags, keine rekursiven neuen Arbeitsaufträge. Andere selbständig fachlich schreibende Automatisierungen sind dagegen journalpflichtig.

**Grenze:** Die [Schutz- und Betriebsbeschreibung](schutz_und_betrieb.md) enthält die administrativ offene Sollkonfiguration und deren Abnahme. Ohne passend eingerichteten erforderlichen Statuscheck und Schutz gegen Umgehung kann ein fehlgeschlagener Lauf allein den direkten Push nicht verhindern. Bei dieser Einführung wurde `main` ungeschützt vorgefunden; ein erforderlicher Check wurde nicht als eingerichtet behauptet. Für eine technische Merge-Sperre ist der Check `journal` aus dem Workflow `Arbeitsjournal` als erforderlich einzustellen und die wirksame Bypass-Regel zu prüfen. Änderungen am Prüfprogramm/Workflow selbst benötigen eine entsprechende Methodenprüfung; Selbstprüfung allein ist keine manipulationssichere Absicherung.

JSON-Validität beweist nicht Wahrhaftigkeit, fachliche Vollständigkeit, Identität des Berichtenden, Datenschutz oder jede unsichtbare Tätigkeit. Angegebene erfolgreiche Prüfungen sind Berichte mit Grenzen; reale externe Abläufe benötigen ihre eigenen Belege.

## Wiedereinstieg und Informationsschutz

Aktuellen Auftrag und `HEAD` feststellen. [Entscheidungsregister](../05_entscheidungen/README.md), [Bestandsabgleich](../01_quellen_und_bestand/bestands_und_lueckenanalyse.md) und einschlägige Journalereignisse lesen; dann nur erforderliche Quellen und Ergebnisdateien öffnen. Nicht jedes Mal das gesamte Journal kopieren. Offene Punkte anhand aktueller Angaben erneut bewerten; historische Aussagen nicht zum heutigen Fakt hochstufen.

Keine Geheimnisse, Originalverträge, Roh-E-Mails, personenbezogenen Fälle oder interne Gedankengänge einstellen. [Informationsschutz](../00_systemkern/informationsschutz.md#schutz-im-arbeitsjournal) gilt auch für Referenzen und Dateinamen. Ein veröffentlichungsgeeigneter Kurzbericht kann auf eine zugangsbeschränkte Quelle verweisen, ohne ihren Inhalt offenzulegen.


## Zeit und Schemafortschreibung

Neue Ereignisse verwenden **Schema v2**, sobald diese Version in der Vergleichsbasis des Repositorys vorhanden ist. Bereits veröffentlichte v1-Ereignisse und `schema_v1.json` bleiben bytegleich. Ein vor Einführung gestarteter v1-Auftrag kann mit einem v2-Ereignis fortgesetzt werden. Alte Zeitangaben werden weder nachträglich präzisiert noch durch vermeintlich bessere Schätzungen ersetzt.

`zeitpunkt` ist der wirkliche Aufzeichnungszeitpunkt in UTC mit Datum, Stunden, Minuten und Sekunden, optional Sekundenbruchteilen, abgeschlossen mit `Z`. Das hier gewählte Format ist ein eingeschränktes RFC-3339-Profil; nicht jeder dort zulässige Sonderfall wird akzeptiert. Eine bloße Datumsangabe, eine fehlende Zone oder der unbekannte Offset `-00:00` genügen nicht. Die Systemuhr ist eine benannte Zeitquelle, kein beglaubigter Zeitstempel.

`arbeitszeitraum.von` und `.bis` beschreiben den bekannten Zeitraum der berichteten Tätigkeit, nicht automatisch die gesamte verstrichene Arbeitszeit eines Menschen. Eine offene oder unbekannte Grenze bleibt `null` und wird begründet. `zeitquelle` unterscheidet Systemuhr, belegte Quelle und unbekannte Herkunft. Bei einem Beginn bleibt das Ende offen; ein Zeitraum oder eine behauptete Prüfung darf nicht nach seinem Aufzeichnungszeitpunkt liegen. Für jede Prüfungsangabe steht ein eigener tatsächlicher Zeitpunkt, auch für die Feststellung „nicht geprüft“. Er bezeichnet dann diese Feststellung, keine vorgetäuschte Prüfung.

Quellendatum, fachliche Geltung, Arbeitszeitraum, Beobachtungszeit und Git-Veröffentlichung sind unterschiedliche Zeiten. Der Prüfer kontrolliert Form und erklärte Reihenfolge, nicht Uhrensynchronisation oder Wahrheit. Gleichzeitige Ereignisse werden über explizite Vorgänger verbunden; eine spätere Uhrzeit allein erzeugt keine Abhängigkeit. Eine handschriftlich unbekannte historische Uhrzeit wird nicht auf Mitternacht gesetzt.

Ein Schema, eine Vorlage oder ein administrativer API-Datensatz ist selbst kein ausgeführtes Ereignis. Solche JSON-Dateien erhalten deshalb keine erfundenen Ausführungszeiten oder API-fremden Zusatzfelder. Ihre wirkliche Bearbeitung wird mit Zeitpunkten und Blobbezug im Journal beschrieben.

## Herkunftsprüfung und reproduzierbare Gegenfälle

In v2 nennen Änderungen neben `vorher`/`nachher` auch `modus_vorher`/`modus_nachher`; eine neue oder gelöschte Datei verwendet auf der nicht vorhandenen Seite `null`. Der erklärte Basiscommit muss lokal verfügbar sein, und sein Inhalt muss zu den Vorherwerten passen. Reine Dateimodusänderungen sind damit darstellbar. Eine absichtliche falsche Vorherangabe wird nicht mehr allein durch einen passenden Nachherhash verdeckt.

Bei mehrteiligen Arbeiten können veröffentlichte Zwischenberichte einen damals zutreffenden Ergebnisblob enthalten, der im abschließenden PR bereits ersetzt wurde. Solche Berichte bleiben zulässig, wenn der Commit, der genau diese Ereignisdatei eingeführt hat, auch den berichteten Zwischenstand trägt und in der geprüften Historie auffindbar ist. Ein neu erfundener Zwischenstand ohne diesen Beleg wird abgewiesen. Die Prüfung eines bloßen Git-Baums ohne passende Historie hat insoweit eine engere Nachweisgrenze.

[selbsttest.py](selbsttest.py) erzeugt positive und negative Testfälle in temporären Verzeichnissen, führt keine Netzaufrufe aus und entfernt diese Eingaben anschließend. Es enthält keine echten Gesellschaften oder betrieblichen Nachweise. Es prüft unter anderem Zeitreihenfolge, unbekannte Daten, Schemafortschreibung, unveränderte Alteinträge, Ereignis-/Delegationsbezüge, Pfade, Änderungsabdeckung und Vorher-/Nachherherkunft. Die Tests werden im selben `journal`-Job vor der eigentlichen Kandidatenprüfung ausgeführt. Ein geänderter Test oder Prüfer benötigt weiterhin eine fachlich-methodische Durchsicht.


## Deterministische Kalenderprüfung

Der Prüfer registriert seine Kalender-/Zeitzonenprüfung ausdrücklich an der eigenen
`FormatChecker`-Instanz. Sie verwendet die Python-Standardbibliothek und hängt nicht
von optional installierten `date-time`-Erweiterungen ab. Das v2-Schema begrenzt neue
Zeitangaben weiterhin auf das oben beschriebene UTC-Profil; veröffentlichte Schemas
und Ereignisse werden dafür nicht geändert.

Hintergrund: Laut [jsonschema-Dokumentation](https://python-jsonschema.readthedocs.io/en/stable/validate/#validating-formats)
können Formate zusätzliche Pakete benötigen. Deshalb genügt ein lokal vorhandener
Formatprüfer nicht als Nachweis für dasselbe Verhalten in einer sauberen
CI-Umgebung. Die Selbsttests prüfen gültige und unmögliche Kalenderdaten zusätzlich
bei fehlendem oder wirkungslosem optionalem `date-time`-Prüfer. Ein fehlgeschlagener
Selbsttest stoppt den Job; die nachfolgende Journalprüfung gilt dann als nicht
ausgeführt, nicht als bestanden.
