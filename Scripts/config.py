# Created by taka the 1/25/21 at 5:23 PM

import os


# ----- lequipe website info -----
lequipe = 'https://www.lequipe.fr'
ligue1_season_calendar = os.path.join(lequipe, "Football/ligue-1/saison-{}-{}/page-calendrier-resultats/")

years = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet',
         'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']


# ----- project paths -----
scripts_path = os.path.dirname(os.path.abspath(__file__))

project_path = scripts_path + '/..'

data_path = project_path + '/Data'


# ----- So FIFA website info ----
so_fifa_player_search = 'https://sofifa.com/players?keyword='

so_fifa = 'https://sofifa.com'


so_fifa_players = 'https://sofifa.com/players/?showCol%5B0%5D=oa&col=oa&sort=desc&offset='

so_fifa_top5_21 = 'https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg' \
                  '%5B4%5D=53&showCol%5B%5D=ae&showCol%5B%5D=oa&showCol%5B%5D=pi&offset='

so_fifa_top5_20 = 'https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg' \
                  '%5B4%5D=53&showCol%5B0%5D=ae&showCol%5B1%5D=oa&showCol%5B2%5D=pi&r=200061&set=true&offset='

so_fifa_top5_19 = 'https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg' \
                  '%5B4%5D=53&showCol%5B0%5D=ae&showCol%5B1%5D=oa&showCol%5B2%5D=pi&r=190075&set=true&offset='

so_fifa_top5_18 = 'https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg' \
                  '%5B4%5D=53&showCol%5B0%5D=ae&showCol%5B1%5D=oa&showCol%5B2%5D=pi&r=180084&set=true&offset='

so_fifa_top5_17 = 'https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg' \
                  '%5B4%5D=53&showCol%5B0%5D=ae&showCol%5B1%5D=oa&showCol%5B2%5D=pi&r=170099&set=true&offset='

so_fifa_top5_16 = 'https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg' \
                  '%5B4%5D=53&showCol%5B0%5D=ae&showCol%5B1%5D=oa&showCol%5B2%5D=pi&r=160058&set=true&offset='

so_fifa_top5_15 = 'https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg' \
                  '%5B4%5D=53&showCol%5B0%5D=ae&showCol%5B1%5D=oa&showCol%5B2%5D=pi&r=150059&set=true&offset='

so_fifa_top5_urls = [so_fifa_top5_21, so_fifa_top5_20, so_fifa_top5_19, so_fifa_top5_18, so_fifa_top5_17,
                     so_fifa_top5_16, so_fifa_top5_15]


# player's name, Club's name, delimiter
players_dataset_info = {
    '2018': ['Name', 'Club','Overall', ','],
    '2019': ['Name', 'Club', 'Overall', ','],
    '2020': ['short_name', 'Club', 'Overall', ','],
    '2021': ['name', 'team', 'overall', ';']
}


composed_teams_names = ['Paris-Saint-Germain', 'Saint-Etienne', 'Manchester-United', 'Manchester-City']

teams_names_exceptions = [
    ['PSG', 'Paris Saint Germain', 'Paris SG', 'Paris-Saint-Germain']
]

players_career_columns = ['Name', 'ID', '2015', '2016', '2017', '2018', '2019', '2020', '2021']


career_top5_file = os.path.join(data_path, 'players_career_top5_complete.csv')
