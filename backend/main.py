import logging
import sentry_sdk
from fastapi import FastAPI, status, Response, HTTPException

from backend.settings import PROJECT_NAME
from backend.utils import scoring_function
from backend.schemas import Account, Result

sentry_sdk.init(
    dsn="https://79787ff14c5a49759a343d153cc70904@o4504587752374272.ingest.sentry.io/4504587756240896",
    traces_sample_rate=1.0,
)

app = FastAPI()
logger = logging.getLogger(PROJECT_NAME)


@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "Welcome to the scoring system! "
                       "Send POST request to /scoring URL with a corresponding data"}


@app.post("/scoring", status_code=status.HTTP_202_ACCEPTED, response_model=Result)
def post_scoring(account: Account):
    return scoring_function(account=account)