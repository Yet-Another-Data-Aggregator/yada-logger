import configparser

from src.channel import from_config

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    print(config.sections())

    for key in filter(lambda section: section.startswith("channel/"), config.sections()):
        device = from_config(config[key])
        print(device)
        device.write_to_config(config)

    with open("config.ini", "w") as config_file:
        config.write(config_file)