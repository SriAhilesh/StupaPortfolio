import os
import re
import json
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import HTTPException

# ----------------------------
# ENV + Gemini Setup
# ----------------------------
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_KEY)
MODEL_NAME = "gemini-2.5-flash"

# ----------------------------
# JSON Utilities
# ----------------------------
def safe_parse_json(raw_text: str):
    """Clean and safely parse model output JSON."""
    text = raw_text.strip()
    text = re.sub(r"^```(?:json)?", "", text)
    text = re.sub(r"```$", "", text)
    text = re.sub(r"//.*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return json.loads(text)

# ----------------------------
# Gemini Call Function
# ----------------------------
def call_gemini(prompt: str) -> str:
    model = genai.GenerativeModel(MODEL_NAME)
    resp = model.generate_content(prompt)
    text = ""
    for c in resp.candidates:
        for p in c.content.parts:
            if hasattr(p, "text"):
                text += p.text

    # 🪵 Log raw Gemini output for debugging
    os.makedirs("logs", exist_ok=True)
    with open("logs/raw_gemini_output.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ Gemini raw response saved to logs/raw_gemini_output.txt")

    return text.strip()


# ----------------------------
# Portfolio Enhancement
# ----------------------------
import json, os
#from utils.gemini_utils import call_gemini  # or your gemini client

def enhance_portfolio_with_llm(base_portfolio: dict, variant: str):
    """
    Enhances and rewrites portfolio JSON for different use cases:
      - Academic: Focus on research, analysis, scholarly tone.
      - Industry: Focus on practical impact, technology, software, teamwork.
    It rewrites even short entries (like "Top 10") into complete, professional statements.
    """

    # 🧠 Define style context blocks
    if variant == "academic":
        context_block = """
        Focus areas:
        - Highlight research experience, analytical rigor, technical depth, and academic achievements.
        - Emphasize research projects, publications, methodologies, or teaching potential.
        - Describe tools as instruments for discovery, innovation, or computational experimentation.
        - Tone: formal, articulate, precise.
        """
    else:
        context_block = """
        Focus areas:
        - Highlight software development, product impact, scalability, and problem-solving.
        - Emphasize real-world application of technologies and teamwork.
        - Stress efficiency, innovation, and measurable outcomes.
        - Tone: confident, energetic, and professional.
        """

    # 🎯 Main enrichment prompt
    prompt = f"""
    You are a professional portfolio enhancer specializing in creating structured, context-rich, and professional portfolio JSONs.

    Task:
    Take the following JSON and rewrite/enrich every text field (even if already filled).
    Convert short raw entries like "Top 10" or "Intern" into full, natural professional statements.
    Do not change JSON keys or structure. Only rewrite content.

    Rules:
    - Keep JSON structure identical.
    - For every object type:
        * "user": make 'portfolio_tagline' extremely short — 2 to 4 impactful words only (e.g., "AI Innovator", "Full Stack Developer", "Research Visionary").'short_bio' should be a 2-line summary describing background and goals.
        * "education": expand 'achievements', 'degree', and add 'short_summary' describing what was studied or achieved.
        * "experience": enrich 'role', 'description', and add 'short_summary' that captures impact and skills gained.
        * "projects": summarize goals, methods, and tools in 'short_summary' (1-2 lines).
        * "skills": make 'description' actionable — what the skill enables you to do.
        * "certifications": make 'title' clear and 'notes' meaningful, add 'short_summary' stating what expertise it validates.
    - Include industry- or research-appropriate keywords.
    - NEVER change key names.
    - Output valid JSON only. No markdown or code blocks.

    Context:
    {context_block}

    JSON to enhance:
    {json.dumps(base_portfolio, indent=2, ensure_ascii=False)}
    """

    raw = call_gemini(prompt).strip()

    if "```" in raw:
        raw = raw.split("```json")[-1].split("```")[0].strip()

    try:
        enriched = json.loads(raw)
    except Exception as e:
        print("⚠️ JSON parse failed — fallback used:", e)
        with open("logs/fallback.txt", "w", encoding="utf-8") as f:
            f.write(raw)
        enriched = base_portfolio

    # Clean nulls
    def clean_none(v):
        if isinstance(v, dict):
            return {k: clean_none(val) for k, val in v.items()}
        elif isinstance(v, list):
            return [clean_none(x) for x in v]
        elif v is None:
            return ""
        return v

    enriched = clean_none(enriched)

    # Fallback rewriters (same as before)
    for edu in enriched.get("education", []):
        ach = edu.get("achievements", "").strip().lower()
        if ach and "top" in ach and "gpa" not in ach:
            gpa = edu.get("gpa_/_cgpa", "")
            edu["achievements"] = f"Ranked among the top students in Computer Science with a GPA of {gpa}."
        if not edu.get("short_summary"):
            edu["short_summary"] = f"Pursuing {edu.get('degree','')} at {edu.get('institution','')}, demonstrating academic excellence and curiosity."

    for exp in enriched.get("experience", []):
        if not exp.get("short_summary"):
            exp["short_summary"] = f"As a {exp.get('role','')}, contributed to impactful software and business solutions at {exp.get('company','')}."

    for cert in enriched.get("certifications", []):
        if not cert.get("short_summary"):
            cert["short_summary"] = f"Certified in {cert.get('title','')}, validating expertise and practical understanding of the domain."

    return enriched
