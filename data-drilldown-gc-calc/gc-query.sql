WITH close as (
	SELECT * FROM read_csv("SPY_close_price_5Y.csv")
),
ma AS (
    SELECT
        date,
        close,
        -- 50-Day Moving Average
        CASE
            WHEN COUNT(close) OVER (
                ORDER BY date
                ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
            ) = 50
            THEN AVG(close) OVER (
                ORDER BY date
                ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
            )
            ELSE NULL
        END AS ma_50,
        -- 200-Day Moving Average
        CASE
            WHEN COUNT(close) OVER (
                ORDER BY date
                ROWS BETWEEN 199 PRECEDING AND CURRENT ROW
            ) = 200
            THEN AVG(close) OVER (
                ORDER BY date
                ROWS BETWEEN 199 PRECEDING AND CURRENT ROW
            )
            ELSE NULL
        END AS ma_200
    FROM close
),
lagged AS (
    SELECT
        date,
        close,
        ma_50,
        ma_200,
        LAG(ma_50) OVER (ORDER BY date) AS prev_ma_50,
        LAG(ma_200) OVER (ORDER BY date) AS prev_ma_200
    FROM ma
)
SELECT
    date,
    close,
    CASE
        WHEN prev_ma_50 < prev_ma_200 AND ma_50 > ma_200 THEN 'Golden Cross'
        WHEN prev_ma_50 > prev_ma_200 AND ma_50 < ma_200 THEN 'Death Cross'
        ELSE NULL
    END AS signal
FROM lagged
WHERE signal IS NOT NULL
ORDER BY date DESC;