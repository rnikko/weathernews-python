import json


# comes from https://weathernews.jp/s/topics/img/wxicon/
# but that list is incomplete, I went and added to the JSON file
# below as I find filenames that were not on the list
icon_details = json.load(open("./weathernews/data/icon_details.json", "r"))
