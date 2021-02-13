from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, storage

import config_utils

PREFIX = "ProfileScripts/Template/"

logger_id = ""
template_id = ""
server_address = ""
template_modified_date = datetime.now()
template_modified_date_format = ""

cred = credentials.Certificate("../secret/yada-comp451-firebase-adminsdk-bi2lk-86047272ca.json")
firebase_admin.initialize_app(cred)

channel_module_path = "channels/"

db = firestore.client()

logger_snapshot = None
template_snapshot = None


def initialize(config):
    global logger_id, template_id, server_address, template_modified_date, template_modified_date_format
    global channel_module_path

    if "config" not in config:
        return

    config = config["config"]

    logger_id = config_utils.required(config, "logger_id", "Logger ID is required")
    template_id = config_utils.required(config, "template_id", "Template ID is required")
    server_address = config_utils.required(config, "server_address", "Server address is required")
    template_modified_date_format = config.get("template_modified_date_format", "%Y-%m-%d %H:%M:%S.%f")
    template_modified_date = datetime.strptime(
        config.get("template_modified_date", datetime.now()),
        template_modified_date_format
    )
    channel_module_path = config.get("channel_module_path", "channels/")

    global template_snapshot
    template_snapshot = db.collection("ChannelTemplates").document(template_id).get().to_dict()


def should_update_template():
    """
    Checks whether the channel template should be updated.

    :return: True if the template should be updated, otherwise False.
    """
    return channel_template_invalid() or channel_template_outdated()


def channel_template_invalid():
    """
    Checks if the config template id is the same as the server's template id.

    :return: True if the template is incorrect, otherwise False.
    """
    return db.collection("Loggers").document(logger_id).get().to_dict()["channelTemplate"] != template_id


def channel_template_outdated():
    """
    Checks whether the config channel modified date is earlier than the server's modified date.

    :return: True if the config is outdated, otherwise False.
    """
    date_string = db.collection("ChannelTemplates").document(template_id).get().to_dict()["modified"]
    return template_modified_date < datetime.strptime(date_string, template_modified_date_format)


def fetch_channels():
    bucket = storage.bucket("yada-comp451.appspot.com")

    for channel_name, file_url in template_snapshot["channels"].items():
        blob = bucket.blob(f"{PREFIX}{file_url}")
        blob.download_to_filename(f"{channel_module_path}{channel_name}.py")


def upload_data(data):
    pass
