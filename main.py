from fastapi import FastAPI, Depends, HTTPException, Path, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
import google.generativeai as genai
import httpx
import os
import time

# ---------------- ENV ----------------

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

# ---------------- APP ----------------

app = FastAPI(title="AI Trade Opportunities")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# templates
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

sessions = {}
rate_store = {}

RATE_LIMIT = 5
RATE_WINDOW = 60

# ---------------- MODELS ----------------

class AnalysisResponse(BaseModel):
    sector: str
    report_markdown: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------------- TOKEN ----------------

def create_token(username: str):

    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "exp": expire
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    sessions[username] = {"created": time.time()}
    rate_store[username] = {"tokens": RATE_LIMIT, "time": time.time()}

    return token


# ---------------- AUTH ----------------

async def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------- RATE LIMIT ----------------

def check_rate(user):

    bucket = rate_store[user]

    now = time.time()

    if now - bucket["time"] > RATE_WINDOW:
        bucket["tokens"] = RATE_LIMIT
        bucket["time"] = now

    if bucket["tokens"] <= 0:
        raise HTTPException(429, "Rate limit exceeded")

    bucket["tokens"] -= 1


# ---------------- MARKET DATA ----------------

async def fetch_market_news(sector):

    url = "https://api.duckduckgo.com/"

    params = {
        "q": f"{sector} sector india market news",
        "format": "json"
    }

    async with httpx.AsyncClient() as client:

        try:
            response = await client.get(url, params=params)
            data = response.json()

            return data.get("AbstractText", "No data available")

        except:
            return "Market data unavailable"


# ---------------- GEMINI ----------------

def analyze_with_gemini(sector, news):

    prompt = f"""
Analyze the {sector} sector in India.

Market Data:
{news}

Provide:
1. Market Trends
2. Trade Opportunities
3. Risks and Challenges
4. Investment Outlook
"""

    try:

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text
        else:
            return "AI response format unexpected."

    except Exception as e:
        return f"AI analysis unavailable. Error: {str(e)}"


# ---------------- REPORT ----------------

def generate_report(sector, analysis):

    date = datetime.utcnow().strftime("%Y-%m-%d")

    return f"""
# Market Analysis Report

## Sector
{sector}

## Date
{date}

## AI Market Analysis
{analysis}

## Disclaimer
AI generated insights. Not financial advice.
"""


# ---------------- WEBSITE ----------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------- AUTH ROUTES ----------------

@app.get("/guest", response_model=TokenResponse)
async def guest():

    username = f"guest_{int(time.time())}"

    token = create_token(username)

    return {"access_token": token}


@app.post("/login", response_model=TokenResponse)
async def login():

    username = "user"

    token = create_token(username)

    return {"access_token": token}


# ---------------- MAIN API ----------------

@app.get("/analyze/{sector}", response_model=AnalysisResponse)
async def analyze_sector(
    sector: str = Path(..., min_length=2, max_length=50),
    user: str = Depends(get_current_user)
):

    check_rate(user)

    news = await fetch_market_news(sector)

    analysis = analyze_with_gemini(sector, news)

    report = generate_report(sector, analysis)

    return {
        "sector": sector,
        "report_markdown": report
    }
