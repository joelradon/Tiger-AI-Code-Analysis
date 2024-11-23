
# README: Setup and Use Instructions for "Tiger AI Code Analysis" Python App

## Overview

The "Tiger AI Code Analysis" application allows you to analyze and ask questions about your entire codebase using OpenAI and Pinecone. By running this script, you can store your codebase embeddings in Pinecone and then interact with the codebase using a custom GPT model ("gpt-4o-mini"), which provides affordable and quick code analysis.

The app is designed to help you extract insights from your codebase by querying it directly, enabling detailed explanations of code functionality.

### Prerequisites

Before getting started, ensure you have the following accounts set up:

1. **Pinecone Account (Free Tier)**
   - Go to [Pinecone's website](https://www.pinecone.io/) and sign up for a free account.
   - Create a project and retrieve your Pinecone API key.

2. **OpenAI API Key (Free Tier Available)**
   - Visit [OpenAI](https://platform.openai.com/) to sign up for an API key (you can use the free tier for testing purposes).
   - Once logged in, navigate to the API section to generate your key.

---

## Step-by-Step Guide

### Step 1: Clone or Download the Code Repository

1. Clone or download the code repository containing the Python app.
   
   ```bash
   git clone <repository_url>
   ```

2. After cloning, navigate to the folder where the app resides.

### Step 2: Prepare Code Files

1. **Copy your Codebase**:
   
   - Save the following script depending on your OS (Linux or Windows) `ListAndPrintFileContents.sh` or `ListAndPrintFileContents.ps1`
   
   

3. **Run the Copy Script Script**:

   Run the script to process your codebase:
   
   ```bash
   ./ListAndPrintFileContents.sh
   ```

   The script will:
   - Prompt you for the source directory (where your code is located).
   - Prompt you for the destination directory (where the processed file will be saved).
   - It will then process all files in the source directory, excluding `README.md`, and save their contents to `processed_code_output.txt` in the destination directory.

---

### Step 3: Set Up the Python Environment

1. **Install Required Python Packages**:

   - Create and activate a Python virtual environment:
   
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
     ```

   - Install dependencies using `pip`:
   
     ```bash
     pip install openai pinecone-client
     ```

2. **Set Up Environment Variables**:
   
   - Create a `.env` file in the root directory of your project.
   - Add your OpenAI and Pinecone API keys in the following format:

     ```bash
     OPENAI_API_KEY=your_openai_api_key
     PINECONE_API_KEY=your_pinecone_api_key
     ```

### Step 4: Run the Python Script

1. **Run the Script**:

   Navigate to the directory where the `python` app script resides. Run the Python script:

   ```bash
   python app.py
   ```

2. The script will:
   - Load the `processed_code_output.txt` file.
   - Split the code into smaller chunks for processing.
   - Generate embeddings for each code chunk using OpenAI.
   - Store the embeddings in Pinecone for fast retrieval.

### Step 5: Query Your Codebase

1. **Interact with the Codebase**:

   After storing the code embeddings in Pinecone, you can interact with your codebase by querying it with natural language prompts.

   - Once the script finishes processing, you will be prompted to enter a custom query. You can ask questions like:

     - "What does this function do?"
     - "Explain the logic behind this code snippet."
     - "How does this class work?"

   - The system will search for similar code snippets in the database and provide a detailed explanation using the GPT model (`gpt-4o-mini`).

### Step 6: View the Response

1. **View Responses in Markdown**:

   - The responses will be saved to a `.md` file (e.g., `gpt_response.md`).
   - Open the `.md` file in a markdown viewer (e.g., **Visual Studio Code** with a markdown extension) to view the results.

### Step 7: Repeating Queries

You can repeat the query process as many times as necessary by interacting with the Python script and asking new questions based on your codebase.

---

## Example of Running the Application

### 1. Copy Your Codebase
   - Run the Bash script to process the code.

### 2. Run the Python App
   ```bash
   python app.py
   ```

### 3. Enter a Query:
   ```
   Enter your prompt: What does this function do?
   ```

### 4. View the Result
   Open `gpt_response.md` to see the generated response.

---

## Advantages of Using Tiger AI Code Analysis

1. **Affordable GPT-4 Model**: The app utilizes the `gpt-4o-mini` model, which is significantly more affordable for smaller-scale tasks.
2. **Quick Responses**: By splitting the code into chunks and using Pinecone for fast searches, queries are answered quickly and efficiently.
3. **Cost-Effective**: Suitable for analyzing your codebase without excessive cost, thanks to the lightweight `gpt-4o-mini`.

---

## Troubleshooting

- **Missing API Key Error**: Ensure you have set your `OPENAI_API_KEY` and `PINECONE_API_KEY` in the `.env` file.
- **Pinecone Connection Issues**: Make sure you have created a Pinecone project and used the correct region and API key.

---

## Conclusion

With this Python application, you can interactively query and analyze your codebase using OpenAI and Pinecone. It provides affordable and detailed explanations of your code, which can help streamline development and debugging processes.

---
