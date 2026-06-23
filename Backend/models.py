from pydantic import BaseModel

class FactualMetrics(BaseModel):
    total_word_count: int
    h1_count: int
    h2_count: int
    h3_count: int
    internal_links: int
    external_links: int
    cta_count: int
    total_images: int
    images_missing_alt: int
    images_missing_alt_percentage: float
    meta_title: str | None
    meta_description: str | None
    clean_text: str  # We will use this to feed the AI later


class AIInsights(BaseModel):
    seo_structure: str
    messaging_clarity: str
    cta_usage: str
    content_depth: str
    ux_structural_concerns: str

class Recommendation(BaseModel):
    priority: int
    recommendation: str
    reasoning: str # Must be tied to factual metrics

class AIAuditResult(BaseModel):
    insights: AIInsights
    recommendations: list[Recommendation]

class FullAuditResponse(BaseModel):
    factual_metrics: FactualMetrics
    ai_analysis: AIAuditResult