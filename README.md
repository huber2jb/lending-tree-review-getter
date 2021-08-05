# lending-tree-review-getter
Goes to the LendingTree review website and returns a JSON list of reviews for a specific url.

## Package Requirements
- bs4 - BeautifulSoup
- flask - Flask
- Uses Python 3.8.11

## Running the API
- Create your virtual environment and install needed packages. I used *Anaconda* for my environment and package manager but *virtualenv* and *pip* should work just fine
- Then run `py -m flask run` or `python -m flask run`. Whichever works for how you have python installed.
- The API runs on the default for Flask - *127.0.0.1:5000*
- Just put wanted https://lendingtree.com/reviews URL to receive the reviews on that page
- If you just go to the 127.0.0.1:5000 without the URL it should return a BadRequest on the screen
