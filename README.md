COPY DB - pgloader mysql://thx:1H3d4s8w*@64.227.112.119/medication postgresql://postgres:postgres@localhost/medication /n
CONNECT PSQL - sudo -u postgres psql /n
GENERATE MODELS - sqlacodegen --schema medication postgresql://postgres:postgres@localhost:5432/medication > model.py /n

SWAGGER - localhost:5000//api /n
ADMIN - localhost:5000/admin /n
HTTP REQUEST - postman /n
SIGNALS IN RMQ - http://localhost:15672/#/queues/%2F/MARK%20SIGNALS /n
	login - guest /n
	password - guest /n
