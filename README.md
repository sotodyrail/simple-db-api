COPY DB - pgloader mysql://thx:1H3d4s8w*@64.227.112.119/medication postgresql://postgres:postgres@localhost/medication
CONNECT PSQL - sudo -u postgres psql
GENERATE MODELS - sqlacodegen --schema medication postgresql://postgres:postgres@localhost:5432/medication > model.py

