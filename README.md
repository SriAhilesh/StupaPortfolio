# 🚀 AI-Powered Portfolio Generator

An end-to-end full-stack application that automatically generates professional developer portfolios using AI. This project uses structured data from Notion and transforms it into a polished, ready-to-use portfolio through an intelligent backend pipeline and a clean frontend interface.

---

## 📌 Overview

The AI Portfolio Generator simplifies the process of building a professional portfolio. Instead of manually writing and formatting content, users prepare their data in a structured Notion template, and the system generates a complete portfolio automatically.

This project demonstrates:

* Full-stack development (Frontend + Backend)
* AI/LLM integration
* Notion API integration
* Modular system design
* Real-world deployment architecture

---

## 🧠 Key Features

* ✨ AI-enhanced project descriptions and summaries
* 🧩 Notion-based structured input system
* 🎨 Clean and responsive frontend interface
* ⚡ Fast content generation pipeline
* 🔁 Scalable and reusable backend architecture
* 📄 Ready-to-use portfolio output

---

## 🧭 How to Use

This project follows a **Notion-driven workflow**, where users prepare their data in a predefined template.

👉 **Full step-by-step guide:**
[How to Generate Your Portfolio](./docs/StupaWorking.md)

### Quick Summary

1. Download and duplicate the Notion template
2. Fill in all required details (projects, skills, etc.)
3. Generate a Notion integration token
4. Share your Notion page with the integration
5. Provide:

   * Notion Token
   * Notion Page URL
6. Click **Generate Portfolio**
7. View and download your portfolio

---

## 🏗️ Project Structure

```
StupaPortfolio/
│
├── frontend/        # React-based user interface
├── backend/         # Python backend (AI processing)
├── docs/            # Documentation (usage guide, etc.)
│   └── StupaWorking.md
├── README.md
└── .gitignore
```

---

## 🛠️ Tech Stack

### Frontend

* React.js
* Vite (or Create React App)
* Tailwind CSS

### Backend

* Python
* FastAPI / Flask
* Notion API
* LLM integration (GPT-based / Gemini)

### Tools

* Git & GitHub
* REST APIs
* JSON-based data flow

---

## ⚙️ Setup Instructions

### 🔹 1. Clone the Repository

```
git clone https://github.com/your-username/StupaPortfolio.git
cd StupaPortfolio
```

---

### 🔹 2. Setup Frontend

```
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173   (Vite)
OR
http://localhost:3000   (CRA)
```

---

### 🔹 3. Setup Backend

```
cd backend
python -m venv venv
```

Activate environment:

**Windows:**

```
venv\Scripts\activate
```

**Mac/Linux:**

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run server:

```
python main.py
```

OR:

```
uvicorn main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

## 🔗 Connecting Frontend & Backend

Create `.env` inside `frontend/`:

```
VITE_API_URL=http://localhost:8000
```

Restart frontend after updating.

---

## 🧠 How It Works (Architecture)

1. **Notion as Data Source**

   * User fills structured template

2. **API Integration**

   * Backend fetches data using Notion API

3. **Processing Layer**

   * Data is cleaned and structured

4. **AI Enhancement**

   * LLM improves descriptions and formatting

5. **Output Generation**

   * Portfolio content is generated

6. **Frontend Rendering**

   * UI displays and allows download

---

## 📦 Important Notes

* `node_modules/` is excluded (use `npm install`)
* `venv/` is excluded (recreate locally)
* `.env` files are not pushed (keep secrets safe)

---

## 🚀 Deployment Guide (Basic)

### Frontend

* Deploy using Vercel or Netlify
* Root directory: `/frontend`

### Backend

* Deploy using Render / Railway
* Root directory: `/backend`
* Add environment variables

### Connect Both

```
VITE_API_URL=https://your-backend-url.com
```

---

## ⚠️ Common Issues

### ❌ Notion data not loading

* Ensure page is shared with integration
* Verify token is correct

### ❌ Frontend not connecting

* Check `.env` API URL
* Ensure backend is running

### ❌ Dependencies missing

* Run `npm install` / `pip install -r requirements.txt`

---

## 🌱 Future Improvements

* Authentication system
* Multiple portfolio templates
* Export as PDF / hosted website
* Drag-and-drop customization
* Database integration

---

## 👨‍💻 Author

Sri Ahilesh

Developed as a full-stack AI project demonstrating real-world AI integration, system design, and frontend-backend architecture.

---

## 📜 License

This project is open-source and available for learning and development purposes.

---

## 💡 Final Note

This project separates **content creation (Notion)** from **presentation (Portfolio UI)** — enabling a scalable, AI-driven approach to portfolio generation.

---
