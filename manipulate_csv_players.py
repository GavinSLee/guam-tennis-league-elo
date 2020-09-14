import pandas as pd
import glob


def concatenate_csv():
    path = r'C:\Users\Gavin Lee\Desktop\guam_tennis_league_elo\players\Men'
    all_files = glob.glob(path + "/*.csv")

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)
    df.to_csv('Master Men Players Roster.csv', index=False)
    print("Done")

def drop_duplicates():
    df = pd.read_csv(r"C:\Users\Gavin Lee\Desktop\guam_tennis_league_elo\Master Men Players Roster.csv")
     
    df = df.drop_duplicates(subset='Player', keep='first', inplace=False)
    df.to_csv("Master Men Players Roster.csv", index=False)

def sort_by_elo():
    df = pd.read_csv(r"C:\Users\Gavin Lee\Desktop\guam_tennis_league_elo\Master Men Players Roster.csv")
    df = df.sort_values(by = ['Elo Score']) 

    df.to_csv("Master Men Players Roster.csv", index = False)

if __name__ == "__main__":
    sort_by_elo() 
