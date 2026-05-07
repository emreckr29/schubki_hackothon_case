import os
import pandas as pd
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.llms.openai import OpenAI
from llama_index.core.program import LLMTextCompletionProgram
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

# --- 1. VERİ ŞEMASI ---
class SepsisFinding(BaseModel):
    predictor: str = Field(description="Predictor variable (e.g., Lactate, SOFA score, IL-6)")
    sample_size: str = Field(description="Number of patients (N)")
    outcome: str = Field(description="Outcome definition (e.g., 28-day mortality)")
    effect_size: str = Field(description="Odds Ratio, Hazard Ratio, or AUC value with 95% CI")
    p_value: str = Field(description="Statistical significance (p-value)")
    source_quote: str = Field(description="Exact sentence from the text supporting this value for verification")
    method: str = Field(description="Statistical method used (e.g., ROC analysis, Logistic Regression)")

class SepsisStudy(BaseModel):
    study_name: str = Field(description="Author and Year (e.g., Smith et al. 2023)")
    population: str = Field(description="Patient cohort description (e.g., Septic shock in ICU)")
    findings: List[SepsisFinding]

# --- 2. OPENROUTER & LLM AYARI ---
# OpenRouter üzerinden model çağırıyoruz
llm = OpenAI(
    model="gpt-4o", # Model ismini burada OpenAI gibi yazalım ama OpenRouter bunu anlayacak
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
    is_chat_model=True,
    reuse_client=False,
    default_headers={
        "HTTP-Referer": "https://localhost",
        "X-Title": "Sepsis Atlas Hackathon"
    }
)

def process_article(file_path):
    print(f"\n--- {file_path} analiz ediliyor ---")
    
    # PDF Parsing
    parser = LlamaParse(result_type="markdown")
    documents = parser.load_data(file_path)
    full_text = "\n".join([doc.text for doc in documents])

    # Extraction Program
    prompt_template = (
        "You are an expert clinical data scientist. Extract all statistical findings "
        "related to mortality predictors in sepsis from the text below.\n"
        "Focus on: Severity scores, biomarkers, and clinical variables.\n"
        "If a value is missing, write 'not reported'.\n"
        "Text content: {text}\n"
    )

    program = LLMTextCompletionProgram.from_defaults(
        output_cls=SepsisStudy,
        prompt_template_str=prompt_template,
        llm=llm,
        verbose=True
    )

    return program(text=full_text)

# --- 3. ÇALIŞTIRMA VE KAYDETME ---
articles_dir = "articles"
output_data = []

# Sadece ilk 2-3 dosya ile test etmek istersen os.listdir(articles_dir)[:3] yapabilirsin
# --- 3. ÇALIŞTIRMA VE KAYDETME ---
articles_dir = "articles"
output_data = []

# Klasördeki dosyaları listele
all_files = [f for f in os.listdir(articles_dir) if f.endswith(".pdf")]

if not all_files:
    print("Hata: 'articles' klasöründe PDF bulunamadı!")
else:
    # SADECE İLK DOSYAYI TEST ET
    test_file = all_files[0] 
    path = os.path.join(articles_dir, test_file)
    
    try:
        result = process_article(path)
        for f in result.findings:
            row = {
                "Study": result.study_name,
                "Population": result.population,
                "Predictor": f.predictor,
                "N": f.sample_size,
                "Outcome": f.outcome,
                "Effect Size": f.effect_size,
                "P-Value": f.p_value,
                "Method": f.method,
                "Source Quote": f.source_quote
            }
            output_data.append(row)
            
        # Sonucu hemen ekrana bas ki görelim
        print("\n--- TEST SONUCU ---")
        print(pd.DataFrame(output_data).to_string())
        
        # CSV'ye de kaydet
        pd.DataFrame(output_data).to_csv("test_result.csv", index=False)
        print("\n✅ Test başarılı! 'test_result.csv' oluşturuldu.")
        
    except Exception as e:
        print(f"Test sırasında hata oluştu: {str(e)}")