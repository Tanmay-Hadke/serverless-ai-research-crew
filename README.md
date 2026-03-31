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


## 💡 The Motivation: Why Build This?
The era of "single-prompt" AI is ending. While tools like ChatGPT are incredibly powerful, relying on a single large language model (LLM) to research, synthesize, and format complex information in one shot frequently leads to shallow responses, missed context, and—most dangerously—hallucinations. 

I chose to build this project to transition from **Generative AI** to **Agentic AI**. By orchestrating a crew of specialized AI agents—where one plans, one researches, one writes, and one strictly fact-checks—we can mimic a real-world human research team. Furthermore, building this entirely on serverless cloud infrastructure (AWS) allowed me to solve enterprise-level engineering challenges, such as bypassing strict API rate limits and handling asynchronous HTTP timeouts.

## ⚠️ The Real-World Problem
In today's information economy, professionals face two major bottlenecks:
1. **The Time Cost of Synthesis:** Deep-diving into a complex topic (e.g., "The impact of solid-state batteries on EV supply chains") requires hours of reading disparate sources, extracting key facts, and formatting them into a digestible brief.
2. **The Trust Deficit in AI:** When professionals try to shortcut this process using standard AI chatbots, they are forced to spend almost as much time manually verifying the AI's claims because standard models prioritize "sounding confident" over factual accuracy.

## 🎯 Who is Most Affected?
This "Trust vs. Time" dilemma heavily impacts professionals whose work relies on rapid, highly accurate data aggregation:
* **Market Analysts & Consultants:** Who need to generate industry landscape briefs for clients overnight.
* **Academic Researchers & Students:** Who need to quickly map out the current state of literature on a niche scientific topic.
* **Technical Writers & Product Managers:** Who need to understand new technologies or competitor features without getting bogged down in marketing fluff.
* **C-Suite Executives:** Who require 2-page executive summaries on complex geopolitical or economic shifts to make informed decisions.

## 🛠️ How They Can Use This Project
This project abstracts the complex cloud architecture into a beautifully simple, consumer-friendly interface. 

1. **The Input:** A user simply types a broad or complex topic into the sleek UI (e.g., *"What are the economic implications of migrating enterprise software from Monolith to Microservices?"*).
2. **The Orchestration:** They click "Deploy Agents" and can step away. They don't need to write clever prompts or chain thoughts together. The AWS backend automatically spins up the four-agent Step Function pipeline.
3. **The Verification:** Because the final "Reviewer Agent" is strictly instructed to delete any claims not explicitly found in the raw research, the user receives a report they can actually trust.
4. **The Output:** Within 2-3 minutes, the user receives a fully formatted, beautifully stylized Markdown report that they can instantly export to PDF, copy to their clipboard, or save as a raw `.md` file to drop directly into their internal knowledge bases (like Notion or Obsidian).
