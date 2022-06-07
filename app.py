from flask import Flask
from flask_cors import CORS
import const, utils

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r'*': {'origins': 'https://c2lv.github.io'}})

@app.route("/ambition", methods=["GET"])
def today_ambition_score():
    today_ambition_sub_score = utils.today_lol_score(const.AMBITION_SUB_ACCOUNT_ID, const.AMBITION_SUB_SUMMONER_ID)
    if type(today_ambition_sub_score) == dict:
        return today_ambition_sub_score
    today_ambition_main_score = utils.today_lol_score(const.AMBITION_MAIN_ACCOUNT_ID, const.AMBITION_MAIN_SUMMONER_ID)
    if type(today_ambition_main_score) == dict:
        return today_ambition_main_score
    youtubeComment = '오늘의 앰비션 점수\n' + today_ambition_sub_score + today_ambition_main_score
    return {"youtubeComment": youtubeComment}

@app.route("/by-name/<summoner_name>", methods=["GET"])
def today_summoner_score(summoner_name):
    account_id, summoner_id = utils.get_account_and_summoner_id(summoner_name)
    today_summoner_score = utils.today_lol_score(account_id, summoner_id)
    if type(today_summoner_score) == dict:
        return today_summoner_score
    youtubeComment = f'오늘의 {summoner_name} 점수\n' + today_summoner_score
    return {"youtubeComment": youtubeComment}