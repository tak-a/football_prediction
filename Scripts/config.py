# Created by taka the 1/25/21 at 5:23 PM

import os

website = 'https://www.lequipe.fr'

script_path = os.path.dirname(os.path.abspath(__file__))

project_path = script_path + '/..'

data_path = project_path + '/Data'


sofifa_player_search = 'https://sofifa.com/players?keyword='

composed_teams_names = ['Paris-Saint-Germain', 'Saint-Etienne', 'Manchester-United', 'Manchester-City']

so_fifa_url = 'https://sofifa.com'

so_fifa_players = 'https://sofifa.com/players/?showCol%5B0%5D=oa&col=oa&sort=desc&offset='

# player's name, Club's name, delimiter
players_dataset_infos = {
    '2018': ['Name', 'Club','Overall', ','],
    '2019': ['Name', 'Club', 'Overall', ','],
    '2020': ['short_name', 'Club', 'Overall', ','],
    '2021': ['name', 'team', 'overall', ';']
}

teams_names_exceptions = [
    ['PSG', 'Paris Saint Germain', 'Paris SG', 'Paris-Saint-Germain']
]

players_career_columns = ['Name', 'ID', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
