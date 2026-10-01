# Agentic Ops Workshop

Workshop-Unterlagen für erfahrene Linux-/OpenShift-Operator:innen: LLM-Grundlagen, Agenten, MCP und ein kontrollierter Agentic-Ops-Showcase.

Das Deck ist eine [Slidev](https://sli.dev)-Präsentation mit Speaker Notes. Die Animationen sind mit [Manim](https://www.manim.community) gerendert und werden per Klick Schritt für Schritt weitergeschaltet.

## Inhalt

- `slides.md` — die Folien samt Speaker Notes, in einer kompakten Markdown-Schreibweise
- `setup/` — übersetzt diese Schreibweise in das HTML der Folien
- `style.css`, `layouts/`, `components/`, `global-top.vue` — Gestaltung und Bausteine des Decks
- `animations.py` — die Manim-Szenen
- `public/media/` — die gerenderten Videos
- `AGENTS.md` — Regeln und Konventionen für Änderungen am Deck und für neue Workshop-Decks

## Voraussetzungen

- Node.js 22.12 oder neuer
- Google Chrome, nur für den PDF-Export
- [uv](https://docs.astral.sh/uv/) und Python 3.11 oder neuer, nur zum Rendern der Animationen

## Präsentation starten

```bash
npm install
npm start
```

Anschließend `http://localhost:3030` öffnen. Die gerenderten Videos liegen im Repository, zum Starten ist also kein Manim nötig. Alles wird lokal installiert; die Präsentation braucht während des Workshops keine Internetverbindung.

- Navigation: Pfeiltasten oder Leertaste
- Presenter-Ansicht mit Notizen: `http://localhost:3030/presenter/`
- Übersicht: `o`
- Vollbild: `f`

Vor einem Termin die Folien mit Videos einmal im Präsentationsbrowser durchklicken.

## PDF-Export

```bash
npm run export
```

Schreibt `slides-export.pdf` mit einer Seite pro Klickzustand. Liegt Chrome nicht als `google-chrome` im Pfad, den Pfad über `CHROME_PATH=…` angeben.

## Animationen rendern

Nur nötig, wenn `animations.py` geändert wurde.

```bash
uv sync
./scripts/render-animations.sh
```

Die Videos landen in `public/media/`. Manim benötigt unter Linux unter anderem FFmpeg, Cairo und Pango; abhängig von der Distribution können zusätzliche Systempakete nötig sein.

## Veröffentlichung über GitHub Pages

Jeder Push auf `main` veröffentlicht die Präsentation automatisch unter `https://<benutzer>.github.io/<repository>/`.

Einmalig im Repository einstellen: **Settings → Pages → Source: GitHub Actions**.

## Änderungen am Deck

Die Regeln für Inhalt, Aufbau und Technik stehen in `AGENTS.md`. Vor dem Committen muss `npm run check:strict` ohne Warnung durchlaufen.

## Lizenz

Siehe `LICENSE`. Slidev wird über npm eingebunden und behält seine eigene MIT-Lizenz.
