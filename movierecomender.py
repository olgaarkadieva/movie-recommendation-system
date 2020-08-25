

import pandas as pd
# Pandas is a high-level data manipulation tool .It is built on the Numpy package and its key data structure is called the DataFrame.
#  DataFrames allow you to store and manipulate tabular data in rows of observations and columns of variables.


# in this function i am taking user input to search for a movie and display a list of 10 similar movies related to that movie .


def recommendmovie():
    movie_title = str(input("Enter the movie title:"))

    column_names = ["user_id", "item_id", "rating", "timestamp"]
    path = "file.tsv"
    data_frame = pd.read_csv("file.tsv", sep="\t", names=column_names)

    # creating a dataframe by using read_csv function . 

    movie_title_items = pd.read_csv("movie_title.csv")

    # crating another dataframes of movie title and and item

    merged_data_set = pd.merge(left=data_frame, right=movie_title_items, on="item_id")

    # joining two data frame on basis of item_id ... only those data set will be merge if item_id is found on both side of column i-e data_frame and movie_title_items

    if movie_title not in list(merged_data_set["title"]):
        # check if movie title entered by user is found 
        print(f"sorry no movie found with title {movie_title}. try again")
        return None

# storing rating of movie 
    ratings = pd.DataFrame(merged_data_set.groupby("title")["rating"].mean())

    # this will create 2 dimensional table to store rating of movie by title


    ratings["num of ratings"] = pd.DataFrame(merged_data_set.groupby("title")["rating"].count())
    #  store total rating of movie in 'num of ratings' columns

    moviemat = merged_data_set.pivot_table(index="user_id", columns="title", values="rating")

    # applying aggregate on rating column and result be retured as table 



    movie_user_rating = moviemat[movie_title]

    cors_movie = moviemat.corrwith(movie_user_rating)

    # corrwith functoin checks computes correlation with another dataframe  between rows or columns of two DataFrame objects
    # in this case we are  checking correlation of movie_title column and movie

    similar_movies = pd.DataFrame(cors_movie, columns=["Correlation"])

    similar_movies.dropna(inplace=True)
    # Determine if rows or columns which contain missing values are  removed.

    similar_movies = similar_movies.join(ratings["num of ratings"])

    return (
        similar_movies[similar_movies["num of ratings"] > 100]
        .sort_values("Correlation", ascending=False)
        .head(10)
    )

    

print(recommendmovie())
