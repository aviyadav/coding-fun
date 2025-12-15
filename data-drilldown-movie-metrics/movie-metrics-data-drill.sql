WITH users AS (
    SELECT
        *
    FROM users.csv
),
activity AS (
    SELECT
        *
    FROM activity.csv
),
first_last AS (
    SELECT DISTINCT
    user_id,
    FIRST_VALUE(movie_name) OVER (PARTITION BY user_id ORDER BY date) AS name_first_finished,
    FIRST_VALUE(movie_name) OVER (PARTITION BY user_id ORDER BY date DESC) AS name_last_finished
    FROM activity
    WHERE finished = 1
)
SELECT u.id AS user_id,
    MIN(u.created_at) AS user_created_at,
    MIN(
        CASE
            WHEN finished = 1 THEN a.date
            ELSE NULL
        END
    ) AS first_date_finished,
    MIN(fl.name_first_finished) AS name_first_finished,
    MAX(
        CASE
            WHEN finished = 1 THEN a.date
            ELSE NULL
        END
    ) AS last_date_finished,
    MAX(fl.name_last_finished) AS name_last_finished,
    COUNT(DISTINCT a.id) AS movies_started,
    COUNT(
        DISTINCT CASE
            WHEN finished = 1 THEN a.id
            ELSE NULL
        END
    ) AS movies_finished
FROM users u
    LEFT JOIN activity a ON u.id = a.user_id
    LEFT JOIN first_last fl ON fl.user_id = u.id
GROUP BY u.id
HAVING MAX(fl.name_last_finished) = 'Fight Club'
;