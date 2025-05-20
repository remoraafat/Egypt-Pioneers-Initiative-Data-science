# 💼 Resume Screening System  
**Final Project – DEPI Internship | EYouth**

A smart, AI-powered resume screening application that leverages **Natural Language Processing (NLP)** and **Large Language Models (LLMs)** to automate and optimize the hiring process. Built to help HR professionals efficiently filter and evaluate resumes based on job requirements.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Sample Output](#-sample-output)
- [Screenshots](#-screenshots)
- [Contributors](#-contributors)

---
## 📌 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [project Structure](#-Project-Structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Sample Output](#-sample-output)
- [Screenshots](#-screenshots)

---
## 📄 Overview

Recruitment is often slowed down by manual resume screening. This project introduces a smart resume screening system that uses **NLP**, **LLMs**, and **data analysis** techniques to evaluate resumes by extracting key information like skills, experience, and education. It automatically compares resumes to job descriptions and provides feedback on candidate-job fit.

This project was developed as part of our **DEPI Internship in collaboration with EYouth**, showcasing the potential of **AI in HR tech**.

---

## 🛠️ Tech Stack

### 🧠 Artificial Intelligence
- **Natural Language Processing (NLP)**:
  - Tokenization, Named Entity Recognition (NER), Part-of-Speech tagging
  - Used to extract structured data from unstructured resumes
- **Large Language Models (LLMs)** (optional/future-ready):
  - Models like **Openrouter API** for feedback generation
  - Used for semantic comparison between resumes and job descriptions
- **Text Similarity & Semantic Matching**:
  - TF-IDF Vectorization
  - Cosine Similarity for comparing candidate content to job criteria

  ### 📚 Python Libraries

| Library        | Purpose                                      |
|----------------|----------------------------------------------|
| `spaCy`        | NLP pipeline for skill and experience extraction |
| `nltk`         | Tokenization and text preprocessing           |
| `PyPDF2`       | Extracting resume text from PDF files         |
| `pandas`       | Data manipulation and analysis                 |
| `scikit-learn` | TF-IDF vectorization and similarity matching  |
| `openrouter`   | Integration API for language model capabilities  |
| `qwen`         | AI-powered search and data retrieval for enhanced resume matching |
| `deepseek`     | Deep learning-based semantic search to improve matching accuracy |
| `streamlit`    | Interactive UI framework for building user-friendly web apps |


---

## ✨ Features

- ✅ Extracts skills, experience, education, and keywords from resumes
- ✅ Compares resumes against job descriptions using NLP
- ✅ Ranks candidates based on job relevance
- ✅ Provides **human-readable feedback** 
- ✅ Modular and easy to extend for new features
- ✅ Prepares the system for chatbot integration (future)

---
## 🧱 System Architecture

```
PDF Resumes
   |
   |--[PyPDF2]--> Extracted Text
   |
   |--[LLM]--> Feedback Generation
   |
   |--> HR Review Output
```

---

## 📂 Project Structure

```bash
.
├── app.py                 # Main Streamlit application
├── auth.py                # User authentication (register/login)
├── chat_memory.py         # Chat history management
├── resume_analyzer.py     # Resume evaluation using LLM
├── resume_parser.py       # PDF text extraction
├── .env                   # API credentials
├── /DB/                   # Contains SQLite databases
└── requirements.txt       # Python dependencies
```

---

## ⚙️ Installation

1. **Clone the Repository**  
```
git clone 
cd resume-screening/Chatbot_version_1
```

2. **Create a Virtual Environment (Recommended)**  
```
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
***or using Conda:***
```
conda create --name resume-chatbot python=3.10
conda activate resume-chatbot

```

3. **Install Dependencies**  
```
pip install -r ../requirements.txt
```

---
## ▶️ Usage

Run the main script for resume analysis:

```
python app.py
```

## 🖼️ Screenshots

| Chatbot Resume Upload | Login & Register | Matching Results & Feedback |
|----------------------|------------------|----------------------------|
| ![Chatbot Upload](https://github.com/user-attachments/assets/c4532bfc-34d5-4c41-bcb3-c2455cc307b9) <br> The chatbot interface allows users to upload their resume files for screening. | ![Login/Register](https://github.com/user-attachments/assets/c17361f0-42aa-4d7f-affc-d83c09df2648) <br> Simple and secure login and registration forms for candidate access. | ![Matching Results & Feedback](https://github.com/user-attachments/assets/43b68cda-e28b-40cf-90e0-5c3ea979488f) <br> View AI-generated matching results with job descriptions and get real-time feedback on how well the resume matches the position. |



---

## 🏢 Developed For

This project was built as part of the **Digital Egypt Pioneers Initiative (DEPI)** and **EYouth**, focusing on solving real-world HR problems using Artificial Intelligence and modern software engineering practices.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).