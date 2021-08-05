import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Intial URL retrival and response check
# response = requests.get("https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183")
# soup = BeautifulSoup(response.text, features='lxml')
# totalReviews = soup.select_one('b.hidden-xs').text[:-8]


@app.route('/<path:url>')
def review_get(url):
    reviewText, reviewAuthor, reviewTitle, reviewRating, reviewDate, reviewLoanType = [],[],[],[],[],[]
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='lxml')
        for review in soup.findAll('div', attrs={'class':'mainReviews'}):
            reviewTitle.append(review.find('p', attrs={'class':'reviewTitle'}).text.strip())
            reviewText.append(review.find('p', attrs={'class':'reviewText'}).text.strip())
            reviewAuthor.append(review.find('p', attrs={'class':'consumerName'}).text.strip()[:20].strip())
            reviewRating.append(review.find('div', attrs={'class':'numRec'}).text.strip()[1:7])
            reviewDate.append(review.find('p', attrs={'class':'consumerReviewDate'}).text.strip()[12:])
            reviewLoanType.append(review.find('div', attrs={'class':'loanType'}).text.strip())
    except Exception as e:
        print(e)

    dataJson = {'Reviews': [{'reviewNumber':number+1,
                            'reviewTitle':title, 
                            'reviewText':text,
                            'reviewAuthor':author,
                            'reviewRating':rating,
                            'reviewDate':date,
                            'reviewLoanType':loanType} for number, (title, text, author, rating, date, loanType) in enumerate(zip(reviewTitle, reviewText, reviewAuthor, reviewRating, reviewDate, reviewLoanType))]}

    return json.dumps(dataJson, indent=4)