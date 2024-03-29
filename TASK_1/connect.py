from mongoengine import connect
import configparser
from pymongo import MongoClient
config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB','user')
mongo_pass = config.get('DB','pass')
db_name = config.get('DB','db_name')
domain = config.get('DB','domain')
cluster_name  = config.get('DB','cluster')




connect(host=f"""mongodb+srv://{mongo_user}:{mongo_pass}@{domain}?retryWrites=true&w=majority&appName={cluster_name}""",db='AuthorsDB',ssl=True)