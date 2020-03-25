from pymongo import MongoClient
import requests
from flask import Flask, render_template, request, redirect, url_for
import json, os, ast, fileinput
from bson import json_util
import time, datetime
import re

template_dir = os.path.abspath('../../templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/get_notes', methods=['GET', 'POST'])
def get_notes():
    if request.method == 'POST':
        params = request.json
        print(params)
        keyword = params['keyword']
        if keyword.strip() == "":
            return ''
        if not os.path.exists('notes.txt'):
            return ''
        with open('notes.txt', 'r') as f:
            lines = f.readlines()
            match = {}
            for line in lines:
                data = ast.literal_eval(line)
                if data['keyword'] == keyword:
                    match = data

            if not (match):
                return ''
            else:
                print(match['notes'])
                return str(match['notes'])
                # return render_template('index.html', notes=match['notes'])
    return ''


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        # print("in")
        params = request.json
        print(params)
        keyword = params['keyword']
        note = params['note']
        print(keyword)
        if not os.path.exists('notes.txt'):
            read_mode = "w+"
        else:
            read_mode = "r"
        with open('notes.txt', read_mode) as f:
            lines = f.readlines()
            print(lines)
            if len(lines) == 0:
                dic = {}
                dic['keyword'] = keyword
                dic['notes'] = [note]
            else:
                match = {}
                for line in lines:
                    data = ast.literal_eval(line)
                    if data['keyword'] == keyword:
                        match = data
                        print("new: ")
                        print(data['notes'])
                        print("\n")
                if not (match):
                    dic = {}
                    dic['keyword'] = keyword
                    dic['notes'] = [note]
                else:
                    match['notes'].append(note)
                    dic = {}
                    dic = match
        with open('notes.txt', 'a') as f:
            print("appended")
            json.dump(dic, f, ensure_ascii=False)
            f.write("\n")
        return ''
        # return render_template('index.html', data=None)
    return ''
    # return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5003")
