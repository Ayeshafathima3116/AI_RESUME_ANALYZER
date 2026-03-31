# 🧠 AI-Powered Resume Analyzer & Job Matcher

A 100% free, LLM-powered application that analyzes resumes, matches candidates with job descriptions using semantic similarity, and provides actionable improvement suggestions.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-green)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange)
![HuggingFace](https://img.shields.io/badge/HuggingFace-all--MiniLM--L6--v2-yellow)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)

## ✨ Features

- **📄 Resume Analysis** — Upload PDF/DOCX resumes and get instant AI-powered skill extraction, experience analysis, and profile breakdown with radar chart visualizations.
- **🎯 Job Matching** — Semantic similarity matching using RAG architecture powered by Pinecone vector database to find your best-fit job opportunities.
- **💡 Improvement Suggestions** — Personalized, actionable suggestions for skill gap analysis and career growth (with visual coverage metrics).
- **💸 100% Free Architecture** — Built entirely on free-tier services (Groq API, local HuggingFace embeddings, Pinecone Serverless).
- **⚡ Blazing Fast AI** — Instant natural language processing powered by Groq's LPU inference engine.
- **🎨 Premium UI/UX** — Modern, dark-themed Streamlit interface with customized interactive components and seamless a top-to-bottom wizard navigation flow.

## 🏗️ Architecture

```
Resume Upload → PDF/DOCX Parser → Groq LLM Extraction → HuggingFace Embeddings
                                                              ↓
Improvement Suggestions ← RAG Chain ← Pinecone Semantic Search ← Vector Store
```

**Key Components:**
- **LangChain** — RAG orchestration, prompt chaining, and structured LLM output.
- **Groq** — Using `llama-3.3-70b-versatile` for lightning-fast profile extraction and semantic matching analysis.
- **HuggingFace** — Using local `all-MiniLM-L6-v2` models for cost-free, high-quality vectorization.
- **Pinecone** — Serverless vector database for semantic job mapping and retrieval.
- **Streamlit** — Interactive web UI with a custom premium CSS theme.

## 🚀 Setup

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
pip install -r requirements.txt
```

### 2. Configure API Keys

Create an `.env` file in the root directory with your API keys:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
PINECONE_API_KEY=pcsk_your_pinecone_key_here
PINECONE_INDEX_NAME=resume-analyzer-free
```

**Get Free API Keys:**
- Groq: [console.groq.com/keys](https://console.groq.com/keys)
- Pinecone: [app.pinecone.io](https://app.pinecone.io) (Serverless Free tier)

### 3. Run the Application

```bash
streamlit run app.py
```

## 📖 Usage Flow

The application features a seamless, linear wizard flow:
1. **Upload Resume** — Go to "Resume Analysis" page, upload a PDF/DOCX file and wait for the AI extraction.
2. **Continue to Job Matching** — Click the prominent CTA button at the bottom of the analysis page. Adjust sliders and find semantic matches.
3. **Continue to Improvements** — Click the Next Step button to identify specific skill gaps against those job matches.
4. **Analyze Another** — Hit the massive "Analyze Another Resume" button at the end of the pipeline to clear session state and start fresh.

## 🗂️ Project Structure

```
AI_RESUME_ANALYZER/
├── app.py                        # Main Streamlit dashboard
├── config.py                     # Configuration for Groq/Pinecone
├── requirements.txt
├── DEPLOYMENT.md                 # Cloud Deployment Guide
├── core/
│   ├── models.py                 # Pydantic data models
│   ├── resume_parser.py          # PDF/DOCX text extraction
│   └── skill_extractor.py        # Groq LLM skill extraction
├── vectordb/
│   ├── pinecone_manager.py       # Pinecone index management
│   └── embeddings.py             # HuggingFace embedding pipeline
├── matching/
│   ├── rag_chain.py              # RAG retrieval chain
│   ├── matcher.py                # Job matching logic
│   └── suggestions.py            # Improvement suggestion engine
├── pages/
│   ├── 1_📄_Resume_Analysis.py
│   ├── 2_🎯_Job_Matching.py
│   └── 3_💡_Improvements.py
└── assets/
    └── style.css                 # Premium dark custom theme
```

## 📄 License

MIT License
