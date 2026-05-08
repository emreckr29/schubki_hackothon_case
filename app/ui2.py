import streamlit as st
import pandas as pd

from retrieval.retriever import search
from extraction.queryLlm3 import extract_clinical_evidence

# ===================================
# PAGE
# ===================================

st.set_page_config(
    page_title="Sepsis Atlas",
    layout="wide"
)

st.title("🧬 Sepsis Atlas")
st.caption(
    "AI-powered clinical evidence extraction"
)

# ===================================
# SIDEBAR
# ===================================

st.sidebar.header("Settings")

top_k = st.sidebar.slider(
    "Retrieved Chunks",
    3,
    20,
    8
)

# ===================================
# QUERY
# ===================================

query = st.text_input(
    "Clinical Question",
    placeholder="e.g. relationship between lactate and 28-day mortality"
)

run_button = st.button(
    "Generate Evidence Table"
)

# ===================================
# RUN
# ===================================

if run_button and query:

    # -----------------------------
    # RETRIEVE
    # -----------------------------

    with st.spinner("Retrieving evidence..."):

        chunks = search(
            query=query,
            top_k=top_k
        )

    st.success(
        f"Retrieved {len(chunks)} relevant chunks"
    )

    # -----------------------------
    # EXTRACT
    # -----------------------------

    with st.spinner(
        "Extracting structured evidence..."
    ):

        evidence = extract_clinical_evidence(
            query=query,
            chunks=chunks
        )

    # -----------------------------
    # SHOW TABLE
    # -----------------------------

    if evidence:

        df = pd.DataFrame(evidence)

        st.subheader(
            "📊 Structured Evidence Table"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning(
            "No structured evidence extracted"
        )

    # -----------------------------
    # SOURCE TRACEABILITY
    # -----------------------------

    st.subheader("🔎 Source Evidence")

    for chunk in chunks:

        with st.expander(
            f"{chunk['paper_id']} | "
            f"{chunk['section']}"
        ):

            st.markdown(chunk["text"])