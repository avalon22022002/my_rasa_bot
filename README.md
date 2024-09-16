### my_rasa_bot
Rasa chat bot  -- JUICERO
please open files in Read_Me folder

demo vedio on youtube: [link](https://youtu.be/KJ2jtecqijE)

### Building and running via docker

start/stop your application with docker:
1) `docker compose down -v` properly shut-down if it was running before.
2) `docker compose up --build`. Start application , it may take a some time and space. <br/>
    Your application will be available at http://localhost:8000 .
3) `docker compose down -v` to properly shut-down


### Steps to run without docker
1) install python 3.7.4
2) setup cmds for windows. <br/>
  -`python -m venv myenv` --Install virtual env. <br/>
  -`myenv/scripts/activate`  ---Activate virtual env. <br/>
  -`pip install --upgrade pip==19.3 setuptools wheel` --Make sure this is done successfully.<br/>
  -`pip install -r requirements.txt` or below cmd
  -`pip install rasa==2.5.1 rasa-sdk==2.5.0 mysql-connector-python==8.0.25` --To install project dependecies.<br/>
3) in ./endpoints.yml and ./actions/actions.py replace 'host.docker.internal' by 'localhost'. make sure you have a mysql db running and apply to it the cmds in ./myrasabot-dump.sql .<br/>
follow to save .sql dump file as UTF 8 if mysql server throws similar error [link](https://stackoverflow.com/questions/17158367/enable-binary-mode-while-restoring-a-database-from-an-sql-dump)
4) `rasa train` -- model will be saved in ./models directory
5) in terminal 1: `rasa run actions --debug`
6) in terminal 2: `rasa run -m models --enable-api --cors '*' --debug`
7) for front end [ use chrome and zoom at 80% for best view ] 
either <br/>
    -simply open ./my_rasa_bot_front_end/index.html via any browser <br/>
    -or `python -m http.server 8000 --directory ./my_rasa_bot_front_end` and open localhost:8000 in chrome at 80% zoom.
8) when done exit virtual evn cmd = `deactivate` in windows
