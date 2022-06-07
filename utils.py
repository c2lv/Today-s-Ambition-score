import requests, time, const
from bs4 import BeautifulSoup

def get_account_and_summoner_id(summoner_name):
    get_a_summoner_url = const.GET_A_SUMMONER_HEAD_URL + summoner_name \
        + '?api_key=' + const.DEVELOPMENT_API_KEY
    response = requests.get(get_a_summoner_url)
    if response.status_code == 200:
        return response.json()['accountId'], response.json()['id']
    else:
        return response.status_code, response.reason

def get_today_wins_losses_and_ranking(summoner_name):
    fow_kr_summoner_search_url = const.FOW_KR_SUMMONER_SEARCH_HEAD_URL + summoner_name
    response = requests.get(fow_kr_summoner_search_url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        ranking = soup.find("span", attrs={"class":"tipsy_live"}).attrs['tipsy'].split()[2]
        wins_losses = {"승": 0, "패": 0}
        for i in range(1, 21):
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            record_start_time = soup.select_one(f'body > div:nth-child(7) > div:nth-child(1) > div:nth-child(2) > div.div_recent > table.tablesorter.table_recent > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(10) > span.tipsy_live').attrs['tipsy'].split()[1]
            game_type = soup.select_one(f'body > div:nth-child(7) > div:nth-child(1) > div:nth-child(2) > div.div_recent > table.tablesorter.table_recent > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(3)').text
            if today == record_start_time and game_type == '랭크':
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
        return {"message": summoner_id, "status_code": account_id}
    get_league_entries_in_all_queues_url = const.GET_LEAGUE_ENTRIES_IN_ALL_QUEUES_HEAD_URL \
        + summoner_id \
        + '?api_key=' + const.DEVELOPMENT_API_KEY
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
            return {"message": today_wins_losses, "status_code": ranking}
        tier = summoner["tier"][0] if summoner["tier"] != const.TIER[7] else 'GM'
        if summoner["tier"] not in const.TIER[6:]:
            for i in range(len(const.RANK)):
                if summoner["rank"] == const.RANK[i]:
                    tier += str(i + 1)
        today_lol_score = f'[{summoner["summonerName"]} - {ranking}] ({today_wins_losses})\n' \
            + f'{tier} {summoner["leaguePoints"]}P - {summoner["wins"]}승 {summoner["losses"]}패\n'
        return today_lol_score
    else:
        return {"message": response.reason, "status_code": response.status_code}