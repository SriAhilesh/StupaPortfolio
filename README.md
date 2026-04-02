# 🚀 AI-Powered Portfolio Generator

An end-to-end full-stack application that automatically generates professional developer portfolios using AI. This project takes minimal user input and transforms it into structured, polished, and ready-to-use portfolio content through an intelligent backend pipeline and a clean frontend interface.

---

## 📌 Overview

The AI Portfolio Generator is designed to simplify the process of creating a developer portfolio. Instead of manually writing descriptions, structuring projects, and formatting content, users can input basic information and let the system generate a complete portfolio.

This project demonstrates:

* Full-stack development (Frontend + Backend)
* AI/LLM integration
* Modular system design
* Real-world deployment architecture

---

## 🧠 Key Features

* ✨ AI-generated project descriptions and summaries
* 🧩 Modular backend pipeline (input → processing → output)
* 🎨 Clean and responsive frontend interface
* ⚡ Fast content generation with structured output
* 🔁 Reusable and scalable architecture
* 📄 Ready-to-use portfolio content

---

## 🏗️ Project Structure

```
StupaPortfolio/
│
├── frontend/        # React-based user interface
│
├── backend/         # Python backend (AI processing)
│
├── README.md        # Project documentation
└── .gitignore       # Ignored files and folders
```

---

## 🛠️ Tech Stack

### Frontend

* React.js
* Vite (or Create React App)
* Tailwind CSS (if used)

### Backend

* Python
* FastAPI / Flask (depending on your setup)
* LLM integration (GPT-based or similar)

### Tools

* Git & GitHub
* REST APIs
* JSON-based data flow

---

## ⚙️ Setup Instructions

### 🔹 1. Clone the Repository

```
git clone https://github.com/your-username/stupa-portfolio-generator.git
cd stupa-portfolio-generator
```

---

### 🔹 2. Setup Frontend

```
cd frontend
npm install
npm run dev
```

Frontend will run at:

```
http://localhost:5173   (Vite)
OR
http://localhost:3000   (CRA)
```

---

### 🔹 3. Setup Backend

Create virtual environment (recommended):

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

Run backend server:

```
python main.py
```

OR (if using FastAPI):

```
uvicorn main:app --reload
```

Backend will run at:

```
http://localhost:8000
```

---

## 🔗 Connecting Frontend & Backend

Create a `.env` file inside `frontend/`:

```
VITE_API_URL=http://localhost:8000
```

Restart frontend after adding this.

---

## 🧠 How It Works (Architecture)

1. **User Input (Frontend)**

   * User enters project details, skills, etc.

2. **API Request**

   * Frontend sends data to backend via REST API

3. **Processing Engine (Backend)**

   * Input is structured and passed to AI model
   * Prompt engineering enhances content quality

4. **Content Generation**

   * AI generates descriptions, summaries, formatting

5. **Response to Frontend**

   * Structured JSON is returned

6. **Rendering**

   * Frontend displays ready-to-use portfolio content

---

## 📦 Important Notes

* `node_modules/` is excluded (use `npm install`)
* `venv/` is excluded (recreate locally)
* `.env` files are not pushed (store secrets securely)

---

## 🚀 Deployment Guide (Basic)

### Frontend

* Deploy using Vercel or Netlify
* Set root directory to `/frontend`

### Backend

* Deploy using Render / Railway
* Set root directory to `/backend`
* Add environment variables in platform dashboard

### Connect Both

Update frontend `.env`:

```
VITE_API_URL=https://your-backend-url.com
```

---

## ⚠️ Common Issues

### ❌ Frontend not connecting to backend

* Check API URL in `.env`
* Ensure backend is running

### ❌ Module not found errors

* Run `npm install` again

### ❌ Python dependencies missing

* Run `pip install -r requirements.txt`

---

## 🌱 Future Improvements

* Authentication system
* Multiple portfolio templates
* Export as PDF / Website
* Drag-and-drop customization
* Database integration

---

## 👨‍💻 Author

Sri Ahilesh
Developed as a full-stack AI project demonstrating real-world application of LLMs, frontend engineering, and backend system design.

---

## 📜 License

This project is open-source and available for learning and development purposes.

---

## 💡 Final Note

This project is not just about generating portfolios — it represents a scalable approach to combining AI with real-world applications. The architecture, modular design, and automation reflect production-level thinking.

---
