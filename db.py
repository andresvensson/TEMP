import configparser
import mysql.connector
from helpers import *

INSERT_QUERY = "INSERT INTO " \
               "readings(readingtimestamp, sensor, temperature, humidity, location) " \
               "VALUES (%(timestamp)s, %(sensor)s, %(temp)s, %(humidity)s, %(location)s)"
SELECT_QUERY = "SELECT * FROM readings WHERE {0}"
config = configparser.ConfigParser()
TEST_STRINGS = {"connection": ["[*] Testing database connection...",
                               "[*] Server connection OK!"],
                "database": ["[*] Checking if the database exists...",
                             "[*] Database OK!"]
                }


def load_config():
    config.read('DHT22.cfg')


def get_reading_dict(reading_dict):
    read_dict = {"timestamp": "", "sensor": "", "temp": "", "humidity": "", "location": ""}
    reading_dict = read_dict
    return reading_dict


def create_new_database(database_name):
    load_config()
    cnx = mysql.connector.connect(host=config["database"]["host"],
                                  user=config["database"]["user"],
                                  password=config["database"]["password"])
    cursor = cnx.cursor()
    try:
        cursor.execute("CREATE DATABASE {}".format(database_name))
    except mysql.connector.Error as err:
        print(bcolors.FAIL, "[!] Could not create database", bcolors.ENDC)
        print(bcolors.FAIL, "[!] Error message: ", err, bcolors.ENDC)

    cnx.commit()
    cnx.close()


def create_table():
    load_config()
    cnx = mysql.connector.connect(**dict(config.items('database')))
    cursor = cnx.cursor()
    cursor.execute("CREATE TABLE {} (readingtimestamp datetime, sensor varchar(20), "
                   "temperature decimal, humidity decimal, location varchar(20));".format(config["readwrite"]["table"]))
    cnx.commit()
    cursor.execute("DESCRIBE {}".format(config["readwrite"]["table"]))
    print(bcolors.UNDERLINE, "[ Table Columns ]", bcolors.ENDC)
    for row in cursor:
        print(row[0], ":", row[1])
    cnx.close()


def test_connection(cfg, test_for):
    print(bcolors.OKBLUE, TEST_STRINGS[test_for][0], bcolors.ENDC)
    if not len(cfg) > 0:
        load_config()
    try:
        if len(cfg) > 0:
            cnx = mysql.connector.connect(**cfg)
        else:
            cnx = mysql.connector.connect(**dict(config.items('database')))
    except mysql.connector.Error as err:
        print(bcolors.FAIL, err, bcolors.ENDC)
        if err.errno == 2003:
            print("Please check that you supplied the correct host.")
        if err.errno == 1045:
            print(bcolors.WARNING, "Wrong username or password.", bcolors.ENDC)
        if err.errno == 1049:
            print(bcolors.WARNING, "The database does not exist.", bcolors.ENDC)
        return False
    print(bcolors.OKGREEN, TEST_STRINGS[test_for][1], bcolors.ENDC)
    cnx.close()
    return True


def table_exists():
    load_config()
    cnx = mysql.connector.connect(**dict(config.items('database')))
    cursor = cnx.cursor()
    cursor.execute('SHOW TABLES')
    for table in cursor:
        if config["readwrite"]["table"] in table:
            return True
    cnx.close()
    return False


def insert_row(data):
    stmt = INSERT_QUERY
    run_query(stmt, data)


def run_query(stmt, data=''):
    load_config()
    cnx = mysql.connector.connect(**dict(config.items('database')))
    cursor = cnx.cursor()
    cursor.execute(stmt, data)
    cursor.execute(stmt, data)
    cnx.commit()
    cnx.close()


if __name__ == "__main__":
    load_config()

