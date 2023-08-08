import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"


def find_best_players(url: str) -> None:
    """Finds the best players in the semifinals of the nba and plots their stats.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds.

    Args:
        - html (str) : html string from wiki basketball
    """
    
    # find all teams 
    teams = get_teams(url)
    assert len(teams) == 8

    all_players = {}

    # find all players from team and add to dict with name as key and url as value
    for team in teams:
        name = team['name']
        team_url = team['url']
        all_players[name] = get_players(team_url)

    # append the value of players with the player stats
    for team, players in all_players.items():
        for player in players:
            player_url = player['url']
            player.update(get_player_stats(player_url, team))

    best = {}
    top_stat = "points"

    # loops through all players, finding the top 3 players for each team
    for team, players in all_players.items():
        top_3 = []

        players_with_points = []
        for player in players:
            if top_stat in player.keys():
                players_with_points.append(player)
        
        # convert to sorted list and get the last 3 indexes to find top 3
        sorted_by_points = sorted(players_with_points, key=itemgetter(top_stat))
        
        top_3.append(sorted_by_points[-1])
        top_3.append(sorted_by_points[-2])
        top_3.append(sorted_by_points[-3])
        best[team] = top_3

    stats_to_plot = ["points", "assists", "rebounds"]

    for stat in stats_to_plot:
        plot_best(best, stat=stat)


def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team.

    Args:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """

    stats_dir = "NBA_player_statistics"
    count = 0
    all_names = []

    for team, players in best.items():
        desired_stat = []
        names = []

        for player in players:
            names.append(player["name"])
            desired_stat.append(player[stat])

        all_names.extend(names)
        x = range(count, count + len(players))
        count += len(players)
        bars = plt.bar(x, desired_stat, label=team)
        plt.bar_label(bars, label_type="edge", padding=0, fontsize=7)

    plt.xticks(range(len(all_names)), all_names, rotation=90)
    #plt.legend(loc="lower left", mode="expand", ncol=3)
    plt.legend(bbox_to_anchor=(1, 1), loc="best", borderaxespad=0, fontsize=9)
    plt.tight_layout()
    plt.grid(True)
    plt.title(f"{stat} per game")
    filename = f"{stat}.png"

    print(f"Creating {filename}")
    if not os.path.exists(stats_dir):
        os.mkdir(stats_dir)

    plt.savefig(f"{stats_dir}/{filename}", bbox_inches="tight")
    plt.close()


def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba.

    Args:
        - url (str): 
            url of the nba finals wikipedia page
    Returns:
        teams (list): 
            list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page}
    """

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    rows = table.find_all("tr")
    rows = rows[2:]

    # starts with E or W followed by digit (1-8), end of string
    seed_pattern = re.compile(r"^[EW][1-8]$")

    team_links = {}  
    in_semifinal = set() 

    # find all teams in semi-final
    for row in rows:
        cols = row.find_all("td")

        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> list:
    """Gets all the players from a team that were in the roster for semi finals.
    
    Args:
        team_url (str) : the url for the team
    Returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """

    print(f"Finding players in {team_url}")

    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Roster").find_next("table")

    players = []
    
    rows = table.find_all("tr")
    rows = rows[3:]

    for row in rows:
        cols = row.find_all("td")
        namecol = cols[2]

        name = namecol.get_text(strip=True)
        # remove string if zero or more occurences of any digit inbetween parentheses
        name = re.sub(r"\(.*\)", "", name)
        name_link = namecol.find('a')['href']
    
        player = {'name': name, 'url': urljoin(base_url, name_link)}
        players.append(player)

    return players


def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team
    
    Args:
        player_url (str):
            url for the wiki page of player
        team (str): 
            the name of the team the player plays for
    Returns:
        stats (dict): 
            dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")

    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")
    id_ = re.compile("(NBA_)?[Cc]areer_statistics")
    #NBA = soup.find(id="NBA")
    #table = NBA.find_next("table", {"class":"wikitable sortable"})
    table = soup.find(id=id_).find_next('table').find_next('table')
    stats = {}

    rows = table.find_all("tr")
    rows = rows[1:]

    for row in rows:
        cols = row.find_all("td")
        season = cols[0].get_text(strip=True)
        team_ = cols[1].get_text(strip=True)
        
        # find relevant stats for season 2021-22
        if team_.lower() == team.lower() and season.startswith('2021–22'):

            stats['points'] = float(cols[12].get_text(strip=True).strip('*')) # PPG
            stats['assists'] = float(cols[9].get_text(strip=True).strip('*')) # APG
            stats['rebounds'] = float(cols[8].get_text(strip=True).strip('*')) # RPG   
        
    return stats


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    find_best_players('https://en.wikipedia.org/wiki/2022_NBA_playoffs')