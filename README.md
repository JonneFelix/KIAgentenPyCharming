# KIAgentenPyCharming -- PDF Chat Application

## Table of Contents

1. [Introduction/Overview](#introductionoverview)
2. [What's New?](#whats-new)
3. [Features](#features)
4. [System Requirements](#system-requirements)
5. [LLM Models](#llm-models)
6. [Packages Installation](#packages-installation)
7. [Deployment (Starting the Server)](#deployment-starting-the-server)
8. [How to Use?](#how-to-use)
    - [Landing Page](#landing-page)
    - [Chat Page](#chat-page)
9. [JSON Structure](#json-structure)
10. [Common Issues](#common-issues)
11. [Contributors](#contributors)
12. [Roles](#roles)
13. [Use AI Assistants](#use-ai-assistants)
14. [Project Files](#project-files)
15. [Environment Variables](#environment-variables)
16. [API Details](#api-details)
17. [Screenshots/Demo](#screenshotsdemo)
18. [Acknowledgements](#acknowledgements)

## Introduction/Overview

Welcome to the PDF Chat Application! This project was developed as part of a university course in Business Informatics by the group KIAgentenPyCharming. The application allows users to upload a PDF file (specifically sustainability reports) and then ask questions about the content of the PDF to a chatbot. The application uses Flask for the backend and a frontend composed of HTML, CSS, and JavaScript.

One of the key features of this application is the ability to download a JSON file containing extracted information from the uploaded PDF. This JSON file includes various details such as CO2 emissions, NOX levels, number of electric vehicles, and more, making it easier to analyze and utilize the data from sustainability reports.

## What's New?

- Introduction of an interactive chat interface for PDF documents.
- Support for multiple LLM models.
- User-friendly interface for PDF upload and chat interaction.
- JSON download feature to extract information from sustainability reports.
- Chunking option to select the size of PDF chunks.
- Toggle list to switch between LLM models on the chat page.

## Features

- **PDF Upload:** Upload a PDF file to get started.
- **Chat Functionality:** Ask questions about the PDF content through a user-friendly chat interface.
- **Model Selection:** Choose from various LLM models for processing requests.
- **PDF Display:** View the uploaded PDF alongside the chat window.
- **JSON Download:** Download logs in a JSON file containing extracted information from the uploaded PDF.
- **Chunking Option:** Select the chunk size for processing the PDF (500, 400, 300, or 200).
- **LLM Model Toggle:** Switch between different LLM models on the chat page.

## System Requirements

- Python 3.7 or higher
- Flask 1.1.2 or higher
- Modern web browsers (Chrome, Firefox, Edge)

## LLM Models

- qwen1.5-72b-chat
- intel-neural-chat-7b
- mixtral-8x7b-instruct
- meta-llama-3-70b-instruct

## Packages Installation

Ensure you have the necessary packages installed. Run the following command:

```bash
pip install -r requirements.txt

```

## Deployment (Starting the Server)

To start the server, use the following command:

```bash
python main.py

```

The server will run on `http://127.0.0.1:5004`.

## How to Use?

### Landing Page

1. **Visit the Homepage:** Navigate to the application's homepage.
2. **Upload PDF:** Upload a PDF file via the homepage.
3. **Select Chunk Size:** Choose the chunk size (500, 400, 300, or 200) for processing the PDF.
4. **Proceed to Chat:** Click on the "Proceed to Chat" button to be redirected to the chat page.

### Chat Page

1. **View PDF and Chat:** The chat page displays the uploaded PDF on the right side and the chat window on the left side.
2. **Ask Questions:** Enter your questions in the chat window about the content of the PDF.
3. **Switch LLM Models:** Use the toggle list in the upper right corner to switch between different LLM models.
4. **Download JSON:** Click on the "Download JSON" button to download a JSON file containing extracted information from the uploaded PDF.

### JSON Structure

The downloaded JSON file will contain the following information about the uploaded sustainability report:

```json
{
    "name": "NAME_OF_THE_PDF",
    "CO2": "...",
    "NOX": "...",
    "Number_of_Electric_Vehicles": "...",
    "Impact": "...",
    "Risks": "...",
    "Opportunities": "...",
    "Strategy": "...",
    "Actions": "...",
    "Adopted_policies": "...",
    "Targets": "..."
}

```

## Common Issues

- **Error Uploading PDF:** Ensure the file is in PDF format.
- **No Response from Chatbot:** Check your internet connection and ensure the server is running.
- **PDF Text Not Recognized:** PDFs that contain images of text (e.g., scanned documents) cannot have their text extracted and recognized by the chatbot.

## Contributors

- **Jakob Strade:** Frontend
- **Alexander Kunn:** Backend / LLM / Presentation Design
- **Timo Heyn:** Backend / RAG / Chunk Size
- **Leo Rogalla:** Frontend
- **Oliver Petersen:** Backend / LLM / Download JSON
- **Jonne Schwegmann:** Backend / LLM

## Roles

- **Project Lead:** Responsible for overall project management.
- **Backend Developer:** Develops server-side logic.
- **Frontend Developer:** Develops the user interface.

## Use AI Assistants

- **Chat-GPT:** Assisted with development and documentation.
- **Github CoPilot:** Helps with code completion and generation.

## Project Files

- **main.py:** Contains the Flask application and API endpoints.
- **pdftest.py:** PDF processing logic.
- **home.html:** Homepage of the application.
- **chat.html:** Chat page of the application.
- **_header.html, _footer.html:** Header and footer parts of the pages.
- **upload.js, chat.js, script.js, download-jason.js:** JavaScript files for various interactions on the website.
- **styles.css, landing.css, upload.css, chat.css:** CSS files for styling the application.

## Environment Variables

Set the following environment variables to configure the application:

- `FLASK_ENV`: Set to `development` for development mode.
- `SECRET_KEY`: A secret key for session management.
- `API_KEY`: The API key for the chatbot service.

## API Details

The application provides the following API endpoints:

- **`POST /api/chat`**: Accepts a message and returns a response from the chatbot.
- **`POST /upload`**: Handles PDF file uploads.
- **`GET /download-json`**: Provides a JSON file containing extracted information from the uploaded PDF.

## Screenshots/Demo

Here an exemplary illustration of the Landing Page:
<img width="775" alt="Screenshot 2024-07-04 at 13 58 24" src="https://github.com/JonneFelix/KIAgentenPyCharming/assets/165815670/617e9854-22d5-4abe-a8d3-9ea3d51fcad3">


Here an exemplary illustration of the Chatbot Page:
![Screenshot 2024-07-04 at 15 48 20](https://github.com/JonneFelix/KIAgentenPyCharming/assets/165815670/0025dea0-9be5-4d9e-ae7c-4894a1be06b6)

## Acknowledgements

- Flask: A lightweight WSGI web application framework.
- Bootstrap: For responsive UI components.
- OpenAI: For the Chat-GPT assistance.

If you have any further questions, do not hesitate to contact us!
