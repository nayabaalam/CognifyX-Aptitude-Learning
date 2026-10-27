# CognifyX Advanced
## Intelligent Aptitude Assessment & Analytics Platform

CognifyX is an academic demonstration project with a modern browser dashboard and a C-language decision engine. It includes a working light/dark theme toggle, four selectable background styles, assessment workflow, question bank, student directory, scoring, results history, analytics, and local data backup.

> **Architecture note:** The dashboard itself is HTML/CSS/JavaScript so it can deliver a polished browser interface and a responsive theme system. The scoring/adaptive-decision engine is implemented in C and is called through a small Python standard-library local server. This is a hybrid academic project, not a UI written entirely in C.

## Quick start (Windows)

1. Extract the ZIP file into a normal folder, e.g. `Desktop\CognifyX_Advanced_Project`.
2. Install **Python 3**. During installation, enable **Add Python to PATH**.
3. Recommended for C-engine integration: install **MinGW-w64/GCC** and add the folder containing `gcc.exe` to PATH.
4. Double-click `start_cognifyx.bat`.
5. The browser should open `http://127.0.0.1:8765`. Keep the console window open while using the application.
6. To stop the server, click the console window and press `Ctrl+C`.

### Run without the Python server

You can double-click `index.html` to preview the dashboard. Most UI interactions and theme controls still work, and scoring uses a JavaScript fallback. In this mode the C engine is not connected, and the browser may handle local file storage differently. For the intended end-to-end demo, use `start_cognifyx.bat`.

## C engine commands

The Python server automatically attempts to compile `c_engine/cognifyx_engine.c` with GCC at startup. You can also run `compile_c_engine.bat` on Windows, then use `demo_c_engine.bat` to show the scoring, adaptive transition and weakest-topic recommendation in a viva.

If GCC is already available on a terminal, compile manually:

```bash
gcc -std=c11 -O2 -Wall -Wextra c_engine/cognifyx_engine.c -o build/cognifyx_engine
```

Example commands (Windows executable path may end in `.exe`):

```bash
build/cognifyx_engine score 7 2 1 402 10
build/cognifyx_engine adapt 2 1
build/cognifyx_engine recommend 62 82 74 78
```

Run the included regression checks with:

```bash
python tests/test_c_engine.py
```

Expected behaviour:
- `score`: validates that correct + wrong + skipped equals total and returns JSON with net marks, accuracy and percentage.
- `adapt`: moves the target difficulty up one level after a correct answer or down one level after an incorrect answer, bounded to Easy (1) through Hard (3).
- `recommend`: returns the lowest-scoring category and a rule-based practice recommendation.

## Included features

- Dashboard KPI cards and interactive SVG performance chart.
- Functional light, dark, and system theme setting.
- Four background choices: Aurora, Mesh grid, Minimal, and Midnight glow.
- Assessment templates and timed practice test.
- Question navigation, answer selection, mark-for-review, auto-submit timer, and adaptive next-question selection when suitable unused questions exist.
- Scoring: +4 correct, −1 incorrect, 0 skipped; accuracy excludes skipped answers.
- Answer explanations and result review after submission.
- Question bank: add, edit, delete, search, category/difficulty filter, and CSV export.
- Student directory: add, view profile, delete, search, and CSV export.
- Results table, category analytics, exportable JSON/CSV, browser-local persistence, and reset-to-demo controls.
- JSON backup export, responsive mobile layout, keyboard shortcut `Ctrl+K` / `⌘K` for global search.

## Data and privacy

Demo records are stored in your current browser's `localStorage`; they are not uploaded to a cloud service. The local server binds to `127.0.0.1` and is intended for a single-computer academic demo. Do not place real student personal data into this prototype. Browser storage can be cleared, so use the JSON backup feature when needed.

## Limits to be aware of

- This is an educational prototype, not a production exam system.
- The interface uses client-side HTML/CSS/JavaScript. Do not describe it as an all-C user interface.
- The C engine implements transparent rule-based scoring and adaptive difficulty; it does **not** implement validated IRT calibration or AI-based proctoring.
- The built-in sample students/results are fictional demonstration records and can be reset from Settings.
- If GCC is not found, the dashboard still works with a JavaScript fallback; the footer indicates the active mode.
- Internet is not required for the core app. Google Fonts are an optional enhancement; system fonts are used if they cannot load.

## Suggested viva demo

1. Switch between Light and Dark mode and show that the chosen background style changes independently.
2. Add a question with an explanation and confirm it appears in the question bank.
3. Start a practice test, answer some questions, mark a question for review, and submit.
4. Explain the +4/−1/0 scoring rule and show how the C engine returns JSON via `/api/score`.
5. Open Results & Reports and export a CSV; open Settings and download a JSON backup.

## Preview images

- `docs/preview.png` — light mode dashboard.
- `docs/dark_mode_preview.png` — dark mode dashboard with Midnight glow background.

## Folder map

```text
CognifyX_Advanced_Project/
├── index.html
├── assets/
│   ├── app.js
│   └── style.css
├── c_engine/
│   └── cognifyx_engine.c
├── build/                    # executable generated at runtime
├── tests/
│   └── test_c_engine.py
├── docs/
│   ├── PROJECT_REPORT.md
│   ├── VIVA_QUESTIONS.md
│   ├── preview.png
│   └── dark_mode_preview.png
├── server.py
├── start_cognifyx.bat
└── compile_c_engine.bat
```
