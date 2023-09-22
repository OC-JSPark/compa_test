from flask import Flask, render_template, jsonify, request, redirect, url_for
import jwt
from datetime import datetime, timedelta
import hashlib
from pymongo import MongoClient
import math

from d7 import *
from bson import json_util, ObjectId

SECRET_KEY = 'DTAAS'

app = Flask(__name__)

client = MongoClient('mongodb://127.0.0.1', 27017, username="dtaas", password="dtaas")
db = client.flask

# news_data = [
#     {"title": "카드 뉴스 1", "content": "카드 뉴스 내용 1"},
#     {"title": "카드 뉴스 2", "content": "카드 뉴스 내용 2"},
#     {"title": "카드 뉴스 3", "content": "카드 뉴스 내용 3"},
#     {"title": "카드 뉴스 4", "content": "카드 뉴스 내용 4"},
#     {"title": "카드 뉴스 5", "content": "카드 뉴스 내용 5"},
# ]

@app.route('/')
def home():
    news_data = db.newsData.find()
    return render_template('index.html', news_data=news_data)

@app.route('/about_us', methods=['GET', 'POST'])
def about_us():
    page = int(request.args.get('page', 1))
    per_page = 5
    total_posts = db.post.count_documents({})
    total_pages = (total_posts + per_page - 1) // per_page
    offset = (page - 1) * per_page

    posts = db.post.find().skip(offset).limit(per_page)
    post_id = -1
    return render_template('ubout_us.html', posts=posts, current_page=page, total_pages=total_pages, post_id=post_id)

@app.route('/about_us/<post_id>')
def show_post(post_id):
    post = db.post.find_one({'_id': ObjectId(post_id)})
    return render_template('ubout_us.html', post=post, post_id=post_id)

@app.route('/service')
def service():
    return render_template('service.html')

# 검색
@app.route('/search', methods=['GET', 'POST'])
# ,appno,문헌종류코드,appdate,pubno,pubdate,공고번호,공고일,regNo,regDate,국가코드,country,특실구분,devName,발명의 명칭(영문),appname,출원인(영문),출원인 국적,출원인 대표명화 코드,출원인 대표명화 명칭(영문),출원인 대표명화 명칭(국문),inventor,발명자/고안자 국적,agent,우선권 번호,우선권 국가,우선권 주장일,Original CPC Main,Original CPC All,Original IPC Main,Original IPC All,Current CPC Main,Current CPC All,Current IPC Main,Current IPC All,IPC 건수,인용 문헌 수(B1),인용 문헌번호 (B1),심사관인용문헌(B1),비 특허 참고문헌(B1),인용 문헌 수(F1),인용 문헌번호 (F1),심사관인용문헌(F1),패밀리 문헌번호 (출원기준),패밀리 문헌 수 (출원기준),패밀리 개별국 문헌수(출원기준),패밀리 국가수(출원기준),상태정보,심사청구 여부,존속기간(예상)만료일,현재권리자,통상권자,전용권자,summary,mainClaim,청구항수,독립항,종속항,description,idx,bio

# 출원번호, 출원일, 등록번호, 발명의 명칭, 대표청구항, 발명자, 출원인, 출원인?
# appno, appdate, regNo, devName, mainClaim, inventor, 출원인(영문), appname
def go_search():
    data = []
    page = request.args.get("page", 1, type=int)
    limit = 10
    if request.args.get('keyword'):
        key = request.args.get('keyword')
        ser =[{"출원번호": {'$regex': key}}, {"발명자" : { '$regex' : key }}, {"발명의 명칭": {'$regex': key}}, {"대표청구항": {'$regex': key}}, {"출원인": {'$regex': key}}, {"등록번호": {'$regex': key}}, {"메인 IPC": {'$regex': key}}, {"출원일": {'$regex': key}}]

        data = db.data.find({"$or":[ser[0]]}).skip((page - 1) * limit).limit(limit)
        total_count = db.data.count_documents({"$or":[ser[0]]})
        last_page_num = math.ceil(total_count / limit)

        block_size = 5
        block_num = int((page - 1) / block_size)
        block_start = (block_size * block_num) + 1
        block_end = block_start + (block_size - 1)

        return render_template('ser_result.html', data = data, limit = limit, page = page, key = key, total_count = total_count,
                                block_start = block_start, block_end = block_end, last_page_num = last_page_num)

    else:
        if request.args.get("app_num") or request.args.get("app_date") or request.args.get("reg_num") or request.args.get("in_title") or request.args.get("represent") or request.args.get("applicant") or request.args.get("inventor") or request.args.get("ipc"):
            keys = []
            counts = []
            key_val = [None]*8
            ko = ["출원번호", "출원일", "등록번호", "발명의 명칭", "대표청구항", "출원인", "발명자", "메인 IPC"]
            en = ["app_num", "app_date", "reg_num", "in_title", "represent", "applicant", "inventor", "ipc"]
            for i, val in enumerate(ko):
                if request.args.get(en[i]):
                    keys.append("\""+ ko[i] +"\": " + request.args.get(en[i]))
                    counts.append("\""+ ko[i] +"\": " + str({'$regex': request.args.get(en[i])}))
                    key_val[i] = request.args.get(en[i])

            if len(counts) != 1:
                count = ', '.join(map(str, counts))
                key = ', '.join(keys)
                count = eval("{" + count + "}")
            else:
                count = eval("{" + counts[0] + "}")
                key = keys[0]

            data = db.data.find(count).skip((page - 1) * limit).limit(limit)

            if data:
                total_count = db.data.count_documents(count)
            else:
                data = Null
                total_count = 0

            last_page_num = math.ceil(total_count / limit)

            block_size = 5
            block_num = int((page - 1) / block_size)
            block_start = (block_size * block_num) + 1
            block_end = block_start + (block_size - 1)

            return render_template('ser_result.html', data = data, limit = limit, page = page, key = key, total_count = total_count,
                                key_val = key_val, block_start = block_start, block_end = block_end, last_page_num = last_page_num)
        else:
            return render_template('service.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/sitemap')
def sutemap():
    return render_template('site_map.html')

@app.template_filter('enumerate')
def jinja2_enumerate(iterable, start=0):
    return enumerate(iterable, start)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)