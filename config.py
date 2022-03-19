import sys

import yaml


class Config:
    def __init__(self):
        self.all_cards_path = ""
        self.all_prices_path = ""
        self.all_cards_reduced_path = ""
        self.card_list_path = ""

    def __repr__(self):
        return "{ \n\t" + self.all_cards_path + "\n\t" + self.all_prices_path + " }"


def load_config():
    with open("./res/config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
            config_obj = Config()
            config_obj.all_prices_path = config["paths"]["ALL_PRICES_PATH"]
            config_obj.all_cards_path = config["paths"]["ALL_CARDS_PATH"]
            config_obj.all_cards_reduced_path = config["paths"]["ALL_CARDS_REDUCED_PATH"]
            config_obj.card_list_path = config["paths"]["CARD_LIST_PATH"]
            return config_obj
        except yaml.YAMLError as exc:
            sys.exit(exc)
