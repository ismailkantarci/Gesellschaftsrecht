# Journalprüfung, Veröffentlichung und Branchschutz

**Status:** Die [Sollkonfiguration](schutzregel.json) ist ein administrativ anzuwendender API-Datensatz, keine bereits aktive Einstellung. Im [Auftrag #2](https://github.com/ismailkantarci/Gesellschaftsrecht/issues/2) wurde der Zugriffsversuch mit `403 Resource not accessible by integration` dokumentiert. Die verfügbare Verbindung besitzt keine Aktion zum Setzen von Branchschutz oder Rulesets. Eine Inhaltsänderung oder ein grüner Prüflauf beseitigt diese Administrationsgrenze nicht.

## Vier getrennte Nachweise

**Arbeitsregel:** Ein beauftragter Bearbeiter muss den Auftrag und seine tatsächliche Arbeit dokumentieren. Diese Pflicht steht im [Journal](README.md) und in [AGENTS.md](../AGENTS.md).

**Prüfprogramm:** JSON-Form, Zeitangaben, Ereignisbezüge und die dokumentierten Dateiveränderungen werden geprüft. Der Prüfer kann fehlende oder widersprüchliche Angaben erkennen, aber weder Wahrheit noch tatsächliche Autorität des Berichtenden garantieren.

**Ausgeführter Check:** Der Job `journal` muss für den konkreten Kandidaten tatsächlich laufen. In den Jobschritten sind Selbsttest und Journalprüfung zu sehen. Ein erfolgreicher oder übersprungener anderer Lauf ist kein Ergebnis dieses Kandidaten.

**Serverseitige Zusammenführungssperre:** Erst eine aktive, auf `main` wirkende Regel verlangt einen erfolgreichen Check vor dem Merge und untersagt andere Wege entsprechend ihrem Geltungsbereich. Diese Ebene ist administrativ offen. Ein Workflow allein verhindert keinen direkten Push auf eine ungeschützte Branch.

## Gewählte Sollkonfiguration

Die Konfiguration richtet sich ausschließlich auf `refs/heads/main`; keine anderen Repositorys oder Arbeitszweige. Sie verlangt Pull Requests, den aktuellen Check `journal` von **GitHub Actions (App-ID 15368)** und eine auf den Basisstand aktualisierte Prüfung. Sie verbietet Löschung und nicht vorspulende Aktualisierung von `main`. Die Liste privilegierter Umgehungsakteure bleibt leer.

Der erwartete App-Ursprung wurde am vorhandenen erfolgreichen Check des Ausgangscommits `918b6157ef123645bcc760e189041daeb9a43849` abgelesen. Ein zufällig gleich benannter Commit-Status eines anderen Erzeugers soll nicht genügen. Bei einem späteren Anbieterwechsel muss diese Zuordnung bewusst neu bewertet werden.

Vorgesehen ist die Merge-Methode `merge`. Damit bleiben die tatsächlich journalisierten Zwischencommits auffindbar; ein Squash oder Rebase soll ihre als Quelle benannten Commitobjekte nicht aus der sichtbaren Entwicklungslinie entfernen. Das ist eine Entscheidung für diese Herkunftsspur, keine allgemeine Git-Vorgabe.

Die Mindestzahl formaler Review-Zustimmungen ist zunächst **0**. Es ist kein verlässlich verfügbarer unabhängiger zweiter Prüfer benannt; eine fiktive Zweitprüfung oder ein nicht erfüllbarer Freigabeweg wird nicht eingerichtet. Pull Request und erfolgreiche automatische Prüfung bleiben dennoch erforderlich. Bei tatsächlich besetzter Prüferrolle kann die Administration eine Zustimmungspflicht festlegen. Die [fachliche Prüftiefe](../00_systemkern/arbeitsweise_und_freigaben.md) wird durch diesen technischen Wert nicht reduziert.

## Vorgehen der befugten Administration

Zuerst vorhandene Rulesets, klassische Branchschutzregeln, Berechtigung und wirksame Einschränkungen lesen. Bereits bestehende stärkere Regeln nicht überschreiben oder abschwächen. Bei vergleichbarem vorhandenem Ruleset dessen Inhalt abgleichen, statt ein zweites unübersichtlich überlagerndes Regelwerk anzulegen.

Bei nachweislich fehlender gleichartiger Regel kann die beauftragte Administration mit einem regulär angemeldeten GitHub-CLI-Konto und der benötigten Repository-Administrationsberechtigung den Datensatz anlegen:

```bash
gh api --method POST repos/ismailkantarci/Gesellschaftsrecht/rulesets   --input 09_arbeitsjournal/schutzregel.json
```

Der Befehl verändert eine Repository-Einstellung. Er wird von diesem Repository nicht automatisch ausgeführt und benötigt weder ein im Repository gespeichertes Geheimnis noch erweiterte Workflow-Rechte. `enforcement: active` im JSON ist der angeforderte Sollwert; erst die erfolgreiche Serverantwort mit Ruleset-ID und anschließendes Zurücklesen belegen die Einstellung. Ein verweigerter Aufruf bleibt offen, statt über einen anderen Identitäts- oder Geheimnisweg umgangen zu werden.

## Abnahme der Schutzkonfiguration

Die Administration muss Ruleset-ID, zurückgelesene Konfiguration, Zielbranch, erwarteten Check-Erzeuger und Zeitpunkt festhalten. Danach an einem geeigneten Pull Request prüfen, ob der aktuelle Head geprüft wurde und ein fehlender oder fehlgeschlagener Check das Zusammenführen tatsächlich verhindert. Eine lesende Auswertung der Merge-Sperre genügt für den negativen Fall; keinen absichtlich ungültigen Commit nach `main` schreiben. Für die technische Abnahme sichere temporäre Arbeitszweige nach Ende entfernen, nicht fachliche Dateien löschen.

Den positiven Fall an einem korrekt journalisierten Kandidaten prüfen. Ergänzend Lösch-/Force-Push-Regeln, aktive Bypass-Liste und die tatsächliche Rolle des ausführenden Kontos auswerten. Keine destruktiven Versuche an `main`. Ohne diese Beobachtungen lautet das Ergebnis „konfiguriert, Sperrwirkung nicht vollständig erprobt“, nicht „unumgehbar“.

## Grenzen und Schutz des Prüfers

Ein Bearbeiter mit Änderungsrechten am Workflow könnte versuchen, den Prüfer im selben Pull Request abzuschwächen. Der normale `pull_request`-Workflow läuft deshalb nur mit Leserechten und ohne dauerhafte Zugangsdaten; er enthält keine administrativen Schreibschritte. Änderungen an Workflow, Prüfer, versioniertem Schema oder Schutzregeln müssen als methodisch wesentlich behandelt werden. Ein Selbsttest ist kein Schutz gegen vorsätzliche gemeinsame Manipulation von Test und Programm.

Für stärkere Absicherung sind eine tatsächlich unabhängige Freigabe oder ein gesondert administrierter vertrauenswürdiger Prüfweg nötig. Diese sind nicht als eingerichtet behauptet. Auch eine leere Bypass-Liste entzieht dem Repository-Inhaber nicht jede Möglichkeit, die Regeln später administrativ zu ändern. Solche Änderungen sind eigene journalpflichtige Aufträge mit erneutem Wirksamkeitsnachweis.

Der Workflow prüft normale PR-Kandidaten, Pushes und manuell angeforderte Läufe. Er ist nicht als Merge-Queue-Konfiguration eingerichtet. Vor Einführung einer Merge Queue muss deren Ereignis-/Vergleichsmodell ergänzt und erprobt werden. Keine verdeckte Hintergrundüberwachung und keine Erfassung aller Lesezugriffe.

## Quellen

Die verwendeten GitHub-Dokumentationen zu geschützten Branches, sicherer Workflow-Ausführung und Ruleset-API sind in [QU-0006, QU-0007 und QU-0013](../01_quellen_und_bestand/methodenquellen.md) mit Übernahmegrenzen dokumentiert. GitHub-Funktionsumfang, Regeln und tatsächlicher Kontozugriff müssen bei späterer Aktivierung erneut geprüft werden.

## Formularprüfung vor Create

Ein importiertes Formular ist noch keine gespeicherte Regel. Vor Create nicht nur die Häkchen, sondern beide Bereiche **Show additional settings** öffnen und mit der Sollkonfiguration vergleichen:

| Bereich | Zu bestätigender Wert |
|---|---|
| Geltung | Ziel `main`, Enforcement `Active`, Bypass-Liste leer |
| PR | PR erforderlich, Merge-Methode `merge`, erforderliche Zustimmungen `0`, offene Review-Diskussionen müssen gelöst sein |
| Statuscheck | Konkreter Eintrag `journal`, Quelle GitHub Actions; „Require branches to be up to date before merging“ aktiv |
| Schutz | Restrict deletions und Block force pushes aktiv |
| Kein unbeabsichtigtes Blockieren | Restrict updates und Require linear history aus; keine zusätzliche Signaturpflicht in diesem Sollpaket |

Geschlossene Detailbereiche belegen weder den ausgewählten Check noch dessen Quelle. Auch ein sichtbarer Wert `Active` wirkt erst nach dem erfolgreichen Speichern. Danach Ruleset-ID, Rücklesezeitpunkt, Ziel, Checkquelle und tatsächliche Durchsetzung getrennt dokumentieren. Die unabhängige fachliche Prüfung wird nicht durch `0` technische Zustimmungen ersetzt. Quelle: [GitHub – Creating rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository).

## Sauberer Zweigabschluss

Am Ende eines abgeschlossenen Auftrags liegt der freigegebene letzte Inhalt auf `main`; der konkrete Prüflauf wurde zurückgelesen. Es bleibt kein offener Inhalts-PR und kein erledigter eigener Arbeitszweig als Ersatz für einen ordentlichen Abschluss. Ein berechtigt noch offener Auftrag ist dagegen kein Abfall: seine Änderungen weder zwangsweise zusammenführen noch löschen.

Vor einer Zweiglöschung den tatsächlichen Kopf, die vollständig erhaltene Aufnahme in die main-Historie, etwaige neue Commits und andere offene PRs prüfen, die den Zweig als Quelle oder Ziel verwenden. Nur einen vollständig übernommenen, nicht mehr verwendeten eigenen Arbeitszweig entfernen; `main`, geschützte Zweige und fremde Arbeit bleiben unangetastet. Nach erfolgreichem Merge einen erledigten Pflegezweig nicht für neue Arbeit wiederverwenden.

Die Entfernung des Zweignamens entfernt keine bereits über die Merge-Historie erhaltenen Fachinhalte oder Journale. Löschung und anschließende Branchliste dennoch getrennt überprüfen. Eine fehlende Aktion oder verweigerte Berechtigung wird als offener Bereinigungspunkt dokumentiert, nicht über alternative Identitäten oder eine abgewiesene Automatisierung umgangen. Inhalt bereits auf main, PR gemergt, Zweig gelöscht und Regel aktiviert sind vier verschiedene Aussagen.

Der abschließende Journalbericht nennt den tatsächlich verifizierten main-Stand, Prüfungen und die erledigte oder offen gebliebene Bereinigung. Eine noch notwendige manuelle Bedienung bleibt am maßgeblichen Verfolgungsort sichtbar. Kein allgemeines „alles fertig“, solange eine ausdrücklich beauftragte Abnahme offen ist.
