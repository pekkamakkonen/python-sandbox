import requests
import sqlite3


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

    def get_game_data(self):
        game_ids = self.get_game_ids()

        with sqlite3.connect("nhldb.sqlite3") as conn:

            for game_id in game_ids:
                url = f"https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live"
                response = requests.get(url)
                game_data = response.json()["gameData"]
                game = game_data["game"]
                date_time = game_data["datetime"]
                status = game_data["status"]
                venue = game_data["venue"]

                conn.execute("INSERT INTO Game VALUES (?, ?, ?, ?, ?, ?, ?)", (
                             game.get("pk"),
                             game.get("season"),
                             game.get("type"),
                             date_time.get("dateTime"),
                             date_time.get("endDateTime"),
                             status.get("statusCode"),
                             venue.get("name")
                             )
                             )
            conn.commit()

          #  games.append(game)
         #   print(game)
      #  return games

 #   def save_games(self):
 #       games = self.get_game_data()

#        for game in games:
 #           print(game)
            # print(response.text)


games = Game("20192020")
# games.get_game_ids()
games.get_game_data()
