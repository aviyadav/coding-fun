import pandas as pd

def main():
    lessons_df = (
        pd.read_csv("LessonStreaks.csv", parse_dates=["date"])
        .drop_duplicates(["user_id", "date"])
        .sort_values(["user_id", "date"])
    )

    lessons_df["streak"] = lessons_df.groupby("user_id")["date"].diff().ne(pd.Timedelta(days=1)).cumsum()
    # print(lessons_df["streak"].head())

    streaks = lessons_df.groupby(["user_id", "user_name", "streak"]).agg(
        streak_length=("date", "count"),
        start_date=("date", "min"),
        end_date=("date", "max"),
    ).reset_index()
    
    active_date = pd.to_datetime("2025-09-28")
    print(streaks.query("end_date >= @active_date").sort_values("streak_length", ascending=False).head(10))


if __name__ == "__main__":
    main()
