import re
import json
from pathlib import Path

PARSED_DIR = Path("data2/parsed")
CHUNK_DIR = Path("data2/chunks")

CHUNK_DIR.mkdir(parents=True, exist_ok=True)

MAX_CHARS = 1800
MIN_CHARS = 300
OVERLAP = 250

# ---------------------------------------------------
# REMOVE LOW-VALUE SECTIONS
# ---------------------------------------------------

REMOVE_SECTIONS = {
    "references",
    "reference",
    "bibliography",
    "acknowledgment",
    "acknowledgements",
    "acknowledgments",
    "funding",
    "conflict of interest",
    "appendix",
    "supplementary",
    "author contributions"
}

# ---------------------------------------------------
# IMPORTANT SECTIONS BOOST
# ---------------------------------------------------

HIGH_VALUE_SECTIONS = {
    "abstract",
    "methods",
    "results",
    "outcomes",
    "statistical analysis",
    "multivariate analysis",
    "patient characteristics",
    "baseline characteristics",
    "discussion"
}

# ---------------------------------------------------
# SECTION PARSER
# ---------------------------------------------------

def parse_sections(markdown_text):

    lines = markdown_text.split("\n")

    sections = []

    current = None

    hierarchy = {}

    heading_pattern = re.compile(r"^(#{1,6})\s+(.*)")

    for line in lines:

        match = heading_pattern.match(line)

        if match:

            level = len(match.group(1))

            title = match.group(2).strip()

            if current:
                sections.append(current)

            hierarchy[level] = title

            remove_keys = [k for k in hierarchy if k > level]

            for k in remove_keys:
                del hierarchy[k]

            tree = [hierarchy[k] for k in sorted(hierarchy.keys())]

            current = {
                "title": title,
                "level": level,
                "tree": tree,
                "content": ""
            }

        else:

            if current:
                current["content"] += line + "\n"

    if current:
        sections.append(current)

    return sections

# ---------------------------------------------------
# FILTER LOW VALUE SECTIONS
# ---------------------------------------------------

def should_skip_section(title):

    title = title.lower().strip()

    return any(skip in title for skip in REMOVE_SECTIONS)

# ---------------------------------------------------
# TABLE EXTRACTION
# ---------------------------------------------------

def extract_tables(text):

    table_pattern = re.compile(
        r"((?:\|.*\|\s*\n)+)",
        re.MULTILINE
    )

    tables = []

    for match in table_pattern.finditer(text):

        table_text = match.group(1).strip()

        if "---" in table_text:

            tables.append({
                "text": table_text,
                "table_type": infer_table_type(table_text)
            })

    return tables

# ---------------------------------------------------
# TABLE TYPE INFERENCE
# ---------------------------------------------------

def infer_table_type(table_text):

    lower = table_text.lower()

    if "baseline" in lower:
        return "baseline_characteristics"

    if "multivariate" in lower:
        return "multivariate_analysis"

    if "mortality" in lower:
        return "mortality_outcomes"

    if "auc" in lower or "sensitivity" in lower:
        return "performance_metrics"

    return "clinical_table"

# ---------------------------------------------------
# REMOVE TABLES
# ---------------------------------------------------

def remove_tables(text):

    table_pattern = re.compile(
        r"((?:\|.*\|\s*\n)+)",
        re.MULTILINE
    )

    return re.sub(table_pattern, "", text)

# ---------------------------------------------------
# SENTENCE SPLITTING
# ---------------------------------------------------

def split_sentences(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    return [s.strip() for s in sentences if s.strip()]

# ---------------------------------------------------
# CHUNKING
# ---------------------------------------------------

def chunk_text(text,
               max_chars=MAX_CHARS,
               overlap=OVERLAP):

    sentences = split_sentences(text)

    chunks = []

    current = ""

    for sentence in sentences:

        if len(current) + len(sentence) < max_chars:

            current += " " + sentence

        else:

            current = current.strip()

            if len(current) >= MIN_CHARS:

                chunks.append(current)

            overlap_text = current[-overlap:]

            current = overlap_text + " " + sentence

    if current.strip():

        chunks.append(current.strip())

    return chunks

# ---------------------------------------------------
# CLINICAL SIGNAL DETECTION
# ---------------------------------------------------

CLINICAL_KEYWORDS = [
    "mortality",
    "survival",
    "sofa",
    "apache",
    "lactate",
    "lymphocyte",
    "biomarker",
    "icu",
    "septic shock",
    "hazard ratio",
    "odds ratio",
    "auc",
    "sensitivity",
    "specificity",
    "multivariate",
    "logistic regression",
    "cox regression"
]

def detect_clinical_signals(text):

    lower = text.lower()

    found = []

    for keyword in CLINICAL_KEYWORDS:

        if keyword in lower:
            found.append(keyword)

    return found

# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

markdown_files = list(PARSED_DIR.glob("*.md"))

print(f"Found {len(markdown_files)} markdown files")

all_chunks = []

for md_file in markdown_files:

    paper_id = md_file.stem

    with open(md_file, "r", encoding="utf-8") as f:
        markdown = f.read()

    sections = parse_sections(markdown)

    for section in sections:

        title = section["title"]

        if should_skip_section(title):
            continue

        content = section["content"].strip()

        if not content:
            continue

        importance = "normal"

        if any(
            x in title.lower()
            for x in HIGH_VALUE_SECTIONS
        ):
            importance = "high"

        # ----------------------------------------
        # TABLE CHUNKS
        # ----------------------------------------

        tables = extract_tables(content)

        for idx, table in enumerate(tables):

            table_chunk = {

                "paper_id": paper_id,

                "chunk_id": f"{paper_id}_table_{idx}",

                "chunk_type": "table",

                "table_type": table["table_type"],

                "section": title,

                "section_tree": section["tree"],

                "importance": importance,

                "clinical_signals": detect_clinical_signals(
                    table["text"]
                ),

                "is_table": True,

                "text": table["text"]
            }

            all_chunks.append(table_chunk)

        # ----------------------------------------
        # NORMAL TEXT
        # ----------------------------------------

        clean_content = remove_tables(content)

        text_chunks = chunk_text(clean_content)

        for idx, chunk in enumerate(text_chunks):

            chunk_data = {

                "paper_id": paper_id,

                "chunk_id": f"{paper_id}_{title}_{idx}",

                "chunk_type": "text",

                "section": title,

                "section_tree": section["tree"],

                "importance": importance,

                "clinical_signals": detect_clinical_signals(
                    chunk
                ),

                "is_table": False,

                "text": chunk
            }

            all_chunks.append(chunk_data)

# ---------------------------------------------------
# SAVE
# ---------------------------------------------------

output_path = CHUNK_DIR / "chunks.json"

with open(output_path, "w", encoding="utf-8") as f:

    json.dump(
        all_chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"\nSaved {len(all_chunks)} chunks")