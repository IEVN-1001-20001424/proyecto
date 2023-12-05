
import pymysql

class DevelopmentConfig():
    DEBUG=True
    MYSQL_HOST='localhost'
    MYSQL_USER='root'
    MYSQL_PASSWORD=''
    MYSQL_DB='api_utl'

config={
    'development':DevelopmentConfig
}

def obtener_conexion():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='api_utl')