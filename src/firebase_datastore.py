from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, storage

import config
from config import Config

from network import Datastore


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

# The name of the file with database authentication credentials
credential_file = ""


@config.section("config")
def load_variables(section):
    """
    Loads configuration variables from the "config" section

    :param section: The configuration section
    """
    global logger_id, template_id, server_address, template_modified_date, template_modified_date_format
    global channel_module_path, credential_file

    logger_id = Config.required(section, "logger_id", "Logger ID is required")
    template_id = Config.required(section, "template_id", "Template ID is required")
    server_address = Config.required(section, "server_address", "Server address is required")
    template_modified_date_format = section.get("template_modified_date_format", "%Y-%m-%d %H:%M:%S.%f")
    channel_module_path = section.get("channel_module_path", "channels/")
    credential_file = Config.required(section, "credentials", "Credential file is required")

    if "template_modified_date" in section:
        template_modified_date = datetime.strptime(section["template_modified_date"], template_modified_date_format)


class FireDatastore(Datastore):
    def __init__(self):
        load_variables()

        self.cred = credentials.Certificate(f"secret/{credential_file}")
        firebase_admin.initialize_app(self.cred)

        self.db = firestore.client()

        self.template_snapshot = self.db.collection("ChannelTemplates").document(template_id).get()
        self.logger_snapshot = self.db.collection("Loggers").document(logger_id).get()

    def should_update_template(self):
        return self.channel_template_invalid() or self.channel_template_outdated()

    def channel_template_invalid(self):
        return self.logger_snapshot.to_dict()["channelTemplate"] != template_id

    def channel_template_outdated(self):
        date_string = self.template_snapshot.to_dict()["modified"]
        return template_modified_date < datetime.strptime(date_string, template_modified_date_format)

    def fetch(self):
        if self.channel_template_invalid():
            self.fetch_template()

        self.fetch_channels()

        Config.write_changes()

    def fetch_template(self):
        global template_id
        template_id = self.logger_snapshot.to_dict()["channelTemplate"]

        self.template_snapshot = self.db.collection("ChannelTemplates").document(template_id).get()

        Config.get()["config"]["template_id"] = template_id

    def fetch_channels(self):
        config = Config.get()
        bucket = storage.bucket("yada-comp451.appspot.com")

        downloaded_files = []

        template = self.template_snapshot.to_dict()
        for channel_name, filename in template["channels"].items():
            if filename in downloaded_files:
                continue

            blob = bucket.blob(f"{PREFIX}{filename}")
            blob.download_to_filename(f"{channel_module_path}{channel_name}.py")

            config[f"channel/{channel_name}"] = {
                "module": filename.replace(".py", "")
            }

        config["config"]["template_modified_date"] = template["modified"]

    def upload_data(self, data):
        self.db.collection("Loggers").document(logger_id).update({
            "data": firestore.firestore.ArrayUnion([data])
        })
