# AI-Powered Resume Analyzer & Job Matcher

## Planning
- [/] Design project architecture and folder structure
- [/] Create implementation plan with all components
- [ ] Get user approval on the plan

## Phase 1: Project Setup
- [ ] Initialize project structure and virtual environment
- [ ] Create `requirements.txt` with all dependencies
- [ ] Set up `.env` for API keys (OpenAI, Pinecone)
- [ ] Create configuration module

## Phase 2: Core Backend — Resume Parsing
- [ ] Build PDF/DOCX resume parser (`resume_parser.py`)
- [ ] Implement skill extraction using NER + LLM (`skill_extractor.py`)
- [ ] Create resume data models (`models.py`)

## Phase 3: Vector Database & RAG
- [ ] Set up Pinecone index initialization (`pinecone_manager.py`)
- [ ] Build embedding pipeline with LangChain + OpenAI (`embeddings.py`)
- [ ] Implement RAG retrieval chain (`rag_chain.py`)

## Phase 4: Job Matching Engine
- [ ] Build job description ingestion (`job_manager.py`)
- [ ] Implement semantic similarity matching (`matcher.py`)
- [ ] Create resume improvement suggestion engine (`suggestions.py`)

## Phase 5: Streamlit UI
- [ ] Build main app layout and navigation (`app.py`)
- [ ] Create Resume Upload & Analysis page
- [ ] Create Job Matching page
- [ ] Create Resume Improvement Suggestions page
- [ ] Style with premium dark theme

## Phase 6: Verification & Polish
- [ ] Write unit tests for core modules
- [ ] End-to-end testing via browser
- [ ] Create README.md with setup instructions
- [ ] Create walkthrough artifact
