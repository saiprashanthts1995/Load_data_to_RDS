import datetime
from sqlalchemy import create_engine
import pandas as pd
import os
import json
from loguru import logger


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
        logger.info("Total_time taken to load the function {}".format(end_ts-start_ts))
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
            logger.exception("Exception details are {}",format(e))
    return wrapper


@udf_exception
def format_print(message, type_of_message="body"):
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


@udf_exception
def read_config():
    """
    This udf is used to load the config.json file and return the config connection
    :return:postgres connection
    """
    with open("../config/config.json") as f:
        config = json.load(f)
    logger.add('Read config.json')
    return config['postgres']


@udf_exception
def create_postgres_connection():
    """
    This udf is used to connect to postgres
    :return: connection
    """
    config_details = read_config()
    engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{database}".format(**config_details))
    connection = engine.connect()
    logger.add("connected to postgres is successful")
    return connection


@udf_exception
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
    logger.info("read the file as pandas dataframe")
    return data


@udf_exception
def current_path():
    """
    This will find the current working directory
    :return: current working directory
    """
    logger.info("found the current path")
    return os.path.dirname(os.path.realpath(__file__))


@udf_exception
def load_tables(table_name):
    """
    This udf provides details about the table details of the table name which is passed
    :param table_name: Name of the Table to be loaded
    :return: table details
    """
    with open("../scripts/load_details.json") as f:
        table_details = json.load(f)
    logger.info("found the load details of table")
    return table_details[table_name.upper()]


@udf_exception
def logging():
    """
    This is used to log the internal message into a file so that it can be used later for debugging purpose
    :return: logger object
    """
    logger.add("../logs/load_data_to_RDS_instance.log",
               level='INFO',
               retention='10 days',
               rotation='10 days')
    return logger


@udf_exception
def load_data_into_table(data, table_name):
    """
    This UDF is used to load data into table
    :param data: Source data
    :param table_name: target table name
    :return: True
    """
    table_details = load_tables(table_name)
    connection = create_postgres_connection()
    data.to_sql(table_name, if_exists="replace", index=False, con=connection)
    logger.info("Loaded data into postgres table for {}".format(table_name))
    return True


if __name__ == "__main__":
    print(read_config())
    print(load_tables('iris'))