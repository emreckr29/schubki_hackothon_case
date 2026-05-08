# extraction/schemas.py

from pydantic import BaseModel, Field, ConfigDict


class ClinicalEvidenceRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    study: str | None = Field(
        default=None,
        description="Study name, first author/year, or paper title if available."
    )
    population: str | None = Field(
        default=None,
        description="Patient population or cohort description."
    )
    sample_size: str | None = Field(
        default=None,
        description="Sample size exactly as reported."
    )
    predictor: str | None = Field(
        default=None,
        description="Predictor, biomarker, score, treatment, phenotype, or clinical variable."
    )
    outcome: str | None = Field(
        default=None,
        description="Outcome definition, e.g. 28-day mortality."
    )
    timing: str | None = Field(
        default=None,
        description="Timing of predictor measurement or outcome assessment."
    )
    method: str | None = Field(
        default=None,
        description="Statistical method, e.g. ROC analysis, logistic regression, Cox model."
    )
    effect_size: str | None = Field(
        default=None,
        description="Reported effect size, e.g. OR, HR, AUC, cutoff, coefficient."
    )
    performance: str | None = Field(
        default=None,
        description="Performance metrics, e.g. AUC, sensitivity, specificity, CI, p-value."
    )
    notes: str | None = Field(
        default=None,
        description="Short caveats, adjustments, or missing details."
    )
    source_text: str = Field(
        description="Exact short quote from the provided context supporting this row."
    )
    paper_id: str = Field(
        description="Paper ID from the retrieved chunk."
    )
    section: str | None = Field(
        default=None,
        description="Section path from the retrieved chunk."
    )


class ClinicalEvidenceExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rows: list[ClinicalEvidenceRow] = Field(
        default_factory=list,
        description="Extracted structured evidence rows."
    )