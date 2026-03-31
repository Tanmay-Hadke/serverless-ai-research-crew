# 🧠 Serverless Multi-Agent AI Research Pipeline

An enterprise-grade, asynchronous AI research application built with React, AWS Lambda, AWS Step Functions, and the Groq API (Llama 3.1). 

## 🏗️ Architecture Overview

This project abandons standard linear API calls in favor of a **Distributed Multi-Agent State Machine**. When a user submits a complex research topic, an AWS API Gateway triggers an asynchronous Step Function pipeline containing four specialized AI agents:

1. **Agent 1 (The Planner):** Breaks the main topic down into targeted sub-queries.
2. **Agent 2 (The Researcher):** Acts as a RAG/Search simulator, pulling factual data for each query.
3. **Agent 3 (The Synthesizer):** Formats the raw data into a cohesive Markdown report.
4. **Agent 4 (The Reviewer):** Cross-references the final draft against the raw notes to eliminate LLM hallucinations.

### ⚙️ Tech Stack
* **Frontend:** React.js, standard CSS (Glassmorphism UI), Lucide Icons.
* **Backend:** Python 3.12, AWS Lambda, AWS API Gateway (HTTP APIs).
* **Orchestration:** AWS Step Functions (State Machines).
* **LLM:** Meta Llama 3.1 8B (via Groq API).
* **Networking:** Custom Lambda Layers (`requests`), Asynchronous polling to bypass 29s API timeouts.

## 🚀 Features
* **Asynchronous Execution:** Frontend polls the AWS backend via an Execution ARN, preventing Gateway timeouts during long LLM inference times.
* **Rate-Limiting Resilience:** Step Function includes native `Wait` states to gracefully handle third-party API token limits (TPM).
* **Export Options:** Instantly export the dynamically generated report to `.md`, `.txt`, or `.pdf`.
* **Zero-Hallucination Guardrails:** The final node in the pipeline is strictly dedicated to fact-checking the previous node's output.


# 🧠 Serverless Multi-Agent AI Research Pipeline

An enterprise-grade, asynchronous AI research application built with React, AWS Lambda, AWS Step Functions, and the Groq API (Llama 3.1). 

## 🏗️ Architecture Overview

This project abandons standard linear API calls in favor of a **Distributed Multi-Agent State Machine**. When a user submits a complex research topic, an AWS API Gateway triggers an asynchronous Step Function pipeline containing four specialized AI agents:

1. **Agent 1 (The Planner):** Breaks the main topic down into targeted sub-queries.
2. **Agent 2 (The Researcher):** Acts as a RAG/Search simulator, pulling factual data for each query.
3. **Agent 3 (The Synthesizer):** Formats the raw data into a cohesive Markdown report.
4. **Agent 4 (The Reviewer):** Cross-references the final draft against the raw notes to eliminate LLM hallucinations.

### ⚙️ Tech Stack
* **Frontend:** React.js, standard CSS (Glassmorphism UI), Lucide Icons.
* **Backend:** Python 3.12, AWS Lambda, AWS API Gateway (HTTP APIs).
* **Orchestration:** AWS Step Functions (State Machines).
* **LLM:** Meta Llama 3.1 8B (via Groq API).
* **Networking:** Custom Lambda Layers (`requests`), Asynchronous polling to bypass 29s API timeouts.

## 🚀 Features
* **Asynchronous Execution:** Frontend polls the AWS backend via an Execution ARN, preventing Gateway timeouts during long LLM inference times.
* **Rate-Limiting Resilience:** Step Function includes native `Wait` states to gracefully handle third-party API token limits (TPM).
* **Export Options:** Instantly export the dynamically generated report to `.md`, `.txt`, or `.pdf`.
* **Zero-Hallucination Guardrails:** The final node in the pipeline is strictly dedicated to fact-checking the previous node's output.
