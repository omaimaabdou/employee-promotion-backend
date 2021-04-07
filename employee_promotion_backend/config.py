# config.py

MYSQL_HOST = '127.0.0.1' 
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'hahaah'
MYSQL_DATABASE = 'rhdb'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+MYSQL_USERNAME+':'+MYSQL_PASSWORD+'@'+MYSQL_HOST+'/'+MYSQL_DATABASE
SERVER_HOST = '0.0.0.0'
KEY_JWT = 'mySecret'  # Prod
MAIL_SERVER = 'smtp.gmail.com'
MAIL_USERNAME = 'redaabdou49@gmail.com'
MAIL_PASSWORD = 'hahah'
