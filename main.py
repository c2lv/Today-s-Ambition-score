import os, requests, time
from bs4 import BeautifulSoup

"""
Const
"""
TIER = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
RANK = ['I', 'II', 'III', 'IV']
GET_A_SUMMONER_HEAD_URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
GET_LEAGUE_ENTRIES_IN_ALL_QUEUES_HEAD_URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"
FOW_KR_SUMMONER_SEARCH_HEAD_URL = 'http://fow.kr/find/'
AMBITION_MAIN_ACCOUNT_ID = "4loQSUxcaUtJQ353pR6Qa7oYVWeWfITQ6SY-_QJdzDhu"
AMBITION_SUB_ACCOUNT_ID = "oLRxI--OhFkFlvVsZ-PCyrM27EydrltshVtwV8glyjo"
AMBITION_MAIN_SUMMONER_ID = "RGEp5dohxYE4WQfv8-yhSPr5ypuHtd9PXP0m-HHckXn84g"
AMBITION_SUB_SUMMONER_ID = "pAfu9zAEyDbcQeDuRe3IVLyV6W3s2gkm1hNPF4CBP3Sa2g"

DEVELOPMENT_API_KEY = os.environ.get('RIOTGAMES_API_KEY')

"""
Function
"""
def get_account_and_summoner_id(summoner_name):
    get_a_summoner_url = GET_A_SUMMONER_HEAD_URL + summoner_name \
        + '?api_key=' + DEVELOPMENT_API_KEY
    response = requests.get(get_a_summoner_url)
    if response.status_code == 200:
        return response.json()['accountId'], response.json()['id']
    else:
        return response.status_code, response.reason

def get_today_wins_losses_and_ranking(summoner_name):
    fow_kr_summoner_search_url = FOW_KR_SUMMONER_SEARCH_HEAD_URL + summoner_name
    response = requests.get(fow_kr_summoner_search_url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        ranking = soup.find("span", attrs={"class":"tipsy_live"}).attrs['tipsy'].split()[2]
        wins_losses = {"승": 0, "패": 0}
        for i in range(1, 21):
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            record_start_time = soup.select_one(f'body > div:nth-child(7) > div:nth-child(1) > div:nth-child(2) > div.div_recent > table.tablesorter.table_recent > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(10) > span.tipsy_live').attrs['tipsy'].split()[1]
            if today == record_start_time:
                record = soup.select_one(f'body > div:nth-child(7) > div:nth-child(1) > div:nth-child(2) > div.div_recent > table.tablesorter.table_recent > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(1)').text
                wins_losses[record] += 1
        if wins_losses['승'] == wins_losses['패'] == 0:
            today_wins_losses = '전적없음'
        else:
            today_wins_losses = f"{wins_losses['승']}승 {wins_losses['패']}패"
        return today_wins_losses, ranking
    else:
        return response.status_code, response.reason

def today_lol_score(account_id, summoner_id):
    if type(account_id) == int:
        return f'get_account_and_summoner_id() Error: {account_id} {summoner_id}'
    get_league_entries_in_all_queues_url = GET_LEAGUE_ENTRIES_IN_ALL_QUEUES_HEAD_URL \
        + summoner_id \
        + '?api_key=' + DEVELOPMENT_API_KEY
    response = requests.get(get_league_entries_in_all_queues_url)
    summoner = response.json() # Unranked return empty list
    if not summoner:
        return 'Unranked'
    elif response.status_code == 200: # 200: OK
        for data in summoner:
            if data['queueType'] == "RANKED_SOLO_5x5":
                summoner = data
                break
        today_wins_losses, ranking = get_today_wins_losses_and_ranking(summoner["summonerName"])
        if type(today_wins_losses) == int:
            return f'get_today_wins_losses_and_ranking() Error: {today_wins_losses} {ranking}'
        tier = summoner["tier"][0] if summoner["tier"] != TIER[7] else 'GM'
        if summoner["tier"] not in TIER[6:]:
            for i in range(len(RANK)):
                if summoner["rank"] == RANK[i]:
                    tier += str(i + 1)
        today_lol_score = f'[{summoner["summonerName"]} - {ranking}] ({today_wins_losses})\n' \
            + f'{tier} {summoner["leaguePoints"]}P - {summoner["wins"]}승 {summoner["losses"]}패\n'
        return today_lol_score
    else:
        return f'today_lol_score() Error: {response.status_code} {response.reason}'

"""
Run
"""
title = '오늘의 앰비션 점수\n'
today_ambition_sub_score = today_lol_score(AMBITION_SUB_ACCOUNT_ID, AMBITION_SUB_SUMMONER_ID)
today_ambition_main_score = today_lol_score(AMBITION_MAIN_ACCOUNT_ID, AMBITION_MAIN_SUMMONER_ID)
additional_comments = '이 남자.. 챌린저에선 어떨까?'

print(title + today_ambition_sub_score + today_ambition_main_score + additional_comments)
