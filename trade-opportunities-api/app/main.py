from fastapi import FastAPI, Header, HTTPException
from app.auth import create_access_token, verify_token
from app.rate_limiter import check_rate_limit
from app.services.search_service import fetch_market_news
from app.services.ai_service import analyze_market
from app.utils.markdown import generate_markdown

app = FastAPI(title="Trade Opportunities API")


@app.post("/login")
def login(username: str):
    token = create_access_token(username)
    return {"access_token": token}


@app.get("/analyze/{sector}")
def analyze_sector(sector: str, authorization: str = Header(...)):
    try:
        verify_token(authorization)
        check_rate_limit(authorization)

        news = fetch_market_news(sector)
        analysis = analyze_market(sector, news)
        report = generate_markdown(analysis)

        return {
            "sector": sector,
            "report_markdown": report
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def health_check():
    return {"status": "API is running"}
