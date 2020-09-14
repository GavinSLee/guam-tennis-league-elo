import pandas as pd
import numpy as np 



def map_elo():
    path = r"C:\Users\Gavin Lee\Desktop\guam_tennis_league_elo\Master Men Players Roster.csv"
    df = pd.read_csv(path) 
    players = df['Player'].to_list() 
    elos = df['Elo Score'].to_list() 
    elos = [int(i) for i in elos]
    elo_map = {}

    for i in range(len(players)):
        elo_map[players[i]] = elos[i] 

    return elo_map

def calculate_elos():
    path = r"C:\Users\Gavin Lee\Desktop\guam_tennis_league_elo\match_history\Men\Men Master Match History (Cleaned).csv"

    elo_map = map_elo() 
    df = pd.read_csv(path) 

    numpy_array = df.to_numpy()

    num_rows = np.shape(numpy_array)[0] 

    for i in range(num_rows):
        home_win = 0
        visitor_win = 0
        home_player_one = numpy_array[i][5]
        home_player_two = numpy_array[i][7]

        visitor_player_one = numpy_array[i][9]
        visitor_player_two = numpy_array[i][11] 

        home_score = numpy_array[i][np.shape(numpy_array)[1] - 2]
        visitor_score = numpy_array[i][np.shape(numpy_array)[1] - 1]

        home_elo = (elo_map[home_player_one] + elo_map[home_player_two]) / 2
        visitor_elo = (elo_map[visitor_player_one] + elo_map[visitor_player_two]) / 2 

        home_expected, visitor_expected = elo_algorithm(home_elo, visitor_elo)

        if home_score > visitor_score: 
            home_win = 1
        else:
            visitor_win = 1
        
        elo_map[home_player_one] = int(elo_map[home_player_one] + 32 * (home_win - home_expected))
        elo_map[home_player_two] = int(elo_map[home_player_two] + 32 * (home_win - home_expected))

        elo_map[visitor_player_one] = int(elo_map[visitor_player_one] + 32 * (visitor_win - visitor_expected))

        elo_map[visitor_player_two] = int(elo_map[visitor_player_two] + 32 * (visitor_win - visitor_expected))

    elo_map = sorted(elo_map.iteritems(), key = lambda x : x[1])

    for player in elo_map:
        print(player)

def elo_algorithm(elo1, elo2):
    exponent_a = (elo2 - elo1)/400 
    e_a = 1 / (1+10**(exponent_a))

    exponent_b = (elo1 - elo2)/400 
    e_b = 1/ (1+10**(exponent_b))

    return e_a, e_b





if __name__ == "__main__":
    calculate_elos()