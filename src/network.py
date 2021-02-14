from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, storage

from config import Config

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


def initialize():
    global logger_id, template_id, server_address, template_modified_date, template_modified_date_format
    global channel_module_path

    config = Config.get()

    if "config" not in config:
        return

    config = config["config"]

    logger_id = Config.required(config, "logger_id", "Logger ID is required")
    template_id = Config.required(config, "template_id", "Template ID is required")
    server_address = Config.required(config, "server_address", "Server address is required")
    template_modified_date_format = config.get("template_modified_date_format", "%Y-%m-%d %H:%M:%S.%f")
    template_modified_date = datetime.strptime(
        config.get("template_modified_date", datetime.now()),
        template_modified_date_format
    )
    channel_module_path = config.get("channel_module_path", "channels/")

    global template_snapshot, logger_snapshot
    template_snapshot = db.collection("ChannelTemplates").document(template_id).get()
    logger_snapshot = db.collection("Loggers").document(logger_id).get()


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
    return logger_snapshot.to_dict()["channelTemplate"] != template_id


def channel_template_outdated():
    """
    Checks whether the config channel modified date is earlier than the server's modified date.

    :return: True if the config is outdated, otherwise False.
    """
    date_string = template_snapshot.to_dict()["modified"]
    return template_modified_date < datetime.strptime(date_string, template_modified_date_format)


def fetch():
    print("Hello")

    if channel_template_invalid():
        fetch_template()

    fetch_channels()

    Config.write_changes()


def fetch_template():
    global template_id, template_snapshot
    template_id = logger_snapshot.to_dict()["channelTemplate"]
    template_snapshot = db.collection("ChannelTemplates").document(template_id).get()

    config = Config.get()
    config["config"]["template_id"] = template_id


def fetch_channels():
    config = Config.get()
    bucket = storage.bucket("yada-comp451.appspot.com")

    downloaded_files = []

    template = template_snapshot.to_dict()
    for channel_name, filename in template["channels"].items():
        if filename in downloaded_files:
            continue

        blob = bucket.blob(f"{PREFIX}{filename}")
        blob.download_to_filename(f"{channel_module_path}{channel_name}.py")

        config[f"channel/{channel_name}"] = {
            "module": filename.replace(".py", "")
        }

    config["config"]["template_modified_date"] = template["modified"]


def upload_data(data):
    pass
