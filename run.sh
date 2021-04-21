export FLASK_APP=main.py & sudo kill -9 $(sudo lsof -t -i:5000) & flask run;

