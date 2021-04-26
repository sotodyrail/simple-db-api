COPY DB - pgloader mysql://thx:1H3d4s8w*@64.227.112.119/medication postgresql://postgres:postgres@localhost/medication

CONNECT PSQL - sudo -u postgres psql

GENERATE MODELS - sqlacodegen --schema medication postgresql://postgres:postgres@localhost:5432/medication > model.py

SWAGGER - localhost:5000//api 

ADMIN - localhost:5000/admin 

HTTP REQUEST - postman 

SIGNALS IN RMQ - http://localhost:15672/#/queues/%2F/MARK%20SIGNALS 
	login - guest 
	password - guest 


RUN
-----------

sudo kill -9 $(sudo lsof -t -i:8080) & flask run --host=0.0.0.0 --port=8080

sudo -u postgres psql -U postgres -d medication -a -f initial.sql 

python3 get.py 
python3 patch.py 
