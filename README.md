# Agentic Ops Workshop

Workshop-Unterlagen für erfahrene Linux-/OpenShift-Operator:innen: LLM-Grundlagen, Agenten, MCP und ein kontrollierter Agentic-Ops-Showcase.

## Inhalt

- `slides.md` — Slidev-Präsentation mit Speaker Notes (HTML-Folien, Kommentare am Folienende sind Notizen)
- `style.css`, `layouts/deck.vue`, `global-top.vue`, `components/` — Gestaltung, Folienlayout, Kopf-/Fußzeile, Stationsleiste und Video-Komponente
- `animations.py` — neun Manim-Szenen für die zentralen Konzepte, mit Klick-Haltepunkten
- `OUTLINE.manual.md` — handschriftliche Struktur, Grundlage der Folien

## Konventionen im Deck

- Jede Inhaltsfolie startet leer: sichtbar sind nur Eyebrow und Titel, alles andere erscheint per `v-click="N"`. Die Klicknummern sind explizit, weil verschachtelte `v-click` sonst in falscher Reihenfolge zählen.
- Jede Inhaltsfolie endet mit einer Kernaussage (`class="bottom-line"`), damit sie auch ohne Vortrag trägt.
- Die Grundlagen-Folien tragen im Frontmatter `step:` (die Übungsfolien `exercise:`) und zeigen oben rechts ihre Station.
- `section:` im Frontmatter steuert die Kapitelanzeige unten rechts, `bg:` eine abweichende Hintergrundfarbe.
- Durchgängiges Beispiel: „Aus dem kleinen Setzling wurde ein großer …“ → „Baum“ (Konstanten in `animations.py`).

## Einmalig einrichten

```bash
npm install
uv sync
```

Slidev wird lokal installiert; die Präsentation benötigt während des Workshops keine Internetverbindung.

## Animationen rendern

```bash
./scripts/render-animations.sh
```

Die MP4-Dateien landen in `public/media/`, zusammen mit je einer `*.steps.json` mit den Haltepunkten.

Die Videos laufen nicht automatisch, sondern werden per Klick weitergeschaltet. In `animations.py` beendet `self.step()` einen Hauptschritt einer Szene. In `slides.md` steht das Video als `<StepVideo src="media/x.mp4" steps="media/x.steps.json">Fallback</StepVideo>`; ein Element mit `v-click` und `data-video-step="N"` spielt es bis Haltepunkt N. Unsichtbare Schritte sind `<span class="video-step" v-click="K" data-video-step="N"></span>`. `npm run check` meldet, wenn Klicks und Haltepunkte nicht zusammenpassen. Ohne gerenderte Videos zeigt die Präsentation an deren Stelle einen beschrifteten Fallback. Manim benötigt unter Linux unter anderem FFmpeg, Cairo und Pango; abhängig von der Distribution können zusätzliche Systempakete nötig sein.

Für einen schnellen Einzeltest:

```bash
uv run manim -ql --format=mp4 animations.py AgentLoop
```

## Präsentation starten

```bash
npm start
```

Anschließend `http://localhost:3030` öffnen.

- Navigation: Pfeiltasten oder Leertaste
- Presenter-Ansicht mit Notizen: `http://localhost:3030/presenter/`
- Übersicht: `o`
- Vollbild: `f`
- PDF-Export: `npm run export` (schreibt `slides-export.pdf`, ein Klickzustand pro Seite). Der Export nutzt Google Chrome statt des
  Playwright-Chromiums, weil dieses kein H.264 abspielt und die Videobilder sonst leer blieben; anderer Pfad über `CHROME_PATH=…`.

## Prüfen

```bash
npm run check          # zählt Folien, meldet Warnungen
npm run check:strict   # dasselbe, bricht bei Warnungen ab (CI)
```

Der Check zählt die Slides und meldet noch nicht gerenderte Videos. Geprüft werden außerdem die Konventionen oben: leerer Folienstart, Kernaussage je Folie und passende Klick-Haltepunkte.

## Veröffentlichung über GitHub Pages

`.github/workflows/pages.yml` prüft bei jedem Push und Pull Request die Folien und veröffentlicht
den Stand von `main` auf GitHub Pages. Der Build läuft über `slidev build` mit dem Repository-Namen als
Basis-Pfad nach `_site`. Folien-URLs nutzen Hash-Routing (`#/12`), damit Direktlinks auf GitHub Pages funktionieren.

Einmalig im Repository einstellen: **Settings → Pages → Source: GitHub Actions**. Danach
erscheint die Präsentation unter `https://<benutzer>.github.io/<repository>/`.

Die Videos liegen im Repository, das Rendern mit Manim läuft bewusst nicht in der Pipeline.
Nach Änderungen an `animations.py` also lokal `./scripts/render-animations.sh` ausführen und die
neuen Dateien aus `public/media/` mit committen.

## Lizenz

Siehe `LICENSE`. Slidev wird über npm eingebunden und behält seine eigene MIT-Lizenz.

## Demo vor Ort

Vor dem Kundentermin sollten zusätzlich geprüft werden:

1. Videos lokal gerendert und im Präsentationsbrowser getestet.
2. Test-Namespace und dedizierter Read-only-ServiceAccount verfügbar.
3. LiteLLM-, MCP- und OpenCode-Konfiguration ohne sichtbare Secrets vorbereitet.
4. Incident reproduzierbar und Reset-Schritt dokumentiert.
5. Screen Recording oder statische Tool-Ausgaben als Offline-Fallback vorhanden.
