import pandas as pd

from app.retrieval.search import search
from app.extraction.extractor import extract_evidence


QUERY = "lactate mortality sepsis SOFA AUROC"


def is_valid(e):

    if e is None:
        return False

    predictor = e.get("predictor")
    outcome = e.get("outcome")

    if not predictor and not outcome:
        return False

    return True


def main():

    print(f"\nQUERY: {QUERY}")

    # retrieve more chunks
    results = search(QUERY, top_k=10)

    all_evidence = []

    for i, result in enumerate(results):

        print("\n" + "="*80)
        print(f"CHUNK {i+1}")
        print(result["paper_id"], "Page:", result["page"])

        evidence = extract_evidence(result["text"])

        if is_valid(evidence):

            evidence["paper_id"] = result["paper_id"]
            evidence["page"] = result["page"]

            all_evidence.append(evidence)

            print("✓ Extracted")

        else:
            print("✗ Empty")


    df = pd.DataFrame(all_evidence)

    print("\n" + "="*80)
    print("FINAL EVIDENCE TABLE")
    print(df)

    df.to_csv("evidence_table.csv", index=False)

    print("\nSaved to evidence_table.csv")


if __name__ == "__main__":
    main()