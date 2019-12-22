from setuptools import setup

setup(
    name='movie_classifier',
    version='0.1',
    py_modules=['movieCLI'],
    install_requires=[
        'Click',
        'Spacy',
        'FastAPI',
    ],
    entry_points={
        'console_scripts': [
            'movie_classifier=movieCLI:classify_movie',
        ]
    }
)