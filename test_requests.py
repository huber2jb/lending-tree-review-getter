import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound


def review_get(url):
    if (url.find('lendingtree.com/reviews') == -1):
        return BadRequest


    reviewText, reviewAuthor, reviewTitle, reviewRating, reviewDate, reviewLoanType = [],[],[],[],[],[]
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='html.parser')
        urlNotFound = soup.select_one(".error404")
        reviewHomePage = soup.select_one(".lenderReviewTitle")
        if urlNotFound != None: return NotFound
        if reviewHomePage != None: return "Given URL is not a lendingtree.com/review URL or returned back to homepage. Please try again."

        for review in soup.findAll('div', attrs={'class':'mainReviews'}):
            reviewTitle.append(review.find('p', attrs={'class':'reviewTitle'}).text.strip())
            reviewText.append(review.find('p', attrs={'class':'reviewText'}).text.strip())
            reviewAuthor.append(review.find('p', attrs={'class':'consumerName'}).text.strip()[:20].strip())
            reviewRating.append(review.find('div', attrs={'class':'numRec'}).text.strip()[1:7])
            reviewDate.append(review.find('p', attrs={'class':'consumerReviewDate'}).text.strip()[12:])
            reviewLoanType.append(review.find('div', attrs={'class':'loanType'}).text.strip())
    except Exception as e:
        return e

    dataJson = {'Reviews': [{'reviewNumber':number+1,
                            'reviewTitle':title, 
                            'reviewText':text,
                            'reviewAuthor':author,
                            'reviewRating':rating,
                            'reviewDate':date,
                            'reviewLoanType':loanType} for number, (title, text, author, rating, date, loanType) in enumerate(zip(reviewTitle, reviewText, reviewAuthor, reviewRating, reviewDate, reviewLoanType))]}

    return 'Passed'

def test_bad_url():
    rv = review_get("https://www.google.com")
    assert rv == BadRequest
    rv = review_get("/")
    assert rv == BadRequest

def test_not_found():
    rv = review_get("https://www.lendingtree.com/reviews/mortgage/reliance-first-capital-llc")
    assert rv == NotFound

def test_homepage():
    rv = review_get("https://www.lendingtree.com/reviews/")
    assert rv == 'Given URL is not a lendingtree.com/review URL or returned back to homepage. Please try again.'

def test_working_url():
    rv = review_get("https://www.lendingtree.com/reviews/mortgage/reliance-first-capital-llc/45102840")
    assert rv == 'Passed'