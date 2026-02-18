# SENTRIFIX AI: FERPA-Compliant AI Security Gateway

SENTRIFIX AI is a security governance middleware designed to ensure FERPA compliance and prevent data leakage when using Large Language Models (LLMs) in higher education. The project functions as a "Zero-Leak Intelligence Gateway" using a Zero-Knowledge architecture.

## Project Overview
The system acts as a protective layer between the user and the AI. It utilizes Microsoft Presidio and custom regular expressions to detect and mask sensitive information, such as 7-digit student IDs, in real-time. Personal data is only restored ("rehydrated") on the authorized advisor's local dashboard after the AI has processed the information.

## Technical Stack
* Backend: Python and Flask.
* AI Orchestration: Ollama for local model execution.
* Privacy Engine: Microsoft Presidio for PII (Personally Identifiable Information) detection and anonymization.

## Installation and Setup
All commands should be run from the project root directory.

1. Install Dependencies:
   
   pip install -r requirements.txt

2. Install Python Libraries:
   
   pip install flask ollama presidio-analyzer presidio-anonymizer spacy

3. Install Language Model:
   The following model is required for Microsoft Presidio to analyze and identify sensitive text.

   python -m spacy download en_core_web_lg

4. Configure Ollama:
   Ensure Ollama is installed and running locally. Pull the specific model used for this project:

   ollama pull llama3.2

5. Execution
   Once the setup is complete, launch the application:

   python app.py
   
   The Aurora Dashboard will be accessible at http://localhost:5000.

Security Implementation
Local Inference: By using Ollama, no data is sent to external AI providers, keeping sensitive records within the local network.

Audit Logging: Every interaction is captured in a local audit log for governance and security reviews.

PII Redaction: The system automatically identifies and replaces sensitive entities with placeholders before the AI processes the notes.

* **Local Governance Interface:** This view demonstrates the SENTRIFIX secure gateway where users input sensitive text. The interface highlights identified PII (like 7-digit student IDs) in real-time using local Microsoft Presidio logic, ensuring that no raw data ever leaves the local environment for processing.
![Dashboard Redaction View](assets/dash1.png)

* **Privacy-Preserving Summarization:** This image shows the "Zero-Leak" workflow in action. Before reaching the local Ollama LLM, all sensitive identifiers are masked with generic tokens. The resulting summary provides academic insights without the AI ever having access to the student’s actual identity.
![Local Inference Logs](assets/dash2.png)



