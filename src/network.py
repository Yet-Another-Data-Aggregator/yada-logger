from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, storage

import config
from config import Config

# Path of firebase template storage
PREFIX = "ProfileScripts/Template/"

# ID of this logger
logger_id = ""

# ID of the template this logger is using
template_id = ""

# Address of the database server
server_address = ""

# Latest modified date of the template. Used to know when to update the channel template.
template_modified_date = datetime.fromtimestamp(0)

# Format of the template modified date
template_modified_date_format = ""

# Path to store downloaded channels in
channel_module_path = "channels/"


@config.section("config")
def load_variables(section):
    """
    Loads configuration variables from the "config" section

    :param section: The configuration section
    """
    global logger_id, template_id, server_address, template_modified_date, template_modified_date_format
    global channel_module_path

    logger_id = Config.required(section, "logger_id", "Logger ID is required")
    template_id = Config.required(section, "template_id", "Template ID is required")
    server_address = Config.required(section, "server_address", "Server address is required")
    template_modified_date_format = section.get("template_modified_date_format", "%Y-%m-%d %H:%M:%S.%f")
    channel_module_path = section.get("channel_module_path", "channels/")

    if "template_modified_date" in section:
        template_modified_date = datetime.strptime(section["template_modified_date"], template_modified_date_format)


class Network:
    cred = credentials.Certificate("../secret/yada-comp451-firebase-adminsdk-bi2lk-86047272ca.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    template_snapshot = None
    logger_snapshot = None

    @staticmethod
    def initialize():
        """
        Loads config variables and initializes database objects.
        """
        load_variables()

        Network.template_snapshot = Network.db.collection("ChannelTemplates").document(template_id).get()
        Network.logger_snapshot = Network.db.collection("Loggers").document(logger_id).get()

    @staticmethod
    def should_update_template():
        """
        Checks whether the channel template should be updated.

        :return: True if the template should be updated, otherwise False.
        """
        return Network.channel_template_invalid() or Network.channel_template_outdated()

    @staticmethod
    def channel_template_invalid():
        """
        Checks if the config template id is the same as the server's template id.

        :return: True if the template is incorrect, otherwise False.
        """
        return Network.logger_snapshot.to_dict()["channelTemplate"] != template_id

    @staticmethod
    def channel_template_outdated():
        """
        Checks whether the config channel modified date is earlier than the server's modified date.

        :return: True if the config is outdated, otherwise False.
        """
        date_string = Network.template_snapshot.to_dict()["modified"]
        return template_modified_date < datetime.strptime(date_string, template_modified_date_format)

    @staticmethod
    def fetch():
        if Network.channel_template_invalid():
            Network.fetch_template()

        Network.fetch_channels()

        Config.write_changes()

    @staticmethod
    def fetch_template():
        """
        Fetches the new or updated template from the database.
        """
        global template_id
        template_id = Network.logger_snapshot.to_dict()["channelTemplate"]

        Network.template_snapshot = Network.db.collection("ChannelTemplates").document(template_id).get()

        Config.get()["config"]["template_id"] = template_id

    @staticmethod
    def fetch_channels():
        """
        Downloads new or updated channels from database.
        """
        config = Config.get()
        bucket = storage.bucket("yada-comp451.appspot.com")

        downloaded_files = []

        template = Network.template_snapshot.to_dict()
        for channel_name, filename in template["channels"].items():
            if filename in downloaded_files:
                continue

            blob = bucket.blob(f"{PREFIX}{filename}")
            blob.download_to_filename(f"{channel_module_path}{channel_name}.py")

            config[f"channel/{channel_name}"] = {
                "module": filename.replace(".py", "")
            }

        config["config"]["template_modified_date"] = template["modified"]

    @staticmethod
    def upload_data(data):
        """
        Uploads the given data to the database.

        :param data: The data as a dictionary to be added to this Logger's data
        """
        Network.db.collection("Loggers").document(logger_id).update({
            "data": firestore.firestore.ArrayUnion([data])
        })
