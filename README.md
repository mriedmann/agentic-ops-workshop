# SVC AI Workshop

Workshop-Unterlagen für erfahrene Linux-/OpenShift-Operator:innen: LLM-Grundlagen, Agenten, MCP und ein kontrollierter Agentic-Ops-Showcase.

## Inhalt

- `index.html` — RevealJS-Präsentation mit Speaker Notes
- `animations.py` — neun Manim-Szenen für die zentralen Konzepte, mit Klick-Haltepunkten
- `OUTLINE.manual.md` — handschriftliche Struktur, Grundlage der Folien
- `OUTLINE.md` — älterer, ausformulierter Entwurf; nicht die Grundlage der aktuellen Folien
- `llm-explained.py` — ursprünglicher, umfangreicher Manim-Entwurf (nicht von der Präsentation verwendet)

## Konventionen im Deck

- Jede Inhaltsfolie startet leer: sichtbar sind nur Eyebrow und Titel, alles andere ist ein Fragment.
- Jede Inhaltsfolie endet mit einer Kernaussage (`class="bottom-line"`), damit sie auch ohne Vortrag trägt.
- Die Grundlagen-Folien tragen `data-step` und zeigen oben rechts ihre Station in der GPT-Pipeline.
- Durchgängiges Beispiel: „Aus dem kleinen Setzling wurde ein großer …“ → „Baum“ (Konstanten in `animations.py`).

## Einmalig einrichten

```bash
npm install
uv sync
```

RevealJS wird lokal installiert; die Präsentation benötigt während des Workshops keine Internetverbindung.

## Animationen rendern

```bash
./scripts/render-animations.sh
```

Die MP4-Dateien landen in `media/`, zusammen mit je einer `*.steps.json` mit den Haltepunkten.

Die Videos laufen nicht automatisch, sondern werden per Klick weitergeschaltet. In `animations.py` beendet `self.step()` einen Hauptschritt einer Szene. In `index.html` spielt ein Fragment mit `data-video-step="N"` das Video bis Haltepunkt N; unsichtbare Schritte sind `<span class="fragment video-step" data-video-step="N"></span>`. `npm run check` meldet, wenn Fragmente und Haltepunkte nicht zusammenpassen. Ohne gerenderte Videos zeigt die Präsentation an deren Stelle einen beschrifteten Fallback. Manim benötigt unter Linux unter anderem FFmpeg, Cairo und Pango; abhängig von der Distribution können zusätzliche Systempakete nötig sein.

Für einen schnellen Einzeltest:

```bash
uv run manim -ql --format=mp4 animations.py AgentLoop
```

## Präsentation starten

```bash
npm start
```

Anschließend `http://localhost:8000` öffnen.

- Navigation: Pfeiltasten oder Leertaste
- Speaker View: `S`
- Übersicht: `Esc`
- Vollbild: `F`
- PDF-Export: `http://localhost:8000/?print-pdf` öffnen und über den Browser als PDF drucken

## Prüfen

```bash
npm run check
```

Der Check zählt die Slides und meldet noch nicht gerenderte Videos. Geprüft werden außerdem die Konventionen oben: leerer Folienstart, Kernaussage je Folie und passende Klick-Haltepunkte.

## Demo vor Ort

Vor dem Kundentermin sollten zusätzlich geprüft werden:

1. Videos lokal gerendert und im Präsentationsbrowser getestet.
2. Test-Namespace und dedizierter Read-only-ServiceAccount verfügbar.
3. LiteLLM-, MCP- und OpenCode-Konfiguration ohne sichtbare Secrets vorbereitet.
4. Incident reproduzierbar und Reset-Schritt dokumentiert.
5. Screen Recording oder statische Tool-Ausgaben als Offline-Fallback vorhanden.
