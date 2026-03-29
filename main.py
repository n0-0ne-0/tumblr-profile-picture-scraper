import os
import time
from playwright.sync_api import sync_playwright, Response
from PIL import Image
from io import BytesIO

URL = "https://www.tumblr.com/importantdogimages/780782959388131328"
OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def scroll_down():
    global page
    while True:

        prev_height = page.evaluate(
            "document.querySelector('.rEGcu').scrollHeight"
        )

        page.evaluate(
            """
            const el = document.querySelector('.rEGcu');
            el.scrollTop = el.scrollHeight;
            """
        )

        end_time = time.time() + 5
        while time.time() < end_time:
            if page.evaluate("document.querySelector('.rEGcu').scrollHeight") > prev_height:
                break
        else:
            print("end")
            break

n = 1
def save_image(content):
    global n
    name = str(n) + ".png"
    path = os.path.join(OUTPUT_FOLDER, name)
    n+=1

    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(content)

    return path

def on_response(response: Response):
    request = response.request

    if request.method != "GET":
        return
    url = response.url.lower()
    if not url.endswith((".png", ".jpg", ".jpeg", ".webp", ".pnj", ".img")):
        return
    if not response.ok:
        return
    
    content = response.body()
    img = Image.open(BytesIO(content))
    if img.size == (64, 64) or img.size == (48, 48):
        save_image(content)

def scrape_images():
    global page
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(URL, wait_until="domcontentloaded")
        print("loaded")
        page.wait_for_selector("#likes", state="visible")
        page.on("response", on_response)
        page.click("#likes")
        print("starting")
        scroll_down()

        browser.close()

scrape_images()
