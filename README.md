# tumblr-profile-picture-scraper

some people will say it's not a scraper because it uses the public API, i say i am scraping the API

for real now, i had made one that actually scraped the page with playwright, but it's so much cleaner to just use the public API

## Usage

first you need to add your API keys either as environment variables or in a .env file, after creating an account on tumblr and verifying the email you can easily create many API keys at https://www.tumblr.com/oauth/apps (most of the field are optional or accept anything you put in, besides the URL ones where it needs to start with "https://". I won't make a step by step tutorial but you can figure it out, it's easy)

you can put as many keys as you want but after like 20 it stops making a difference

with this out of the way, just install the requirements and run the file.

when you run the file you will have to input which blog you want to scrape, it's important to notice what you need to insert is the at, not the visible name

<img width="558" height="367" alt="image" src="https://github.com/user-attachments/assets/8bdb3440-23cd-4326-87eb-4540854a8843" />

after that you just watch it work until you are satisfied with the amount of pictures, you could leave it running until you have all the pictures of all the likes of all the posts, but normally that would be way too many. To stop it just use the keyboard interrupt
