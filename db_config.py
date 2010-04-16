try:
	from db_password import PASSWORD
except:
	PASSWORD = ""
	
DB_ENGINE = "postgresql_psycopg2"
DB_NAME = "ConceptNet"
DB_HOST = "csc-sql.media.mit.edu"
DB_PORT = "5432"
DB_USER = "openmind"
DB_PASSWORD = PASSWORD
DB_SCHEMAS = "public"
