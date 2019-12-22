FROM continuumio/anaconda3

WORKDIR /training

# Adding the training notebook and the MovieLens dataset
ADD ./training.ipynb ./training.ipynb
ADD ./movies_metadata.csv ./movies_metadata.csv

# Installing Spacy and downloading the en_core_web_lg model
RUN pip install spacy[cuda100] \
    && python -m spacy download en_core_web_lg

EXPOSE 8888

# Launching the jupyter instance
CMD jupyter notebook --ip 0.0.0.0 --port 8888 --allow-root