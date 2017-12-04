import db
from helpers import *
import configparser


def get_database_connection_details(cfg):
    cfg["database"]["host"] = input("Database host: ")
    cfg["database"]["user"] = input("Database user: ")
    cfg["database"]["password"] = input("Password: ")


def get_database_and_table(cfg):
    cfg["database"]["database"] = input("Database name: ")
    cfg["readwrite"]["table"] = input("Database table name: ")


def create_config_file(cfg):
    conf = configparser.ConfigParser()
    print(bcolors.OKGREEN, "-"*20)
    print("Your config: ")
    print("-" * 20, bcolors.ENDC)
    for key in cfg:
        conf.add_section(key)
        for key2 in cfg[key]:
            print(key2, ':', cfg[key][key2])
            conf.set(key, key2, cfg[key][key2])
    print(bcolors.OKGREEN, "\r\n", "-" * 20, bcolors.ENDC)
    with open('DHT22.cfg', 'w') as file:
        conf.write(file)
        print(bcolors.OKBLUE, "Config file created: ", file.name, bcolors.ENDC)
    print(bcolors.OKGREEN, "-" * 20, bcolors.ENDC)


def do_setup():
    cfg = {"database": {}, "readwrite": {}}
    print(bcolors.HEADER,
          "Hello! Seems like it's your first time running this program, let's do some setup...", bcolors.ENDC)
    get_database_connection_details(cfg)
    db.test_connection(cfg["database"], "connection")
    get_database_and_table(cfg)
    create_config_file(cfg)
    if not db.test_connection(cfg["database"], "connection"):
        if query_yes_no("[!] The database {} doesn't exist,. Create it?".format(cfg["database"]["database"])):
            db.create_new_database(cfg["database"]["database"])
            print(bcolors.OKGREEN, "[*] Database Created.", bcolors.ENDC)
    if not db.table_exists():
        if query_yes_no("[!] The table {} doesn't exist. Create it?".format(cfg["readwrite"]["table"])):
            db.create_table()
            print(bcolors.OKGREEN, "[*] Table Created.", bcolors.ENDC)

if __name__ == "__main__":
    do_setup()
    print(bcolors.HEADER, "Setup complete.", bcolors.ENDC)