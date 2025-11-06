from rich.console import Console
from rich.table import Table

from player_reader import PlayerReader
from player_stats import PlayerStats

console = Console()

def main():
    console.print("[red]Exit[/red] by typing: exit")
    # season
    console.print("Season [bold magenta][2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/2025-26][/bold magenta] [bold cyan]2024-25[/bold cyan]:", end=" ")
    season = input()
    if season == "":
        season = "2024-25"
    if season == "exit":
        return

    while True:
        # players
        url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
        players_json = PlayerReader(url)
        players = PlayerStats(players_json.get_players())

        # nationality
        nationalities = "/".join(sorted(players.different_nationalities()))
        console.print(f"Nationality [bold magenta][{nationalities}][/bold magenta] [bold cyan]()[/bold cyan]:", end=" ")
        nationality = input()
        if nationality == "":
            nationality = "FIN"
        if nationality == "exit":
            return

        # stats
        players = players.top_scorers_by_nationality(nationality)

        # rich table
        table = Table(title=f"Season {season} players from {nationality}")
        table.add_column("Players", style="cyan")
        table.add_column("Teams", style="magenta")
        table.add_column("goals", style="green")
        table.add_column("assists", style="green")
        table.add_column("points", style="green")

        for player in players:
            table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.points))

        console.print(table)

if __name__ == "__main__":
    main()