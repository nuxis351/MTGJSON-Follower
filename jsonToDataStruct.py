import collections
import json

import pandas as pd

from config import load_config

config = load_config()


def search_for_card():
    with open(config.all_cards_reduced_path, "r") as json_file:
        try:

            _json = json.load(json_file)["data"]
            # print(_json[])

        except ValueError:
            print("decoding JSON has failed")


def get_prices(price_json, uuid):
    p = {}
    try:
        card = price_json[uuid]
        if "paper" in card.keys():
            card = card["paper"]
            if "tcgplayer" in card.keys():
                card = card["tcgplayer"]
                if "retail" in card.keys():
                    retail = card["retail"]
                    retailDict = {}
                    for card_type in retail.keys():
                        retailDict[card_type] = retail[card_type][max(retail[card_type], key=lambda ev: ev)]
                    p["retail"] = retailDict

                if "buylist" in card.keys():
                    buylist = card["buylist"]
                    buylistDict = {}
                    for card_type in buylist.keys():
                        buylistDict[card_type] = buylist[card_type][max(buylist[card_type], key=lambda ev: ev)]
                    p["buylist"] = buylistDict

    except KeyError:
        print("card with uuid: " + uuid + " does not exist in price data")
    return p


def build_card_dictionary():
    d = {}
    with open(config.all_cards_path, "rb") as allCardsJSON:
        try:
            all_prices = json.load(open(config.all_prices_path, "rb"))["data"]
            all_card_sets = json.load(allCardsJSON)
            latest_date = all_card_sets["meta"]["date"]
            d["meta"] = latest_date
            all_card_sets = all_card_sets["data"]
            card_set_keys = list(all_card_sets.keys())
            for card_set in card_set_keys:
                cards_in_set = all_card_sets[card_set]["cards"]
                for set_card in cards_in_set:
                    key = set_card["name"]
                    prices = get_prices(all_prices, set_card["uuid"])
                    if key in d.keys():
                        existing_set = d[key]
                        existing_set[card_set] = {"uuid": set_card["uuid"], "prices": prices}
                        d[key] = existing_set
                    else:
                        d[key] = {card_set: {"uuid": set_card["uuid"], "prices": prices}}
        except ValueError:
            print("decoding JSON has failed")

    with open(config.all_cards_reduced_path, "w") as save_reduced_cards:
        try:
            save_reduced_cards.write(json.dumps(d, indent=4))
        except ValueError:
            print("error")


build_card_dictionary()
