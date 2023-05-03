# headliner

![headliner_screenshot](https://cloud.githubusercontent.com/assets/2948894/24990892/be02364c-1fdc-11e7-8ba1-88778cd237f7.png)

http://headlinr.herokuapp.com/

### Prereqs (all available through PyPI)

Headlinr uses poetry for build management.

To run the heroku build, first install heroku cli:

https://devcenter.heroku.com/articles/heroku-command-line

For a local build, run:

`heroku local`

To run the REST API, simply run:

`heroku local web`

To run the data pipeline, run:

`python src/data/main.py`
