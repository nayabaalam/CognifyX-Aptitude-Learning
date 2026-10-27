# CognifyX: An Intelligent Aptitude Assessment and Analytics Platform

**Project type:** Computing Aptitude / MCA mini project  
**Implementation:** C decision engine + Python standard-library local bridge + HTML/CSS/JavaScript dashboard  
**Project status:** Functional academic prototype. The C engine compiled locally, six C regression tests passed, C API endpoints were smoke-tested, and browser interaction smoke tests covered theme switching, background selection, adding a question and submitting a practice test. Run the supplied Windows launcher on the target lab machine before submission.

## 1. Abstract

CognifyX is a small assessment and analytics platform intended to demonstrate how aptitude testing can be supported by digital workflows. The application provides a responsive dashboard, question-bank management, student records, a timed practice test, rule-based adaptive question selection, scoring, answer explanations, performance summaries, and exportable records. A C program provides the scoring and difficulty-transition decisions. A local Python HTTP server serves the interface and passes selected operations to that C executable. Browser-local storage preserves demo records between visits.

The project is designed as a transparent learning prototype. Its recommendation logic is rule-based; sample data are illustrative; adaptive difficulty is not claimed to be a psychometrically calibrated CAT model. Authentication, multi-user synchronization, database-backed storage, and production security are outside the current scope.

## 2. Problem statement

A basic quiz program usually reports only a final score. It often lacks structured question management, topic-level feedback, progress history, theme customization, result export, and a repeatable way to demonstrate scoring logic. CognifyX combines these functions in one local prototype while keeping the scoring/adaptation rules visible in C source code.

## 3. Objectives

1. Provide a professional, responsive aptitude dashboard.
2. Support separate Light, Dark, and System appearance modes.
3. Offer independent background presets (Aurora, Mesh grid, Minimal, Midnight glow).
4. Manage questions by category and difficulty.
5. Run a timed practice test with navigation, review markers and automatic submission.
6. Calculate negative-marking scores, accuracy, and category summaries.
7. Demonstrate simple adaptive difficulty using C code.
8. Preserve demo data locally and support CSV/JSON exports.
9. Present limitations and design decisions clearly for academic viva.

## 4. Scope and intended users

The prototype has two main personas: an administrator who maintains questions and student entries, and a learner who attempts the available practice assessment. In the current front-end demo, the exam flow runs as the signed-in sample administrator/learner name; roles are not protected by authentication. It is intended for local classroom demonstration, not formal high-stakes examination.

## 5. System architecture

```text
Browser UI (index.html + CSS + JavaScript)
        │  HTTP GET /api/score, /api/adapt, /api/health
        ▼
Python standard-library HTTP server (server.py)
        │  validates query arguments and runs child process
        ▼
C decision engine (cognifyx_engine.c)
        │  JSON result on stdout
        ▼
Browser renders scores, explanations, history and analytics

Browser localStorage: students, questions, assessment templates, results, theme, wallpaper, daily checklist
```

The C executable is compiled automatically when `server.py` starts if GCC or Clang is available. If it cannot be compiled, the interface uses JavaScript fallback scoring and indicates fallback mode.

## 6. Main modules

### 6.1 Dashboard and appearance

KPI cards, recent assessment activity, category bars, performance trend, and a daily checklist. Theme preference and background selection are saved locally. Light and dark modes use CSS custom properties, while the wallpaper presets affect the background layer separately.

### 6.2 Question bank

Each question includes an identifier, text, topic, difficulty, marks, four options, correct option and explanation. Add/edit operations check required fields and distinct options. Search, category/difficulty filters, and CSV export support basic administration.

### 6.3 Assessment workflow

The learner can answer questions, jump through a question palette, mark for review, move backward and forward, and submit. The timer triggers automatic submission at zero. Rule-based adaptation may replace a future question with an unused question matching the target difficulty when such an item exists in the current question bank.

### 6.4 Student directory

Profiles are created locally with name, email, join date and status. A profile shows stored attempts, average score and best score. This is a directory demo only; it has no secure login or email verification.

### 6.5 Analytics and exports

The dashboard shows category-level summaries and attempts. The user can export a CSV of students, questions or results, or download a JSON backup of the local workspace. These exports are intended for demonstration and do not substitute for secure server-side data governance.

## 7. Algorithms

### 7.1 Score calculation

Let `C` be correct answers, `W` incorrect answers, `S` skipped answers and `N = C + W + S` total questions.

- Net marks: `score = 4C - W`
- Maximum marks: `max_score = 4N`
- Display percentage: `clamp(100 × score / max_score, 0, 100)`
- Accuracy: `100 × C / (C + W)` when `C + W > 0`; otherwise 0.
- Input validation requires nonnegative counts and `C + W + S = N`.

### 7.2 Adaptive difficulty transition

Difficulty is represented by 1 = Easy, 2 = Medium, 3 = Hard. After a correct answer the target advances one level; after an incorrect answer it drops one level. The target is clamped to [1, 3]. The UI uses that target to choose a suitable unused question if one is available. This is a simple demonstration heuristic, not an Item Response Theory model.

### 7.3 Weak-category recommendation

The C engine accepts category scores from 0 to 100, locates the minimum score, and returns a predefined topic-specific practice recommendation. Ties resolve to the first category in the defined ordering.

## 8. Example calculation

Suppose a learner has 7 correct, 2 wrong and 1 skipped answer across 10 questions:

- Net marks = `(7 × 4) − 2 = 26`
- Maximum marks = `10 × 4 = 40`
- Display percentage = `26 / 40 × 100 = 65%`
- Accuracy = `7 / (7 + 2) × 100 ≈ 77.78%`

Expected command:

```text
cognifyx_engine score 7 2 1 402 10
```

Example JSON output:

```json
{"correct":7,"wrong":2,"skipped":1,"total":10,"seconds":402,"score":26,"max_score":40,"accuracy":77.78,"percentage":65.00}
```

## 9. Requirements

- Windows 10/11 recommended for the provided `.bat` launchers.
- Python 3.9+ (standard library only).
- GCC / MinGW-w64 recommended to compile the C engine; no third-party Python packages are required.
- Current desktop browser such as Microsoft Edge, Chrome or Firefox.
- Network access is not needed for core operation; Google Fonts are optional.

## 10. Testing and verification checklist

| Test | Expected result |
|---|---|
| Compile C engine with GCC | Executable created without compiler errors — passed locally |
| Score 7 correct, 2 wrong, 1 skipped | 26/40 marks, 77.78% accuracy, 65% score — passed locally |
| `adapt 2 1` | next level = 3 / Hard — passed locally |
| `adapt 2 0` | next level = 1 / Easy — passed locally |
| Invalid score totals (e.g. 5+1+1 for total 10) | rejected with nonzero exit code |
| Toggle Light / Dark | colors switch immediately and selected mode persists after refresh |
| Change background preset | backdrop changes without changing theme mode |
| Add question / add student | row appears and remains after refresh in same browser |
| Submit practice test | score, answer review and history appear |
| Download CSV / JSON backup | file downloads with exported local data |
| Timer reaches zero | test submits automatically |

## 11. Limitations

- Local browser storage is not a centralized database and may be cleared.
- No secure authentication, role enforcement, cloud sync, multi-client networking, or server-side audit trail is included.
- The JavaScript UI and Python bridge are not implemented in C; the scoring/adaptive decision engine is.
- Demo student and attempt records are fictional.
- No psychometric validity, fairness certification, or real-world proctoring detection is claimed.
- The current sample dashboard trends are for demonstration; proper conclusions require enough real assessment data.

## 12. Future scope

A future version could add SQLite-backed records, password hashing and roles, import/restore of validated backups, LAN examination sessions, question exposure limits, calibrated IRT/CAT, formal question-item analysis, accessibility audits, automated integration tests, and signed result certificates. Any high-stakes use would require security, privacy, fairness and assessment-validity review.

## 13. Conclusion

CognifyX demonstrates the integration of a professional interactive dashboard with a C-language scoring and adaptive-decision engine. It covers core programming concepts, input validation, modular design, local persistence, data visualization, file export, and a practical UI. Its simple rule-based algorithms are explainable and suitable for an MCA demonstration; more advanced psychometric and security features are explicitly future work rather than unsupported claims.
