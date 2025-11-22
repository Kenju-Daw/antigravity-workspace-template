# Antigravity Remote Coding Assistant - Setup Guide

## Current Status

✅ **Docker**: Running  
✅ **Ollama**: Running in Docker container  
⏳ **Models**: Downloading (llama3.2 & tinyllama)  
✅ **Backend**: Running on http://localhost:8000  
✅ **Frontend**: Ready at `frontend/index.html`  

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Your Browser                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Frontend UI (index.html)                          │ │
│  │  - Drag & Drop Upload 📎                           │ │
│  │  - Chat Interface 💬                               │ │
│  │  - File Tree Visualization 📁                      │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │ WebSocket
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                 │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Orchestrator (Hybrid Intelligence)                │ │
│  │  ├─ Gemini Client (Cloud, Premium)                 │ │
│  │  └─ Local Client (Ollama, Fast & Private)         │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │  RAG System (ChromaDB)                             │ │
│  │  - Vector Store for Documents                      │ │
│  │  - Semantic Search                                 │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP API
                       ▼
┌─────────────────────────────────────────────────────────┐
│           Ollama (Docker Container)                      │
│           Port 11434                                     │
│  - llama3.2 (Primary Model)                             │
│  - tinyllama (Fast Testing Model)                       │
└─────────────────────────────────────────────────────────┘
```

## How It Works

### 1. **Hybrid Intelligence**
   - **Simple queries** → Local Ollama (fast, private)
   - **Complex tasks** → Gemini (powerful, cloud-based)
   - **Auto-fallback** → If Local fails, uses Gemini

### 2. **RAG (Retrieval Augmented Generation)**
   - Upload files via drag-and-drop or 📎 button
   - Files chunked and stored in ChromaDB
   - Queries automatically enriched with relevant context

### 3. **File Management**
   - Files uploaded to `drop_zone/`
   - Automatic watching for changes
   - Real-time file tree updates

## Quick Start

### Option 1: With Gemini (Cloud, Recommended)
```bash
# 1. Create .env file
echo GEMINI_API_KEY=your_actual_key_here > .env

# 2. Restart backend (it should already be running)
# The backend will auto-reload with the new .env
```

### Option 2: Local Only (Ollama)
```bash
# Models are downloading automatically
# Once complete, test with:
docker exec ollama ollama list

# Should show: llama3.2 and tinyllama
```

### Option 3: Both (Best)
- Set `GEMINI_API_KEY` in `.env` for fallback
- Use Ollama for daily tasks (fast & private)
- Gemini kicks in for complex queries

## Testing

### 1. Open the UI
```bash
# Just open in browser
start frontend/index.html
```

### 2. Test Upload
- Drag any file onto the page
- OR click the 📎 button
- File appears in sidebar

### 3. Test Chat
- Type: "Hello"
- Should see "Thinking..." animation
- Response from Local (Ollama) or Gemini

### 4. Test RAG
```bash
# 1. Upload a file (e.g., README.md)
# 2. Ask: "What does this project do?"
# Agent will retrieve context from uploaded file
```

## Monitoring

### Check Ollama Status
```bash
docker ps                      # Should show 'ollama' container
curl http://localhost:11434    # Should return: "Ollama is running"
docker exec ollama ollama list # Show available models
```

### Check Backend
```bash
# Backend logs (should be running in a terminal)
# Look for: "Orchestrator initialized with Hybrid Intelligence & RAG"
```

### Check Models Downloading
```bash
docker logs ollama --follow
```

## Configuration

### Environment Variables (.env)
```bash
# Gemini (Optional but recommended for fallback)
GEMINI_API_KEY=your_key_here

# Local Model (Optional, defaults to llama3.2)
LOCAL_MODEL=llama3.2
```

## Troubleshooting

### "Offline" status in UI
- Backend not running → Start: `uvicorn main:app --reload` (from `backend/` dir)
- Wrong port → Check `http://localhost:8000`

### "Could not connect to Ollama"
- Container not running → `docker ps` to check
- Wrong port → Should be `11434`
- Model not downloaded → Wait for download or use Gemini

### "Gemini API Key not configured"
- Create `.env` file with `GEMINI_API_KEY=your_key`
- Restart backend

### Models downloading slowly
- Normal on slow connection
- `tinyllama` is smaller (637MB) - will finish first
- `llama3.2` is larger (2GB) - may take 7-10 minutes

## Next Steps

1. ✅ Models are downloading (wait ~10 minutes)
2. ⏳ Add Gemini API key for fallback (optional)
3. 🎯 Test the system end-to-end
4. 🚀 Upload your project files for RAG
5. 💡 Ask questions about your codebase!

## Advanced Features (TODO)

- [ ] D3.js Knowledge Graph Visualization
- [ ] Sound Effects
- [ ] Multi-model comparison
- [ ] Code generation & editing
- [ ] Git integration
