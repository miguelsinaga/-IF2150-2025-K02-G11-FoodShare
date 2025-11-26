import os
import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request, jsonify

def get_connection():
    config = {
        'user': os.getenv('DB_USER', 'foodshare_user'),
        'password': os.getenv('DB_PASS', 'janganbuangbuangmakanan'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'database': os.getenv('DB_NAME', 'foodshare'),
    }
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None
