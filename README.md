# Agentic Ops Workshop

Workshop-Unterlagen für erfahrene Linux-/OpenShift-Operator:innen: LLM-Grundlagen, Agenten, MCP und ein kontrollierter Agentic-Ops-Showcase.

Das Deck ist eine [Slidev](https://sli.dev)-Präsentation mit Speaker Notes. Die Animationen sind Vue-Komponenten mit [anime.js](https://animejs.com) und werden per Klick Schritt für Schritt weitergeschaltet.

## Inhalt

- `slides.md` — die Folien samt Speaker Notes, in einer kompakten Markdown-Schreibweise
- `setup/` — übersetzt diese Schreibweise in das HTML der Folien
- `style.css`, `layouts/`, `components/`, `global-top.vue` — Gestaltung und Bausteine des Decks
- `components/anim/`, `animations/` — die Animationen und das durchgehende Beispiel
- `AGENTS.md` — Regeln und Konventionen für Änderungen am Deck und für neue Workshop-Decks

## Voraussetzungen

- Node.js 22.12 oder neuer

## Präsentation starten

```bash
npm install
npm start
```

Anschließend `http://localhost:3030` öffnen. Alles wird lokal installiert; die Präsentation braucht während des Workshops keine Internetverbindung.

- Navigation: Pfeiltasten oder Leertaste
- Presenter-Ansicht mit Notizen: `http://localhost:3030/presenter/`
- Übersicht: `o`
- Vollbild: `f`

Vor einem Termin die Folien mit Animationen einmal im Präsentationsbrowser durchklicken.

## PDF-Export

```bash
npm run export
```

Schreibt `slides-export.pdf` mit einer Seite pro Klickzustand. Der Export nutzt das von `npm install` mitinstallierte Chromium; ein anderer Browser lässt sich über `CHROME_PATH=…` angeben.

```bash
npm run export:handout
```

Kurzfassung für Teilnehmende: `slides-handout.pdf` zeigt jede Folie einmal im Endzustand, Folien mit Animation einmal pro Animationsschritt. Die Sprechernotizen landen in `slides-handout-notes.pdf`.

## Veröffentlichung über GitHub Pages

Jeder Push auf `main` veröffentlicht die Präsentation automatisch unter `https://<benutzer>.github.io/<repository>/`.

Einmalig im Repository einstellen: **Settings → Pages → Source: GitHub Actions**.

## Änderungen am Deck

Die Regeln für Inhalt, Aufbau und Technik stehen in `AGENTS.md`. Vor dem Committen muss `npm run check:strict` ohne Warnung durchlaufen.

## Lizenz

Siehe `LICENSE`. Slidev wird über npm eingebunden und behält seine eigene MIT-Lizenz.
