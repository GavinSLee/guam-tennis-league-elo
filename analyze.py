import math
import csv
import pandas as pd
import matplotlib.pyplot as plt


class Analyze:

    def __init__(self):
        self.csv_file = r"C:\Users\Gavin Lee\Desktop\guam_tennis_league_elo\Master Men Players Roster.csv"
        self.elo_mean = 1500
        self.elo_sd = 150
        self.rating_mean, self.rating_median, self.rating_sd = self.find_statistics()
        print("RATING MEAN: " + str(self.rating_mean))
        print("RATING MEDIAN: " + str(self.rating_median)) 
        print("RATING STD " + str(self.rating_sd)) 

    def find_statistics(self):
        df = pd.read_csv(self.csv_file)
        mean = df['Rating'].mean()
        median = df['Rating'].median()
        std = df['Rating'].std()

        return mean, median, std

    def convert_rating_to_elo(self, rating):
        diff = abs(rating - self.rating_mean)

        point_diff = (self.elo_sd / self.rating_sd) * diff

        if rating > self.rating_mean:
            return int(self.elo_mean + point_diff)
        else:
            return int(self.elo_mean - point_diff)

    def update_csv_with_elo(self):

        df = pd.read_csv(self.csv_file)
        ratings = df['Rating']


        elo_scores = [] 


        for i in range(len(ratings)):
            elo_scores.append(self.convert_rating_to_elo(ratings[i]))
        


        df["Elo Score"] = elo_scores
        df.to_csv(self.csv_file, index = False) 

            
if __name__ == "__main__":
    analyze = Analyze()
    analyze.update_csv_with_elo()