# AI Trade Opportunities API
### Hosted at https://appscrip-8pjm.onrender.com

## Overview
AI Trade Opportunities is a full-stack application that analyzes a given industry sector and generates an AI-powered market analysis report.

The system uses a **FastAPI backend**, integrates with **Google Gemini AI**, and provides a simple **web interface** for users to interact with the API.

Users can enter a sector (e.g., technology, pharmaceuticals, finance) and receive a structured analysis including market trends, trade opportunities, and potential risks.

Note : This is just a backend server not end to end web application.
---

# Features

- AI-generated market analysis
- FastAPI REST API
- JWT authentication
- Rate limiting
- Gemini AI integration
- Market data via DuckDuckGo API
- Swagger API documentation
- Simple web frontend

---

# Technologies Used

## Backend
- Python
- FastAPI
- Uvicorn
- python-jose (JWT authentication)
- HTTPX
- Google Generative AI (Gemini)

## Frontend
- HTML
- CSS
- JavaScript

## External APIs
- Google Gemini AI
- DuckDuckGo Instant Answer API

---

# Project Architecture
Frontend (HTML + JS)
↓
FastAPI Backend
↓
External APIs
├── DuckDuckGo (market data)
└── Gemini AI (analysis generation)


---

# Project Structure
project/
│
├── main.py
├── requirements.txt
├── .env
│
├── frontend/
│ ├── index.html
│ ├── script.js
│ └── style.css
│
└── README.md


---

# Steps Followed to Build the Project

1. Created FastAPI backend.
2. Implemented REST endpoints.
3. Added JWT authentication.
4. Implemented session-based rate limiting.
5. Integrated DuckDuckGo API for market context.
6. Connected Google Gemini AI for analysis generation.
7. Generated Markdown reports from AI responses.
8. Built frontend using HTML, CSS, and JavaScript.
9. Connected frontend with backend via fetch API.
10. Enabled CORS for browser requests.
11. Tested endpoints using Swagger UI.

---

# Setup Instructions
this is local deployment i have deployed it on Render platform too.
to test and check out the deployment u can skip to step 5

## 1. Clone Repository

```bash
git clone https://github.com/PRATIKSHETAKE/AppScrip
cd AppScrip
```

## 2. Start Virtual Enviournment

if not created run

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```


## 3. Install Neccesary Libraries from requirements.txt

You can use following command
```bash
pip install -r requirements.txt
```

## 4. Setup Enviournment variable

This part contains your Gemini API key

I have not given my api key in the .env file due to security issues and billing issues.

To create one use following steps
1. go to https://aistudio.google.com/
2. create new key
3. setup your key name
4. select app or create a new app
5. and copy api key string

then edit ur .env file.

which should have something like this
SECRET_KEY=<your_secret_key>
GEMINI_API_KEY=<your_api_key_string>

## 5. run the fast api

before running the server check the available models at https://ai.google.dev/gemini-api/docs/models
i have used "gemini-2.5-flash"

```bash
uvicorn main:app --reload
```

then ur server will run at(default)
```bash
http://127.0.0.1:8000
```

## 6. Testing the FastAPI
1. Open Swagger documentation.
   ```bash
   http://127.0.0.1:8000/docs
   ```
2. Under /guest select click try it out
3. then click execute
4. now in server response there is response block which is in json format select the all text in the inverted commas this is ur access token valid for only 30 sec.
5. now at right top of the website you will see the authorize button.
6. in password paste the following text
   ```bash
   Bearer <text_copied>
   ```
7. Then authorize n close the window.
8. now under /analyze/{sextor} click test it out
9. there is the sector input box with technology placeholder type the sector you want eg. technology, education pharmaceutical, etc.
10. now in response there is json file with 2 fields sector and report markdown.
There is another branch with simple end to end website
If there is any error just comment i will look into it.
