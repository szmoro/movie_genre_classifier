import click
import json
import operator
import requests
from pprint import pprint

# Url of the API endpoint exposing the movie classification model
url = "http://localhost:8000/genre"

@click.command()
@click.option('--title', help='The movie title. A mandatory non-empty string.')
@click.option('--description', help='The movie description. A mandatory non-empty string.')
def classify_movie(title, description):
    """Simple command-line application that given a title and a short movie description returns an appropriate genre."""
    # Preparing paylod for API request
    payload = {"title": title, "description": description}

    # API request to obtain predictions
    response = requests.request("POST", url, data=json.dumps(payload), headers={ 'Content-Type': 'application/json' })

    # In case of error response (status code 400 or 500) print error message
    if response.status_code // 4:
        print('Unable to retrieve answer')
    else:
        # Retrieving prediction with highest score and printing result
        genre = max(json.loads(response.text).items(), key=operator.itemgetter(1))[0]
        payload['genre'] = genre
        pprint(payload)

if __name__ == '__main__':
    classify_movie()