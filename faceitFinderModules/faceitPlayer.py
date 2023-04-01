from faceitFinderModules.pythonValve.valve.steam.id import SteamID
from urllib.request import urlopen
import json
from api_keys import APIKEY

levelPath = [
"",
"https://beta.leetify.com/assets/images/rank-icons/faceit1.png",
"https://beta.leetify.com/assets/images/rank-icons/faceit2.png",
"https://beta.leetify.com/assets/images/rank-icons/faceit3.png",
"https://beta.leetify.com/assets/images/rank-icons/faceit4.png",
"https://beta.leetify.com/assets/images/rank-icons/faceit5.png",
"https://beta.leetify.com/assets/images/rank-icons/faceit6.png",
"https://beta.leetify.com/assets/images/rank-icons/faceit7.png",
"https://beta.leetify.com/assets/images/rank-icons/faceit8.png",
"https://beta.leetify.com/assets/images/rank-icons/faceit9.png",
"https://beta.leetify.com/assets/images/rank-icons/faceit10.png"
]

SteamAPI = APIKEY.getKey('steam')
GAMEKEY = "csgo"

def getNameSteamWithID(URL):
    url = str(URL).replace("https://", "")
    nameEnd = url.find('/', 23)
    name = url[22:] if nameEnd == -1 else url[22:nameEnd]
    url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={SteamAPI}&vanityurl={name}"
    response = urlopen(url)
    data = json.loads(response.read())
    return data['response']['steamid']

def getNameSteam(URL):
    url = str(URL)
    urlEnd = url.find('/', 37)
    if urlEnd != -1:
        url = url[:urlEnd]
    steam = SteamID.from_community_url(url)
    return steam.as_64()

def getNameFaceit(URL):
    url = str(URL).replace("https://", "")
    nameEnd = url.find('/', 27)
    name = url[26:] if nameEnd == -1 else url[26:nameEnd]
    print(name)
    return name

def average(list):
    total = 0
    for value in list:
        total += float(value)
    return total / len(list)


class faceitPlayer():
    def __init__(self, faceitAPI, URL, is20):
        self.faceitAPI = faceitAPI
        self.URL = URL
        self.playerData = {}
        if self.URL.find("steamcommunity.com/id/") != -1:
            self.playerData = self.faceitAPI.player_details(game_player_id=getNameSteamWithID(self.URL), game=GAMEKEY)
        elif self.URL.find("steamcommunity.com/profiles/") != -1:
            self.playerData = self.faceitAPI.player_details(game_player_id=getNameSteam(self.URL), game=GAMEKEY)
        elif self.URL.find("www.faceit.com/en/players/") != -1:
            self.playerData = self.faceitAPI.player_details(nickname=getNameFaceit(self.URL), game=GAMEKEY)
        self.playerID = self.playerData['player_id']
        self.playerStats = self.faceitAPI.player_stats(player_id=self.playerID, game_id=GAMEKEY)
        self.nickname = self.playerData['nickname']
        self.avatar = self.playerData['avatar']
        self.url = self.playerData['faceit_url']
        self.url = self.url.replace('{lang}', 'en')
        self.level = self.playerData['games'][GAMEKEY]['skill_level']
        self.elo = self.playerData['games'][GAMEKEY]['faceit_elo']
        self.levelIMG = levelPath[self.level]
        self.kd = self.playerStats['lifetime']['Average K/D Ratio']
        self.matches = self.playerStats['lifetime']['Matches']
        self.WRp = self.playerStats['lifetime']['Win Rate %']
        self.HSp = self.playerStats['lifetime']['Average Headshots %']
        self.winStreak = self.playerStats['lifetime']['Longest Win Streak']
        self.recentMatches = self.playerStats['lifetime']['Recent Results']
        if is20:
            kills20 = []
            KD20 = []
            KR20 = []
            HS20 = []
            games = []
            last20Matches = self.faceitAPI.player_matches(player_id=self.playerID, game=GAMEKEY)['items']
            last20ids = []
            for match in last20Matches:
                last20ids.append(match['match_id'])
            for matchID in last20ids:
                match = self.faceitAPI.match_stats(matchID)
                for rounds in match['rounds']:
                    fullScore = rounds['round_stats']['Score']
                    for team in rounds['teams']:
                        score = team['team_stats']['Final Score']
                        for player in team['players']:
                            if player['nickname'] == self.nickname:
                                kills20.append(player['player_stats']['Kills'])
                                KD20.append(player['player_stats']['K/D Ratio'])
                                KR20.append(player['player_stats']['K/R Ratio'])
                                HS20.append(player['player_stats']['Headshots %'])
                                scores = fullScore.split(' / ')
                                if score == scores[0]:
                                    myScore = int(scores[0])
                                    otherScore = int(scores[1])
                                elif score == scores[1]:
                                    myScore = int(scores[1])
                                    otherScore = int(scores[0])
                                else:
                                    self.kills20 = None
                                    self.KD20 = None
                                    self.KR20 = None
                                    self.HS20 = None
                                    self.games = None
                                    self.games2 = None
                                    return None
                                if myScore > otherScore:
                                    games.append('W')
                                elif myScore == otherScore:
                                    games.append('T')
                                else:
                                    games.append('L')
            
            self.kills20 = round(average(kills20), 2)
            self.KD20 = round(average(KD20), 2)
            self.KR20 = round(average(KR20), 2)
            self.HS20 = round(average(HS20), 2)
            self.games = "-".join(games[:10])
            self.games2 = "-".join(games[10:])
        
