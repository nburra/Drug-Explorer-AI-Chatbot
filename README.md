# Drug Explorer AI Chatbot

An AI-powered healthcare application that leverages **Retrieval-Augmented Generation (RAG)** to deliver accurate, context-aware medication information using a structured MySQL database and a Large Language Model (Llama 3.1).

Rather than relying solely on an LLM's pretrained knowledge, the application retrieves verified medication data from a database before generating responses, reducing hallucinations and improving response reliability.

---

# Business Problem

Large Language Models can produce inaccurate or hallucinated responses when answering medical questions, making them unreliable for healthcare applications without access to trusted data.

This project explores how Retrieval-Augmented Generation (RAG) can improve the accuracy of AI-generated responses by grounding the model in structured medication data.

---

# Solution

Developed an end-to-end AI chatbot that combines database retrieval with an LLM to answer medication-related questions.

The application:

- Retrieves structured medication information from a MySQL database
- Injects relevant data into the LLM context
- Generates context-aware responses using Llama 3.1
- Maintains conversation history throughout the session
- Provides an intuitive Streamlit interface for user interaction

---

# System Architecture

```
                User
                  │
                  ▼
          Streamlit Interface
                  │
                  ▼
        Medication Selection
                  │
                  ▼
        MySQL Database Query
                  │
                  ▼
      Structured Medication Data
                  │
                  ▼
      Prompt + Retrieved Context
                  │
                  ▼
        Groq API (Llama 3.1)
                  │
                  ▼
        AI Generated Response
```

---

# Retrieval-Augmented Generation (RAG) Workflow

Unlike traditional chatbots, this application retrieves relevant medication information before generating a response.

### Step 1

The user selects a medication from the application.

### Step 2

A SQL query retrieves structured information including:

- Composition
- Uses
- Side Effects
- Manufacturer
- Patient Review Statistics

### Step 3

The retrieved data is injected into the LLM system prompt.

### Step 4

The user question, structured medication data, and conversation history are sent to Llama 3.1 through the Groq API.

### Step 5

The model generates a response grounded in the retrieved database information rather than relying solely on pretrained knowledge.

---

# Features

- AI-powered medication assistant
- Retrieval-Augmented Generation (RAG)
- MySQL database integration
- Streamlit web interface
- Persistent conversation history
- Dynamic medication selection
- Responsive chat interface
- Docker containerization

---

# Technologies

## Programming

- Python

## AI

- Retrieval-Augmented Generation (RAG)
- Llama 3.1
- Prompt Engineering
- Groq API

## Database

- MySQL
- SQL

## Frontend

- Streamlit
- HTML/CSS

## Deployment

- Docker

---

# Repository Structure

```
Drug-Explorer-AI-Chatbot/

│
├── app.py
├── Medicine_Details.csv
├── README.md
└──requirements.txt

```

---

# Results

The completed application successfully demonstrates how Retrieval-Augmented Generation can improve the reliability of healthcare-focused AI systems.

Key outcomes include:

- Reduced hallucinations by grounding responses in structured database records
- Integrated relational database retrieval with a Large Language Model
- Delivered an interactive web application through Streamlit
- Implemented a modular architecture supporting future database expansion and additional medical datasets

---

# Future Improvements

Potential enhancements include:

- Integration with external medical APIs
- Semantic vector search using embeddings
- Citation-aware responses
- Authentication and clinician-specific workflows
- Deployment to a cloud platform
- Support for PDF medical references and clinical guidelines

---

# Skills Demonstrated

- Artificial Intelligence
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- AI Product Development
