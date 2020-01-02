# Movie genre classifier

## Overview

This project contains a movie genre classifier. It is entirely developed in Python, using the [Spacy](https://spacy.io/) NLP library, deployed via Docker and accessible via a simple CLI application.

The movie_classifier application uses the Spacy "core_web_en_lg" model, with an additional text classifier module trained to predict the genre of the movie given in input from its description. The model is internally exposed via a single API endpoint. Once launched, the application is accessible via CLI, with the movie_classifier command. The CLI interface takes in input the movie title and description, it sends an HTTP request to the API and returns the genre with the highest confidence score predicted by the model. 

This repository is organized in two subfolders:
 - movie_classifier: contains the movie_classifier application, composed of the spacy_model folder, the movieAPI.py API and the movie_classifier_cli python package.
 - training: contains the data and code used to train the NLP model found in the movie_classifier/spacy_model folder.

## The movie_classifier application

### Launching the movie_classifier container

To launch the movie_classifier application clone this repository and cd into the movie_classifier folder:

```bash
git clone https://github.com/szmoro/movie_genre_classifier.git
cd movie_genre_classifier/movie_classifier
```
Then download and unzip the NLP model

```bash
curl -L -o spacy_model.zip https://www.dropbox.com/s/lgs9mrb892ht0a4/spacy_model.zip?dl=1
unzip spacy_model.zip
```

And then just run:

```bash
docker-compose up
```

This command will build and run the movie_classifier docker container; the terminal window will show the log of the API calls.

### Using the CLI application

The CLI interface, which is provided by the movie_classifier_cli package, has the following signature:

```bash
Usage: movie_classifier [OPTIONS]

  Simple command-line application that given a title and a short movie
  description returns an appropriate genre.

Options:
  --title TEXT        The movie title. A mandatory non-empty string.
  --description TEXT  The movie description. A mandatory non-empty string.
  --help              Show this message and exit.
```
 
The movie_classifier_cli package comes pre-installed in the movie_classifier container and it is ready to use when the container is launched. There are two ways of interacting with the CLI application: the user can either open a shell inside the container and run the CLI movie_classifier command

```bash
docker exec -it movie_classifier /bin/bash
movie_classifier --title "Othello" --description "The evil Iago pretends to be friend of Othello in order to manipulate him to serve his own end in the film version of this Shakespeare classic."

{'description': 'The evil Iago pretends to be friend of Othello in order to '
                'manipulate him to serve his own end in the film version of '
                'this Shakespeare classic.',
 'genre': 'Drama',
 'title': 'Othello'}
```

or run the command directly from outside the container with the "docker exec" directive

```bash
docker exec movie_classifier movie_classifier --title "Othello" --description "The evil Iago pretends to be friend of Othello in order to manipulate him to serve his own end in the film version of this Shakespeare classic."

{'description': 'The evil Iago pretends to be friend of Othello in order to '
                'manipulate him to serve his own end in the film version of '
                'this Shakespeare classic.',
 'genre': 'Drama',
 'title': 'Othello'}
```
### Accessing the model predictions

As previously mentioned, the model predictions can be obtained via a single API call. This API is implemented with [FastAPI](https://github.com/tiangolo/fastapi) which is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
FastAPI automatically generates the OpenAPI 3.0 documentation of the API and exposes it at the /docs endpoint. The container exposes the API on port 8000, so after launching it, the user can explore the API documentation at http://localhost:8000/docs. Here the user will be able to access the /genre endpoint documentation and even perform some test calls on it to explore the API request and response formats.

Here is an example of a request with its response:

```bash
curl --location --request POST 'localhost:8000/genre' \
     --header 'Content-Type: application/json' \
     --data-raw '{
         "title": "Othello",
         "description": "The evil Iago pretends to be friend of Othello in order to manipulate him to serve his own end in the film version of this Shakespeare classic."
     }'

{
    "Action": 0.01206315215677023,
    "Comedy": 0.1740693598985672,
    "Drama": 0.5714808106422424,
    "Romance": 0.008160477504134178,
    "Thriller": 0.009414901956915855
}
```

## Training

The model contained in the movie_classifier/spacy_model folder was trained on the [MovieLens](https://www.kaggle.com/rounakbanik/the-movies-dataset/version/7#movies_metadata.csv) dataset using the training.ipynb jupyter notebook that can be found in the training folder.

The model was obtained by training a multi-label classifier on the embedding produced by the Spacy "en_core_web_lg" model. The classifier was trained with early stopping, using a batch_size of 64 and a patience of 5.

To obtain a balanced training dataset, only the genres that appeared in at least 5000 movies were selected. After applying this filter, only 5 genres were left: 
- Action
- Comedy
- Drama
- Romance
- Thriller

The resulting dataset was then split to obtain:
- A training set of around 25000 samples.
- A test set of around 7000 samples.
- A validation set of around 2800 samples. 

The performance of the currently available model when measured on the independent test set is the following:
- Precision: 0.692
- Recall: 0.629
- F1 Score: 0.659
- Accuracy: 0.798
  
### Using the training notebook
To access and reuse this notebook just cd into the training folder and type

```bash
docker-compose up
```

This will launch a docker container with a running instance of jupyter from which the user can access and run the training.ipynb notebook. After executing the notebook and training the model, the best performing instance will be saved in the spacy_model folder. To use this model with the movie_classifier application just move outside of the training folder and type the following commands:

```bash
cp training/spacy_model movie_classifier/spacy_model
cd movie_classifier
docker-compose up --build
```

These commands will copy the newly trained spacy nlp model into the movie_classifier folder and rebuild the container so that when it is launched it uses the new model. 
