<div align="center">

# ⚖️ LexAssist AI

### *Intelligent Legal Document Analysis Platform*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![PyTorch](https://img.shields.io/badge/PyTorch-AI%20Engine-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> **LexAssist AI** is a professional-grade legal document analysis engine powered by NLP and Transformer models.  
> Upload any legal document — contracts, policies, agreements — and get instant insights.

---

</div>

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **PDF Extraction** | Parse and extract text from legal PDFs with high accuracy |
| 🧠 **AI Summarization** | Condense lengthy legal documents into concise summaries |
| ⚠️ **Risk Analysis** | Identify and score potential legal risks in contracts |
| 🔍 **Named Entity Recognition** | Detect parties, dates, clauses, and key legal entities |
| 📋 **Statutory Comparison** | Compare documents against statutory provisions |
| ⚡ **Text Preprocessing** | Clean and normalize legal text for accurate analysis |

---

## 🏗️ Project Architecture

```
lexassist_ai/
│
├── backend/                    # FastAPI Backend
│   ├── main.py                 # App entry point & middleware
│   ├── models/
│   │   ├── legal_model.py      # AI model definitions
│   │   └── schemas.py          # Pydantic schemas
│   ├── routes/
│   │   └── upload_routes.py    # API endpoints
│   ├── services/
│   │   ├── pdf_extractor.py    # PDF text extraction
│   │   ├── summarizer.py       # Document summarization
│   │   ├── risk_analyzer.py    # Risk scoring engine
│   │   ├── ner_module.py       # Named Entity Recognition
│   │   ├── statutory_comparer.py  # Legal statute comparison
│   │   └── text_preprocessor.py   # Text cleaning pipeline
│   └── utils/
│       ├── logger.py           # Logging utility
│       └── helpers.py          # Helper functions
│
├── frontend/
│   └── app_ui.py               # Streamlit UI
│
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/ahir-arpit/lexassist_ai.git
cd lexassist_ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download spaCy language model

```bash
python -m spacy download en_core_web_sm
```

---

## 🖥️ Running the App

### Start the Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload
```

> API will be live at: `http://localhost:8000`  
> Swagger Docs: `http://localhost:8000/docs`

### Start the Frontend (Streamlit)

```bash
streamlit run frontend/app_ui.py
```

> UI will open at: `http://localhost:8501`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API welcome message |
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Upload & analyze legal document |

---

## 🧰 Tech Stack

- **Backend** — [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn
- **Frontend** — [Streamlit](https://streamlit.io/)
- **AI / NLP** — [HuggingFace Transformers](https://huggingface.co/), [spaCy](https://spacy.io/), [PyTorch](https://pytorch.org/)
- **PDF Parsing** — PyMuPDF + PyPDF2
- **Logging** — Python logging with custom formatter

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ by **[Arpit Yadav](https://github.com/ahir-arpit)**

⭐ Star this repo if you found it helpful!

</div>
