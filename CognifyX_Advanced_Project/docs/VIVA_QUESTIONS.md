# CognifyX — Viva Voce Questions and Answers

1. **What is CognifyX?**  
   A local aptitude assessment and analytics prototype with question management, practice tests, results, and appearance settings.

2. **Why did you choose this project?**  
   It combines programming logic, data handling, scoring algorithms, user interface design and result analysis in a domain students can demonstrate clearly.

3. **Is the complete user interface written in C?**  
   No. The interface uses HTML, CSS and JavaScript for a responsive browser dashboard. The scoring/adaptive decision engine is written in C and is called through a Python standard-library server.

4. **What is the role of C in the project?**  
   C validates scoring inputs, calculates net marks and accuracy, transitions the difficulty target, and selects a rule-based weakest-topic recommendation.

5. **How is the final score calculated?**  
   Net marks = 4 × correct answers − incorrect answers. A skipped answer gives zero marks.

6. **How is the displayed percentage calculated?**  
   Net marks divided by maximum possible marks, multiplied by 100 and clamped between 0% and 100%.

7. **How is accuracy different from score percentage?**  
   Accuracy counts correct answers among attempted questions, excluding skipped questions. The score percentage also reflects negative marking and the maximum marks.

8. **How does adaptive difficulty work?**  
   A correct answer moves the target difficulty up one level; an incorrect answer moves it down one level. The level is bounded from Easy to Hard, and a matching unused question must be available.

9. **Is the adaptive method a real IRT-based CAT model?**  
   No. It is a simple rule-based demonstration. IRT requires calibrated question parameters and suitable response data.

10. **How are questions represented?**  
    As objects with an ID, question text, category, difficulty, marks, four options, correct option and explanation. The C component is kept separate from the UI question bank.

11. **What is localStorage?**  
    A browser key-value store used to preserve demo data between visits on the same browser profile.

12. **Where is data stored?**  
    In the browser's localStorage. Data are not automatically sent to a cloud database. This is not appropriate for real sensitive student records.

13. **What does the Python server do?**  
    It serves the static dashboard and forwards selected algorithm requests to the compiled C program, then returns the program's JSON output.

14. **Why use JSON between components?**  
    JSON is a simple structured format that is easy for the C command output and JavaScript client to exchange through HTTP.

15. **How does dark mode work?**  
    CSS custom properties change the interface color palette when the body theme attribute switches from light to dark. The selected setting is saved locally.

16. **How is background selection independent of dark mode?**  
    A separate wallpaper attribute chooses Aurora, Mesh grid, Minimal or Midnight glow background layers without changing the theme mode.

17. **How do you export results?**  
    CSV files are generated in the browser for spreadsheets; JSON is used for a full workspace backup or individual attempt report.

18. **What input validation is performed by the C engine?**  
    It checks numeric inputs, nonnegative counts, the correct/wrong/skipped sum, valid difficulty bounds, and category scores between 0 and 100.

19. **What testing did you perform?**  
    The C engine was compiled with GCC and sample score/adaptive/recommendation commands were run. A browser interaction smoke test covered theme changes, background selection, adding a question and submitting a practice test. The supplied Windows launcher should also be tested on the target college/lab machine.

20. **What are the current limitations?**  
    No production authentication, centralized database, LAN exam sessions, formal psychometric validation, or proctoring are included.

21. **How can you improve the project in future?**  
    Integrate SQLite, password hashing and roles, validated backup restore, LAN sessions, question exposure control, calibrated IRT, automated integration tests and a security review.

22. **What programming concepts are used?**  
    Functions, conditionals, numeric validation, process communication, HTTP request handling, JSON exchange, arrays/objects, DOM events, browser storage and data visualization.
