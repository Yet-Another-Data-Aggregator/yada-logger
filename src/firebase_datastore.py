import config
import firebase_admin
import os
import os.path
import re
import time
from config import Config
from datetime import datetime
from firebase_admin import credentials, firestore, storage
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

notes = ""


@config.section("config")
def load_variables(section):
    """
    Loads configuration variables from the "config" section

    :param section: The configuration section
    """
    global logger_id, template_id, server_address, template_modified_date, template_modified_date_format
    global channel_module_path, credential_file, notes

    logger_id = section.get("logger_id", None)
    template_id = section.get("template_id", None)
    server_address = Config.required(section, "server_address", "Server address is required")
    template_modified_date_format = section.get("template_modified_date_format", "%Y-%m-%d %H:%M:%S.%f")
    channel_module_path = section.get("channel_module_path", "channels/")
    credential_file = Config.required(section, "credentials", "Credential file is required")
    notes = section.get("notes", "")

    if "template_modified_date" in section:
        template_modified_date = datetime.strptime(section["template_modified_date"], template_modified_date_format)


class FireDatastore(Datastore):
    def __init__(self, should_update_callback):
        load_variables()

        self.cred = credentials.Certificate(f"secret/{credential_file}")
        firebase_admin.initialize_app(self.cred)

        self.db = firestore.client()

        if logger_id is not None and logger_id != "":
            self.logger_snapshot = self.db.collection("Loggers").document(logger_id).get()
        else:
            self.create_logger()

        def set_should_update(doc_snapshot, changes, real_time):
            should_update_callback(doc_snapshot[0].to_dict()["collectingData"])

        self.db.collection("Loggers").document(logger_id).on_snapshot(set_should_update)

        if template_id is not None and template_id != "":
            self.template_snapshot = self.db.collection("ChannelTemplates").document(template_id).get()
        else:
            self.template_snapshot = None

    def create_logger(self):
        reference = self.db.collection("Loggers").add({
            "channelTemplate": "",
            "data": [],
            "collectingData": True,
            "equipment": "",
            "faults": [],
            "name": "",
            "site": "",
            "ip": "",
            "mac": "",
            "notes": notes,
        })

        self.logger_snapshot = reference[1].get()

        global logger_id
        logger_id = reference[1].id

        Config.get()["config"]["logger_id"] = logger_id
        Config.write_changes()

    def should_update_template(self):
        return self.channel_template_invalid() or  self.channel_template_outdated()

    def channel_template_invalid(self):
        return self.logger_snapshot.to_dict()["channelTemplate"] != template_id

    def channel_template_outdated(self):
        date_string = self.template_snapshot.to_dict()["modified"]
        return template_modified_date < datetime.strptime(date_string, template_modified_date_format)

    def fetch(self):
        # Update notes if they have changed
        if Config.get()["config"]["notes"] != notes:
            self.update_notes()

        while self.template_snapshot is None or template_id == "":
            self.fetch_template()

            if self.template_snapshot is None or template_id == "":
                time.sleep(5)

        self.fetch_channels()

        Config.write_changes()

    def update_notes(self):
        self.db.collection("Loggers").document(logger_id).update({
            "notes": Config.get["config"]["notes"]
        })

    def fetch_template(self):
        global template_id
        template_id = self.logger_snapshot.to_dict()["channelTemplate"]

        if template_id == "" or template_id is None:
            return

        self.template_snapshot = self.db.collection("ChannelTemplates").document(template_id).get()

        Config.get()["config"]["template_id"] = template_id

    def fetch_channels(self):
        config = Config.get()
        bucket = storage.bucket("yada-comp451.appspot.com")

        for key in filter(lambda section: section.startswith("channel/"), config.sections()):
            config.remove_section(key)

        for root, dirs, files in os.walk(channel_module_path):
            for file in files:
                os.remove(os.path.join(root, file))

        template = self.template_snapshot.to_dict()
        for channel_name, filename in template["channels"].items():
            blob = bucket.blob(f"{PREFIX}{filename['script']}")
            blob.download_to_filename(f"{channel_module_path}{channel_name}.py")

            config[f"channel/{channel_name}"] = {
                "module": filename['script'].replace(".py", "")
            }

        config["config"]["template_modified_date"] = template["modified"]

    def upload_data(self, data):
        self.db.collection("Loggers").document(logger_id).update({
            "data": firestore.firestore.ArrayUnion(data)
        })

    def upload_faults(self, faults):
        self.db.collection("Loggers").document(logger_id).update({
            "faults": firestore.firestore.ArrayUnion(faults)
        })

        self.db.collection("Notifications").add({
            "logger": logger_id,
            "message": f"The following faults occurred for logger {logger_id}:\n {str(faults)}"
        })
