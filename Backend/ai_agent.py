import os
import json
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from models import FactualMetrics, AIAuditResult

# Load environment variables and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def log_prompt_trace(system_prompt: str, user_prompt: str, raw_input_data: dict, raw_output: str):
    """Saves the prompt logs to fulfill the assignment deliverable."""
    log_dir = os.path.join(os.path.dirname(__file__), "..", "Prompt_Logs")
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_data = {
        "timestamp": timestamp,
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "structured_inputs": raw_input_data,
        "raw_model_output": raw_output
    }
    
    file_path = os.path.join(log_dir, f"audit_log_{timestamp}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4)

def analyze_website(metrics: FactualMetrics) -> AIAuditResult:
    # 1. Prepare data (Trimming clean text to avoid exceeding token limits)
    words = metrics.clean_text.split()
    trimmed_text = ' '.join(words[:2000]) # First 2000 words
    
    metrics_dict = metrics.model_dump(exclude={'clean_text'})
    
    # Generate the JSON schema from our Pydantic model so Gemini knows the exact format
    schema_definition = AIAuditResult.model_json_schema()
    
    # 2. Construct Prompts
    system_prompt = """You are an expert AI SEO and UX Consultant for EIGHT25MEDIA. 
Your job is to audit webpages based on strictly factual scraped metrics and the page's text content.
Rules:
- Be highly specific and non-generic.
- GROUND ALL INSIGHTS AND RECOMMENDATIONS IN THE EXTRACTED METRICS. 
- E.g., Don't just say 'Improve alt text', say 'Since 45% of images are missing alt text, update them.'"""

    user_prompt = f"""
Here are the extracted factual metrics for the webpage:
{json.dumps(metrics_dict, indent=2)}

Here is the truncated text content of the page:
{trimmed_text}

Analyze this data and provide structured insights and 3-5 prioritized recommendations.

IMPORTANT: You must return ONLY valid JSON that strictly conforms to this schema:
{json.dumps(schema_definition, indent=2)}
"""

    # 3. Call Gemini 2.5 Flash with JSON mode enabled
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=system_prompt
    )
    
    response = model.generate_content(
        user_prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.2, # Keep temperature low for more factual/analytical responses
        )
    )
    
    raw_output_json = response.text
    
    # 4. Parse the output back into our Pydantic model to ensure it is perfectly structured
    try:
        result = AIAuditResult.model_validate_json(raw_output_json)
    except Exception as e:
        print(f"Error parsing Gemini output: {raw_output_json}")
        raise ValueError("Gemini failed to return valid structured JSON.") from e
    
    # 5. Extract Result and Save Prompt Logs
    log_prompt_trace(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        raw_input_data=metrics_dict,
        raw_output=raw_output_json
    )
    
    return result