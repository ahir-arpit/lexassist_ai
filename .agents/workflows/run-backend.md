---
description: how to run the LexAssist AI backend server
---

To run the backend server, follow these steps:

1. **Open a terminal** and navigate to the `backend` directory:
```powershell
cd c:\Users\arpit\Desktop\lexassist_ai\backend
```

2. **Run the server** using the project's virtual environment:
```powershell
..\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.
