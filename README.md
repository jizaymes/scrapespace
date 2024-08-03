I made this out of pure rage due to Squarespace not providing a means of exporting the images/asset-library. In my use case, I only had about 50 images, and no video, and used a basic user login. This wont work with out modifications for users with SSO/Social logins. 


To get it to work
copy the env.example to .env

do the normal python virtual env bits

python -m venv .venv

For Linux
`.venv/bin/activate`
or for Windows
`.venv\Scripts\activate.ps1`

then run `python scrapespace.py`
