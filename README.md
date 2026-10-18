# AI News Research Agent — Phase 5

A console-based Python research agent. It searches the web for source snippets, asks an OpenAI model to synthesize a structured report, and exports both Markdown and TXT versions.

## Features
- Accepts a user-entered research topic
- Searches for source titles, URLs, and snippets
- Creates an executive summary, key findings, detailed analysis, source references, and conclusion
- Exports reports to the `reports/` directory as `.md` and `.txt`
- Validates empty input and handles missing API keys, search failures, and AI/API errors
- Repeats for multiple topics without restarting

## Setup (Windows / VS Code)
1. Install Python 3.10 or newer.
2. Open this project folder in VS Code.
3. Open the terminal and run:
   ```bash
   python -m venv .venv
   ```
4. Activate the environment:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`.
5. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
6. Copy `.env.example` to a new file named `.env`.
7. Open `.env` and replace the example value with your own OpenAI API key. Never upload `.env` to GitHub.
8. Run:
   ```bash
   python news_research_agent.py
   ```

## Example test
Enter `Artificial Intelligence in Education` at the topic prompt. The program should search for sources, generate a report, and show the paths of the saved `.md` and `.txt` files. Try a second topic to confirm the repeated workflow works. Enter a blank topic to test validation, then enter `q` to quit.

## Output format
Each report includes:
1. Research Topic
2. Executive Summary
3. Key Findings
4. Detailed Analysis
5. Source References
6. Conclusion

## Important accuracy note
The web search returns source snippets, not necessarily complete articles. The report is grounded in the retrieved snippets and includes their URLs, but important claims should be verified by opening the original sources. If no sources are found, the report notes that limitation instead of pretending live research succeeded.

## Phase 5 submission screenshots
Capture real screenshots after running the program:
1. Terminal showing the topic entered and sources found.
2. Terminal showing the report preview and successful export paths.
3. The generated Markdown report opened in VS Code.
4. Optional: test a second topic and show empty-input validation.

Submit these screenshots on the internship page. Do not use fabricated screenshots; run the program first.
