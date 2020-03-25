from pymongo import MongoClient
import requests
from flask import Flask, render_template, request, redirect, url_for
import json, os, ast, fileinput
from bson import json_util
import time, datetime
import re

client = MongoClient('mongodb://54.205.214.239', 27017)
books_db = client.books_db

books_collection = books_db.books
file_info_collection = books_db.file_info


template_dir = os.path.abspath('../../templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/search_catalogue', methods=['GET', 'POST'])
def search_catalogue():
    print("yes")
    if request.method == 'POST':
        print("in")
        keyword = request.json
        keyword = keyword['data']
        if keyword.strip() == "":
            return ''
        cur = list(books_collection.find({"$or": [{"title": {"$regex": keyword}}, {"author": {"$regex": keyword}}]}))
        print(cur)
        if len(cur) == 0:
            return ''
        # print(keyword, cur)
        json_docs = []
        for doc in cur:
            json_doc = json.dumps(doc, default=json_util.default)
            json_docs.append(json_doc)
        with open('catalogue.txt', 'a') as f:
            json.dump(json_docs, f, ensure_ascii=False)
            f.write("\n")
        data_list = []
        for item in cur:
            dic = {"title":item['title'], "author":item['author']}
            data_list.append(dic)
        return str(data_list)
        # return {'data':cur, 'keyword':keyword}
        # return render_template('index.html', data=cur, keyword=keyword)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5002")
