# UNDER CONSTRUCTION
## Execution & Deployment
On this section you will find how to run the code locally, and how to deploy to GCP App Engine.

### Python environment
To build a local version of the solution you will need an environment with python 3.8.0 and the libraries listed in 
requirements.txt. In case you do not have such environment, you can create it as follows with conda:
 
```
conda create -n [] python=3.8.0 pip
pip install -r requirements.txt
```

To make last line to work you will need to change directory to the repo path in your local machine.

### Environment Variables

You will need to create a file called .env on the root of the python folder with the next environment variables:

```
SECRET_KEY = [this is the secret key of your flask app] 
USER = [name of user for flask app]
PASSWORD = [werkzeug.security.generate_password_hash(your_password)]
SERVER_HOST = [database host]
DATABASE_NAME = [name of accounting database]
USER_NAME = [name of database user]
USER_PASSWORD = [password of database user]
DATABASE_PORT_N = [host port]
```

### Local execution with flask server
To execute locally with the flask server:

```
set FLASK_APP=main.py
flask run
In case of error try: python -m flask run 
```


## Testing
You need to have installed pytest==7.2.0 on your local environment. 
The scope of the terminal should be located on folder python. 
To execute tests locally you have to run on the terminal:

```
python -m pytest -vv
```
