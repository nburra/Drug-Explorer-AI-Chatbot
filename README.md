# Drug-Explorer-AI-Chatbot
The Drug Explorer AI Chatbot is an interactive AI-powered web application that implements a Retrieval-Augmented Generation (RAG) workflow to answer questions, provide expanded explanations, and display metrics about specific drugs stored in a database. The application retrieves relevant drug information and uses an LLM to generate accurate, context-based responses.

## RAG Workflow
The user selects a specific medication from a drop down list and types in a prompt. Information about this specific medication is retrieved using SQL queries. This structured data is then injected into the system message passed to the LLM. The user prompt is appended to the retrieved data and chat history. The LLM generates a response that relies explicitly on the structured data. Responses and prompts are logged to a chat history.

## Tools
The application is built using Streamlit for a dynamic UI, and a MySQL database to house structured data about medications. The entire application is containerized with Docker to support consistent deployment. GroqAPI is used to connect to the llama-3.1-8b-instant LLM. CSS styling is implemented to create a clean, chat-style layout, improving readability and UX.

## Use
The Drug Explorer Chatbot is intended for healthcare professionals and patients seeking reliable and quick information about medications. By using a RAG approach, the chatbot bases its responses from the structured database, reducing hallucinations and improving accuracy. The chatbot can be incorporated into clinical workflows as a decision-support tool and help patients better understand a specific drug’s uses, side effects, and overall profile.
