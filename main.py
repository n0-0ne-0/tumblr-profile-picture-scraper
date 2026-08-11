import time
import asyncio
from curl_cffi.requests import AsyncSession
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()
api_keys = os.getenv("TUMBLR_API_KEYS").split()
if not api_keys:
    raise ValueError("Please provide API keys in the environment variables")

api_key = api_keys.pop(0)
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


api_key_lock = None
fetch_ids_semaphore = None
fetch_image_semaphore = None
semaphore_limit = 400


async def change_api_key(failed_key):
    global api_keys, api_key, api_key_lock
    if api_key_lock is None:
        api_key_lock = asyncio.Lock()

    async with api_key_lock:
        if api_key != failed_key:
            return
        if not api_keys:
            raise ValueError("All API keys have been exhausted")

        api_key = api_keys.pop(0)
        print("Switching API key to:", api_key)


async def handle_429_err(msg, failed_key):
    err_code = msg["errors"][0]["code"]
    if err_code == 0:
        await change_api_key(failed_key)
    elif err_code == 5029:
        await asyncio.sleep(3)


async def fetch_ids(blog_name, offset):
    global fetch_ids_semaphore
    if fetch_ids_semaphore is None:
        fetch_ids_semaphore = asyncio.Semaphore(semaphore_limit)

    async with fetch_ids_semaphore:
        async with AsyncSession() as session:
            try:
                while True:
                    current_key = api_key
                    url = f"https://api.tumblr.com/v2/blog/{blog_name}/posts?api_key={current_key}&offset={offset}&limit=20"
                    response = await session.get(url)

                    if response.status_code == 200:
                        data = response.json()
                        posts = data.get("response", {}).get("posts", [])
                        return [post["id"] for post in posts]
                    elif response.status_code == 429:
                        if response.headers.get("Content-Type") == "text/html":
                            await asyncio.sleep(1)
                        else:
                            msg = response.json()
                            await handle_429_err(msg, current_key)
                        continue
                    else:
                        print(f"Error at offset {offset}: {response.status_code}")
                        return []
            except ValueError:
                raise
            except Exception as e:
                print(f"Error fetching offset {offset}: {e}. Retrying...")
                await asyncio.sleep(2)


async def get_post_ids(blog_name):
    post_ids = set()

    async with AsyncSession() as session:
        while True:
            current_key = api_key
            url: str = (
                f"https://api.tumblr.com/v2/blog/{blog_name}/posts?api_key={current_key}&offset=0&limit=20"
            )
            response = await session.get(url)
            if response.status_code == 429:
                msg = response.json()
                await handle_429_err(msg, current_key)
            elif response.status_code != 200:
                print(f"An API error occurred: {response.status_code}")
            else:
                break

        data = response.json()["response"]

        if isinstance(data, int):
            raise ValueError(f"An API error occurred: {data}")
        total_posts = data["total_posts"]
        print(f"Total posts from API: {total_posts}")

    post_ids.update(post["id"] for post in data["posts"])

    offsets = range(20, total_posts, 20)
    print(f"Starting {len(offsets)} independent requests")

    tasks = [fetch_ids(blog_name, offset) for offset in offsets]
    results = await asyncio.gather(*tasks)

    for result in results:
        post_ids.update(result)

    return post_ids


def save_image(content: bytes, name: str):
    """Save image to disk. Should be called via asyncio.to_thread to prevent blocking."""
    img = Image.open(BytesIO(content))
    img.save(f"{OUTPUT_FOLDER}/{name}.png")


async def fetch_image(url: str, name: str):
    """
    Downloads the image and converts it to a PIL object using threads.
    """
    global fetch_image_semaphore
    if fetch_image_semaphore is None:
        fetch_image_semaphore = asyncio.Semaphore(semaphore_limit)

    async with fetch_image_semaphore:
        async with AsyncSession() as session:
            try:
                while True:
                    response = await session.get(url)

                    if response.status_code == 429:
                        if response.headers.get("Content-Type") == "text/html":
                            await asyncio.sleep(1)
                        else:
                            msg = response.json()
                            await handle_429_err(msg, api_key)
                        continue
                    elif response.status_code != 200:
                        print(
                            f"Error downloading image for {name}: Status {response.status_code}"
                        )
                        break

                    content = response.content
                    await asyncio.to_thread(save_image, content, name)
                    break

            except Exception as e:
                print(f"Error downloading image for {name}: {e}. Retrying...")
                await asyncio.sleep(1)


async def process_post_likes(blog_name: str, post_id: str):
    before_timestamp = str(int(time.time()))
    image_tasks = []

    async with AsyncSession() as session:
        while True:
            current_key = api_key
            url = f"https://api.tumblr.com/v2/blog/{blog_name}/notes?api_key={current_key}&mode=likes&id={post_id}&before_timestamp={before_timestamp}"

            try:
                response = await session.get(url)
            except Exception as e:
                print(f"Error fetching notes for post {post_id}: {e}. Retrying...")
                await asyncio.sleep(0.5)
                continue

            if response.status_code == 429:
                msg = response.json()
                await handle_429_err(msg, current_key)
                continue
            elif response.status_code != 200:
                print(f"Tumblr API error: {response.status_code}")
                return

            response_data = response.json().get("response", {})
            notes = response_data.get("notes", [])

            if not notes:
                break

            for note in notes:
                img_url = note["avatar_url"]["64"]
                name = note["blog_name"]
                image_tasks.append(asyncio.create_task(fetch_image(img_url, name)))

            links = response_data.get("_links", {})
            next_link = links.get("next")

            if next_link and "query_params" in next_link:
                before_timestamp = next_link["query_params"].get("before_timestamp")
                if not before_timestamp:
                    break
            else:
                break

        if image_tasks:
            await asyncio.gather(*image_tasks)


async def main():
    blog_name = input("Enter the blog name: ")

    start = time.time()
    post_ids = await get_post_ids(blog_name)

    print(f"Total posts found: {len(post_ids)}")

    for post_id in post_ids:
        print("Processing post", post_id)
        await process_post_likes(blog_name, post_id)

    print(f"Total execution time: {time.time() - start:.2f} seconds")
    input("Press Enter to exit...")


if __name__ == "__main__":
    asyncio.run(main())
