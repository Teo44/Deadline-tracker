# Installing and running Deadline-tracker

## Cloning the repository and downloading dependencies

Python 3 and pip must to be installed on the system.

- Clone the repository from github
```
git clone https://github.com/Teo44/deadline-tracker
cd Deadline-tracker
```
- Create and activate a Python virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
- Download the applications dependencies with pip
```
pip install -r requirements.txt
```

## Running Deadline-tracker locally on a Unix-system

- Run the Python executable, which will start a Flask-server
```
python run.py
```

The application can now be accessed on a browser from the address 127.0.0.1:5000. 

The Flask-server is not meant for hosting the application on the internet. Below are instructions for setting up Deadline-tracker on Heroku, to run it on the internet.

## Running Deadline-tracker remotely on Heroku

To run the application on Heroku, [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and a Heroku account are required.

- Create a new Heroku app (note that the name could be taken, change if needed)
```
heroku create deadline-tracker
```

- Add the Heroku remote repository to git
```
git remote add heroku https://git.heroku.com/deadline-tracker.git
```

- Push the project to the Heroku repository
```
git add .
git commit -m'Heroku commit'
git push heroku master
```

- Set the Heroku environment variable
```
heroku config:set HEROKU=1
```

- Create a new database in Heroku
```
heroku addons:add heroku-postgresql:hobby-dev
```

- Restart the Heroku dyno
```
heroku restart
```

Deadline-tracker should now be running on your Heroku account at https://deadline-tracker.herokuapp.com

