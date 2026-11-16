-- Reference schema; the Python pipeline creates the table automatically.
CREATE TABLE IF NOT EXISTS sales (
 order_id TEXT PRIMARY KEY, order_date TEXT NOT NULL, customer_id TEXT NOT NULL,
 product TEXT NOT NULL, category TEXT NOT NULL, region TEXT NOT NULL, city TEXT NOT NULL,
 sales_channel TEXT NOT NULL, quantity INTEGER NOT NULL, unit_price REAL NOT NULL,
 unit_cost REAL NOT NULL, revenue REAL NOT NULL, total_cost REAL NOT NULL,
 profit REAL NOT NULL, profit_margin_pct REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date);
CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region);

-- Revenue and profit by region
SELECT region,SUM(revenue) revenue,SUM(profit) profit
FROM sales GROUP BY region ORDER BY revenue DESC;

-- Monthly revenue
SELECT substr(order_date,1,7) month,SUM(revenue) revenue
FROM sales GROUP BY month ORDER BY month;

-- Product performance
SELECT product,SUM(quantity) units_sold,SUM(revenue) revenue,SUM(profit) profit
FROM sales GROUP BY product ORDER BY revenue DESC;
