# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import json
import bigjson
import pathlib
import pandas as pd
import config

import requests

import card

ALL_PRICES_PATH = pathlib.Path("AllPrintings.json")

config = config.load_config()


def today_date():
    return datetime.date.today().strftime('%Y-%m-%d')


my_cards = card.load_card_list(config.card_list_path)

with open(config.all_cards_reduced_path, "r") as card_ref:
    try:
        card_ref_json = json.load(card_ref)
        card_list = my_cards.list
        for card_key in card_list.keys():
            current_card = card_list[card_key]
            if current_card["name"] in card_ref_json.keys():
                select_ref_card = card_ref_json[current_card["name"]]
                if current_card["set"] in select_ref_card.keys():
                    select_set_ref_card = select_ref_card[current_card["set"]]["prices"]
                    if len(select_set_ref_card.keys()) > 0:
                        for buy_option in select_set_ref_card.keys():
                            buy_format = select_set_ref_card[buy_option]
                            if current_card["type"] in buy_format.keys():
                                my_cards.add_price(card_key, buy_option, buy_format[current_card["type"]])
                            else:
                                print("there is no " + current_card["type"] + " price data in " + buy_option + " for " +
                                      current_card["name"] + " in the set " + current_card["set"])
                    else:
                        print("there are no prices for " + current_card["name"] + " in set: " +
                              current_card["set"] + "in reference document")
                else:
                    print(current_card["name"] + " does not have set: " +current_card["set"] + " in reference document")
            else:
                print(current_card["name"] + " is missing from the reference document")
    except ValueError:
        print("an error has occurred reading the reduced card file")

print(my_cards)
# allPrices = requests.get('https://mtgjson.com/api/v5/AllPrices.json')
