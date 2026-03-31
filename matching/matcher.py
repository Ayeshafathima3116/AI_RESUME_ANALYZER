"""
Job matching engine.
Handles job ingestion into Pinecone and direct similarity matching.
"""

import json
import uuid
from core.models import JobDescription
from vectordb.pinecone_manager import get_index, init_index, upsert_jobs_batch, get_index_stats
from vectordb.embeddings import embed_text, embed_documents


# ── Sample job data ─────────────────────────────────────

SAMPLE_JOBS = [
    JobDescription(
        job_id="job_ml_engineer",
        title="Machine Learning Engineer",
        company="TechVision AI",
        location="San Francisco, CA (Remote)",
        required_skills=["Python", "TensorFlow", "PyTorch", "Docker", "SQL", "Machine Learning", "Deep Learning"],
        preferred_skills=["Kubernetes", "MLflow", "AWS SageMaker", "LLMs", "Transformers"],
        description="Build and deploy ML models at scale. Work on NLP, computer vision, and recommendation systems. Collaborate with data scientists and engineers.",
        experience_level="Mid-Senior (3-5 years)",
    ),
    JobDescription(
        job_id="job_data_scientist",
        title="Senior Data Scientist",
        company="DataDriven Corp",
        location="New York, NY",
        required_skills=["Python", "R", "SQL", "Statistics", "Machine Learning", "Pandas", "Scikit-learn"],
        preferred_skills=["Spark", "Tableau", "A/B Testing", "Deep Learning", "NLP"],
        description="Lead data science initiatives. Develop predictive models, perform statistical analysis, and drive data-informed decision making across the organization.",
        experience_level="Senior (5+ years)",
    ),
    JobDescription(
        job_id="job_fullstack_dev",
        title="Full-Stack Developer",
        company="WebScale Inc",
        location="Austin, TX (Hybrid)",
        required_skills=["JavaScript", "TypeScript", "React", "Node.js", "PostgreSQL", "REST APIs", "Git"],
        preferred_skills=["Next.js", "GraphQL", "Docker", "AWS", "CI/CD", "Redis"],
        description="Build and maintain web applications. Design RESTful APIs, implement responsive UIs, and ensure application performance and security.",
        experience_level="Mid (2-4 years)",
    ),
    JobDescription(
        job_id="job_devops_eng",
        title="DevOps Engineer",
        company="CloudFirst Solutions",
        location="Seattle, WA (Remote)",
        required_skills=["AWS", "Docker", "Kubernetes", "Terraform", "CI/CD", "Linux", "Python"],
        preferred_skills=["Azure", "Ansible", "Prometheus", "Grafana", "Helm", "ArgoCD"],
        description="Design and manage cloud infrastructure. Implement CI/CD pipelines, automate deployments, and ensure system reliability and scalability.",
        experience_level="Mid-Senior (3-5 years)",
    ),
    JobDescription(
        job_id="job_backend_dev",
        title="Backend Engineer",
        company="FinTech Prime",
        location="Chicago, IL",
        required_skills=["Python", "Django", "PostgreSQL", "Redis", "REST APIs", "Docker", "Git"],
        preferred_skills=["FastAPI", "Celery", "RabbitMQ", "Kubernetes", "GraphQL"],
        description="Design and build scalable backend services for financial applications. Handle high-throughput transaction processing and data integrity.",
        experience_level="Mid (2-4 years)",
    ),
    JobDescription(
        job_id="job_ai_researcher",
        title="AI Research Scientist",
        company="DeepMind Labs",
        location="London, UK (Remote)",
        required_skills=["Python", "PyTorch", "Deep Learning", "NLP", "Computer Vision", "Research", "Mathematics"],
        preferred_skills=["Reinforcement Learning", "GANs", "Transformers", "CUDA", "Publishing Papers"],
        description="Conduct cutting-edge AI research. Develop novel algorithms, publish papers, and translate research into production systems.",
        experience_level="Senior (5+ years)",
    ),
    JobDescription(
        job_id="job_data_eng",
        title="Data Engineer",
        company="BigData Analytics",
        location="Denver, CO (Hybrid)",
        required_skills=["Python", "SQL", "Apache Spark", "Airflow", "AWS", "ETL", "Data Warehousing"],
        preferred_skills=["Kafka", "dbt", "Snowflake", "Delta Lake", "Databricks"],
        description="Build and maintain data pipelines. Design data warehouse schemas, optimize query performance, and ensure data quality across the platform.",
        experience_level="Mid (2-4 years)",
    ),
    JobDescription(
        job_id="job_mobile_dev",
        title="Mobile App Developer",
        company="AppCraft Studios",
        location="Los Angeles, CA",
        required_skills=["React Native", "JavaScript", "TypeScript", "REST APIs", "Git", "Mobile UI/UX"],
        preferred_skills=["Swift", "Kotlin", "Firebase", "Redux", "GraphQL", "App Store Deployment"],
        description="Develop cross-platform mobile applications. Implement smooth animations, offline capabilities, and push notifications.",
        experience_level="Mid (2-4 years)",
    ),
    JobDescription(
        job_id="job_cybersec",
        title="Cybersecurity Analyst",
        company="SecureNet Defense",
        location="Washington, DC",
        required_skills=["Network Security", "SIEM", "Incident Response", "Vulnerability Assessment", "Python", "Linux"],
        preferred_skills=["Penetration Testing", "CISSP", "Cloud Security", "Forensics", "Splunk"],
        description="Monitor and protect enterprise systems. Conduct security assessments, respond to incidents, and implement security best practices.",
        experience_level="Mid-Senior (3-5 years)",
    ),
    JobDescription(
        job_id="job_cloud_architect",
        title="Cloud Solutions Architect",
        company="Enterprise Cloud Co",
        location="Remote",
        required_skills=["AWS", "Azure", "Cloud Architecture", "Networking", "Security", "Terraform", "Microservices"],
        preferred_skills=["GCP", "Serverless", "Cost Optimization", "Multi-cloud", "Solution Design"],
        description="Design enterprise cloud solutions. Lead cloud migration projects, optimize costs, and ensure compliance with security standards.",
        experience_level="Senior (5+ years)",
    ),
    JobDescription(
        job_id="job_frontend_dev",
        title="Senior Frontend Developer",
        company="PixelPerfect Design",
        location="Portland, OR (Remote)",
        required_skills=["React", "TypeScript", "CSS", "HTML", "JavaScript", "Responsive Design", "Git"],
        preferred_skills=["Next.js", "Tailwind CSS", "Figma", "Accessibility", "Performance Optimization", "Testing"],
        description="Build beautiful, performant web interfaces. Collaborate closely with designers. Champion accessibility and web standards.",
        experience_level="Senior (4+ years)",
    ),
    JobDescription(
        job_id="job_nlp_engineer",
        title="NLP Engineer",
        company="LangTech AI",
        location="Boston, MA (Hybrid)",
        required_skills=["Python", "NLP", "Transformers", "Hugging Face", "PyTorch", "LLMs", "Text Processing"],
        preferred_skills=["LangChain", "RAG", "Fine-tuning", "Prompt Engineering", "Vector Databases", "spaCy"],
        description="Build NLP-powered products. Work on LLM integration, RAG pipelines, prompt engineering, and text analytics at scale.",
        experience_level="Mid-Senior (3-5 years)",
    ),
]


def ingest_sample_jobs() -> int:
    """
    Embed and upsert all sample job descriptions into Pinecone.
    Returns the number of jobs ingested.
    """
    index = init_index()

    # Prepare texts for batch embedding
    texts = [job.to_embedding_text() for job in SAMPLE_JOBS]
    embeddings = embed_documents(texts)

    # Build vectors with metadata
    vectors = []
    for job, emb in zip(SAMPLE_JOBS, embeddings):
        metadata = {
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "required_skills": json.dumps(job.required_skills),
            "preferred_skills": json.dumps(job.preferred_skills),
            "description": job.description,
            "experience_level": job.experience_level,
        }
        vectors.append((job.job_id, emb, metadata))

    upsert_jobs_batch(index, vectors)
    return len(vectors)


def ingest_custom_job(job: JobDescription) -> str:
    """
    Embed and upsert a single custom job description.
    Returns the job_id.
    """
    index = get_index()

    if not job.job_id:
        job.job_id = f"custom_{uuid.uuid4().hex[:8]}"

    embedding = embed_text(job.to_embedding_text())
    metadata = {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "required_skills": json.dumps(job.required_skills),
        "preferred_skills": json.dumps(job.preferred_skills),
        "description": job.description,
        "experience_level": job.experience_level,
    }

    index.upsert(vectors=[(job.job_id, embedding, metadata)])
    return job.job_id


def get_db_stats() -> dict:
    """Get Pinecone index statistics."""
    try:
        index = get_index()
        return get_index_stats(index)
    except Exception:
        return {}
