# app/ui.py

import streamlit as st
import json
import faiss
import numpy as np
from pathlib import Path

from retrieval.embedder import get_embedding

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Scientific RAG Explorer",
    layout="wide"
)

st.title("🔬 Scientific RAG Explorer")
st.caption("Semantic search over scientific papers")

# =========================
# LOAD INDEX
# =========================

@st.cache_resource
def load_data():
    index = faiss.read_index("data/index/papers.index")

    with open("data/index/metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata


index, metadata = load_data()

# =========================
# SIDEBAR
# =========================

st.sidebar.header("Settings")

top_k = st.sidebar.slider(
    "Top K Results",
    min_value=1,
    max_value=20,
    value=5
)

show_full = st.sidebar.checkbox(
    "Show Full Chunk",
    value=False
)

# =========================
# QUERY INPUT
# =========================

query = st.text_input(
    "Enter your query",
    placeholder="e.g. lactate mortality sepsis SOFA AUROC"
)

search_button = st.button("Search")

# =========================
# SEARCH
# =========================

if search_button and query:

    with st.spinner("Searching..."):

        query_embedding = np.array(
            [get_embedding(query)],
            dtype="float32"
        )

        distances, indices = index.search(query_embedding, top_k)

    st.success(f"Found {top_k} results")

    # =========================
    # RESULTS
    # =========================

    for rank, idx in enumerate(indices[0]):

        chunk = metadata[idx]
        score = float(distances[0][rank])

        with st.container(border=True):

            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.subheader(f"📄 {chunk['paper_id']}")

            with col2:
                st.markdown(
                    f"**Section:** {chunk.get('section', 'Unknown')}"
                )

            with col3:
                st.metric(
                    "Distance",
                    f"{score:.4f}"
                )

            st.divider()

            text = chunk["text"]

            if not show_full and len(text) > 1500:
                text = text[:1500] + "..."

            st.markdown(text)

# =========================
# FOOTER
# =========================

st.divider()
st.caption("Built with Streamlit + FAISS + OpenRouter")