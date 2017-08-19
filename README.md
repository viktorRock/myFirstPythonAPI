myFirstPythonAPI
==================

A  python restful API to manage integration with Python (could be bots, flask pages and etcetera).

The API is configured to deploy at Heroku

1. The current version contains
   * User management
   * Group management
   * Bot Management
   * Test Pages
   * at /digitalParrot a dummy bot that sends stastic answer (test porppus)
   * Heroku params

2. What is pending ?
   * CI with Travis
   * Link Bot with User
   * Authentication

## How to build locally ?
1.  ENV VARS - You need to create environment vars at local and heroku environments
    1. SECRET_KEY - the secret key of the API host
    2. PORT - The port used to test (HEROKU only)
        1. DATABASE_URL - The DB connection url (HEROKU ENV - if you just want to test locally you can skip this part)
2. Install Python Dependencies
      * ``` pip install -r requirements.txt ```
3. Create and Connect Heroku account (HEROKU ENV - if you just want to test locally you can skip this part)
   * https://devcenter.heroku.com/articles/getting-started-with-python#introduction
4. Prepare database and django static file (always do this when you change views or Models)
   * LOCAL ENV
   * Start Django Migrate
      * ``` python manage.py migrate ```
   * If is justa a Update on a existing table you can do this, before migrate
      * ``` python manage.py makemigrations ```

## Running on Windows (Test Locally)
* Just Python and Django
   * ``` python manage.py runserver ```
* Using Heroku Locally
   * ``` heroku local web -f Procfile.windows ```

## FAQ
* How to create the heroku environments ?
   * Follow this Heroku tutorial - https://devcenter.heroku.com/articles/getting-started-with-python#introduction
* How does it work Djanfo REST API Framework ?
   * Complete Details at - http://www.django-rest-framework.org/
   * Quickstart at - http://www.django-rest-framework.org/tutorial/quickstart/

##. Tips to run at Heroku
1. deploy HEROKU (HEROKU ENV - if you just want to test locally you can skip this part)
   * If you already had connect in Heroku your GitHub account you should (FIRST TIME only)
   *  disable collectstatic frrom Django before create the static folders
   * ``` heroku config:set DISABLE_COLLECTSTATIC=1 ```
2. After Django migrate and collectstatic and build
   * Start the scallabe Dyno
   * ``` heroku ps:scale web=1 ```

## Python on Heroku Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
