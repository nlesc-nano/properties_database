"""Module to read user input and perform the requested input action."""
import argparse
import logging

from argparse import Namespace
from .interface.mongodb_interface import (DatabaseConfig,
                                          store_dataframe_in_mongo)

logger = logging.getLogger(__name__)


__all__ = ["main"]


def store(args: Namespace) -> None: 
    """Store dataframe in the database."""
    msg = f"""
Storing data from: {args.file}
In the database located at {args.name}:{args.port}
With collection name: {args.collection}
"""
    print(msg)
    db_config = DatabaseConfig(args.database, args.name, args.port)
    indices = store_dataframe_in_mongo(db_config, args.collection, args.file)
    print(indices)


def main():
    """Parse the command line arguments to interact with the database."""
    parser = argparse.ArgumentParser("call_database")
    subparsers = parser.add_subparsers(help="Interact with the database", dest="command")

    # Add data diretly to the database
    parser_jobs = subparsers.add_parser("store", help="Store data in the database")
    parser_jobs.add_argument('-f', '--file', type=str, required=True, help="Path to the csv containing the data")
    parser_jobs.add_argument('-c', '--collection', type=str, required=True, help="collection name")
    parser_jobs.add_argument('-db', '--database', type=str, help="databas name", default="properties")
    parser_jobs.add_argument('-n', '--name', type=str, help="hostname or IP address of the database", default="localhost")
    parser_jobs.add_argument('-p', '--port', type=str, help="Port to connect to the database", default=27017)

    #

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()

    if args.command == "store":
        store(args)
    elif args.command == "create":
        prints(args)
        # create_jobs_from_collection()



if __name__ == "__main__":
    main()
