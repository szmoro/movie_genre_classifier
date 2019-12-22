from fastapi import FastAPI
from pydantic import BaseModel
import spacy


app = FastAPI()

# Loads movie classification model
nlp = spacy.load('/opt/spacy_model')

# Class for the /genre endpoint request body
class Movie(BaseModel):
    title: str
    description: str


@app.post("/genre")
async def predict_genre(movie: Movie):
    # Compute predictions using the movie classification model
    doc = nlp(movie.description)
    # Return labels
    return doc.cats