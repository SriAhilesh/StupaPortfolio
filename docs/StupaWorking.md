## 🧭 How to Generate Your Portfolio (Step-by-Step Guide)

This application uses **Notion as the data source** for your portfolio. Instead of filling forms inside the website, you prepare your content in a structured Notion template, and the system transforms it into a polished portfolio using AI.

Follow these steps carefully:

---

## 🔹 Step 1: Download the Notion Template

* Open the frontend application.
* Locate the **Notion Template download link/button**.
* Download or duplicate the template into your own Notion workspace.

This template already contains all required sections such as:

* Projects
* Skills
* Experience
* Education
* Additional details

These are organized as structured tables that the backend will read.

---

## 🔹 Step 2: Fill in Your Details in Notion

Open the duplicated template in Notion and complete all the tables.

### Important:

* Fill **every required field** (don’t leave empty rows)
* Keep the structure unchanged (don’t rename columns unless necessary)
* Write clear and meaningful descriptions (AI will refine them)

Examples of what you’ll add:

* Project titles and descriptions
* Technologies used
* Roles and contributions
* Skills and tools
* Education details

The quality of your portfolio depends on the clarity of this data.

---

## 🔹 Step 3: Get Your Notion Integration Token

To allow the app to read your data, you need a Notion API token.

1. Go to Notion Developers (create integration)
2. Generate a **Notion Integration Token**
3. Copy the token

### Then:

* Open your Notion template page
* Click **Share**
* Invite your integration (very important)

Without sharing access, the app cannot read your data.

---

## 🔹 Step 4: Copy Your Notion Page Link

* Open your filled Notion template
* Copy the page URL from the browser

Example:

```id="p3p94n"
https://www.notion.so/your-workspace/your-page-id
```

---

## 🔹 Step 5: Provide Inputs in the Web App

Go back to your frontend UI and enter:

* **Notion Token**
* **Notion Page URL**

These two inputs connect your Notion data to the backend system.

---

## 🔹 Step 6: Generate Your Portfolio

Click the **"Generate Portfolio"** button.

### What happens internally:

1. The frontend sends your inputs to the backend
2. The backend uses the Notion API to fetch your data
3. Data is cleaned, structured, and validated
4. AI processes and enhances your content
5. A formatted portfolio is generated

---

## 🔹 Step 7: View and Download

* Your generated portfolio will be displayed on the screen
* You can review the content
* Download it if needed (based on available export options)

---

## ⚠️ Common Mistakes to Avoid

* ❌ Not sharing Notion page with the integration
* ❌ Incorrect Notion token
* ❌ Empty or incomplete template fields
* ❌ Modifying template structure heavily

---

## 💡 Tips for Best Results

* Write simple, clear inputs — AI will enhance them
* Be consistent across all sections
* Add meaningful project descriptions
* Use real data instead of placeholders

---

## 🧠 How the System Works (Simplified)

* Notion → Data Source
* Backend → Processing + AI Enhancement
* Frontend → Display + Download

---

## 📌 Final Thought

This system is designed to separate **content creation (Notion)** from **presentation (Portfolio UI)**. Once your Notion template is properly filled, generating a professional portfolio becomes a one-click process.

---
