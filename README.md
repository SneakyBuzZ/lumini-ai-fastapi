# LUMINI FASTAPI SERVER

This repository contains the backend server for the Lumini application specific to RAG, built using FastAPI. It provides APIs for various functionalities including user authentication, code summarization, and more.

## Features

- User Authentication
- Code Summarization using AI models
- CORS Middleware for handling cross-origin requests
- Database integration with PostgreSQL
- Environment configuration management

## Setup Instructions

1. Clone the repository:
   ```bash
    git clone <repo-url>
    cd lumini-fastapi
   ```
2. Create a virtual environment and activate it:
   ```bash
    uv venv .venv
    source .venv/Scripts/activate
   ```
3. Install the required dependencies:
   ```bash
    make install
   ```
4. Set up environment variables:

   - Create a `.env` file in the root directory.
   - Add the necessary environment variables as shown in the `.env.example` file.

5. Run the FastAPI server:
   ```bash
    make start
   ```
