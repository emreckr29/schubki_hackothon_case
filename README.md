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

# ⚙️ Installation

## 1. Clone repository

```bash
git clone https://github.com/emreckr29/schubki_hackothon_case.git
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
python ingest/pdf_to_markdown_new.py
```

---

## Build Chunks

```bash
python ingest/build_chunks_new.py
```

---

## Build Embeddings & FAISS Index

```bash
python retrieval/build_index.py
```

---

## Start UI

```bash
streamlit run app/ui2.py
```

---

# 🔍 Example Query

```text
relationship between lactate and 28-day mortality
```


# 🧠 Technologies Used

* Python
* Streamlit
* FAISS
* OpenAI Embeddings
* OpenRouter
* GPT-4.1
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
openai/gpt-4.1
```


# 🎯 Goal

Build a structured and verifiable clinical evidence system from scientific literature for sepsis research and mortality estimation.
