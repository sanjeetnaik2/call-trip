from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )

def scrape_page(url: str) -> dict:
    driver = create_driver()
    try:
        driver.get(url)
        # TODO: add your waits and scraping logic here
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
