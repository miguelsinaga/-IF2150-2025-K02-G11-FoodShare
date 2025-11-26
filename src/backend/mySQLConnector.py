import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request, jsonify
def get_connection():

    config = {
        'user' : 'foodshare_user',
        'password' : 'janganbuangbuangmakanan',
        'host' : 'localhost',
        'port': 3306,
        'database' : 'foodshare'
    }
    try : 
        cnx = mysql.connector.connect(
            **config
        )
        return cnx

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None