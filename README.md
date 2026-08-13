# tumblr-profile-picture-scraper

What it does:

* Downloads Tumblr profile pictures using the public API.

* You can let it run for as long as you want (likes, posts, whatever the script supports) and it will keep fetching until you're satisfied (or until your API keys run out).

* It's easy to modify if you want to do something else with the scraped images besides downloading it

some people will say it's not a scraper because it uses the public API, i say i am scraping the API

for real now, i had made one that actually scraped the page with playwright, but it's so much cleaner to just use the public API

## API keys
You need to add your API keys either as environment variables or in a .env file following the [example](.env.example) layout.

After creating an account on tumblr and verifying the email it's easy to create many API keys at https://www.tumblr.com/oauth/apps (most of the field are optional or accept anything you put in, besides the URL ones where it needs to start with "https://". I won't make a step by step tutorial but you can figure it out, it's easy)

you can put as many keys as you want but after like 20 it stops making a difference, and each one will give you tens of thousands of images

## Usage
with this out of the way, just install the requirements and run the file.

when you run the file you will have to input which blog you want to scrape, it's important to notice what you need to insert is the at, not the big name

<img width="558" height="367" alt="image" src="https://github.com/user-attachments/assets/8bdb3440-23cd-4326-87eb-4540854a8843" />

after that you just watch it work until you are satisfied with the amount of pictures, you could leave it running until you have all the pictures of all the likes of all the posts, but normally that would be way too many. To stop it just use the keyboard interrupt
