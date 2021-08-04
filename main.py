import requests
from bs4 import BeautifulSoup
import json
response = requests.get("https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183")
soup = BeautifulSoup(response.text, features='lxml')
reviewText, reviewAuthor, reviewTitle, reviewRating, reviewDate = [],[],[],[],[]
reviewLoanType, reviewType = [],[]
totalReviews = soup.select_one('b.hidden-xs').text
print(totalReviews.find('Reviews'))
for review in soup.findAll('div', attrs={'class':'mainReviews'}):
    reviewTitle.append(review.find('p', attrs={'class':'reviewTitle'}).text.strip())
    reviewText.append(review.find('p', attrs={'class':'reviewText'}).text.strip())
    reviewAuthor.append(review.find('p', attrs={'class':'consumerName'}).text.strip()[:20].strip())
    reviewRating.append(review.find('div', attrs={'class':'numRec'}).text.strip()[1:7])
    reviewDate.append(review.find('p', attrs={'class':'consumerReviewDate'}).text.strip()[12:])
    reviewLoanType.append(review.find('div', attrs={'class':'loanType'}).text.strip())

dataJson = {'Reviews': [{'reviewTitle':title, 
                        'reviewText':text,
                        'reviewAuthor':author,
                        'reviewRating':rating,
                        'reviewDate':date,
                        'reviewLoanType':loanType} for title, text, author, rating, date, loanType in zip(reviewTitle, reviewText, reviewAuthor, reviewRating, reviewDate, reviewLoanType)]}

# print(json.dumps(dataJson, indent=4))