from enum import Enum

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import uvicorn

from selenium_parser import RIANewsSeleniumParser
from bs4_parser import RiaNewsBS4Parser


app = FastAPI()


class MethodName(str, Enum):
    selenium = "selenium"
    requests = "requests"


@app.get("/run_parser")
def run_parser(
    method: MethodName = MethodName.selenium
) -> list[dict[str, str]]:
    if method == MethodName.selenium:
        news = RIANewsSeleniumParser()._parse_news()
    elif method == MethodName.requests:
        news = RiaNewsBS4Parser()._parse_news()
    if not news:
        raise HTTPException(404, 'News not found')
    return news


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
