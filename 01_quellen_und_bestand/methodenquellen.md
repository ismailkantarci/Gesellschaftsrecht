# Externe Methodenquellen und begrenzte Übernahme

**Erfasst am:** 2026-09-22T21:54:33Z. **Abrufdatum:** 22.09.2026. **Auftrag:** [ENT-0003](../05_entscheidungen/ent_0003_selbstbeschreibung_und_qualitaet.md). Quellen wurden über die Webrecherche gelesen; dies ist kein unveränderliches Webseitenarchiv und keine Prüfung aller verlinkten Unterseiten. Die Erfassungsuhrzeit bezeichnet diese Quellenaufnahme, nicht eine behauptete Sekundengenauigkeit jedes Abrufs.

Die folgenden Quellen sind Anregungen für die Repository-Methode. Die TAXIPartner-Anwendungsentscheidungen stehen daneben und sind keine Behauptungen der Quellen. Kein neues Zertifizierungsprojekt, keine vollständige Übernahme eines externen Standards und keine neue Prüfung der konkreten Taxi-Rechtslage.

## QU-0006 Branchschutz

**Quelle:** GitHub, [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), Abschnitte zu required status checks und bypass. **Gelesener Typ:** offizielle Produktdokumentation, dynamischer Webstand am Abrufdatum.

**Anregung:** Automatische Prüfung und serverseitige Durchsetzung sind verschiedene Ebenen. **Anwendung hier:** Sollregel mit verpflichtendem Check und ohne eingetragene Bypass-Akteure; Istkonfiguration bleibt separat nachzuweisen. **Grenze:** Keine zugesicherte Unveränderlichkeit gegenüber befugter Administration; technische Erfolgszustände sind keine Fachfreigabe.

## QU-0007 Sichere Prüfabläufe

**Quelle:** GitHub, [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use), Abschnitte zu fremdem Code, minimalen Berechtigungen und vollständigem Commit-Pinning. **Typ:** offizielle Produktdokumentation.

**Anwendung hier:** Read-only-Prüfjob, kein Secretzugriff, keine privilegierte Ausführung fremder PR-Inhalte, fixierter Checkout und Fehler nicht als Erfolg ignorieren. Änderungen am Prüfmittel selbst bleiben besonders prüfbedürftig. Kein allgemeiner Sicherheitsnachweis und keine automatische Erkennung unbemerkter Zugriffe.

## QU-0008 Herkunft und Verantwortung

**Quelle:** W3C, [PROV-DM: The PROV Data Model](https://www.w3.org/TR/prov-dm/), Recommendation vom 30.04.2013, Begriffe Entity, Activity, Agent sowie Nutzung und Erzeugung.

**Anregung:** Informationsobjekt, Bearbeitung und verantwortlicher Akteur werden getrennt verknüpft. **Anwendung hier:** Quellfassung, Tätigkeit, Ergebnis und Akteur im Journal; genaue Verweise in Fachakten. **Nicht übernommen:** Kein RDF-Graph, keine Behauptung PROV-konformer Vollimplementierung, kein Beweis für Identität oder Wahrheit allein aus einer Relation.

## QU-0009 Zeitangaben

**Quelle:** IETF/RFC Editor, [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339), insbesondere Abschnitt 5.6. **Typ:** Spezifikation eines Internet-Zeitformats, Juli 2002.

**Anwendung hier:** Neues Journalprofil mit vollständigen UTC-Zeitangaben bis zur Sekunde, optional Untersekunden. Aufzeichnung, Arbeitszeitraum und Prüfzeit werden getrennt; unbekannte Ereigniszeiten bleiben null mit Erklärung. Das lokale Profil unterstützt keine Schaltsekunden und keinen unbekannten UTC-Offset. Präzise Darstellung ist keine Beglaubigung oder Garantie einer synchronisierten Uhr.

## QU-0010 und QU-0011 Hypothese Versuch und Lernen

**Quellen:** Strategyzer, [Validate Your Ideas with the Test Card](https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card), 05.03.2015, und [Capture Customer Insights and Actions with the Learning Card](https://www.strategyzer.com/library/capture-customer-insights-and-actions-with-the-learning-card), 09.03.2015. **Typ:** Primärdarstellung der Autoren ihrer Methode.

**Anregung:** Annahme und geplanten Test mit Messgröße und Kriterium verbinden; danach Beobachtung von Interpretation und nächster Handlung trennen. **Anwendung hier:** kurze entsprechende Abschnitte in vorhandener Forschung und Nutzenbewertung. **Nicht übernommen:** Keine kopierten Karten, kein Lizenz-/Zertifizierungsversprechen und keine externe Softwarepflicht. Ein TAXIPartner-Versuch benötigt weiter eigenen Umfang und reale Belege.

## QU-0012 Wiener Taxipraxis

**Quelle:** WKO Wien, [Neue Wiener Landesbetriebsordnung ab 1. Jänner 2024](https://www.wko.at/wien/transport-verkehr/befoerderungsgewerbe-personenkraftwagen/die-wiener-landesbetriebsordnung-wurde-neu-erlassen), Seitenstand 18.11.2024, am Abrufdatum gelesen. **Typ:** Brancheninformation, keine Primärnorm.

**Anregung:** Fahrzeug, Ausstattung, Fahrgastinformation und Durchführung werden entlang konkreter Tätigkeiten erklärt. **Anwendung hier:** fachlich fundierte Regeln in kurze rollenbezogene Betriebsanweisungen überführen. **Grenze:** Keine Übernahme von Beträgen, Fristen, technischen Grenzwerten oder Rechtsfolgen aus dieser Quelle als aktuell geprüft. Maßgebliche Normfassung und Einzelfallanwendung bleiben gesonderte Facharbeit.

## QU-0013 Ruleset-API

**Quelle:** GitHub, [REST API endpoints for rules](https://docs.github.com/en/rest/repos/rules#create-a-repository-ruleset), Create a repository ruleset und Rule-Parameter, am Abrufdatum gelesen. **Typ:** offizielle API-Dokumentation.

**Anwendung hier:** JSON-Sollkonfiguration für main, PR-Weg, Checkherkunft und Aktualität. Der tatsächlich beobachtete Check journal stammt von GitHub Actions mit App-ID 15368; dies wurde am bestehenden Repository-Check gelesen. **Grenze:** Schemaabgleich der Konfiguration ersetzt keine vom Dienst angenommene Aktivierung. Rechte, Produktverfügbarkeit und überlagernde Regeln werden administrativ geprüft.

## Pflege

Eine spätere Quellenänderung löst nur für tatsächlich abhängige Aussagen eine neue Prüfung aus. Erfassungsdatum und Rechercheergebnis nicht als ewige Gültigkeit ausgeben. Entscheidend ist die konkrete, begrenzte Anwendung; fremde Methoden werden nicht allein wegen ihres Namens als verbindlicher Oberbau eingesetzt.
