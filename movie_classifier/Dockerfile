FROM continuumio/anaconda3

# Adding movie_classifier_cli python package
ADD ./movie_classifier_cli /opt/movie_classifier_cli
# Adding movieAPI API
ADD ./movieAPI.py .
# Adding Spacy NLP model
ADD ./spacy_model /opt/spacy_model

# Installing spacy fastapi and uvicorn for the API, along with the movie_classifier_cli package
RUN apt-get update && apt-get install -y build-essential \
    && pip install spacy fastapi uvicorn \
    && pip install /opt/movie_classifier_cli

EXPOSE 8000

# Serving the API
CMD uvicorn movieAPI:app --port 8000 --host 0.0.0.0