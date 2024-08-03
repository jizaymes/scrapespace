import re
import os
import io
from PIL import Image
from time import sleep

from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright, expect
import requests
from rich import print

load_dotenv()
SQUARESPACE_USERNAME = os.getenv('SQUARESPACE_USERNAME')
SQUARESPACE_PASSWORD = os.getenv('SQUARESPACE_PASSWORD')
SQUARESPACE_WEBSITE_URL = os.getenv('SQUARESPACE_WEBSITE_URL')
SQUARESPACE_CDN_BASE_URL = os.getenv('SQUARESPACE_CDN_BASE_URL')
IMAGE_PATH = "images/"

if not SQUARESPACE_USERNAME or not SQUARESPACE_PASSWORD or not SQUARESPACE_WEBSITE_URL or not SQUARESPACE_CDN_BASE_URL:
    raise ValueError("Invalid Configuration .env")


def img_download(link):
    new_fn = str(link.split('/')[-1]).split("?")[0]

    if not new_fn:
        print(f"Couldn't download link. {link}")
        print(f"Error with new fn {new_fn}")
        return False

    print(f"o Downloading {new_fn}..", end=None)
    
    response  = requests.get(link).content 
    image_file = io.BytesIO(response)
    image  = Image.open(image_file)

    with open(IMAGE_PATH + new_fn, "wb") as f:
          image.save(f , "JPEG")
          print("DONE")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(SQUARESPACE_WEBSITE_URL)
              
    # Username
    page.get_by_placeholder("name@example.com").click()
    page.get_by_placeholder("name@example.com").fill(SQUARESPACE_USERNAME)

    # Password
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(SQUARESPACE_PASSWORD)

    # Click login
    page.locator("[data-test=\"login-button\"]").click()

    ## TODO: Error check when this login fails
    ## TODO: Maybe handle social/SSO logins?

    sleep(10)
    page.wait_for_load_state('domcontentloaded')

    all_links = page.query_selector_all('img')
    img_list = []

    for link in all_links:
        if SQUARESPACE_CDN_BASE_URL in link.get_attribute('src'):
            img_list.append(link.get_attribute('src'))

    if img_list:
        for image in img_list:
            img_download(image)

    print("Done!")
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
