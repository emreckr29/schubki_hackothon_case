import pandas as pd

from app.retrieval.search import search
from app.extraction.query import extract_evidence
from app.validation.validator import validate_extraction


QUERY = "What does hypotension predict in sepsis? Is it a strong predictor of mortality?"


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
        print(result["paper_id"], "Section:", result["section"])

        evidence = extract_evidence(result["text"])

        if is_valid(evidence):

            validation = validate_extraction(
                result["text"],
                evidence
            )

            if validation["supported"]:

                evidence["validation_reason"] = validation["reason"]
                evidence["paper_id"] = result["paper_id"]
                evidence["section"] = result["section"]

                all_evidence.append(evidence)
                print(result["text"])

                print("✓ Validated")

            else:

                print("✗ Rejected")
                print(validation["reason"])


    df = pd.DataFrame(all_evidence)

    print("\n" + "="*80)
    print("FINAL EVIDENCE TABLE")
    print(df)

    df.to_csv("evidence_table.csv", index=False)

    print("\nSaved to evidence_table.csv")


if __name__ == "__main__":
    main()