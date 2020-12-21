from utils import create_postgres_connection, \
    format_print, logging, load_tables, read_file, \
    calculate_time, load_data_into_table
import argparse


@calculate_time
def run(env):
    if env == "dev":
        logger.info("This is used to load data into RDS instance")
        format_print("This is used to load data into RDS instance", type_of_message="heading")

        # table details
        table_details = load_tables('iris')
        file_name = table_details['source_file_name']
        file_extension = file_name.split('.')[1]
        table_name = table_details['target_table_name']
        logger.info("Name of the source file is {}".format(file_name))
        logger.info("Name of the target table is {}".format(table_name))

        # load data as pandas dataframe
        data = read_file(file_name, filetype=file_extension)
        logger.info("Sample data is shown below for your reference")
        logger.info(data.head())

        # connection to postgres and load data into table
        logger.info("Load into RDS instance process begins")
        load_data_into_table(data, table_name)
        logger.info("Load into RDS instance process completed")

    else:
        print("First complete the development in dev environment and then move on :) ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="to load data to postgres",
        prog="main.py"
    )
    parser.add_argument("--env", "-n", help="Name of the environment",
                        dest="env")
    args = parser.parse_args()
    # logger object
    logger = logging()
    logger.info("We are loading data to {} environment".format(args.env))
    logger.info("Loading data process begins now".format(args.env))
    run(args.env)
    logger.info("Loading data process ends now".format(args.env))



