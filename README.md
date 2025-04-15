# AI-Powered Startup Deck Generator

The AI-Powered Startup Deck Generator allows users to quickly generate a professional startup pitch deck from a single-line idea input using CrewAI agents and Groq LLMs. It generates content in markdown and provides an option to export it as a PDF.

---

## Features
- Enter a startup idea in natural language
- Generate an end-to-end pitch deck using LLM agents
- Review output in markdown format
- Download the deck as a PDF

---

## Tech Stack

| Layer          | Technology           |
|----------------|----------------------|
| UI             | Streamlit            |
| Agents         | CrewAI               |
| LLM Backend    | Groq (via langchain_groq) |
| Markdown to PDF| markdown2, reportlab |
| Config         | YAML                 |
| Env Mgmt       | python-dotenv        |
| Dependency     | Poetry (pyproject.toml) |

---
## System Architecture

```
┌────────────────────────────┐
│        User (Frontend)     │
│   (Interacts via browser)  │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│       Streamlit App        │
│        `app.py`            │
│ - Takes input (idea)       │
│ - Triggers generation      │
│ - Shows markdown preview   │
│ - Offers PDF download      │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│    Core Generation Logic   │
│         `main.py`          │
│ - Calls build_crew()       │
│ - Handles retries, errors  │
│ - Saves output to .md      │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│        CrewAI Engine        │
│         `crew.py`          │
│ - Loads YAML config        │
│ - Creates agents/tasks     │
│ - Calls `Crew.kickoff()`   │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│         Groq LLM           │
│ (via `langchain_groq`)     │
│ - Processes each task      │
│ - Returns task results     │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│     Markdown Formatter     │
│  - `deck_output.md` file   │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│     PDF Generator Module    │
│     `pdf_generator.py`      │
│ - Converts .md → PDF        │
│ - Outputs `deck_output.pdf` │
└────────────────────────────┘
```

---

## Folder Structure
```
startup_deck_generator/
├── app.py               # Streamlit interface
├── main.py              # Core logic with retry/error handling
├── crew.py              # CrewAI build and config
├── pdf_generator.py     # Converts markdown to PDF
├── config/
│   ├── agents.yaml      # Role + behavior for each agent
│   └── tasks.yaml       # Task descriptions & order
├── deck_output.md       # Generated pitch deck in markdown
├── deck_output.pdf      # Final exported PDF file
├── .env                 # GROQ API key
└── pyproject.toml       # Project setup and dependencies
```

---

## Setup Instructions

1. **Install dependencies**  
```bash
poetry install
```

2. **Set your Groq API key**  
Create a `.env` file with the following:
```
GROQ_API_KEY=your_key_here
```

3. **Run the Streamlit app**  
```bash
streamlit run app.py
```

---

## Credits
- Built with [CrewAI](https://docs.crewai.com/)
- Powered by [Groq LLM](https://console.groq.com)
- Uses [markdown2](https://github.com/trentm/python-markdown2), [ReportLab](https://www.reportlab.com/), and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

## License
MIT License

