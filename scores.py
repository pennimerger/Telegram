import requests, json, os
from dotenv import load_dotenv

load_dotenv()
# get live data by listening to sofascore
url = os.getenv("SOFA_LIVE_API")
payload = ""
headers = {"User-Agent": "insomnia/8.4.5"}

response = requests.request("GET", url, data=payload, headers=headers)
json_data = json.loads(response.text)

def get_scores():
    final = ''
    for i in json_data["events"]:
        league = i["tournament"]["name"]
        home_team = i["homeTeam"]["name"]
        away_team = i["awayTeam"]["name"]
        # min90_h_score = i["homeScore"]["normaltime"]
        # min90_a_score = i["awayScore"]["normaltime"]
        h_score = i["homeScore"]["current"]
        a_score = i["awayScore"]["current"]

        report = f"\n{league}\n{home_team} : {h_score} | {a_score} : {away_team}"
        final = final+report
    return final

# def get_teamscores(team="Your team"):
#     final = ''
#     for i in json_data["events"]:
#         league = i["tournament"]["name"]
#         home_team = i["homeTeam"]["name"]
#         away_team = i["awayTeam"]["name"]
#         h_score = i["homeScore"]["current"]
#         a_score = i["awayScore"]["current"]

#         if team in home_team or team in away_team:
#             report = f"\n{league}\n{home_team} : {h_score} | {a_score} : {away_team}"
#             final = final+report
#     return final

# sc = get_teamscores('Real')
# print(sc)

# sc = get_scores()
# print(sc[:100])