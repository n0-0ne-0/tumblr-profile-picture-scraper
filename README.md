# tumblr-profile-picture-scraper

What it does:

- Downloads Tumblr profile pictures using the public API.
- You can let it run for as long as you want (likes, posts, whatever the script supports); it will keep fetching until you're satisfied (or until your API keys run out).
- It's easy to modify if you want to do something else with the images besides downloading them.

Some people will say it's not a scraper because it uses the public API — I say I'm scraping the API.

For real: I originally made one that scraped the page with Playwright, but it's much cleaner to just use the public API.

## API keys

Add your API keys either as environment variables or in a `.env` file following the [example](.env.example) layout.

After creating an account on Tumblr and verifying your email, it's easy to create API keys at https://www.tumblr.com/oauth/apps (most fields are optional or accept anything you put in).

You can add as many keys as you want, but after about 20 it stops making a difference. Each key lets you fetch tens of thousands of images.

## Usage

With that out of the way, just install the requirements and run the script.

When you run it you'll be prompted for which blog you want to scrape — make sure to enter the blog's "at" (the shortname that appears after the `@`), not the display name.

```text
<img width="558" height="367" alt="image" src="https://github.com/user-attachments/assets/8bdb3440-23cd-4326-87eb-4540854a8843" />
```

After that you just watch it work until you are satisfied with the number of pictures. You could leave it running until you have all the pictures from all the likes and posts, but normally that's overkill.
