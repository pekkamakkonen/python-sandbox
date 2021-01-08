import requests


class Game:
    def __init__(self, season):
        self.season = season

    def get_game_ids(self):
        url = f"https://statsapi.web.nhl.com/api/v1/schedule?season={self.season}&gameType=R,P"
        response = requests.get(url)
        dates = response.json()["dates"]
        game_ids = []

        for date in dates:
            for game in date["games"]:
                game_ids.append(game["gamePk"])
        return game_ids


games = Game("20172018")
games.get_game_ids()
