import numpy as np 
import pandas as pd 
import ast 

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')


movies = movies.merge(credits , on = 'title')

#generes 
#id 
#keywords 
#orignal language
#high percentage of english movies so dosent matter here a bit mov
#title(not orignal title)
#Overview 
#cast 
#crew 

movies = movies[['movie_id' , 'title' , 'overview' , 'genres' , 'keywords' , 'cast' , 'crew']]
movies.dropna(inplace=True)


def genres_list(obj):
    L = []
    for i in ast.literal_eval(obj) : 
        L.append(i['name'])
    return L

def genres_list_directors(obj):
    L = []
    for i in ast.literal_eval(obj) : 
        if i['job'] == 'Director' :  
            L.append(i['name'])
        else :  
            continue 
    return L

def genres_list_limit(obj):
    L = []
    counter = 0 
    for i in ast.literal_eval(obj) : 
        if counter != 3 :
            L.append(i['name'])
            counter += 1 
        else : 
            break 
    return L


movies['genres'] = movies['genres'].apply(genres_list)
movies['keywords'] = movies['keywords'].apply(genres_list)
movies['cast'] = movies['cast'].apply(genres_list_limit) 
movies['crew'] = movies['crew'].apply(genres_list_directors)
movies['overview'] = movies['overview'].apply(lambda x : x.split())

movies['genres'] = movies['genres'].apply(lambda x : [i.replace(" " , "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x : [i.replace(" " , "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x : [i.replace(" " , "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x : [i.replace(" " , "") for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew'] 

new_df = movies[['movie_id' , 'title' , 'tags']]

new_df['tags'] = new_df['tags'].apply(lambda x : " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x : x.lower())


print(new_df.head())
new_df.to_csv('preprocessed_data.csv')
