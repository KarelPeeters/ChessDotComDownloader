import datetime
import os

import chessdotcom
from matplotlib import pyplot


def get_games(username: str):
    profile = chessdotcom.get_player_profile(username)

    joined_date = datetime.datetime.utcfromtimestamp(profile.json["joined"]).date()
    today = datetime.date.today()

    print(f"{username} joined {joined_date}")

    games = []
    for year in range(joined_date.year, today.year + 1):
        start_month = joined_date.month if year == joined_date.year else 1
        end_month = today.month if year == today.year else 12

        for month in range(start_month, end_month + 1):
            result = chessdotcom.get_player_games_by_month(username=username, year=year, month=month)
            games += result.json["games"]

    print(f"Found {len(games)} games")
    return games, joined_date


def calculate_times(games):
    times = []
    for game in games:
        epoch = game["end_time"]
        time = datetime.datetime.utcfromtimestamp(epoch).time()
        hour = time.hour + time.minute / 60
        times.append(hour)
    return times


def plot_times(username: str, times, join_date):
    pyplot.hist(times, bins=40)
    pyplot.xlim(0, 24)
    pyplot.xlabel("time (H)")
    pyplot.ylabel("number of games")
    pyplot.xticks(range(0, 24))

    today = datetime.date.today()
    pyplot.title(f"Time of games played by {username}\n{join_date} - {today}\nTotal {len(times)} games")


def save_player_plot(username: str):
    games, joined_date = get_games(username=username)
    times = calculate_times(games)
    plot_times(username, times, joined_date)

    os.makedirs("output", exist_ok=True)
    pyplot.savefig(f"output/{username}")
    pyplot.show()


def main():
    USER_NAMES = [
        "karelpeeters",
        "YaBoiJemo",
        "Robster2357",
        "W-KeyChess",
    ]

    for username in USER_NAMES:
        save_player_plot(username)


if __name__ == '__main__':
    main()
