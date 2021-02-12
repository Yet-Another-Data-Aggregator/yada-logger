import config_utils

logger_id = ""
template_id = ""
server_address = ""


def initialize(config):
    global logger_id, template_id, server_address

    if "config" not in config:
        return

    config = config["config"]

    logger_id = config_utils.required(config, "logger_id", "Logger ID is required")
    template_id = config_utils.required(config, "template_id", "Template ID is required")
    server_address = config_utils.required(config, "server_address", "Server address is required")

