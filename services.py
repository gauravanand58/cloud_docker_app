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

app = Flask(__name__)

def time_converter(ms):
    sec = ms
    return datetime.datetime.fromtimestamp(sec).strftime('%m-%d-%Y %H:%M:%S.%f')

@app.route('/')
def index():
    return render_template('index.html', data=None, res="Enter a keyword")

@app.route('/search', methods=['GET', 'POST'])
def create_log_and_search():
    if request.method == 'POST':
        keyword = request.form.get('book')
        payload = {'data': keyword}
        headers = {'content-type': 'application/json'}
        print(keyword)
        log_response=requests.post('http://log:5001/create_log', data=json.dumps(payload), headers=headers)
        if log_response.text == "":
            return render_template('index.html', data=None, res="Enter a valid keyword")
        print(log_response)
        search_catalogue_response = requests.post('http://catalogue:5002/search_catalogue', data=json.dumps(payload), headers=headers)
        print(search_catalogue_response.text)
        if search_catalogue_response.text == "":
            return render_template('index.html', data=None, res="Enter a valid keyword")
        print(search_catalogue_response.text)
        l = ast.literal_eval(search_catalogue_response.text)
        return render_template('index.html', data=l, keyword=keyword)
    return render_template('index.html', data=None, res="Enter a keyword")

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        note = request.form.get('note')
        payload = {'keyword': keyword, 'note': note}
        headers = {'content-type': 'application/json'}
        log_response = requests.post('http://notes:5003/add_note', data=json.dumps(payload), headers=headers)
        return render_template('index.html', data=None, res="Note added successfully")
    return render_template('index.html', data=None, res="empty")

@app.route('/get_notes', methods=['GET', 'POST'])
def get_notes():
    if request.method == 'POST':
        keyword = request.form.get('book')
        payload = {'keyword': keyword}
        headers = {'content-type': 'application/json'}
        log_response = requests.post('http://notes:5003/get_notes', data=json.dumps(payload), headers=headers)
        if log_response.text == '':
            return render_template('index.html', data=None, res="No notes found")
        else:
            l = ast.literal_eval(log_response.text)
            return render_template('index.html', notes=l, res="")
    return render_template('index.html', data=None, res="")


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port="5000")
