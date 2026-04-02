from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.notion_utils import (
    get_child_databases, 
    get_page_id_from_url,
    query_database_pages,
    clean_notion_properties
)
# Add these imports at top of main.py (if not already)
#from utils.llm_utils import generate_react_projects_from_portfolio
from utils.llm_utils import enhance_portfolio_with_llm

import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="STuPA Portfolio Backend")

from fastapi.staticfiles import StaticFiles
import os

# Serve generated portfolios from /outputs URL
os.makedirs("outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# 🔧 CORS setup – must be immediately after app creation
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"  # leave this while debugging
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Input model for API request
class NotionInput(BaseModel):
    notion_token: str
    page_url: str


@app.get("/")
def home():
    """Health check endpoint."""
    return {"message": "STuPA Backend running successfully!"}


@app.post("/fetch-databases/")
def fetch_databases(data: NotionInput):
    """
    (DEBUG/SETUP)
    Returns all child databases (title and ID) from the given Notion page.
    """
    try:
        notion_token = data.notion_token
        page_url = data.page_url

        # Step 1: Extract page ID
        page_id = get_page_id_from_url(page_url)
        print("🧱 Extracted Page ID:", page_id)

        # Step 2: Fetch all child databases using user’s token
        db_dict = get_child_databases(notion_token, page_id)
        
        return {
            "status": "success",
            "page_id": page_id,
            "found_databases": db_dict
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in /fetch-databases/: {e}")


@app.post("/fetch-data/")
def fetch_all_portfolio_data(data: NotionInput):
    """
    Fetches ALL databases (Education, Experience, Projects, Skills, etc.)
    from the user’s Notion page and returns a clean structured JSON.
    """
    try:
        notion_token = data.notion_token
        page_url = data.page_url

        # 1️⃣ Get Page ID and all databases
        page_id = get_page_id_from_url(page_url)
        db_dict = get_child_databases(notion_token, page_id)

        if not db_dict:
            raise HTTPException(status_code=400, detail="No databases found on the Notion page.")

        portfolio_data = {}

        # 2️⃣ Loop through all discovered databases dynamically
        for db_title, db_id in db_dict.items():
            try:
                pages = query_database_pages(notion_token, db_id)

                if not pages:
                    portfolio_data[db_title.lower().replace(" ", "_")] = []
                    continue

                cleaned_rows = [clean_notion_properties(p["properties"]) for p in pages]

                # Treat "Personal Information" as single-user object
                if db_title.lower().strip() in ["personal information", "personal_info", "user", "profile"]:
                    portfolio_data["user"] = cleaned_rows[0] if cleaned_rows else {}
                else:
                    portfolio_data[db_title.lower().replace(" ", "_")] = cleaned_rows

            except Exception as inner_e:
                print(f"⚠️ Error fetching {db_title}: {inner_e}")
                portfolio_data[db_title.lower().replace(" ", "_")] = f"Error fetching: {inner_e}"

        # 3️⃣ Save to local JSON file
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/portfolio.json", "w", encoding="utf-8") as f:
            json.dump(portfolio_data, f, indent=4, ensure_ascii=False)

        # 4️⃣ Return API response
        return {
            "status": "success",
            "data_source_id": page_id,
            "portfolio": portfolio_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Portfolio data fetch error: {e}")
    
# Clean out empty or placeholder entries before enrichment
def clean_portfolio_data(data: dict) -> dict:
    def is_meaningful(entry: dict):
        if not isinstance(entry, dict):
            return True
        # Count non-empty, non-null fields
        filled = [v for v in entry.values() if v not in (None, "", [], {})]
        return len(filled) > 0

    cleaned = {}
    for key, value in data.items():
        if isinstance(value, list):
            cleaned[key] = [v for v in value if is_meaningful(v)]
        else:
            cleaned[key] = value
    return cleaned


# add at top of main.py:
# from utils.llm_utils import generate_react_projects_from_portfolio
# (you already have or add this import)

from fastapi import HTTPException
import json
import os
from fastapi import HTTPException
import json
import os

@app.post("/generate_portfolio")
def generate_portfolio(style: str = "academic"):
    """
    Generate an enriched portfolio and build a professional website.
    style: 'academic' or 'industry'
    """
    from utils.llm_utils import enhance_portfolio_with_llm

    base_path = "outputs/portfolio.json"
    if not os.path.exists(base_path):
        raise HTTPException(status_code=404, detail="Base portfolio.json not found in outputs/")

    with open(base_path, "r", encoding="utf-8") as f:
        base_data = json.load(f)
    
    # 🧹 Clean raw JSON before enrichment
    base_data = clean_portfolio_data(base_data)


    # 🧠 Enrich portfolio with Gemini
    enriched = enhance_portfolio_with_llm(base_data, style)

    # 💾 Save enriched portfolio JSON
    save_dir = os.path.join("outputs", f"{style}_portfolio")
    os.makedirs(save_dir, exist_ok=True)
    enriched_path = os.path.join(save_dir, "portfolio.json")
    with open(enriched_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    #Auto Save README.md File to the output folder.
    with open(f"{save_dir}/README.md", "w") as readme:
        readme.write(f"# {enriched['user']['name']}'s Portfolio\n\n")
        readme.write(f"**Tagline:** {enriched['user'].get('portfolio_tagline','')}\n\n")
        readme.write("## Summary\n")
        readme.write(enriched['user'].get('short_bio',''))


    # 🕸️ Generate index.html that reads from enriched JSON
    html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{enriched.get("user", {}).get("name", "Portfolio")}</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap" rel="stylesheet">
<style>
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    scroll-behavior: smooth;
  }}
  
  body {{
    font-family: 'Poppins', sans-serif;
    background: #000000;
    color: #ffffff;
    line-height: 1.6;
    overflow-x: hidden;
  }}
  
  /* Animated gradient background */
  body::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, #000000, #0a0a0a, #1a1a1a, #0f0f0f);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    z-index: -2;
  }}
  
  @keyframes gradientShift {{
    0%, 100% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
  }}
  
  /* Floating particles */
  .particles {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    overflow: hidden;
    pointer-events: none;
  }}
  
  .particle {{
    position: absolute;
    background: rgba(59, 130, 246, 0.3);
    border-radius: 50%;
    animation: float 20s infinite;
  }}
  
  .particle:nth-child(1) {{ width: 80px; height: 80px; left: 10%; animation-delay: 0s; }}
  .particle:nth-child(2) {{ width: 60px; height: 60px; left: 30%; animation-delay: 2s; background: rgba(96, 165, 250, 0.25); }}
  .particle:nth-child(3) {{ width: 100px; height: 100px; left: 50%; animation-delay: 4s; background: rgba(147, 197, 253, 0.2); }}
  .particle:nth-child(4) {{ width: 70px; height: 70px; left: 70%; animation-delay: 6s; background: rgba(59, 130, 246, 0.3); }}
  .particle:nth-child(5) {{ width: 90px; height: 90px; left: 85%; animation-delay: 8s; }}
  
  @keyframes float {{
    0%, 100% {{ transform: translateY(100vh) scale(0); opacity: 0; }}
    10% {{ opacity: 1; }}
    90% {{ opacity: 1; }}
    100% {{ transform: translateY(-100px) scale(1); opacity: 0; }}
  }}

  /* Navbar */
  nav {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.2rem 5%;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(59, 130, 246, 0.2);
    z-index: 1000;
    transition: all 0.3s ease;
  }}
  
  nav.scrolled {{
    background: rgba(0, 0, 0, 0.95);
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.2);
    padding: 0.8rem 5%;
  }}
  
  nav .logo {{
    font-size: 1.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #3b82f6, #60a5fa, #93c5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 1px;
  }}
  
  nav ul {{
    display: flex;
    gap: 2.5rem;
    list-style: none;
  }}
  
  nav ul li a {{
    font-weight: 500;
    position: relative;
    transition: color 0.3s ease;
    font-size: 0.95rem;
    color: #ffffff;
  }}
  
  nav ul li a::after {{
    content: "";
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, #3b82f6, #60a5fa);
    transition: width 0.3s ease;
  }}
  
  nav ul li a:hover {{
    color: #60a5fa;
  }}
  
  nav ul li a:hover::after {{
    width: 100%;
  }}

  /* Hero Section */
  header {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    padding: 0 5%;
  }}
  
  .hero-content {{
    z-index: 2;
    animation: fadeInUp 1s ease;
  }}
  
  @keyframes fadeInUp {{
    from {{
      opacity: 0;
      transform: translateY(30px);
    }}
    to {{
      opacity: 1;
      transform: translateY(0);
    }}
  }}
  
  .hero-subtitle {{
    font-size: 1.2rem;
    color: #60a5fa;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
  }}
  
  h1 {{
    font-size: 4.5rem;
    margin-bottom: 1rem;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.2;
    text-shadow: 0 0 40px rgba(59, 130, 246, 0.5);
  }}
  
  .hero-description {{
    font-size: 1.2rem;
    color: #d1d5db;
    max-width: 700px;
    margin: 1.5rem auto;
    line-height: 1.8;
  }}
  
  .btn-group {{
    display: flex;
    gap: 1.5rem;
    margin-top: 2.5rem;
    justify-content: center;
  }}
  
  .btn {{
    padding: 1rem 2.5rem;
    border: none;
    border-radius: 50px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.4s ease;
    font-size: 1rem;
    position: relative;
    overflow: hidden;
  }}
  
  .btn-primary {{
    background: linear-gradient(135deg, #3b82f6, #60a5fa);
    color: #ffffff;
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
  }}
  
  .btn-primary::before {{
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #60a5fa, #93c5fd);
    transition: left 0.4s ease;
    z-index: -1;
  }}
  
  .btn-primary:hover::before {{
    left: 0;
  }}
  
  .btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(96, 165, 250, 0.5);
  }}
  
  .btn-secondary {{
    background: transparent;
    color: #60a5fa;
    border: 2px solid #60a5fa;
  }}
  
  .btn-secondary:hover {{
    background: #60a5fa;
    color: #000000;
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(96, 165, 250, 0.3);
  }}
  
  .scroll-indicator {{
    position: absolute;
    bottom: 3rem;
    font-size: 2rem;
    color: #60a5fa;
    animation: bounce 2s infinite;
    cursor: pointer;
  }}
  
  @keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-15px); }}
  }}

  /* Section Styling */
  section {{
    width: 90%;
    max-width: 1200px;
    margin: 8rem auto;
    padding: 4rem 0;
    opacity: 0;
    transform: translateY(50px);
    animation: fadeUp 1s ease forwards;
  }}
  
  @keyframes fadeUp {{
    to {{
      opacity: 1;
      transform: translateY(0);
    }}
  }}
  
  .section-header {{
    text-align: center;
    margin-bottom: 4rem;
  }}
  
  .section-subtitle {{
    color: #60a5fa;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
  }}
  
  h2 {{
    font-size: 3rem;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 1rem;
    text-shadow: 0 0 30px rgba(59, 130, 246, 0.3);
  }}
  
  .section-description {{
    color: #9ca3af;
    max-width: 600px;
    margin: 0 auto;
    font-size: 1.1rem;
  }}

  /* Cards */
  .card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
  }}
  
  .card {{
    background: rgba(20, 20, 20, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 20px;
    padding: 2rem;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
  }}
  
  .card::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(96, 165, 250, 0.05));
    opacity: 0;
    transition: opacity 0.4s ease;
  }}
  
  .card:hover::before {{
    opacity: 1;
  }}
  
  .card:hover {{
    transform: translateY(-10px);
    border-color: rgba(96, 165, 250, 0.5);
    box-shadow: 0 20px 50px rgba(59, 130, 246, 0.3);
  }}
  
  .card-icon {{
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #3b82f6, #60a5fa);
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
  }}
  
  .card h3 {{
    font-size: 1.5rem;
    color: #ffffff;
    margin-bottom: 0.5rem;
    font-weight: 700;
  }}
  
  .card-meta {{
    color: #60a5fa;
    font-size: 0.9rem;
    margin-bottom: 1rem;
    font-weight: 500;
  }}
  
  .card p {{
    color: #d1d5db;
    line-height: 1.7;
    margin-bottom: 1rem;
  }}
  
  .card-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
  }}
  
  .tag {{
    background: rgba(59, 130, 246, 0.2);
    color: #93c5fd;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    border: 1px solid rgba(59, 130, 246, 0.3);
  }}

  /* Skills Section */
  .skills-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 3rem;
  }}
  
  .skill-card {{
    background: rgba(20, 20, 20, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 15px;
    padding: 1.5rem;
    transition: all 0.3s ease;
  }}
  
  .skill-card:hover {{
    transform: translateY(-5px);
    border-color: rgba(96, 165, 250, 0.5);
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
  }}
  
  .skill-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }}
  
  .skill-name {{
    font-size: 1.1rem;
    font-weight: 600;
    color: #ffffff;
  }}
  
  .skill-level {{
    font-size: 0.85rem;
    color: #60a5fa;
    font-weight: 600;
  }}
  
  .skill-bar {{
    width: 100%;
    height: 8px;
    background: rgba(59, 130, 246, 0.2);
    border-radius: 10px;
    overflow: hidden;
  }}
  
  .skill-progress {{
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #60a5fa);
    border-radius: 10px;
    animation: fillBar 1.5s ease forwards;
    transform-origin: left;
  }}
  
  @keyframes fillBar {{
    from {{ transform: scaleX(0); }}
    to {{ transform: scaleX(1); }}
  }}

  /* Contact Section */
  .contact-container {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    margin-top: 3rem;
  }}
  
  .contact-info {{
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }}
  
  .contact-item {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 1.5rem;
    background: rgba(20, 20, 20, 0.8);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 15px;
    transition: all 0.3s ease;
  }}
  
  .contact-item:hover {{
    border-color: rgba(96, 165, 250, 0.5);
    transform: translateX(10px);
  }}
  
  .contact-icon {{
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #3b82f6, #60a5fa);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
  }}
  
  .contact-details h4 {{
    color: #ffffff;
    font-weight: 600;
    margin-bottom: 0.3rem;
  }}
  
  .contact-details p {{
    color: #d1d5db;
  }}
  
  .social-links {{
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
  }}
  
  .social-link {{
    width: 50px;
    height: 50px;
    background: rgba(59, 130, 246, 0.2);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    transition: all 0.3s ease;
  }}
  
  .social-link:hover {{
    background: linear-gradient(135deg, #3b82f6, #60a5fa);
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
  }}

  /* Footer */
  footer {{
    text-align: center;
    padding: 3rem 5%;
    background: rgba(0, 0, 0, 0.9);
    border-top: 1px solid rgba(59, 130, 246, 0.2);
    margin-top: 8rem;
  }}
  
  footer p {{
    color: #9ca3af;
    font-size: 0.95rem;
    margin: 0.5rem 0;
  }}
  
  .footer-brand {{
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #3b82f6, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
  }}

  /* Responsive */
  @media (max-width: 768px) {{
    h1 {{ font-size: 2.5rem; }}
    h2 {{ font-size: 2rem; }}
    nav ul {{ gap: 1rem; }}
    .contact-container {{ grid-template-columns: 1fr; }}
    .btn-group {{ flex-direction: column; }}
  }}
</style>
</head>
<body>

  <!-- Particles Background -->
  <div class="particles">
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
  </div>

  <!-- Navigation -->
  <nav id="navbar">
    <div class="logo">{enriched.get("user", {}).get("name", "Portfolio")}</div>
    <ul>
      <li><a href="#home">Home</a></li>
      <li><a href="#about">About</a></li>
      <li><a href="#experience">Experience</a></li>
      <li><a href="#projects">Projects</a></li>
      <li><a href="#skills">Skills</a></li>
      <li><a href="#certifications">Certifications</a></li>
      <li><a href="#contact">Contact</a></li>
    </ul>
  </nav>

  <!-- Hero Section -->
  <header id="home">
    <div class="hero-content">
      <div class="hero-subtitle">Welcome to my portfolio</div>
      <h1>Hi, I'm {enriched.get("user", {}).get("name", "Unnamed")}</h1>

      <!-- Punchy tagline (2–4 words only) -->
      <p class="hero-description"
        style="font-size:1.6rem;
                font-weight:700;
                letter-spacing:1px;
                color:#60a5fa;
                margin-top:0.5rem;
                text-transform:uppercase;
                text-shadow:0 0 15px rgba(96,165,250,0.4);">
        {str(enriched.get("user", {}).get("portfolio_tagline") or "")}
      </p>

      <!-- Professional summary (2-liner) -->
      <p class="hero-description" style="max-width:700px;margin:1.2rem auto 0;color:#d1d5db;line-height:1.8;">
        {str(enriched.get("user", {}).get("short_bio") or "")}
      </p>

      <div class="btn-group">
        <button class="btn btn-primary"
          onclick="document.querySelector('#projects').scrollIntoView({{ behavior: 'smooth' }})">
          View My Work
        </button>
        <a href="{enriched.get('user', {}).get('resume_link', '#')}" target="_blank" rel="noopener noreferrer"
          class="btn btn-secondary" style="display:inline-block;text-decoration:none;">
          Download Resume
        </a>
      </div>
    </div>
    <div class="scroll-indicator">↓</div>
  </header>


  <!-- Education Section -->
  <section id="about">
    <div class="section-header">
      <div class="section-subtitle">My Journey</div>
      <h2>Education</h2>
      <p class="section-description">Academic background and qualifications that shaped my career</p>
    </div>
    <div class="card-grid">
      {''.join(f'''<div class="card">
        <div class="card-icon">🎓</div>
        <h3>{e.get('degree', '')}</h3>
        <div class="card-meta">{e.get('institution', '')} • {e.get('duration', '')}</div>
        <p><strong>GPA:</strong> {e.get('gpa_/_cgpa', '')}</p>
        <p>{e.get('achievements', '')}</p>
        <p>{e.get('short_summary', '')}</p>
      </div>''' for e in enriched.get('education', []))}
    </div>
  </section>

  <!-- Experience Section -->
  <section id="experience">
    <div class="section-header">
      <div class="section-subtitle">Professional Journey</div>
      <h2>Work Experience</h2>
      <p class="section-description">Professional roles and responsibilities that enhanced my expertise</p>
    </div>
    <div class="card-grid">
      {''.join(f'''<div class="card">
        <div class="card-icon">💼</div>
        <h3>{exp.get('role', '')}</h3>
        <div class="card-meta">{exp.get('company', '')} • {exp.get('duration', '')}</div>
        <p>{exp.get('description', '')}</p>
        <p>{exp.get('short_summary', '')}</p>
        <div class="card-tags">
          {''.join(f'<span class="tag">{tech}</span>' for tech in exp.get('technologies', []))}
        </div>
      </div>''' for exp in enriched.get('experience', []))}
    </div>
  </section>

  <!-- Projects Section -->
  <section id="projects">
    <div class="section-header">
      <div class="section-subtitle">My Work</div>
      <h2>Featured Projects</h2>
      <p class="section-description">A selection of projects that showcase my skills and expertise</p>
    </div>
    <div class="card-grid">
      {''.join(f'''
      <div class="card">
        <div class="card-icon">🚀</div>
        <h3>{p.get('project_title', '')}</h3>
        <div class="card-meta">{p.get('role', '')}</div>
        <p>{p.get('short_summary', '')}</p>
        <div class="card-tags">
          {''.join(f'<span class="tag">{tech}</span>' for tech in p.get('tools_/_tech_stack', []) if tech)}
        </div>
      </div>
      ''' for p in enriched.get('projects', []) if p.get('project_title') and p.get('short_summary'))}
    </div>

  </section>

  <!-- Skills Section -->
  <section id="skills">
    <div class="section-header">
      <div class="section-subtitle">What I Do</div>
      <h2>Skills & Expertise</h2>
      <p class="section-description">Technologies and tools I work with on a daily basis</p>
    </div>
    <div class="skills-container">
      {''.join(f'''<div class="skill-card">
        <div class="skill-header">
          <span class="skill-name">{s.get('skill_name', '')}</span>
          <span class="skill-level">{s.get('level', '')}</span>
        </div>
        <div class="skill-bar">
          <div class="skill-progress" style="width: {'90%' if s.get('level') == 'Advanced' or s.get('level') == 'Expert' else '75%' if s.get('level') == 'Intermediate' else '60%'};"></div>
        </div>
      </div>''' for s in enriched.get('skills', []))}
    </div>
  </section>

  <!-- Certifications Section -->
  <section id="certifications">
    <div class="section-header">
      <div class="section-subtitle">Achievements</div>
      <h2>Certifications</h2>
      <p class="section-description">Professional certifications and accomplishments</p>
    </div>
    <div class="card-grid">
      {''.join(f'''<div class="card">
        <div class="card-icon">🏆</div>
        <h3>{c.get('title', '')}</h3>
        <div class="card-meta">{c.get('issuer', '')}</div>
        <p>{c.get('notes', '')}</p>
        <p>{c.get('short_summary', '')}</p>
      </div>''' for c in enriched.get('certifications', []))}
    </div>
  </section>

  <!-- Contact Section -->
  <section id="contact">
    <div class="section-header">
      <div class="section-subtitle">Get In Touch</div>
      <h2>Contact Me</h2>
      <p class="section-description">Let's discuss your next project or opportunity</p>
    </div>
    <div class="contact-container">
      <div class="contact-info">
        <div class="contact-item">
          <div class="contact-icon">📧</div>
          <div class="contact-details">
            <h4>Email</h4>
            <p>{enriched.get('user', {}).get('email', '')}</p>
          </div>
        </div>
        <div class="contact-item">
          <div class="contact-icon">📍</div>
          <div class="contact-details">
            <h4>Location</h4>
            <p>{enriched.get('user', {}).get('location', '')}</p>
          </div>
        </div>
        <div class="contact-item">
          <div class="contact-icon">💻</div>
          <div class="contact-details">
            <h4>GitHub</h4>
            <p>{enriched.get('user', {}).get('github', '')}</p>
          </div>
        </div>
        <div class="contact-item">
          <div class="contact-icon">💼</div>
          <div class="contact-details">
            <h4>LinkedIn</h4>
            <p>{enriched.get('user', {}).get('linkedin', '')}</p>
          </div>
        </div>
      </div>
      <div class="contact-info">
        <div class="card">
          <h3>Send a Message</h3>
          <p style="margin-top: 1rem;">I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.</p>
          <button class="btn btn-primary" style="margin-top: 2rem; width: 100%;">Start Conversation</button>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer>
    <div class="footer-brand">{enriched.get("user", {}).get("name", "Portfolio")}</div>
    <p>© 2025 {enriched.get("user", {}).get("name", "Portfolio")} | Built with ❤️ and HTML</p>
    <p>Generated — {style.capitalize()} Portfolio</p>
  </footer>

  <script>
    // Navbar scroll effect
    const nav = document.getElementById('navbar');
    window.addEventListener('scroll', () => {{
      if (window.scrollY > 50) {{
        nav.classList.add('scrolled');
      }} else {{
        nav.classList.remove('scrolled');
      }}
    }});

    // Smooth scroll for navigation links
    document.querySelectorAll('nav a').forEach(link => {{
      link.addEventListener('click', (e) => {{
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }});
    }});

    // Scroll indicator
    document.querySelector('.scroll-indicator').addEventListener('click', () => {{
      document.querySelector('#about').scrollIntoView({{ behavior: 'smooth' }});
    }});

    // Load portfolio data from JSON
    fetch('./portfolio.json')
      .then(r => r.json())
      .then(data => console.log('Portfolio loaded:', data))
      .catch(err => console.error('Error loading portfolio.json', err));
  </script>
</body>
</html>
"""

    html_path = os.path.join(save_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_code)

    return {
    "message": f"{style.capitalize()} portfolio generated!",
    "path": save_dir,
    "preview_url": f"/outputs/{style}_portfolio/index.html",
    "zip_url": f"/download/{style}"
    }

from fastapi.responses import FileResponse
import shutil

@app.get("/download/{style}")
def download_portfolio(style: str):
    """
    Compress and download the generated portfolio folder.
    The ZIP will include index.html, README.md, and portfolio.json.
    """
    folder_path = f"outputs/{style}_portfolio"
    if not os.path.exists(folder_path):
        return {"error": f"Portfolio for '{style}' not found. Generate it first."}

    zip_path = f"{folder_path}.zip"

    # Delete old ZIP if it exists, then recreate
    if os.path.exists(zip_path):
        os.remove(zip_path)

    shutil.make_archive(folder_path, 'zip', folder_path)

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{style}_portfolio.zip"
    )

