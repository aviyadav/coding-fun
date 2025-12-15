WITH lessons AS (
    SELECT *
    FROM LessonStreaks.csv
),
active_days AS (
    SELECT DISTINCT user_name,
    date
    FROM lessons
),
streak_calcs AS (
select
    user_name,
    date,
    LAG(date) OVER (PARTITION BY user_name ORDER BY date) AS prior_date,
    DATEDIFF('day', LAG(date) OVER (PARTITION BY user_name ORDER BY date), date) AS days_since_prior,
    CASE 
        WHEN DATEDIFF('day', LAG(date) OVER (PARTITION BY user_name ORDER BY date), date) = 1 THEN 0
        ELSE 1
    END AS streak_break
FROM active_days
),
streak_groups AS (
SELECT
    user_name,
    date,
    prior_date,
    SUM(streak_break) OVER (PARTITION BY user_name ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS streak_group
FROM streak_calcs
)

SELECT 
    user_name,
    streak_group,
    MIN(date) AS streak_start,
    MAX(date) AS streak_end,
    COUNT(*) AS streak_length  
FROM streak_groups
GROUP BY 1, 2
ORDER BY 4 DESC, 5 DESC;