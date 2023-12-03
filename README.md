# Introdution

This repository is a project of AcuPinchure's personal website.

## Structure

The site's backend is created using Django version 3.2, Django restframework version 3.14.
The frontend is created using React version 18.2, React Router DOM version 5.3.4.

The site currently contains following apps:
### Apps in use
- `twitter_bot`: Twitter bot that randomly posts pictures every hour
### Apps under construction
- `main`: Personal Portfolio
- `local_auth`: An app especially for authentication and app-level permission management
### Apps depricated
- `logistics`: A website about purchasing agent management, discontinued due to demand decreasing

For documentation of each app, see "Apps Documentation" section

## Deploy
If you want to deploy this repository and setup your own website. 
Here's how to do it.

1. Clone this repository
2. Setup python virtual environment
    ```bash
    python -m venv venv

    ./venv/bin/activate

    pip install -r requirements.txt
    ```
3. Setup npm environment for each app (currently only `twitter_bot` has npm project)
    ```bash
    cd ./npm_projects/<app_name>

    npm install --dev
    ```
4. Setup extra configs. These configs does not include in the repository due to sensitive data. You have to setup by yourself.
    * Create data/ folder at root to store website local files and database
    * Create django_keys.json in data/ for django SECRET_KEY
        ```json
        {
            "SECRET_KEY" : "django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
        ```
    * Create setting_local.py to pass localize settings to Django, these settings are different between production and development environment. Develop environment examples:
        ```python
        # Show or hide Django buit-in debug page when an error occurs, highly recommend to set to False in production
        DEBUG = True

        # The allowed host name for the web server, you should only include your DNS host name in production
        ALLOWED_HOSTS = ['*']

        # Django will search static directories in STATICFILES_DIRS in development environment, set it to False in production
        USE_STATICFILES_DIRS = True

        # host name for local network visiting, especially for data crawling server (see twitter_bot documentation)
        LOCAL_HOSTS = ['localhost:8000']
        ```
5. If you want to deploy this website to your own server, you need to setup a Web Server Software such as Apache. [How to use Django with Apache and mod_wsgi](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/modwsgi/)



# Apps Documentation
This section includes documentation of each Django app in this project.
## twitter_bot
An app that manage auto post images of Lovelive seiyuu on Twitter, collecting likes and retweets data and analyze the popularity of each image.
For more information about what this app is for, see the [about page of "Lovelive Seiyuu BOT"](https://acupinchure.ddns.net/bot/).

### Setup
If you want to setup your own image bot, follow the instructions.

1. Follow the steps mentioned in [Deploy](#Deploy) to setup the project.
2. Create your twitter bot account.
3. Setup your Twitter API for the account.
    * Obtain the necessary keys from Twitter API: `api_key`, `api_key_secret`, `access`, `access_secret`, `bearer_token`. See [Twitter Developer Documentation](https://developer.twitter.com/en/docs) for more information.
    * Create `tokens.json` at data/ folder and paste `api_key`, `api_key_secret`, `access`, `access_secret`
        ```json
        {
            "<Your account short name>": {
                "id": "<api_key>",
                "id_secret": "<api_key_secret>",
                "access": "<access>",
                "access_secret": "<access_secret>"
            }
            // more accounts here
        }
        ```
    * `tokens_v2.json` at data/ folder and paste `bearer_token`
        ```json
        {
            "<Your account short name>": {
                "bearer_token": "<bearer_token>"
            }
            // more accounts here
        }
        ```
4. Setup twitter bot account in auto posting service
    * Register a Django user or superuser, see [this tutorial](https://www.w3schools.com/django/django_admin_create_user.php).
    * Create folder `ImportQueue` and `Library` at `data/media/`. Under these 2 folder, create folders for each bot account with desired folder name (the folder names in two directory should be the same for each account).
    * Open Django management shell and register accounts to database
        ```bash
        # terminal

        cd src/
        python manage.py shell
        ```
        ```python
        # python shell

        from twitter_bot.models import Seiyuu
        s = Seiyuu.objects.create(name='<Your account verbose name>', screen_name='<Your account screen name>', id_name='<Your account short name>', image_folder='<Your account image folder name>', activated=False) # set false first before importing any image
        # add other accounts
        ```
    * Put your images into `data/media/ImportQueue/<Your account image folder name>/`. Currently only supports `.jpg`, `.jpeg`, `.png`, `.gif`, `.mp4`.
    * Run import command
        ```bash
        # terminal

        cd src/
        python manage.py import_img
        ```
    * Setup any scheduling service such as Linux Cron to run the `tweet_once` command every hour.
        ```
        #!/bin/bash

        cd /path/to/project/src
        /root/Documents/MySite/venv/bin/python manage.py tweet_once
        echo press Enter
        read reply
        ```
    * Run django dev server, locate to `/bot/login/`, login as the user you created.
    * Go to `Service Config (/bot/config/)`, adjust the post interval with desired value and activate the service (you may also set the interval and activate using django management shell).
    * Now you have your own bot service, for adding new image in the future, just add image to `ImportQueue/<Your account image folder name>/` and run `import_img` command again
### Data collection API
The repository currently does not include data collection service due to Twitter removing free access to Twitter API v1, but you may use the data collection API provided by the app to send collected data to the database and view graphical statistics in `/bot/stats/`.
1. Followers data collection
    * Setup your own data collection service, once you get the followers data, make a POST request to `/bot/api/followers/set` with the following request header and body, the API will auto insert data_time to the database:
    ```json
    // body
    {
        "seiyuu": "<The account screen name>",
        "followers": "<The number of followers in integer>"
    }
    ```
2. Tweet data collection
    * Make a GET request from this endpoint: `http://<the host name you specify in settings_local.LOCAL_HOSTS>/bot/api/tweet/noData/` to get the tweet id list that does not have data collected, you need to pass `?limit=` param as the limited number of posts (to avoid Twitter API throttling). The API will response the following data:
    ```json
    [
        {
            "id": <tweet_id in integer>,
            "post_time": "<The time the tweet is posted, ISO string>",
            "media__seiyuu__screen_name": "<The account screen name>"
        },
        // other tweet
    ]
    ```
    * Setup your own data collection service, once you get the tweet data, make a POST request to `/bot/api/tweet/updateData/<The id of the tweet>/` with the following request body:
        ```json
        {
            "data_time": "<The time the data is collected, ISO string>",
            "like": "<The number of like in this tweet>",
            "rt": "<The number of rt in this tweet>",
            "quote": "<The number of quote in this tweet>",
        }
        ```
