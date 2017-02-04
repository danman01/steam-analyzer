import json
import requests
import requests_cache

requests_cache.install_cache('api_cache')

APIPATH = r'C:\api_keys.json'
cred = json.load(open(APIPATH))
STEAM_API_KEY = cred["STEAM_API_KEY"]
STEAM_USER_URL = "http://api.steampowered.com/ISteamUser/{}/{}/"
STEAM_PLAYER_URL = "http://api.steampowered.com/IPlayerService/{}/{}/"
VERSION = 'v0002'



def make_steam_request(steam_url, endpoint, version, payload):
    """
    Make a GET request to a steam endpoint with the provided version.

    :param endpoint: string endpoint attached to STEAM_USER_URL
    :param version: string 'v0001' or 'v0002'
    :param payload: dictionary of GET params to send to endpoint
    :return: json response from server
    """

    url = steam_url.format(endpoint, version)
    response = requests.get(url, params=payload).json()
    return response


def get_persona_name(steam_id):
   # get custom player summary using key and provided user ID
   payload = {
       'key': STEAM_API_KEY,
       'steamids': steam_id,
   }
   json_response = make_steam_request(
       steam_url = STEAM_USER_URL,
       endpoint = "GetPlayerSummaries",
       version = VERSION,
       payload = payload,
   )
   # drill down into player summary JSON and get persona name
   persona_name = json_response["response"]["players"][0]["personaname"]
   # return the persona name
   return persona_name

def get_avatar(steam_id):
   # get custom player summary using key and provided user ID
   payload = {
       'key': STEAM_API_KEY,
       'steamids': steam_id,
   }
   json_response = make_steam_request(
       steam_url = STEAM_USER_URL,
       endpoint = "GetPlayerSummaries",
       version = VERSION,
       payload = payload,
   )
   # drill down into player summary JSON and get avatar
   avatar = json_response["response"]["players"][0]["avatarfull"]
   # return the avatar
   return avatar


def get_friends_list(steam_id):
   # get custom friends list using key and provided user ID

   friends_json =  requests.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={0}&steamid={1}&relationship=friend".format( STEAM_API_KEY, steam_id)).json()
   # drill down into JSON and get friends list
   friends_list = friends_json["friendslist"]["friends"]
   # return the friends list
   return friends_list


def get_game_list(steam_id):
   # get custom games list using key and provided user ID
   games_json =  requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&include_appinfo=1".format( STEAM_API_KEY, steam_id)).json()
   # drill down into JSON and get games list and count
   game_list = games_json["response"]["games"]
   game_count = games_json["response"]["game_count"]
   # return the games list
   return {'count': game_count ,'games': game_list}