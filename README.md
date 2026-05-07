# 🧬 Sepsis Atlas

AI-powered clinical evidence extraction system for scientific sepsis papers.

This project converts unstructured medical PDFs into structured, searchable, and verifiable clinical evidence tables using Retrieval-Augmented Generation (RAG) and LLMs.

---

# 🚀 Features

* PDF → Markdown conversion
* Clinical-aware chunking
* Table-aware extraction
* Semantic search with FAISS
* LLM-based structured evidence extraction
* Source-grounded outputs
* Streamlit UI

---

# 🏗️ Architecture

```text
PDF Papers
    ↓
Markdown Conversion
    ↓
Chunking & Table Extraction
    ↓
Embedding Generation
    ↓
FAISS Vector Search
    ↓
LLM Evidence Extraction
    ↓
Structured Evidence Table
```

---

# 📂 Project Structure

```text
project/
│
├── app/
│   └── ui.py
│
├── preprocessing/
│   ├── pdf_to_markdown.py
│   └── build_chunks.py
│
├── retrieval/
│   ├── embedder.py
│   ├── retriever.py
│   └── build_index.py
│
├── llm/
│   ├── extractor.py
│   └── prompts.py
│
├── data/
│   ├── parsed/
│   ├── chunks/
│   └── index/
│
├── articles/
│
├── requirements.txt
└── README.md
```

---

# 🧠 Technologies Used

* Python
* Streamlit
* FAISS
* OpenAI Embeddings
* OpenRouter
* GPT-5.5 Pro
* Docling
* Pandas
* NumPy

---

# 🤖 Models

## Embedding Model

```python
openai/text-embedding-3-large
```

## LLM

```python
openai/gpt-5.5-pro
```

---

# ⚙️ Installation

## 1. Clone repository

```bash
git clone <repo_url>
cd project
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Add API key

Create `.env`

```env
OPENROUTER_API_KEY=your_api_key
```

---

# ▶️ Running the Pipeline

## Convert PDFs to Markdown

```bash
python preprocessing/pdf_to_markdown.py
```

---

## Build Chunks

```bash
python preprocessing/build_chunks.py
```

---

## Build Embeddings & FAISS Index

```bash
python retrieval/build_index.py
```

---

## Start UI

```bash
streamlit run app/ui.py
```

---

# 🔍 Example Query

```text
relationship between lactate and 28-day mortality
```

---

# 🎯 Goal

Build a structured and verifiable clinical evidence system from scientific literature for sepsis research and mortality estimation.
