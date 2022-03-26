
import os
import requests
import json
from replit import db



def get_quote():
  response =     requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def get_review(book_title):
    response=requests.get(f"https://api.nytimes.com/svc/books/v3/reviews.json?title={book_title}&api-key={os.getenv('my_key')}")
    data = response.json()
    if response.status_code not in range(200, 299) or len(data["results"])==0:
        return None
    else:
        return data["results"][0]['url']
    
    
def update_encouragement(message):
    if "encouragements" in db.keys():
        encouragements= db["encouragements"]
        encouragements.append(message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [message]
def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index] 
        db["encouragements"] = encouragements