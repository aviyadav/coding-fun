import pandas as pd
import polars as pl

def main_pd():
    users = pd.read_csv("users.csv")
    # print(users.head())

    activity = pd.read_csv("activity.csv", parse_dates=["date"])
    # print(activity.head())

    start_finish = (
        activity
        .groupby("user_id", as_index=False)
        .agg(
            started_movies = ("finished", "count"),
            finished_movies = ("finished", "sum"),
            )
    )
    # print(start_finish.head())

    finished = activity.query("finished == 1")
    # print(finished.head())

    first_finished = (
        finished
        .sort_values(["user_id", "date"])
        .groupby("user_id", as_index=False)
        .agg(first_finished_date = ("date", "first"),
            first_finished_name = ("movie_name", "first"))
    )   
    # print(first_finished.head())

    last_finished = (
        finished
        .sort_values(["user_id", "date"], ascending=[True, False])
        .groupby("user_id", as_index=False)
        .agg(last_finished_date = ("date", "first"),
            last_finished_name = ("movie_name", "first"))
    )
    # print(last_finished.head())    

    result = (users
    .merge(first_finished, how="left", left_on="id", right_on="user_id")
    .merge(last_finished, how="left", left_on="id", right_on="user_id")
    .merge(start_finish, how="left", left_on="id", right_on="user_id")
    ).drop(columns=["user_id_x", "user_id_y"]).query("last_finished_name == 'Fight Club'")
    
    print(result)

def main_pl():
    users = pl.scan_csv("users.csv")
    
    activity = pl.scan_csv("activity.csv", try_parse_dates=True)

    start_finish = (
        activity
        .group_by("user_id")
        .agg([
            pl.col("finished").count().alias("started_movies"),
            pl.col("finished").sum().alias("finished_movies"),
        ])
    )

    finished = activity.filter(pl.col("finished") == 1)

    first_finished = (
        finished
        .sort(["user_id", "date"])
        .group_by("user_id")
        .agg([
            pl.col("date").first().alias("first_finished_date"),
            pl.col("movie_name").first().alias("first_finished_name")
        ])
    )   

    last_finished = (
        finished
        .sort(["user_id", "date"], descending=[False, True])
        .group_by("user_id")
        .agg([
            pl.col("date").first().alias("last_finished_date"),
            pl.col("movie_name").first().alias("last_finished_name")
        ])
    )

    result = (users
    .join(first_finished, left_on="id", right_on="user_id", how="left")
    .join(last_finished, left_on="id", right_on="user_id", how="left")
    .join(start_finish, left_on="id", right_on="user_id", how="left")
    .filter(pl.col("last_finished_name") == "Fight Club")
    .collect()
    )
    
    print(result)

if __name__ == "__main__":
    # main_pd()
    main_pl()
