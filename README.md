# WORK IN PROGRESS
# What is this?
This is a personal project to build a WebApp for expenses and incomes accounting & equity control.  
It is build in Python-Flask for the input of data while the visualisation is done with Dash-Plotly. It is ready to
be deployed on Heroku as a container.
Currently only is implemented the 

## Execution & Deployment
On this section you will find how to run the code locally, with docker/docker-compose or how to deploy to Heroku.

### Python environment
To build a local version of the solution you will need an environment with python 3.7.0 and the libraries listed in 
requirements.txt. In case you do not have such environment, you can create it as follows with conda:
 
```
conda create -n [] python=3.8.0 pip
pip install -r env/requirements.txt
```

To make last line to work you will need to change directory to the path where the project resided.

### Environment Variables

You will need to create a file called .env on the folder <path-to-project>/env with the next environment variables:

```
SECRET_KEY = [this is the secret key of your flask app] 
USER = [name of user]
PASSWORD = [werkzeug.security.generate_password_hash(your_password)]
DATABASE_URL = [connection to main database where assests and account data is stored]
```

### Local execution with flask server
To execute locally with the flask server:

```
set FLASK_APP=app.py
flask run
In case of error try: python -m flask run 
```

### Local execution with Docker
In order to execute the webapp with Docker you will need to use the next code in your Terminal:

```
docker build -t app-cuentas .
docker run -v [path-to-project]:/app -dp 8081:80 app-cuentas
```

### Local execution with Docker-compose
In order to execute the webapp with Docker-compose you will need to use the next code in the Terminal:

```
docker-compose up
```

### Deployment to Heroku as Stack heroku-18 and framework python --deprecated
In order to deploy to Heroku you will need to use the next code in the Terminal:
```
heroku login
heroku git:remote -a [app-name]
git push heroku master
```

Deprecation: Files under folder env/heroku-stack-heroku-18 has to be copied directly under root folder.

### Deployment to Heroku as a Container
First thing will be to create an app on Heroku. After that, the stack of the app has to be changed to container, 
in order to do so, you can use next code on your CLI:

```
heroku login
heroku stack:set container --app [app-name]
```

After that, the easier way will be to connect the app to a GitHub repository where the project resides. 
It will be also a good idea to check for automatic deploys. This way, with each push to GitHub of your code, Heroku 
automatically will create a new image and changes will be applied.

Also, you will need to create several env variables on settings, the same ones that you can find on section
_Environment Variables_. Tables definition can be found on section _Tables definition_.


## PostgreSQL code deployment

To execute build_scaffolding:
```commandline
{path to psql executable} -h {server host} -U {user name} -d {database name} -p {port} -f {path to build_scaffolding.psql} -L {path to file where to save logs}
```


## Testing
You need to have installed pytest on your local environment. 
The scope of the terminal should be located on the root folder of this repository. 
To execute tests locally you have to run on the terminal:

```
python -m pytest -vv
```

