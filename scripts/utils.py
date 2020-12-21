import datetime
from sqlalchemy import create_engine
import pandas as pd
import os
import json


def calculate_time(method1):
    """
    This Decorator is used to display how much time each function takes to execute
    :param method1: udf function
    :return: function output and time taken
    """
    def wrapper(*args, **kwargs):
        start_ts = datetime.datetime.now()
        result = method1(*args, **kwargs)
        end_ts = datetime.datetime.now()
        print("Total_time taken to load the function {}".format(end_ts-start_ts))
        return result
    return wrapper


def udf_exception(method1):
    """
    This decorator is used to display udf exception, so that exception need not be repeated always
    :param method1: udf function
    :return: function output and user defined exception
    """
    def wrapper(*args, **kwargs):
        try:
            result = method1(*args, **kwargs)
            return result
        except Exception as e:
            print(e)
    return wrapper


def format_print(message, type_of_message="heading"):
    """
    This UDF is used to print formatted messages
    :param message: User defined message as input
    :param type_of_message: if message type is heading or not
    :return: print in the formatted fashion
    """
    if type_of_message == "heading":
        print("="*50)
        print("{}".format(message))
        print("="*50)
    else:
        print("{}".format(message))


def read_config():
    with open("../config/config.json") as f:
        config = json.load(f)
    return config['postgres']


def create_postgres_connection():
    """
    This udf is used to connect to postgres
    :return: connection
    """
    config_details = read_config()
    engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{database}".format(**config_details))
    connection = engine.connect()
    return connection


def read_file(filename, filetype, sheet_name=""):
    """
    This UDF is used to read data using pandas and return it using pandas dataframe
    :param filename: Name of the source file
    :param filetype: file type can be CSV or EXCEL
    :param sheet_name: sheet_name if EXCEL is used
    :return: final data as dataframe object
    """
    if filetype.upper() == "CSV":
        data = pd.read_csv("../data/{}".format(filename))
    elif filetype.upper() == "EXCEL":
        data = pd.read_excel("../data/{}".format(filename),sheet_name=sheet_name)
    return data


def current_path():
    return os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":
    print(read_config())