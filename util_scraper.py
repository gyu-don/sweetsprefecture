import os.path
import json
import requests
import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# 都道府県
prefs = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', 
    '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', 
    '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県',
    '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
    '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
    '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県',
    '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

# 県庁所在地、東京23区。
major_cities = {'札幌市': '北海道', '盛岡市': '岩手県', '仙台市': '宮城県',
    '水戸市': '茨城県', '宇都宮市': '栃木県', '前橋市': '群馬県', 'さいたま市': '埼玉県',
    '横浜市': '神奈川県', '金沢市': '石川県', '甲府市': '山梨県', '名古屋市': '愛知県',
    '津市': '三重県', '大津市': '滋賀県', '松江市': '島根県', '高松市': '香川県',
    '松山市': '愛媛県', '那覇市': '沖縄県',
    '足立区': '東京都', '荒川区': '東京都', '板橋区': '東京都', '江戸川区': '東京都',
    '大田区': '東京都', '葛飾区': '東京都', '北区': '東京都', '江東区': '東京都',
    '品川区': '東京都', '渋谷区': '東京都', '新宿区': '東京都', '杉並区': '東京都',
    '墨田区': '東京都', '世田谷区': '東京都', '台東区': '東京都', '中央区': '東京都',
    '千代田区': '東京都', '豊島区': '東京都', '中野区': '東京都', '練馬区': '東京都',
    '文京区': '東京都', '港区': '東京都', '目黒区': '東京都'}

def mk_major_cities():
    vals = major_cities.values()
    for pref in prefs:
        if pref not in vals:
            major_cities[pref[:-1] + '市'] = pref

mk_major_cities()

def find_pref(txt):
    for pref in prefs:
        if pref in txt:
            return pref
    for city in major_cities.keys():
        if city in txt:
            return major_cities[city]
    return ''


def get_domain(url):
    return urlparse(url).netloc


def get_soup(url):
    response = requests.get(url)
    html = response.text.encode(response.encoding)
    soup = BeautifulSoup(html, "lxml")
    return soup


def update(d):
    fname = 'shop/' + d['domain'] + '.json'
    if os.path.exists(fname) and d['lastChecked']['status'] == 'OK':
        with open(fname) as f:
            exists_json = json.load(f, encoding="utf-8")
        if exists_json['shops'] == d['shops']:
            d['lastUpdated'] = exists_json['lastUpdated']
        else:
            d['lastUpdated'] = d['lastChecked']
    else:
        d['lastUpdated'] = d['lastChecked']
    with open(fname, "w") as f:
        json.dump(d, f, ensure_ascii=False)


def do_scraping(name, url, shoplist_finder, name_finder, address_finder):
    ls = []
    d = {'name': name, 'url': url, 'domain': get_domain(url), 'shops': ls}
    soup = get_soup(url)
    status = 'OK'
    t = shoplist_finder(soup)
    for s1, s2 in zip(name_finder(t), address_finder(t)):
        try:
            name = s1.text.strip()
            address = s2.text.strip()
            pref = find_pref(address)
            if not pref:
                status = "Failure to find a prefecture."
            ls.append({
                'name': name,
                'address': address,
                'pref': pref })
        except:
            status = "Failure to parse."
    d['lastChecked'] = {'date': datetime.datetime.now().isoformat(), 'status': status}
    update(d)
