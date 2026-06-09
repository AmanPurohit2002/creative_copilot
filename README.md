# Creative Copilot 🎬🤖

**🚀 Live Demo:** [https://creative-copilot-one.vercel.app/](https://creative-copilot-one.vercel.app/)

An Agentic Multi-Agent workflow built with **LangGraph**, **FastAPI**, **React**, and **Groq**, designed to transform a one-line ad idea into a fully annotated, shot-by-shot storyboard with AI-generated image panels.

## 🌟 Features

- **Multi-Agent Architecture**: Autonomous AI agents (Creative Director, Brainstormer, Reviewer, Screenwriter, Storyboard Artist) collaborate to refine ideas.
- **Agentic Reflection Loop**: The Brainstormer and Reviewer agents engage in a self-correcting loop, iterating on concepts up to 3 times to ensure diversity, feasibility, and alignment with the brief.
- **Human-in-the-Loop**: The autonomous graph pauses to allow the user to select their favorite concept before proceeding to script and image generation.
- **Blazing Fast LLM**: Powered by **Groq** (Llama 3) for near-instant text generation and `instructor` for guaranteed structured JSON outputs.
- **Persistent Memory**: Uses **Redis** as a Checkpointer to save the LangGraph state, allowing the graph to pause for human input and seamlessly resume later.
- **PDF Export**: Automatically generates a highly polished, downloadable PDF storyboard.

## 🏗️ Architecture & LLD (Low-Level Design)

The backend uses a **LangGraph StateGraph** to orchestrate the agents. 

### Agentic Flow:
1. **Idea Input** → User provides a raw idea.
2. **Creative Director** → Expands the idea into a structured Creative Brief.
3. **Brainstormer** → Generates 3 unique creative concepts based on the brief.
4. **Reviewer (Reflection Loop)** → Critiques the concepts. If they are generic or miss the mark, it routes back to the Brainstormer with feedback (up to a `MAX_REVISIONS` limit).
5. **Human Interrupt** → Graph pauses (`interrupt_before=["screenwriter"]`). The frontend polls the state and asks the user to pick a concept.
6. **Screenwriter** → Breaks the chosen concept down into a shot-by-shot script.
7. **Storyboard Artist** → Generates image generation prompts and fetches placeholder images for the final panels.

## 🛠️ Tech Stack

### Frontend
- **React** (Vite)
- **Vanilla CSS** (Custom styling with animations and glassmorphism)

### Backend
- **FastAPI** (Python async backend)
- **LangGraph** (Multi-agent orchestration and StateGraph)
- **LangChain Core** & **Instructor** (Structured LLM outputs)
- **Redis** (State persistence and checkpointer)
- **Groq API** (Llama 3 70B for fast reasoning)
- **ReportLab** (PDF generation)

## 🚀 Setup & Installation

### Prerequisites
- Docker and Docker Compose installed
- A Groq API Key

### 1. Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Run with Docker
Start the entire stack (Frontend, Backend, and Redis) using Docker Compose:
```bash
docker compose up -d --build
```

### 3. Access the Application
- **Frontend App**: [http://localhost:3080](http://localhost:3080)
- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📝 Usage Flow
1. **Enter Idea**: Type a simple prompt like *"A 15s reel for a luxury watch brand during Diwali"*.
2. **Agents Work**: Watch the agent activity indicator as the Creative Director, Brainstormer, and Reviewer refine the concepts in the background.
3. **Pick Concept**: Review the brief and select one of the 3 polished concepts.
4. **Storyboard**: The Screenwriter and Storyboard Artist will generate the final shots and panels. Click "Export PDF" to download the result!
