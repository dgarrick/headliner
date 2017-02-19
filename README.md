# headliner

https://headlinr.herokuapp.com/

### Prereqs (all available through PyPI)

I highly suggest using [virtual environments](https://virtualenvwrapper.readthedocs.io/en/latest/) instead of installing packages globally!

`pip install -r requirements.txt`

To run the heroku build, first install heroku cli:

http://devcenter.heroku.com/articles/heroku-command-line

For a local build, run:

`heroku local`

To run the REST API, simply run:

`heroku local web`

To run the data pipeline, run:

`python src/data/main.py`
