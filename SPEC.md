# ResearchPal — Project Specification

## 1. Overview

**Project Name:** ResearchPal  
**Type:** Voice-powered AI Research Assistant  
**Framework:** Google Agent Development Kit (ADK)  
**Model:** gemini-2.5-flash  

---

## 2. Problem Statement

Researching a topic today is slow and fragmented. A person opens multiple browser tabs,
reads through walls of text, switches between tools, and still has to manually piece
everything together. There is no memory of what was researched before, forcing the user
to repeat context every single time.

**ResearchPal solves this by letting you talk to it like a human research assistant.**
You ask a question out loud, it searches multiple sources in parallel, synthesizes the
results, and responds in plain spoken language — while remembering everything you've
asked before.

---

## 3. Goals

- Build a fully voice-interactive research assistant
- Cover every major feature of Google ADK in one project
- Be production-grade: modular, maintainable, and deployable
- Serve as a learning project that progresses from simple to complex

---

## 4. Target Users

- Students doing academic research
- Journalists tracking news and topics
- Professionals who need fast, reliable summaries
- Anyone tired of drowning in browser tabs

---

## 5. Tech Stack

| Layer | Technology |
|---|---|
| AI Framework | Google ADK (`google-adk`) |
| LLM | Gemini 2.5 Flash |
| Voice | Gemini Live API (bidirectional audio streaming) |
| Search | Google Search (built-in ADK tool) |
| Memory | ADK Memory Service |
| Session Management | ADK Session Service |
| Language | Python 3.14+ |
| Environment | python-dotenv |

---

## 6. Architecture

```
User (Voice/Text)
      ↓
VoiceInterface  [Live API — microphone in, speaker out]
      ↓
OrchestratorAgent  [LlmAgent — brain of the system]
      ├── ResearchAgent  [ParallelAgent]
      │       ├── WebSearchAgent    [LlmAgent + google_search tool]
      │       └── NewsAgent         [LlmAgent + google_search tool (news-focused)]
      │
      └── ProcessingPipeline  [SequentialAgent]
              ├── AnalysisAgent     [LlmAgent — filters and ranks results]
              └── SummaryAgent      [LlmAgent — formats for voice delivery]

Supporting Services:
  - MemoryService     [stores past topics, user preferences across sessions]
  - SessionService    [manages individual conversation lifecycles]

Custom Tools:
  - save_report()     [saves a research summary to a local file]
  - get_history()     [retrieves past research topics from memory]
```

---

## 7. ADK Features Covered

| ADK Feature | Where Used |
|---|---|
| `LlmAgent` | Orchestrator, WebSearch, News, Analysis, Summary agents |
| `SequentialAgent` | Analysis → Summary pipeline |
| `ParallelAgent` | WebSearch + News running simultaneously |
| `google_search` tool | WebSearchAgent and NewsAgent |
| Custom Tools (`@tool`) | `save_report`, `get_history` |
| Memory Service | Remembering past research topics and user preferences |
| Session Service | Managing each conversation independently |
| Live Voice API | Microphone input and audio output |
| `LiveRequestQueue` | Streaming audio to the agent in real-time |
| `runner.run_live()` | Consuming agent responses as a stream |

---

## 8. Project File Structure

```
voice-agent/
└── research_pal/
    ├── SPEC.md                  ← this document
    ├── __init__.py              ← exposes root_agent to ADK
    ├── agent.py                 ← defines root_agent (OrchestratorAgent)
    ├── .env                     ← API keys (never commit this)
    │
    ├── sub_agents/
    │   ├── __init__.py
    │   ├── research_agent.py    ← ParallelAgent (web + news)
    │   ├── web_search_agent.py  ← LlmAgent with google_search
    │   ├── news_agent.py        ← LlmAgent with google_search (news-focused)
    │   ├── analysis_agent.py    ← LlmAgent filters raw results
    │   └── summary_agent.py     ← LlmAgent formats response for voice
    │
    └── tools/
        ├── __init__.py
        ├── save_report.py       ← saves research output to file
        └── get_history.py       ← retrieves memory of past topics
```

---

## 9. Build Phases

### Phase 1 — Single Agent + Search Tool
**Goal:** Get a working agent that can search the web and answer a question.

What to build:
- `agent.py` with a single `LlmAgent`
- Wire up `google_search` as a tool
- Test via `adk web` (text interface first)

Success criteria: Ask "What is quantum computing?" and get a sourced, coherent answer.

---

### Phase 2 — Multi-Agent Pipeline
**Goal:** Break the single agent into specialized agents with clear responsibilities.

What to build:
- `web_search_agent.py` — only searches the web
- `news_agent.py` — searches for recent news
- `research_agent.py` — ParallelAgent running both above simultaneously
- `analysis_agent.py` — takes parallel results and filters them
- `summary_agent.py` — formats the final answer cleanly
- Wire them all into a SequentialAgent pipeline inside `agent.py`

Success criteria: Same question now goes through the full pipeline and returns a
richer, better-structured answer than Phase 1.

---

### Phase 3 — Memory + Custom Tools
**Goal:** Give ResearchPal a persistent brain.

What to build:
- `save_report.py` tool — saves the final summary to a `.txt` file
- `get_history.py` tool — retrieves list of previously researched topics
- Wire ADK MemoryService so the agent remembers across sessions
- Update OrchestratorAgent to use memory before searching
  (check if topic was already researched, offer to update or reuse)

Success criteria: Ask about a topic, end the session, start a new one, and ask
"what have I researched before?" — it should know.

---

### Phase 4 — Live Voice Interface
**Goal:** Replace the text interface with real microphone and speaker I/O.

What to build:
- A Python script using `LiveRequestQueue` and `runner.run_live()`
- Capture audio from the microphone in real-time
- Stream audio blobs to the agent
- Play back the agent's audio response through speakers
- Handle interruptions gracefully (user talks while agent is responding)

Success criteria: Full end-to-end voice conversation with ResearchPal —
no typing required.

---

## 10. Environment Variables

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_api_key_here
```

---

## 11. Constraints & Rules

- Never hardcode API keys — always use `.env`
- Each agent has one responsibility only (single responsibility principle)
- Tools are pure Python functions — no side effects beyond their stated purpose
- All agents use `gemini-2.5-flash` unless there is a specific reason to change
- Voice responses must be concise — no walls of text read aloud

---

## 12. Success Definition

ResearchPal is complete when:
1. You can speak a research question out loud
2. It searches the web using parallel agents
3. It returns a clean, spoken summary
4. It remembers what you've researched in past sessions
5. You can ask "what did I research last time?" and get a real answer
