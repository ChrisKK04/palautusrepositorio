import sys

from rich.console import Console
from rich.table import Table

from player_reader import PlayerReader
from player_stats import PlayerStats

console = Console()

VALID_SEASONS = ["2018-19", "2019-20", "2020-21", "2021-22",
                 "2022-23", "2023-24", "2024-25", "2025-26"]

def season_input():
    while True:
        console.print(
            "Season [bold magenta]"
            f"[{"/".join(VALID_SEASONS)}]"
            "[/bold magenta] "
            "[bold cyan]2024-25[/bold cyan]:", end=" ")
        season = input()
        if season == "":
            season = "2024-25"
        elif season not in VALID_SEASONS:
            console.print("[red]Give a valid season![/red]")
            continue
        elif season == "exit":
            sys.exit(0)

        return season

def nationality_input(players):
    nationalities = "/".join(sorted(players.different_nationalities()))
    console.print(
        f"Nationality [bold magenta][{nationalities}][/bold magenta] "
        "[bold cyan]()[/bold cyan]:", end=" ")
    nationality = input()
    if nationality == "":
        nationality = "FIN"
    if nationality == "exit":
        sys.exit(0)

    return nationality

def players_for_table(season):
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    players_json = PlayerReader(url)
    return PlayerStats(players_json.get_players())


def rich_player_table(season, nationality, players):
    table = Table(title=f"Season {season} players from {nationality}")
    table.add_column("Players", style="cyan")
    table.add_column("Teams", style="magenta")
    table.add_column("goals", style="green")
    table.add_column("assists", style="green")
    table.add_column("points", style="green")

    for player in players:
        table.add_row(player.name, player.team,
                        str(player.goals), str(player.assists), str(player.points))

    return table

def main():
    console.print("[red]Exit[/red] by typing: exit")
    season = season_input()

    while True:
        players = players_for_table(season)
        nationality = nationality_input(players)
        top_scorers = players.top_scorers_by_nationality(nationality)

        console.print(rich_player_table(season, nationality, top_scorers))

if __name__ == "__main__":
    main()
