# SVC Workshop: LLMs & Agentic Operations

**Zielgruppe:** 12 erfahrene IT-Operations-Techniker:innen mit Linux-/OpenShift-Fokus, ohne vorausgesetztes ML-Wissen  
**Dauer:** 4 h 30 min inklusive 15 Minuten Pause  
**Format:** kurze Inputs, Visualisierungen, angeleitete Fallarbeit, Live-Demo, drei Vierergruppen  
**Leitfrage:** Wie kommen wir von probabilistischer Textvorhersage zu einer kontrollierbaren Ops-Automation?  
**Ergebnis:** Die Teilnehmenden können eine Agent-Diagnose fachlich prüfen und einen begrenzten, messbaren Ops-Piloten entwerfen. Der Workshop vermittelt dafür Grundlagen und Entscheidungskompetenz; die Implementierung eines produktiven Agenten ist eine Vertiefung.

## Didaktischer Leitfaden

### Ein Incident als roter Faden

**Leitfall:** Nach einem Deployment startet die Anwendung im Namespace `workshop` nicht. Ein referenzierter ConfigMap-Key fehlt. Die Ursache bleibt zu Beginn verdeckt; Ticket, Status, Events und Deployment-Ausschnitte werden schrittweise aufgedeckt. Erfolg bedeutet zunächst: eine belegte Diagnose mit offenen Fragen und einem überprüfbaren Änderungsvorschlag. Der Demo-Agent erhält ausschließlich lesenden Zugriff.

Der Lernweg folgt fünf Fragen:

1. **Was wissen wir bereits?** Bekannte Diagnosepraxis und benötigte Evidenz aktivieren.
2. **Wie entsteht eine Antwort?** Das LLM-Mentalmodell erklärt plausible Aussagen und ihre Grenzen.
3. **Wie wird daraus Handeln?** Kontext, Tools und Agent-Loop am selben Incident verbinden.
4. **Wodurch wird es kontrollierbar?** Berechtigungen, Abbruchbedingungen und Nachweise prüfen.
5. **Wann hilft es uns?** Eine Fallvariante selbst beurteilen und einen eigenen Use Case eingrenzen.

### Gewählter Vermittlungsansatz

Für diese Gruppe eignet sich **problemzentriertes Lernen mit vorgeführtem Lösungsbeispiel, schrittweise reduzierter Anleitung und aktivem Abrufen**: vorhandene Ops-Erfahrung nutzen, neue ML-Begriffe am bekannten Problem verankern, Entscheidungen zuerst vormachen und dann selbst treffen lassen. Der Ablauf orientiert sich an Merrills Aktivierung, Demonstration, Anwendung und Integration ([D1](https://doi.org/10.1007/BF02505024)).

Die Lernenden sind Ops-Expert:innen, aber ML-Einsteiger:innen. Deshalb erklärt die Moderation die neue Modell- und Agentenmechanik an einem ausgearbeiteten Beispiel; in späteren Übungen werden Hilfen reduziert. Das ist eine Übertragung des Worked-Example-Prinzips auf diesen Workshop, kein empirischer Nachweis eines universell optimalen Formats ([D2](https://doi.org/10.1207/s1532690xci0201_3)). Kurze Abruffragen ohne Folien wiederholen zentrale Zusammenhänge; die anschließende Auflösung korrigiert Fehlvorstellungen ([D3](https://doi.org/10.1111/j.1467-9280.2006.01693.x)).

**Moderationsregeln:**

- Pro Lernschritt: konkrete Frage → kurzer Input oder Beispiel → eigene Entscheidung → Feedback. Spätestens nach etwa 10 Minuten erhält die Gruppe eine aktive Aufgabe.
- Zuerst alle kurz einzeln denken lassen, dann zu zweit abgleichen, erst danach Antworten im Plenum sammeln. So werden alle zwölf Personen beteiligt.
- Ein gemeinsames Fallblatt fortschreiben: **Beobachtung/Quelle → Hypothese → fehlende Evidenz → nächster erlaubter Schritt → Stop/Freigabe**.
- Grafiken schrittweise aufbauen und direkt am Beispiel erklären. Analogien ausdrücklich begrenzen: Attention gewichtet Kontext; sie ist weder menschliche Aufmerksamkeit noch ein verlässlicher Erklärungsnachweis.
- Bei Verständnislücken ein zweites Beispiel verwenden und optionale Tiefe kürzen. Übungen, Feedback und Transfer bleiben erhalten.
- Begriffe nur so tief behandeln, wie sie eine Ops-Entscheidung erklären. Historie, Modellarchitekturvarianten und Herleitungen kommen auf den Fragenparkplatz.

## Lernziele und sichtbare Nachweise

| Am Ende können die Teilnehmenden … | Nachweis im Workshop | Wesentliches Learning |
|---|---|---|
| **L1:** die Generierung vom Text bis zum nächsten Token erklären und Training von Inferenz unterscheiden. | Pipeline in Block 2 rekonstruieren; erklären, was ein neues Log im Prompt verändert. | Kontext verändert die aktuelle Ausgabe, normalerweise nicht die Gewichte. |
| **L2:** eine Diagnose nach Evidenz, Aktualität und Unsicherheit bewerten. | Behauptung im Leitfall mit einer konkreten Tool-Ausgabe belegen oder zurückweisen. | Plausibilität und Tokenwahrscheinlichkeit sind keine Wahrheitsgarantie. |
| **L3:** Chat-Oberfläche, festen Workflow und modellgesteuerten Agent-Loop unterscheiden. | Drei Ops-Aufgaben begründet einer Ausführungsform zuordnen. | Autonomie ist eine Architekturentscheidung; ein Chat kann Agenten enthalten. |
| **L4:** einen Arbeitsauftrag formulieren und Tool, Skill, RAG, Memory und MCP passend einordnen. | Auftrag und nächster Tool-Schritt auf dem Fallblatt; Bausteine im Architekturpfad markieren. | Anweisungen, Wissenszugriff, Ausführung und Transport erfüllen verschiedene Aufgaben. |
| **L5:** technische Kontrollgrenzen und Laufzeitgrenzen entwerfen. | Scope, erlaubte Verben, Abbruch und Freigabe für den Leitfall benennen. | Ein Prompt ist keine Berechtigungsschranke; Kontrolle braucht technische Durchsetzung. |
| **L6:** einen Agent-Lauf hinsichtlich Qualität, Zeit und Kosten beurteilen. | Demo anhand einer Prüfrubrik bewerten und mit einem manuellen Ablauf vergleichen. | Ein erfolgreicher Einzellauf ersetzt keine Evaluation. |
| **L7:** einen geeigneten eigenen Ops-Piloten abgrenzen. | Gruppen-Pilotkarte mit Erfolgskriterium, Vergleichsbasis und Stop-Kriterium. | Nutzen entsteht durch überprüfbare Ergebnisse bei vertretbarem Risiko. |

## Ablauf — 270 Minuten

Alle Übungs-, Feedback- und Übergangszeiten sind in den Blöcken enthalten.

| Start | Dauer | Block | Sichtbares Ergebnis |
|---:|---:|---|---|
| 00:00 | 20 min | 1. Incident & Standortbestimmung | Hypothesen und Ausgangsverständnis |
| 00:20 | 50 min | 2. Vom Text zum nächsten Token | Erklärtes LLM-Mentalmodell |
| 01:10 | 25 min | 3. Betrieb & Grenzen | Begründete Evidenz- und Ressourcenentscheidungen |
| 01:35 | 15 min | Pause | |
| 01:50 | 45 min | 4. Vom LLM zum Agenten | Arbeitsauftrag und ergänzter Agent-Loop |
| 02:35 | 25 min | 5. Agentic-Ops-Architektur | Kontrollpunkte im Daten- und Ausführungspfad |
| 03:00 | 40 min | 6. Live-Showcase & Falltransfer | Bewerteter Lauf und selbst bearbeitete Variante |
| 03:40 | 35 min | 7. Use-Case-Lab | Priorisierte Pilotkarten |
| 04:15 | 15 min | 8. Lernnachweis & Abschluss | Individueller Transfer und offener Lernbedarf |

## 1. Incident & Standortbestimmung — 20 min

**Leitfrage:** Was müssten wir wissen, bevor wir eine Diagnose oder Änderung akzeptieren?

- **5 min – Ankommen:** Name, Verantwortungsbereich und eine Erwartung auf Karte. Handzeichen zu Chat- und Agent-Erfahrung.
- **8 min – Ticket öffnen:** Leitfall zeigen. Alle notieren erste Hypothese und benötigte Evidenz; paarweise abgleichen. Gemeinsam zwei Hypothesen samt unterscheidendem Prüfschritt sammeln. Die Moderation demonstriert eine sauber begründete Entscheidung auf dem Fallblatt.
- **5 min – Ausgangsverständnis:** Einzeln drei Aussagen beurteilen: „Ein neues Log im Prompt trainiert das Modell“, „Eine hohe Tokenwahrscheinlichkeit belegt die Diagnose“, „Read-only macht einen Agenten risikofrei“. Antworten sammeln, im Verlauf erneut aufgreifen.
- **2 min – Lernauftrag:** Am Ende sollen alle eine Agent-Diagnose prüfen können. Die Gruppe benennt, welche Teile ihrer bisherigen Diagnosepraxis dafür weiter gelten.

**Übergang:** Ein Modell kann bereits zum Ticket eine überzeugende Antwort formulieren. Um diese richtig zu bewerten, klären wir zuerst, wie sie entsteht.

## 2. Vom Text zum nächsten Token — 50 min

**Leitfrage:** Warum klingt eine Antwort kompetent, obwohl die entscheidenden Cluster-Daten fehlen?  
**Ziele:** L1, L2. **Fachliche Vertiefung:** [F1](https://arxiv.org/abs/1706.03762).

### Vom sichtbaren Ergebnis zur Mechanik — 8 min

- Zwei vorbereitete Antworten zum Ticket vergleichen: eine unbelegte Diagnose und eine Aussage mit Quelle und offener Unsicherheit. Welche ist bereits prüfbar?
- AI → ML → Deep Learning → LLM kurz einordnen; generative AI als Anwendungsklasse. Modell, Chat-Produkt und angeschlossene Tools unterscheiden.
- Satzanfang „Der Pod startet nicht, weil …“ gemeinsam fortsetzen; dann ein Event hinzufügen. Die Änderung der plausiblen Fortsetzungen führt zur Leitidee: **Generierung hängt vom verfügbaren Kontext ab.**

### Pipeline in drei kleinen Schritten — 24 min

Jeweils etwa 5 Minuten erklären und visualisieren, 3 Minuten am Ticket anwenden:

1. **Text → Tokens → Vektoren:** Tokenisierung erzeugt Textstücke/IDs, keine zwingenden Wortgrenzen. Embeddings bilden IDs auf gelernte Vektoren ab; Positionsinformation ergänzt die Reihenfolge. Ticket und Log markieren: Was muss im Kontext stehen, und was kostet Eingabelänge?
2. **Kontext → Repräsentation:** Maskierte Self-Attention verknüpft ein Token mit zulässigem vorherigem Kontext; Feed-forward-Schichten transformieren die Repräsentation. Mehrere Schichten kombinieren diese Schritte. Am ConfigMap-Beispiel benennen, welche Textstellen zusammengehören. Dies ist eine Illustration, keine Messung tatsächlicher Attention-Gewichte.
3. **Repräsentation → nächstes Token → Wiederholung:** Logits sind Scores; Softmax ergibt eine Wahrscheinlichkeitsverteilung. Sampling/Decoding wählt das nächste Token, das in den Kontext eingeht. Temperatur beeinflusst die Auswahl, nicht den Wahrheitsgehalt. Gemeinsam erklären, warum auch ein syntaktisch plausibler, aber falscher Befehl entstehen kann.

### Training, Post-Training und Inferenz — 10 min

- **Vortraining:** Modellgewichte werden anhand großer Datenmengen angepasst, typischerweise mit einem Vorhersageziel. Muster und auch Fakten können in Gewichten gespeichert sein; das ergibt keine verlässlich zitierbare Faktendatenbank.
- **Post-Training:** Weitere Optimierung, etwa auf Instruktionsbefolgung und Präferenzen, verändert das Verhalten; sie garantiert keine sachliche Korrektheit.
- **Inferenz:** Das trainierte Modell verarbeitet den aktuellen Kontext mit normalerweise unveränderten Gewichten. Gesprächsverlauf, Tool-Ergebnisse und abgerufene Dokumente sind Kontext, kein automatisches Nachtrainieren.
- **Kontextfenster:** begrenzter Arbeitsbereich; lange oder irrelevante Eingaben können Kosten und Fehler erhöhen. Mehr Kontext garantiert keine bessere Nutzung der enthaltenen Information.
- Paarfrage: „Was ändert sich, wenn wir ein neues Event hinzufügen – Gewichte, Kontext oder beides?“

### Abruf und Auflösung — 8 min

Ohne Folie die Pipeline zu zweit skizzieren; anschließend gemeinsam korrigieren:

- Wo wird aus Text eine Modellrepräsentation, wo entsteht die Tokenverteilung?
- Warum ist „wahrscheinliche Fortsetzung“ nicht gleich „wahre Diagnose“?
- Was ist bei Training und beim Hinzufügen eines Logs jeweils veränderlich?

**Mindestnachweis:** Tokens → Vektoren/Position → kontextabhängige Verarbeitung → Tokenverteilung → Auswahl/Wiederholung; Inferenz verändert hier den Kontext, nicht die Gewichte. Keine Backpropagation, Optimiererherleitung oder Matrixrechnung erforderlich.

## 3. Betrieb & Grenzen — 25 min

**Leitfrage:** Welche technischen Folgen hat dieses Modell für unseren Betrieb?  
**Ziele:** L2, L6.

### Ressourcen am Incident erklären — 8 min

- GPUs beschleunigen große parallele Matrixoperationen. Gewichte benötigen grob `Parameter × Bytes pro Parameter`; KV-Cache und weitere Laufzeitdaten kommen hinzu.
- Prefill verarbeitet den Eingabekontext, Decode erzeugt die Ausgabe schrittweise. Lange Logs und lange Antworten belasten unterschiedliche Phasen.
- KV-Cache spart erneute Berechnung und braucht Speicher. Quantisierung reduziert den Gewichtsbedarf; Qualität und Performance müssen für den Anwendungsfall gemessen werden.
- Relevante Größen: Time to First Token, Ausgaberate, Queueing, Kontext-/Ausgabelänge, Fehlerquote und Gesamtkosten pro gelöstem Fall.
- Entscheidungsfrage: „Alle Namespace-Logs senden oder relevante Ausschnitte mit Zeitbezug?“ Nutzen, Informationsverlust, Datenschutz und Kosten gegeneinander abwägen.

### Fehlerbilder mit Gegenmaßnahmen — 10 min

Die Paare erhalten jeweils eine fehlerhafte Aussage zum Leitfall und wählen eine Gegenmaßnahme; danach Abgleich:

| Fehlerbild | Learning | Ops-Konsequenz |
|---|---|---|
| Plausible Falschaussage | Flüssige Sprache ist kein Beleg. | Beobachtung und Hypothese trennen; konkrete Quelle prüfen. |
| Veraltetes Wissen/Runbook | Modellwissen und Dokumente können veraltet sein. | Aktuelle Tool-Daten, Version und Zeitstempel berücksichtigen. |
| Unterschiedliche Resultate | Sampling und Laufzeitsystem beeinflussen Ergebnisse. | Einstellungen/versionierte Konfiguration dokumentieren und wiederholt evaluieren; Temperatur 0 garantiert keine identischen Läufe. |
| Kontextverlust | Relevantes kann fehlen, gekürzt oder übersehen werden. | Selektiver Kontext, expliziter Zustand, fehlende Evidenz nachfordern. |
| Prompt Injection in Logs/Runbooks | Externe Daten können Angriffsanweisungen enthalten. | Als untrusted behandeln; Tool- und Datenzugriff technisch begrenzen. |

Die Trennung von Anweisungen und Daten reduziert Angriffsflächen, ist allein aber keine verlässliche Abwehr. Auch lesender Zugriff kann vertrauliche Daten offenlegen ([F5](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)).

### Evidenzcheck — 7 min

Eine Diagnose mit erfundener Quelle und ein lückenhaftes, korrekt zitiertes Ergebnis vergleichen. Alle markieren **belegt / Hypothese / unbekannt** und formulieren den nächsten lesenden Prüfschritt. Auflösung: Auch eine vorhandene Quellenangabe muss die konkrete Behauptung tatsächlich stützen.

**Übergang:** Frische Daten müssen beschafft und geprüft werden. Dafür braucht das Modell ein System, das seine Vorschläge kontrolliert ausführt.

## Pause — 15 min

## 4. Vom LLM zum Agenten — 45 min

**Leitfrage:** Wer entscheidet über den nächsten Schritt, und wer darf ihn ausführen?  
**Ziele:** L3, L4, L5. **Vertiefung:** [F2](https://arxiv.org/abs/2210.03629), [F3](https://www.anthropic.com/engineering/building-effective-agents).

### Wiederaufnahme und Ausführungsformen — 8 min

- Ohne Folie: je ein Satz zu Kontext, Evidenz und Modellgrenze aus dem ersten Teil.
- **Einfacher Chat ohne Tools:** Mensch führt Aktionen aus und bringt Ergebnisse zurück. Chat bezeichnet zunächst die Oberfläche, nicht den Autonomiegrad.
- **Workflow:** Code legt Pfad und Übergänge fest; Modelle können begrenzte Schritte übernehmen.
- **Agent:** Das Modell wählt innerhalb gesetzter Grenzen nächste Aktionen/Tools; die Laufzeit prüft und führt sie aus.
- Drei Aufgaben zuordnen: Logzusammenfassung, festes Zertifikatsablauf-Runbook, offene Incident-Untersuchung. Mehrere Lösungen zulassen, sofern Nutzen und notwendige Autonomie begründet sind.

### Agent-Loop als vorgeführtes Beispiel — 10 min

Am Fallblatt einen vollständigen, vorbereiteten Tool-Schritt zeigen:

1. Ziel, Kontext und Grenzen laden.
2. Beobachtung und offene Hypothesen festhalten.
3. Nächsten Tool-Aufruf mit strukturierten Parametern vorschlagen.
4. Laufzeit validiert Aufruf und Berechtigungen; Tool liefert Ergebnis.
5. Ergebnis auf Fehler, Relevanz und Evidenz prüfen; Zustand aktualisieren.
6. Weiterarbeiten, erfolgreich stoppen oder mit offenen Fragen eskalieren.

Die Moderation erklärt die Entscheidung anhand sichtbarer Daten. Bewertet werden Tool-Trace, Ergebnis und überprüfbare Begründung. Modellseitige Selbsterklärungen sind kein Nachweis interner Denkprozesse. Ein Tool-Fehler darf weder als Beleg noch als Anlass zur eigenmächtigen Rechteausweitung gelten.

### Bausteine am selben Pfad — 10 min

| Baustein | Aufgabe im Leitfall | Abgrenzung |
|---|---|---|
| Tool | z. B. `get_pod_events(namespace, pod)` ausführen | Ausführbarer Vertrag; ein generierter Befehl allein wurde noch nicht ausgeführt. |
| Skill | Diagnoseprozedur mit Tools und Domänenwissen bereitstellen | Wiederverwendbare Anleitung; Begriff und Format sind implementationsabhängig, keine eigene Autorisierung. |
| RAG | Passende Runbook-Passagen suchen und in den Kontext geben | Retrieval zur Laufzeit trainiert das LLM nicht neu; Retrieval- und Antwortqualität getrennt prüfen. |
| Memory | Ausgewählten Zustand über Schritte/Sitzungen erhalten | Explizite Speicherung mit Herkunft, Lebensdauer und Zugriffsregeln; nicht gleich Modellgewichte. |
| MCP | Tools, Ressourcen und Prompts zwischen Host/Client und Server zugänglich machen | Schnittstellenprotokoll; umfasst auch Sicherheitsmechanismen, ersetzt aber weder Agent-Logik noch Cluster-RBAC. |

RAG kann Textsuche, Vektorsuche oder Kombinationen verwenden; eine Vector DB ist keine Voraussetzung für jeden Agenten. Retrieval-Embeddings dienen der Suche und sind nicht mit den internen Token-Embeddings aus Block 2 gleichzusetzen. Quellen: [F4](https://arxiv.org/abs/2005.11401), [F6](https://modelcontextprotocol.io/docs/learn/architecture).

### Angeleitete Anwendung — 17 min

- **5 min:** Paare verbessern „Repariere den Pod“ zu einem Arbeitsauftrag mit **Ziel, Scope, relevanten Daten, erlaubten Aktionen, Ausgabeformat und Stop-Kriterium**. Beispielziel: belegte Diagnose, offene Fragen und Änderungsvorschlag; keine Ausführung von Änderungen.
- **7 min:** Unvollständigen Agent-Trace ergänzen: nächstes Tool samt Parametern, erwartete unterscheidende Evidenz, Reaktion auf fehlende Berechtigung. Danach Runbook-Zugriff oder Live-Tool begründet auswählen.
- **5 min:** Musterlösung vergleichen. Stop bei ausreichender Evidenz, fehlenden Rechten, ausgeschöpftem Zeit-/Tool-/Tokenbudget oder wiederholtem Schritt ohne Informationsgewinn. Fehlende Daten ausdrücklich melden.

**Learning:** Ein guter Auftrag macht Erfolg prüfbar; technische Policies machen Grenzen wirksam. Beides wird benötigt.

## 5. Agentic-Ops-Architektur — 25 min

**Leitfrage:** Wo wird jede Grenze tatsächlich durchgesetzt?  
**Ziele:** L4, L5.

### Referenzpfad lesen — 8 min

```text
Operator → OpenCode (Agent-Host) → LiteLLM → Modell
                 └→ MCP-Client → [optionales MCP-Gateway]
                                      → OpenShift-MCP-Server → Kubernetes API / RBAC
```

Die Verzweigung zeigt Modellzugang und Toolzugang. Tool-Ergebnisse fließen zum Host zurück und können Teil des nächsten Modellkontexts werden.

- **OpenCode:** Beispiel für Session, Tool-Loop und menschliche Interaktion.
- **LiteLLM:** Beispiel für Modellzugang, Routing sowie Kosten-/Budgetkontrolle, abhängig von Konfiguration.
- **OpenShift-MCP-Server:** konkret ausgewählte Implementierung mit begrenztem Tool-Angebot; Name oder Protokoll garantieren keine Lesebeschränkung.
- **OpenShift/RBAC:** serverseitige Autorisierung für die verwendete Identität; eigener ServiceAccount mit minimalem Scope.
- **Optionaler RAG-Zweig:** Runbooks aus einer freigegebenen Wissensquelle; AnythingLLM/Vector DB nur als mögliche Umsetzung, falls im tatsächlichen Aufbau vorhanden.

Produkte illustrieren die Rollen; verpflichtendes Learning ist der Daten- und Kontrollfluss. Quellen: [F6](https://modelcontextprotocol.io/docs/learn/architecture), [F7](https://kubernetes.io/docs/concepts/security/rbac-good-practices/), [F8](https://opencode.ai/docs/), [F9](https://docs.litellm.ai/docs/).

### Kontrollpunkte zuordnen — 10 min

Drei Vierergruppen markieren im Pfad jeweils Berechtigungen, Datenfluss oder Ausführungskontrolle; kurz gegenseitig erklären:

- **Identität und Scope:** User, Agent und Tool-Identität unterscheiden; Namespace, Ressourcen und Verben begrenzen. Auch `exec` und Secret-Zugriff separat betrachten.
- **Daten:** Nur benötigte, freigegebene Informationen an Modell/Tools geben; Secrets redigieren, Egress begrenzen und Aufbewahrung regeln. Prompt- und Tool-Logs können selbst sensible Daten enthalten.
- **Ausführung:** Argumente validieren; Tool-Angebot, Ausgabeumfang, Timeouts, Wiederholungen und Budgets begrenzen. Alternative Shell-/Toolpfade dürfen Beschränkungen nicht umgehen.
- **Writes:** Konkreten Diff, Ziel, erwartete Wirkung, Validierung und Rollback-/Recovery-Pfad prüfen. Eine Freigabe muss an genau diese Aktion gebunden sein; wiederholte Ausführung berücksichtigen.
- **Nachvollziehbarkeit:** Fall-ID, Konfiguration/Versionen, Tool-Aufrufe, relevante Ergebnisse, Freigaben, Fehler, Laufzeit und Kosten angemessen protokollieren.

### Kontrollfrage — 7 min

Ein Log fordert den Agenten auf, Daten an eine externe URL zu senden; ein Tool-Aufruf wird vom Cluster abgelehnt. Gruppe erklärt jeweils erwartetes Verhalten und durchsetzende Komponente.

**Mindestnachweis:** Logtext verleiht keine Autorität; fehlende Rechte führen zur Übergabe. RBAC schützt Cluster-Ressourcen, Egress-Regeln begrenzen Netzwerkziele. Read-only allein schützt nicht vor Datenabfluss.

## 6. Live-Showcase & Falltransfer — 40 min

**Leitfrage:** Können wir den Lauf prüfen und das Vorgehen auf einen anderen Fehler übertragen?  
**Ziele:** L2, L5, L6.

### Vorbereitung

- Reproduzierbarer Leitfall, vorbereitete Musterdiagnose und bekannter Reset-Schritt.
- Festgelegter Namespace, technisch geprüfter Read-only-ServiceAccount, begrenztes Tool-Angebot; keine produktiven Credentials.
- Sichtbarer Arbeitsauftrag und vorab getestetes Zeit-/Tool-/Tokenbudget.
- Fallback-Aufzeichnung und statischer Tool-Trace mit denselben Haltepunkten; nach spätestens zwei Minuten technischer Störung wechseln.

### Demonstration mit Vorhersagepausen — 20 min

1. **3 min:** Ticket, Erfolgskriterium, Architektur und Grenzen wiederholen. Vierergruppen verteilen Rollen: Hypothesen, Evidenz, Berechtigungen, Zeit/Kosten.
2. **12 min:** Agent starten. Vor zwei entscheidenden Tool-Aufrufen pausieren: Alle wählen den nächsten sinnvollen Schritt, dann tatsächlichen Aufruf und Ergebnis vergleichen. Nicht die genaue Tool-Reihenfolge, sondern Informationsgewinn und erlaubten Scope bewerten. Mindestens eine anfängliche Hypothese anhand der Daten verwerfen.
3. **5 min:** Diagnose und Änderungsvorschlag prüfen. Es bleibt bei einem Vorschlag; die Teilnehmenden benennen zusätzlich Validierung und Rollback. Fehlgeschlagene oder unbelegte Ausgaben werden am vorbereiteten Trace ausgewertet.

### Fallvariante ohne Schritt-für-Schritt-Hilfe — 10 min

Neues Material: Ein anderer Pod zeigt `ImagePullBackOff`; die entscheidenden Events fehlen zunächst. Gruppen formulieren Hypothese, benötigte Evidenz, nächsten erlaubten Tool-Aufruf und Stop-Bedingung. Danach Eventkarte aufdecken und Antwort überarbeiten. Eine vorschnell übernommene ConfigMap-Diagnose wird so sichtbar korrigiert.

### Debrief und Evaluation — 10 min

Gemeinsam anhand derselben Rubrik beurteilen: **fachlich korrekt? durch Quellen gestützt? Scope eingehalten? sinnvoll gestoppt? Aufwand vertretbar?**

- Was leistete das Modell, was lieferten Tools und Plattform?
- Wo blieb Unsicherheit, und wie wurde sie kenntlich gemacht?
- Einen manuellen Ablauf als Vergleichsbasis nennen. Für einen Piloten historische Fälle mit erwarteten Belegen, Tool-Fehlern, fehlenden Rechten und irreführenden Inhalten vorsehen.
- Qualität, Regelverstöße, Eskalationen, Zeit und Kosten pro Fall messen; Agent-Läufe bei relevanter Varianz wiederholen. Diagnosequalität und tatsächliche Behebung getrennt bewerten.

**Learning:** Die Demo macht Mechanik sichtbar. Belastbare Aussagen über Nutzen und Zuverlässigkeit brauchen mehrere repräsentative Fälle und eine Vergleichsbasis.

## 7. Use-Case-Lab — 35 min

**Leitfrage:** Welcher begrenzte Einsatz rechtfertigt einen Piloten?  
**Ziele:** L3–L7. Drei Vierergruppen arbeiten mit einer einseitigen Pilotkarte.

### Eigene Fälle und Auswahl — 7 min

Erst still je einen Fall notieren: **Wenn [Signal], soll [System] [prüfbares Ergebnis] liefern, mit [Daten/Tools].** Pro Gruppe einen Kandidaten auswählen. Offenlassen, ob ein Agent nötig ist: manuell, klassischer Workflow und modellgestützter Workflow sind ebenfalls mögliche Ergebnisse.

### Pilotkarte ausarbeiten — 15 min

- **Aufgabe und Nutzen:** Nutzer:in, Häufigkeit, heutiger Aufwand und gewünschte Verbesserung.
- **Ausführungsform:** Warum braucht die Aufgabe diese Autonomie? Was kann deterministisch bleiben?
- **Evidenz und Scope:** Datenquellen, Aktualität, erlaubte Tools/Namespaces; read-only oder konkret begrenzte Writes.
- **Grenzen:** möglicher Blast Radius, sensible Daten, Freigabe, Abbruch, Übergabe und Recovery.
- **Evaluation:** historische Fälle, erwartete Ergebnisse/Belege und manueller oder bestehender automatisierter Vergleichsablauf.
- **Erfolg:** messbare Qualität, maximaler Aufwand und unzulässige Ereignisse; Grenzwerte vor dem Piloten festlegen.

### Peer-Review und Priorisierung — 8 min

Je Gruppe zwei Minuten Pitch, anschließend zwei Minuten gemeinsame Auswahl. Nutzen, Risiko und Umsetzbarkeit jeweils **niedrig/mittel/hoch mit Begründung** markieren; keine scheinpräzise Multiplikation subjektiver Scores.

Reviewfragen: „Woran erkennen wir eine falsche Antwort?“, „Wo wird die Grenze durchgesetzt?“, „Was fehlt für einen testbaren Piloten?“ Fehlende Berechtigungs- oder Datengrundlage bedeutet zunächst Klärungsbedarf. Unter geeigneten Kandidaten priorisiert die Gruppe nach Nutzen.

### Nächsten Schritt konkretisieren — 5 min

Für den stärksten Kandidaten Verantwortliche:n, schmalsten Testumfang, nächste Aktivität und Review-Termin auf der Pilotkarte eintragen. Das Ergebnis ist ein Vorschlag für einen kontrollierten Piloten.

## 8. Lernnachweis & Abschluss — 15 min

- **6 min – Individuelles Exit Ticket ohne Folien:** Die drei Aussagen aus Block 1 erneut beurteilen und jeweils begründen. Zusätzlich zum eigenen Use Case eine Evidenzquelle, eine technische Grenze und eine Erfolgsmetrik nennen.
- **4 min – Auflösen und korrigieren:** Alle drei Einstiegsaussagen sind falsch. Erwartet werden: Kontext statt Gewichtsänderung; Tokenwahrscheinlichkeit statt Wahrheitsbeleg; Datenrisiken trotz Read-only. Verbleibende Fehlvorstellungen unmittelbar am Fall klären.
- **5 min – Transfer:** Erwartungskarten abgleichen; jede Person notiert einen nächsten Anwendungsschritt und eine offene Frage. Individuelle Antworten und Pilotkarten machen weiteren Lernbedarf sichtbar.

**Drei Merksätze:**

1. LLM-Ausgaben brauchen prüfbare Evidenz.
2. Agenten verbinden Modellentscheidungen mit kontrollierter Ausführung.
3. Geeignete Ops-Automation hat klare Grenzen und messbare Ergebnisse.

**Optionale Nachbereitung:** Nach ein bis zwei Wochen eine kurze neue Fallkarte selbst bearbeiten und im Teamreview besprechen; Pilotkarte anhand erster Ergebnisse überarbeiten. Nicht Teil der 270 Minuten.

## Kürzungs- und Vertiefungsoptionen

Die Minuten gelten in der Reihenfolge der Blöcke 1–8; die Pause liegt nach Block 3.

| Format | 1 | 2 | 3 | Pause | 4 | 5 | 6 | 7 | 8 | Gesamt |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Voller Workshop | 20 | 50 | 25 | 15 | 45 | 25 | 40 | 35 | 15 | 270 min |
| Kompakt | 10 | 30 | 15 | 10 | 30 | 15 | 30 | 25 | 15 | 180 min |
| Überblick mit Demo | 5 | 15 | 10 | 0 | 15 | 10 | 25 | 0 | 10 | 90 min |

- **180 Minuten:** Hardware auf Grundidee reduzieren, weniger Pipeline-Details, ein gemeinsames Architekturbeispiel. Fallvariante, Feedback und reduzierte Pilotkarte erhalten.
- **90 Minuten:** L1–L5 nur orientierend behandeln; Demo mit einer Entscheidungsfrage und Abschlusscheck. Kein gleichwertiger Nachweis für selbstständigen Pilotentwurf oder Evaluation (L6/L7).
- **Ganztägige Vertiefung:** Tool-Contract-/Prompt-Lab, Threat Modeling, eigener Eval-Datensatz und kontrollierte Änderung mit Validierung ergänzen. MoE, Quantisierung und Serving-Tuning nur bei entsprechendem Lernbedarf vertiefen.

## Material- und Moderationscheckliste

- Ticket und abgestufte Evidenzkarten zum Leitfall; zusätzliche Fallvariante mit Musterlösung.
- Fallblatt, Pipeline-Karten, Architekturpfad, Demo-Prüfrubrik, Pilotkarte und Exit Ticket passend zu den Lernzielen.
- Drei Vierergruppen, Timer und Fragenparkplatz; keine lokale Agent-Installation für die Teilnahme erforderlich.
- Browser mit Präsentation/Visualisierungen; Demo-Cluster, RBAC, Tool-Angebot und Budgets vorab prüfen.
- Konfiguration ohne sichtbare Secrets; Datenfreigaben und Protokollierung für den Demo-Aufbau klären.
- Screen Recording und statischer Tool-Trace als gleichwertiges Moderationsmaterial bei Demo-Ausfall.
- Unterlagen und Literatur als Nachlese bereitstellen; keine Vorablektüre voraussetzen.

## Literatur und Referenzen

Die didaktischen Quellen begründen die Gestaltung; die Fachquellen dienen der Vertiefung. Forschungsarbeiten sind keine Garantie für einzelne Produkte oder diesen Workshop. Produktdokumentation beschreibt veränderliche Implementierungen; für die Demo verwendete Versionen und Konfigurationen separat festhalten.

### Didaktische Grundlagen — für die Moderation

- **D1 — Merrill, M. D. (2002):** *First Principles of Instruction*. Educational Technology Research and Development, 50(3), 43–59. [DOI](https://doi.org/10.1007/BF02505024). Grundlage für den problemzentrierten Aufbau mit Aktivierung, Demonstration, Anwendung und Integration.
- **D2 — Sweller, J. & Cooper, G. A. (1985):** *The Use of Worked Examples as a Substitute for Problem Solving in Learning Algebra*. Cognition and Instruction, 2(1), 59–89. [DOI](https://doi.org/10.1207/s1532690xci0201_3), [Volltext](https://onderwijs.felienne.nl/vakdidactiek/materiaal/sweller_worked_examples.pdf). Begründet das vorgeführte Lösungsbeispiel für neue Inhalte; ursprünglicher Untersuchungsbereich ist Algebra.
- **D3 — Roediger, H. L. III & Karpicke, J. D. (2006):** *Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention*. Psychological Science, 17(3), 249–255. [DOI](https://doi.org/10.1111/j.1467-9280.2006.01693.x). Grundlage für kurze Abrufphasen und den erneuten Einstiegstest am Ende.

### Fachliche Vertiefung — nach Interesse

- **F1 — Vaswani et al. (2017):** *Attention Is All You Need*. NeurIPS. [Paper](https://arxiv.org/abs/1706.03762). Primärquelle für Transformer, Attention und Positionsinformation; Block 2 verwendet daraus eine vereinfachte Erklärung autoregressiver Generierung, nicht die vollständige ursprüngliche Encoder-Decoder-Architektur.
- **F2 — Yao et al. (2023):** *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR; Preprint 2022. [Paper](https://arxiv.org/abs/2210.03629). Hintergrund zum Wechsel zwischen Modellausgabe, Aktion und Beobachtung in Block 4.
- **F3 — Anthropic (2024):** *Building effective agents*. [Engineering-Artikel](https://www.anthropic.com/engineering/building-effective-agents). Praxisreferenz für Workflow-/Agent-Unterscheidung und einfache, überprüfbare Architekturen; Herstellerperspektive.
- **F4 — Lewis et al. (2020):** *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS. [Paper](https://arxiv.org/abs/2005.11401). Forschungsgrundlage für die Verbindung von Modell und externer Wissensquelle; das Paper trainiert Komponenten, während das Abrufen von Kontext im Workshop keine neue Trainingsphase ist.
- **F5 — OWASP (2025):** *LLM01: Prompt Injection*. [Risikobeschreibung](https://genai.owasp.org/llmrisk/llm01-prompt-injection/). Beispiele und Gegenmaßnahmen zu nicht vertrauenswürdigen Inhalten; Blöcke 3 und 5.
- **F6 — Model Context Protocol:** *Architecture overview*. [Offizielle Dokumentation](https://modelcontextprotocol.io/docs/learn/architecture). Host, Client, Server sowie Tools, Ressourcen und Prompts; Blöcke 4 und 5.
- **F7 — Kubernetes:** *Role Based Access Control Good Practices*. [Offizielle Dokumentation](https://kubernetes.io/docs/concepts/security/rbac-good-practices/). Least Privilege und Grenzen von RBAC; Architektur und Demo.
- **F8 — OpenCode:** [Offizielle Dokumentation](https://opencode.ai/docs/). Referenz für den eingesetzten Agent-Host; konkrete Tools und Permissions vor der Demo prüfen.
- **F9 — LiteLLM:** [Offizielle Dokumentation](https://docs.litellm.ai/docs/). Referenz für Modellzugang und Proxy-Funktionen im konkreten Aufbau.

**Empfohlene Nachlese:** F3 für Architekturentscheidungen, F5/F7 für Kontrollgrenzen, anschließend F1/F2/F4 nach technischem Interesse. D1–D3 dienen der Workshop-Gestaltung und sind keine Pflichtlektüre für Teilnehmende.
