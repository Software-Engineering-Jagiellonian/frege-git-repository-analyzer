import os
import sys
from configparser import ConfigParser
from pathlib import Path


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parents[1]


def config(section):
    config_file_path = 'config/credentials.ini'
    if len(config_file_path) > 0 and len(section) > 0:
        # Create an instance of ConfigParser clas
        config_parser = ConfigParser()
        # Read the configuration file
        config_parser.read(config_file_path)
        # If the configuration file contains the provided section name
        if config_parser.has_section(section):
            # Read the options of the section
            config_params = config_parser.items(section)
            # Convert the list object to a python dictionary object
            # Define an empty dictionary
            conn_dict = {}
            # Loop in the list
            for config_param in config_params:
                # Get options key and value
                key = config_param[0]
                # value = os.environ.get(config_param[1]) if config_param[1] in os.environ else config_param[1]

                # todo uncomment when app will be working correctly
                try:
                    value = os.environ[config_param[1]]
                except KeyError:
                    print(section.upper(), key, "must be provided as,", config_param[1], "environment var!")
                    sys.exit(1)

                # Add the key value pair in the dictionary object
                conn_dict[key] = value
            # Get connection object use above dictionary object
            return conn_dict
