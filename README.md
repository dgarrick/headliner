# headliner

### Prereqs (all available through PyPI)

I highly suggest using [virtual environments](https://virtualenvwrapper.readthedocs.io/en/latest/) instead of installing packages globally!

`pip install -r requirements.txt`

You may also need to install corpora for nltk. Open a new python REPL instance in a terminal and type the following:

`>>> import nltk`

`>>> nltk.download()`

And then download all corpora.

If you want to run the REST API as well, you will also need:

`pip install gunicorn`

`pip install falcon`

To run the API, simply run:

`gunicorn headliner:api` from within `src/api`
