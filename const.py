import os
from pytz import timezone

TIER = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
RANK = ['I', 'II', 'III', 'IV']
GET_A_SUMMONER_HEAD_URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
GET_LEAGUE_ENTRIES_IN_ALL_QUEUES_HEAD_URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"
FOW_KR_SUMMONER_SEARCH_HEAD_URL = 'http://fow.kr/find/'
AMBITION_MAIN_ACCOUNT_ID = "4loQSUxcaUtJQ353pR6Qa7oYVWeWfITQ6SY-_QJdzDhu"
AMBITION_SUB_ACCOUNT_ID = "oLRxI--OhFkFlvVsZ-PCyrM27EydrltshVtwV8glyjo"
AMBITION_MAIN_SUMMONER_ID = "RGEp5dohxYE4WQfv8-yhSPr5ypuHtd9PXP0m-HHckXn84g"
AMBITION_SUB_SUMMONER_ID = "pAfu9zAEyDbcQeDuRe3IVLyV6W3s2gkm1hNPF4CBP3Sa2g"
KST = timezone('Asia/Seoul')

DEVELOPMENT_API_KEY = os.environ.get('RIOTGAMES_API_KEY')