"""
Phase 5 - Console-Based AI News Research Agent
Researches a topic using DuckDuckGo search results, asks an OpenAI model to
synthesize those sources, and exports the report to Markdown or TXT.
"""
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    from ddgs import DDGS
    from openai import OpenAI
except ImportError as exc:
    print(f"Missing dependency: {exc}")
    print("Install requirements with: pip install -r requirements.txt")
    sys.exit(1)

load_dotenv()
OUTPUT_DIR = Path("reports")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def search_sources(topic, max_results=8):
    """Search the web and return a list of source records."""
    results = []
    try:
        with DDGS() as ddgs:
            for item in ddgs.text(topic, max_results=max_results):
                title = (item.get("title") or "Untitled").strip()
                url = (item.get("href") or item.get("url") or "").strip()
                body = (item.get("body") or item.get("snippet") or "").strip()
                if url:
                    results.append({"title": title, "url": url, "snippet": body})
    except Exception as exc:
        print(f"\nSearch warning: could not complete web search ({exc}).")
    return results


def build_prompt(topic, sources):
    if sources:
        source_text = "\n\n".join(
            f"[{i}] {s['title']}\nURL: {s['url']}\nSnippet: {s['snippet']}"
            for i, s in enumerate(sources, start=1)
        )
        source_note = (
            "Use only claims supported by the supplied source snippets. Do not invent "
            "facts, quotes, statistics, or sources. If evidence is limited or sources "
            "disagree, say so. Cite sources in the text as [1], [2], etc."
        )
    else:
        source_text = "No web search results were retrieved."
        source_note = (
            "Do not pretend that live research was completed. Clearly state that no "
            "sources were retrieved and make any uncertain points explicit."
        )

    return f"""
You are a careful research assistant. Prepare a clear, useful research report on:
TOPIC: {topic}

Required sections:
1. Research Topic
2. Executive Summary
3. Key Findings (numbered)
4. Detailed Analysis (with descriptive subheadings)
5. Source References (numbered list using the exact URLs below)
6. Conclusion

Rules:
- {source_note}
- Separate confirmed information from interpretation.
- Do not claim that snippets prove details they do not contain.
- Mention limitations of the research.
- Use readable Markdown and avoid unsupported precise statistics.

AVAILABLE SEARCH RESULTS:
{source_text}
"""


def generate_report(topic, sources):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to a .env file. See .env.example."
        )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You write evidence-aware research reports."},
            {"role": "user", "content": build_prompt(topic, sources)},
        ],
        temperature=0.2,
    )
    report = response.choices[0].message.content
    if not report:
        raise RuntimeError("The AI returned an empty report. Please try again.")
    if not sources:
        report += (
            "\n\n## Research Limitation\n\n"
            "No live search results were retrieved. Verify this report independently "
            "before relying on it."
        )
    return report


def export_report(topic, report):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_topic = re.sub(r"[^A-Za-z0-9_-]+", "_", topic).strip("_")[:60] or "research"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = OUTPUT_DIR / f"{safe_topic}_{stamp}.md"
    txt_path = OUTPUT_DIR / f"{safe_topic}_{stamp}.txt"

    md_path.write_text(report, encoding="utf-8")
    # TXT export uses the same readable report text; Markdown markers remain readable.
    txt_path.write_text(report, encoding="utf-8")
    return md_path, txt_path


def main():
    print("=" * 64)
    print("       AI NEWS RESEARCH AGENT — PHASE 5")
    print("=" * 64)
    print("Research a topic, create a structured report, and export it.")
    print("Type 'q' at the topic prompt to quit.\n")

    while True:
        try:
            topic = input("Enter a research topic: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting. Goodbye!")
            break

        if topic.lower() in {"q", "quit", "exit"}:
            print("Goodbye!")
            break
        if not topic:
            print("Error: topic cannot be empty. Please try again.\n")
            continue

        try:
            print("\nSearching for sources...")
            sources = search_sources(topic)
            print(f"Found {len(sources)} source(s).")
            print("Generating the report with AI...")
            report = generate_report(topic, sources)
            md_path, txt_path = export_report(topic, report)
            print("\n" + "-" * 64)
            print("REPORT PREVIEW")
            print("-" * 64)
            print(report[:2500] + ("\n...[preview shortened]" if len(report) > 2500 else ""))
            print("\n" + "-" * 64)
            print("Report completed successfully.")
            print(f"Markdown file: {md_path}")
            print(f"Text file:     {txt_path}")
            print("-" * 64 + "\n")
        except Exception as exc:
            print(f"\nError: {exc}")
            print("Check your internet connection, API key, model access, and dependencies.\n")


if __name__ == "__main__":
    main()
