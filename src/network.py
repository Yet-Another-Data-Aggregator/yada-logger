class Datastore:
    def __init__(self):
        pass

    def should_update_template(self):
        """
        Checks whether the channel template should be updated.

        :return: True if the template should be updated, otherwise False.
        """
        pass

    def channel_template_invalid(self):
        """
        Checks if the config template id is the same as the server's template id.

        :return: True if the template is incorrect, otherwise False.
        """
        pass

    def channel_template_outdated(self):
        """
        Checks whether the config channel modified date is earlier than the server's modified date.

        :return: True if the config is outdated, otherwise False.
        """
        pass

    def fetch(self):
        pass

    def fetch_template(self):
        """
        Fetches the new or updated template from the database.
        """
        pass

    def fetch_channels(self):
        """
        Downloads new or updated channels from database.
        """
        pass

    def upload_data(self, data):
        """
        Uploads the given data to the database.

        :param data: The data as a dictionary to be added to this Logger's data
        """
        pass
