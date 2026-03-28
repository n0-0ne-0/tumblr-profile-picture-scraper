# Instalation

First of all install the requirements:

```sh
pip install -r requirements.txt
```

Then run playwright specific setup:

windows:
```sh
playwright install
```

linux:
```sh
playwright install --with-deps
```

# How to use

When you run the script it will use playwright to open and control an automated browser window, downloading all the profile pictures that are loading in the likes tab. It can gather dozens of thousands of pictures in just a few minutes (depending on your internet connection, processing power and other variables)

You can change the target post and the output folder by editing the constants at the top of the script.

<img width="554" height="202" alt="image" src="https://github.com/user-attachments/assets/10d305fc-adf0-4074-9f47-5a7169dd14ea" />

Keep in mind that the post you choose influences directly on the profile pictures you get, if it's an anime post you get more anime profile pictures, if it's a post about pets you get more animal profile picture, etc.
