from flask import Flask, render_template, request
import json, os, ast
import time, datetime

template_dir = os.path.abspath('../../templates')

app = Flask(__name__, template_folder=template_dir)


def time_converter(ms):
    sec = ms
    return datetime.datetime.fromtimestamp(sec).strftime('%m-%d-%Y %H:%M:%S.%f')


@app.route('/create_log', methods=['GET', 'POST'])
def create_log():
    if request.method == 'POST':
        print("in")
        keyword = request.json
        keyword = keyword['data']
        if keyword == "":
            return ''
        print(keyword)
        if not os.path.exists('log.txt'):
            read_mode = "w+"
        else:
            read_mode = "r"
        with open('log.txt', read_mode) as f:
            count = -1
            lines = f.readlines()
            for line in lines:
                data = ast.literal_eval(line)
                if data['keyword'] == keyword:
                    count = data['count']
            dic = {}
            dic['keyword'] = keyword
            dic['timestamp'] = time_converter(time.time())
            if count == -1:
                dic['count'] = 1
            else:
                dic['count'] = int(count) + 1
            print(dic)

        with open('log.txt', 'a') as f:
            print("appended")
            json.dump(dic, f, ensure_ascii=False)
            f.write("\n")
        # return render_template('index.html')
        return "<p>Log created with form data</p>"
    return "<p>Log created</p>"
    # return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5001")
