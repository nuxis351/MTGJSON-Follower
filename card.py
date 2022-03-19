import json
import sys

import yaml


class CardList:
    def __init__(self):
        self.list = {}

    def add_card(self, name, card_set, card_type, quantity):
        self.list[card_set + "-" + name + "-" + card_type] = \
            {"name": name, "set": card_set, "type": card_type, "quantity": quantity}

    def add_price(self, key, type, price):
        key_value = self.list[key]
        key_value[type+"-price"] = price
        self.list[key] = key_value

    def __repr__(self):
        str_return = ""
        for key in self.list.keys():
            str_return += key + " -> " + json.dumps(self.list[key]) + "\n"
        return str_return


def load_card_list(path):
    card_list_obj = CardList()
    with open(path, "r") as stream:
        try:
            card_list = yaml.safe_load(stream)
            for card in card_list["cards"]:
                card_list_obj.add_card(card["name"], card["set"], card["type"], card["quantity"])
        except yaml.YAMLError as exc:
            sys.exit(exc)

    return card_list_obj
