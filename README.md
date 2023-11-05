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

## Fork and deploy
If you want to fork this repository and setup your own website. 
Here's how to do it.

1. Fork and clone this repository
2. Setup python virtual environment
    ```
    python -m venv venv

    ./venv/bin/activate

    pip install -r requirements.txt
    ```
3. Setup npm environment for each app (currently only `twitter_bot` has npm project)
    ```
    cd ./npm_projects/<app_name>

    npm install --dev
    ```
4. Setup extra configs. These configs does not include in the repository due to sensitive data. You have to setup by yourself.
    * Create data/ folder at root to store website local files and database
    * Create django_keys.json in data/ for django SECRET_KEY
        ```
        {
            "SECRET_KEY" : "django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
        ```
    * Create setting_local.py to pass localize settings to Django, these settings are different between production and development environment. Develop environment examples:
        ```
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

If you want to setup your own image bot, follow the instructions.

1. Setup the project mentioned in [Fork and deploy](#Fork-and-deploy)
2. Create your twitter bot account
3. Setup your Twitter API for the account.
    * Obtain the necessary keys from Twitter API: `api_key`, `api_key_secret`, `access`, `access_secret`, `bearer_token`. See [Twitter Developer Documentation](https://developer.twitter.com/en/docs) for more information.
    * Create `tokens.json` at data/ folder and paste `api_key`, `api_key_secret`, `access`, `access_secret`
        ```
        {
            "<Your account name>": {
                "id": "<api_key>",
                "id_secret": "<api_key_secret>",
                "access": "<access>",
                "access_secret": "<access_secret>"
            }
            // more accounts here
        }
        ```
    * `tokens_v2.json` at data/ folder and paste `bearer_token`
        ```
        {
            "<Your account name>": {
                "bearer_token": "<bearer_token>"
            }
            // more accounts here
        }
        ```
4. Setup twitter bot account in auto posting service
    * Open `src/twitter_bot/management/commands/_post_handler.py` and modify the account info
        ```
        # _post_handler.py

        if name == '<Your account name>':
            the_token = tokens["<Your account name>"]
            the_token_v2 = tokens_v2["<Your account name>"]
        elif name == '<Other account name>':
            the_token = tokens["<Other account name>"]
            the_token_v2 = tokens_v2["<Other account name>"]
        # ...
        else:
            raise ValueError('Invalid name: {}'.format(name))
        ```
    * Open `src/twitter_bot/management/commands/tweet_once.py` and modify the account info
        ```
        # tweet_once.py

        def post_once(name):
            api, oauth, client = auth_api(name)
            if not (api and oauth and client):
                print("[{}] Error during authentication".format(name))
                return False
            print("[{}] Authentication OK".format(name))

        if name == '<Your account name>':
            search = '<Your account verbose name>'
            bot_id = '<Your account screen name>'
            bot_user_id = '<Your account user id>'
        elif name == '<Other account name>':
            # ...

        # ...

        class Command(BaseCommand):
        help = "Pick a random media and post once"
        
        def handle(self, *args, **kwargs):
            names = ['<Your account name>','<Other account name>']
        ```
    * Create folder `ImportQueue` and `Library` at `data/media/`. Under these 2 folder, create folders for each bot account with desired folder name.
    * Modify `src/twitter_bot/management/commands/import_img.py` and add your image folder name
        ```
        # import_img.py

        class Command(BaseCommand):
        def handle(self, **options):

            for info in [
                ('<Your account verbose name>','<Your account image folder name>'),
                ('<Other account verbose name>','<Other account image folder name>'),
                # ...
            ]:
        ```
    * Open Django management shell and add accounts to database
        ```
        # terminal

        cd src/
        python manage.py shell
        ```
        ```
        # python shell

        from twitter_bot.models import Seiyuu
        s = Seiyuu.objects.create(name='<Your account verbose name>', screen_name='<Your account screen name>', id_name='<Your account short name>')
        # add other accounts
        ```
    * Put your images into `data/media/ImportQueue/<Your account image folder name>/`. Currently only supports `.jpg`, `.jpeg`, `.png`, `.gif`, `.mp4`.
    * Run import command
        ```
        # terminal

        cd src/
        python manage.py import_img
        ```
    * Setup any scheduling service such as Linux Cron to run the `tweet_once` command in desired interval (suggest more than 1 hour)
        ```
        #!/bin/bash

        cd /path/to/project/src
        /root/Documents/MySite/venv/bin/python manage.py tweet_once
        echo press Enter
        read reply
        ```
    * Now you have your own bot service, for adding new image in the future, just add image to `ImportQueue/<Your account image folder name>/` and run `import_img` command again
    * The repository currently does not include data collection function due to Twitter removing free access to Twitter API v1, but you may use the data collection API in this project to send collected data to the database.
        * Make a GET request from this endpoint: `http://<the host name you specify in settings_local.LOCAL_HOSTS>/bot/api/tweet/noData/` to get the tweet id list that does not have data collected, you need to pass `limit` param as the limited number of posts, suggest `limit=12` every hour.
        * Setup your own data collection service, once you get the data, make a POST request to `/bot/api/tweet/updateData/<The id of the tweet>/` with the following data
            ```
            {
                "data_time": "<The time the data is collected, ISO string>",
                "like": "<The number of like in this tweet>",
                "rt": "<The number of rt in this tweet>",
                "quote": "<The number of quote in this tweet>",
            }
            ```