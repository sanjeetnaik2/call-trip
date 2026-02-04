from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os

app = FastAPI()

CHROMIUM_BINARY = os.getenv("CHROMIUM_BINARY", "/usr/bin/chromium")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = CHROMIUM_BINARY

    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

def scrape_page(url: str) -> dict:
    driver = create_driver()
    try:
        driver.get(url)
        title = driver.title
        return {"title": title, "url": url}
    finally:
        driver.quit()

@app.get("/scrape")
def scrape_endpoint(url: str):
    try:
        data = scrape_page(url)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
