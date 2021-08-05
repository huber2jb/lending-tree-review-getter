import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound

# Intialize Flask application
app = Flask(__name__)

# Putting anything other than a secured lending tree url will send a BadRequest.
@app.route('/')
def default():
    raise BadRequest

# Given a secure Lending Tree review URL, look through the page to find the reviews.
@app.route('/<path:url>')
def review_get(url):
    # Check to see if it is actually a Lending Tree review URL
    if (url.find('lendingtree.com/reviews') == -1):
        raise BadRequest

    # Intialize arrays for storage of data
    reviewText, reviewAuthor, reviewTitle, reviewRating, reviewDate, reviewLoanType = [],[],[],[],[],[]

    # Wrapped in a try...except to catch any errors might get for timing out and any other network problems
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='html.parser')     # Used to parse the retrived html
        urlNotFound = soup.select_one(".error404")                      # Check to see if the URL led to the 404 page
        reviewHomePage = soup.select_one(".lenderReviewTitle")          # Check to see if the URL led back to review homepage
        if urlNotFound != None: raise NotFound
        if reviewHomePage != None: return "Given URL is not a lendingtree.com/review URL or returned back to homepage. Please try again."

        # Parsing through the html to find the desired data and add it to the correct array
        for review in soup.findAll('div', attrs={'class':'mainReviews'}):
            reviewTitle.append(review.find('p', attrs={'class':'reviewTitle'}).text.strip())
            reviewText.append(review.find('p', attrs={'class':'reviewText'}).text.strip())
            reviewAuthor.append(review.find('p', attrs={'class':'consumerName'}).text.strip()[:20].strip())
            reviewRating.append(review.find('div', attrs={'class':'numRec'}).text.strip()[1:7])
            reviewDate.append(review.find('p', attrs={'class':'consumerReviewDate'}).text.strip()[12:])
            reviewLoanType.append(review.find('div', attrs={'class':'loanType'}).text.strip())
    except Exception as e:
        raise e

    # Turning each review into a dictionary for easier transfer to json
    dataJson = {'Reviews': [{'reviewNumber':number+1,
                            'reviewTitle':title, 
                            'reviewText':text,
                            'reviewAuthor':author,
                            'reviewRating':rating,
                            'reviewDate':date,
                            'reviewLoanType':loanType} for number, (title, text, author, rating, date, loanType) in enumerate(zip(reviewTitle, reviewText, reviewAuthor, reviewRating, reviewDate, reviewLoanType))]}

    # Presenting on the page the json reviews found on the html
    return jsonify(dataJson)

# If an error occured, show the error to the user
@app.errorhandler(Exception)
def handle_http_exception(e):
    return e