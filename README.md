# Learn Full-Stack Web Development (Python & HTML)

Welcome! This is a simplified, zero-dependency starter project designed specifically for Python developers who want to learn how to build websites with a Python backend.

You only need to know Python to learn and extend this project.

---

## How it works

A modern web application is divided into two parts that communicate over the network:

1. **The Backend (Python)**: Runs a server on your computer (`http://localhost:8000`). It listens for incoming data requests, processes logic (like running algorithms or database queries), and returns structured data (JSON).
2. **The Frontend (HTML/JavaScript)**: The website page you open in your browser. It renders the user interface and uses JavaScript to send requests to the Python backend without needing to reload the page.

```
[ Browser Website ] --( POSTs Topic )---> [ Python Backend (FastAPI) ]
[   (index.html)  ] <--( Returns Paper )-- [   (main.py on Port 8000) ]
```

---

## File Structure

Your project is organized as follows:
- **`backend/`** (Python Server Code)
  - `main.py`: The FastAPI server entrypoint. Sets up CORS so the browser can connect to it.
  - `config.py`: The helper script that reads configurations from `.env`.
  - `.env`: The settings file (API keys, ports).
  - `requirements.txt`: The list of Python libraries to install.
  - `services/llm_service.py`: Connects to OpenAI if a key is provided, otherwise falls back to offline mode.
  - `services/pipeline_manager.py`: Contains the multi-stage research paper generation pipeline.
- **`frontend/`** (Web Client Code)
  - `index.html`: The user interface dashboard styled with Tailwind CSS.

---

## How to run it on Windows

Follow these steps to run the project locally:

### 1. Start the Python Backend
1. Open a PowerShell terminal and navigate to the backend folder:
   ```powershell
   cd "C:\Users\Ashutosh Kumar\.gemini\antigravity\scratch\academic_research_generator\backend"
   ```
2. Create a virtual environment (if you haven't already):
   ```powershell
   py -m venv venv
   ```
3. Install the dependencies:
   ```powershell
   .\venv\Scripts\pip.exe install -r requirements.txt
   ```
4. Start the FastAPI development server:
   ```powershell
   .\venv\Scripts\uvicorn.exe main:app --reload --port 8000
   ```
   *Note: Keep this terminal window open. If you close it, your Python server stops.*

---

### 2. Open the Frontend
Since the frontend is a simple HTML file, **you do not need Node.js or any build tools!**
1. Open Windows File Explorer.
2. Navigate to: `C:\Users\Ashutosh Kumar\.gemini\antigravity\scratch\academic_research_generator\frontend\`
3. **Double-click `index.html`** to open it directly in Google Chrome or any browser.
4. Type a topic (e.g., "Deep Learning") and click **"Generate Research"** to watch the multi-stage pipeline compile a manuscript in real time!

---

## Code Flow Explanation

### 1. Sending the Request (Frontend)
Inside `frontend/index.html`, when you click "Generate Research", this JavaScript code runs:
```javascript
const response = await fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ topic: topic })
});
```
This performs a network fetch to your Python server, passing the topic as JSON data.

### 2. Handling the Request (Backend)
Inside `backend/main.py`, FastAPI receives the request and triggers `run_pipeline(req.topic)`:
```python
@app.post("/api/generate")
async def generate(req: GenerateRequest):
    final_paper = await run_pipeline(req.topic)
    return {"status": "complete", "content": final_paper}
```

### 3. Orchestration Pipeline
Inside `backend/services/pipeline_manager.py`, the pipeline runs in sequential stages:
- **Planning**: Outlines the paper structure.
- **Writing**: Drafts the Introduction, Methodology, and Conclusion sections using `llm_service.py` (which defaults to premium mock text if no OpenAI key is configured).
- **Synthesis**: Combines the sections into a beautifully formatted Markdown paper.
