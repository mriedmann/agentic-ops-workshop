# SVC AI Workshop

Workshop-Unterlagen für erfahrene Linux-/OpenShift-Operator:innen: LLM-Grundlagen, Agenten, MCP und ein kontrollierter Agentic-Ops-Showcase.

## Inhalt

- `OUTLINE.md` — ausformulierter Ablauf für ca. 4,5 Stunden inklusive Übungen und Demo-Dramaturgie
- `index.html` — RevealJS-Präsentation mit Speaker Notes
- `animations.py` — fünf kurze Manim-Szenen für die zentralen Konzepte
- `llm-explained.py` — ursprünglicher, umfangreicher Manim-Entwurf (nicht von der Präsentation verwendet)

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

Der Check zählt die Slides und meldet noch nicht gerenderte Videos. Inhaltliche Zeitboxen, Moderationshinweise und Kürzungsoptionen stehen in `OUTLINE.md`.

## Demo vor Ort

Vor dem Kundentermin sollten zusätzlich geprüft werden:

1. Videos lokal gerendert und im Präsentationsbrowser getestet.
2. Test-Namespace und dedizierter Read-only-ServiceAccount verfügbar.
3. LiteLLM-, MCP- und OpenCode-Konfiguration ohne sichtbare Secrets vorbereitet.
4. Incident reproduzierbar und Reset-Schritt dokumentiert.
5. Screen Recording oder statische Tool-Ausgaben als Offline-Fallback vorhanden.
