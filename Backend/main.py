from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .scraper import scrape_website
from .ai_agent import analyze_website
from .models import FullAuditResponse

app = FastAPI(title="AI Website Audit API")

# VERY IMPORTANT FOR STREAMLIT FRONTEND
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuditRequest(BaseModel):
    url: str

@app.post("/api/audit", response_model=FullAuditResponse)
async def audit_endpoint(request: AuditRequest):
    try:
        # 1. Scrape the factual data
        metrics = scrape_website(request.url)
        
        # 2. Run the AI analysis
        ai_analysis = analyze_website(metrics)
        
        # 3. Exclude the raw text from the final response to keep it clean
        metrics.clean_text = "Redacted for final output"
        
        return FullAuditResponse(
            factual_metrics=metrics,
            ai_analysis=ai_analysis
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))