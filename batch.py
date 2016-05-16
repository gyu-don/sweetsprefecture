#!/usr/bin/python3

# scraping以外の処理を行う。

import os
import json

SHOP_DIR = "shop/"

ls = []
for fname in os.listdir(SHOP_DIR):
    with open(SHOP_DIR + fname) as f:
        ls.append({"name": json.load(f)["name"], "json": SHOP_DIR + fname})

with open("shoplist.json", "w") as out:
    json.dump(ls, out, ensure_ascii=False)
