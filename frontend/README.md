# Creative Copilot Frontend 🎬🤖

**🚀 Live Demo:** [https://creative-copilot-one.vercel.app/](https://creative-copilot-one.vercel.app/)

This is the React frontend for the Creative Copilot application. It features a modern, glassmorphic UI that allows users to interact with the LangGraph multi-agent backend to generate storyboards.

## Features
- **3-Step Wizard**: Idea Input → Concept Selection → Storyboard Generation.
- **Agent Activity Indicators**: Real-time feedback showing which AI agent is currently thinking/working.
- **PDF Export**: Direct download of the generated storyboard.

## Setup
```bash
npm install
npm run dev
```

## Environment Variables
Create a `.env` file for local development or set this in your deployment platform (e.g., Vercel):
```env
# Point this to your backend URL. If running locally via Docker, leave empty or point to http://localhost:8000
VITE_API_BASE=
```
