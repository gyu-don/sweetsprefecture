#!/usr/bin/python3

# scraping以外の処理を行う。

import os
import json
from pprint import pprint

SHOP_DIR = "shop/"

prefs = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', 
    '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', 
    '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県',
    '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
    '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
    '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県',
    '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県', '不明']

ls = []
pref_dict = {pref: [] for pref in prefs}

for fname in os.listdir(SHOP_DIR):
    with open(SHOP_DIR + fname) as f:
        obj = json.load(f)
        shop = {"name": obj["name"], "json": SHOP_DIR + fname}
        ls.append(shop)
        for k in obj["shops"]:
            pref_dict[k].append(shop)

#with open("shoplist.json", "w") as out:
#    json.dump(ls, out, ensure_ascii=False)

with open("preflist.json", "w") as out:
    json.dump(pref_dict, out, ensure_ascii=False)
