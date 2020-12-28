import pandas as pd
from sklearn.cluster import KMeans
import random
import numpy as np

class Clustering():
    def __init__(self):
        self.load_csvs()
        self.allGenres=self.getAllGenres()
    
    def load_csvs(self):
        movies = pd.read_csv('source/movies.csv')
        movies['genres'] = movies['genres'].str.split('|')
        self.movies=movies
        self.ratings= pd.read_csv('source/ratings.csv')
    
    def getAllGenres(self):
        #get all categories
        movies=self.movies
        genres=[]
        for index, row in movies.iterrows():
            eidh=row['genres']
            for genre in eidh:
                if not genre in genres:
                    genres.append(genre)
        return genres
    
    def getMovieGenres(self,movieId):
        movies=self.movies
        index=movies.index[movies['movieId'] == movieId].tolist()[0]#could just write movieId-1
        return movies['genres'][index]
    
    def createUserRatingsDict(self):
        ratings=self.ratings
        userRatings={}
        for index, row in ratings.iterrows():
            userId,movieId=row['userId'],row['movieId']
            rating=row['rating']
            genres=self.getMovieGenres(movieId)

            if not userId in userRatings: 
                #initiate the index of the user with all ratings=0
                genreDict={}
                for genre in self.allGenres:
                    genreDict[genre]={'value':0 ,'count':0 }

                userRatings[userId]=genreDict

            for genre in genres:
                userRatings[userId][genre]['value']+=rating
                userRatings[userId][genre]['count']+=1
        
        userGenreRatingsDict=pd.DataFrame(userRatings).T
        self.userGenreRatingsDict=userGenreRatingsDict
        return userGenreRatingsDict
    
    def setAverageRating(self):
        df=self.userGenreRatingsDict
        userGenreRatings=df.copy(deep=True)#changes will not affect the initial parmaeter
        for index, row in userGenreRatings.iterrows():
            for genre in self.allGenres:                
                if row[genre]['count']==0:
                  pass
                else:
                    userGenreRatings[genre][index]=row[genre]['value']/row[genre]['count']

        self.userGenreRatingsWithMissing=userGenreRatings
        return userGenreRatings
    
    def fillMissingDataPreProcessing(self,missing_data_completion='neutral'):
        df=self.userGenreRatingsWithMissing
        userGenreRatings=df.copy(deep=True)#changes will not affect the initial parmaeter
        for index, row in userGenreRatings.iterrows():
            for genre in self.allGenres:  

                rated_of_column=[ i for i in  userGenreRatings[genre]  if type(i)!=dict ] 
                missing_value={
                   'neutral': 2.5,
                    'out_of_range':-1,
                    'zero':0,
                   'column_mean':sum(rated_of_column) /len(rated_of_column)  
                }

                if type( row[genre] )==dict:
                    userGenreRatings[genre][index]=missing_value[missing_data_completion]
        
        del userGenreRatings['(no genres listed)']

        self.userGenreRatingsMissingFilled=userGenreRatings
        return userGenreRatings
    
    def fit(self):
        kmeans = KMeans(n_clusters=15).fit(self.userGenreRatingsMissingFilled)
        cluster_map = pd.DataFrame()
        cluster_map['userId'] = self.userGenreRatingsMissingFilled.index.values
        cluster_map['cluster'] = kmeans.labels_
        cluster_map.to_csv('usersClusters.csv',index=False)
        
        clusters=[]
        for i in range(15):
            x=list( cluster_map['userId'][cluster_map['cluster'] == i] )
            clusters.append(x)
        self.clusters=clusters



if __name__ == "__main__":
    x=Clustering()
    x.createUserRatingsDict()
    print("Created UserRatingsDict")
    x.setAverageRating()
    print("Set Average Rating")
    #print(self.userGenreRatingsWithMissing.head())
    x.fillMissingDataPreProcessing(missing_data_completion='column_mean')
    print("Filled Missing Data for Kmeans")
    print(x.userGenreRatingsMissingFilled.head())
    x.fit()
    print(x.clusters)