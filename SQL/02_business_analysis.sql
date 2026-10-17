-- ==========================================
-- PAYFLOW DATA ANALYTICS PROJECT
-- SQL BUSINESS ANALYSIS
-- ==========================================

-- Dataset:
-- 25000 customers
-- 152870 transactions

-- Objective:
-- Analyse customer behaviour, transaction, performance, and business opportunities.

USE payflow;


-- ==========================================
-- SECTION 1: CUSTOMER VALUE ANALYSIS
-- ==========================================

-- Business Question 1:
-- Which 10 customers have the highest successful transaction value?.

SELECT
c.customer_id,
c.customer_type,
c.plan,
COUNT(t.transaction_id) AS successful_transactions,
ROUND(SUM(t.amount), 2) AS total_transaction_value

FROM customers AS c

INNER JOIN transactions AS t
ON c.customer_id = t.customer_id

WHERE t.transaction_status = "Successful"

GROUP BY
c.customer_id,
c.customer_type,
c.plan

ORDER BY total_transaction_value DESC

LIMIT 10;

-- KEY FINDINGS:
-- 1. Customer C24907 recorded the highest successful transaction value of 881356.58
--
-- 2. The top 10 customers each processed approximately 832193 to 881357
--
-- 3. Seven of the top 10 customers are individuals, while three are businesses.
--
-- 4. Seven customers use the standart plan, while three use the basic plan.
--
-- BUSINESS IMPLICATION:
-- High value customers may be suitable candidates for targeted and loyalty initiatives.
--
-- NOTE:
-- Transaction value represents payment volume, not company revenue.

-- ==========================================
-- BUSINESS QUESTION 2 
-- Which subscription plans contribute the highest successful value?
-- ==========================================

SELECT
c.plan,
COUNT(DISTINCT c.customer_id) AS active_transacting_customers,
COUNT(t.transaction_id) AS successful_transactions,
ROUND(SUM(t.amount), 2) AS total_transaction_value,
ROUND(
SUM(t.amount) / COUNT(DISTINCT c.customer_id),
2
) AS average_value_per_customer

FROM customers AS c

INNER JOIN transactions AS t
ON c.customer_id = t.customer_id

WHERE t.transaction_status = "Successful"

GROUP BY c.plan

ORDER BY total_transaction_value DESC;

-- KEY FINDINGS:
-- 1. Basic contributes the highest successful transaction value at approximately 3.70B
--
-- 2. Standard contributes approximately 2.34B, followed by premium at 1.09B
--
-- 3. Average successful transaction value per participating customer is approximately 325000 across all three plans
--
-- 4. The differences in total transaction value are largely associated with differences in the numbe of participatin customers
--
-- BUSINESS IMPLICATION:
-- Subscription plans show little differentiation in average sucessful payment volume per customer
--
-- NOTE:
-- Successful payment volume is not company revenue

-- ==========================================
-- BUSINESS QUESTION 3
-- Which customers transact most frequently?
-- ==========================================

SELECT
c.customer_id,
c.customer_type,
c.plan,
COUNT(t.transaction_id) AS total_transactions,
SUM(
CASE
WHEN t.transaction_status = "Successful"
THEN 1
ELSE 0
END
) AS successful_transactions

FROM customers AS c

INNER JOIN transactions AS t
ON c.customer_id = t.customer_id

GROUP BY
c.customer_id,
c.customer_type,
c.plan

ORDER BY
total_transactions DESC,
successful_transactions DESC,
c.customer_id ASC

LIMIT 10;

-- KEY FINDINGS:
-- 1. The maximum observed transaction frequency is 12 transactions per customer.
--
-- 2. All 10 displayed customers completed 12 successful transactions
-- 
-- 3. Nine displayed customers are individual, while one is a business customer
--
-- 4. Seven use the basic plan, while three use the standard plan
--
-- NOTE:
-- Other customers may share the same maximum frequency. LIMIT 10 displays only 10 records
--
-- BUSINESS IMPLICATION:
-- Transaction frequency and successful transaction value measure different aspects of engagement

-- ==========================================
-- BUSINESS QUESTION 4
-- Which customers registered but never made a transaction?
-- ==========================================

SELECT 
c.customer_id,
c.signup_date,
c.customer_type,
c.plan,
c.status

FROM customers AS c

LEFT JOIN transactions AS t
ON c.customer_id = t.customer_id

WHERE t.transaction_id IS NULL

ORDER BY c.customer_id ASC

LIMIT 10;

-- Count customers without transactions and examine their account status

SELECT
c.status,
COUNT(*) AS customers_without_transactions

FROM customers AS c

LEFT JOIN transactions AS t
ON c.customer_id = t.customer_id

WHERE t.transaction_id IS NULL

GROUP BY c.status;

-- KEY FINDINGS:
-- 1. A total of 3082 registered customers have no transaction records.
--
-- 2. These customers represent approximately 12.33% of the total customer base.
--
-- 3. All 3082 non transactiong customers are calssified as inactive
--
-- 4. Non transacting customers appear across basic, standard, and premium plans
--
-- BUSINESS IMPLICATION:
-- Payflow could investigate onboarding and activation barriers affecting customers who registered but never transacted
--
-- NOTE:
-- The dataset does not establish why these customers never completed a transaction

-- ==========================================
-- BUSINESS QUESTION 5
-- How does transaction performance change from month to month?
-- ==========================================

-- KEY FINDING:
-- 1. Transaction volume increased from 5282 in January to a peak 26096 in June
--
-- 2. June recorded the highest successful transaction value at approximately 1.212B
--
-- 3. Transaction volumes declined after June, reaching 4605 in september
--
-- 4. Payment success rates generally declined from 96.18% in January to 91.38% in september. This represents a 4.35 percentage point decrease
-- 
-- BUSINESS IMPLICATION:
-- Payflow could investigate declining payment success rates and changes in transaction activity to identify potential operational improvements
--
-- NOTE:
-- Incomplete observation periods may affect comparisons between months
-- These findings are baased on synthetic data

-- ==========================================
-- BUSINESS QUESTION 6
-- What is the month-over-month growth rate in transaction volume?
-- ==========================================

WITH monthly_transactions AS (
SELECT
DATE_FORMAT(transaction_date, '%Y-%m') AS transaction_month,
COUNT(*) AS total_transactions
FROM transactions
GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
),

monthly_growth AS (
SELECT
transaction_month,
total_transactions,

LAG(total_transactions) OVER (
ORDER BY transaction_month
) AS previous_month_transactions

FROM monthly_transactions
)

SELECT
transaction_month,
total_transactions,
previous_month_transactions,

ROUND(
(
total_transactions - previous_month_transactions
) * 100 / NULLIF(previous_month_transactions, 0),
2
) AS mom_growth_percentage

FROM monthly_growth

ORDER BY transaction_month ASC;

-- KEY FINDINGS:
-- 1. February recorded the highest month-over-month transacion growth at 128.23%
--
-- 2. Positive monthly growth gradually slowed from 71.68% in March to 0.09% in June
--
-- 3. Transaction growth truned negative in July, declining by 22.11%
--
-- 4. August and September recorded further declines of 38.82% and 62.97% respectively
-- 
-- 5. June recorded the highest transaction volume at 26096 transactions
--
-- BUSINESS IMPLICATION:
-- Payflow could investigate changes in transaction activity and the drivers of slowing growth
--
-- NOTE:
-- Month-over-month comparisons may be affected by incomplete reporting periods
-- All findings are based on synthetic data

-- ==========================================
-- BUSINESS QUESTION 7
-- Who are the top 3 highest value customers within each subscription plan?
-- ==========================================

WITH customer_value AS (
SELECT
c.customer_id,
c.customer_type,
c.plan,
COUNT(t.transaction_id) AS successful_transactions,
ROUND(SUM(t.amount), 2) AS total_transaction_value

FROM customers AS c

INNER JOIN transactions AS t
ON c.customer_id = t.customer_id

WHERE t.transaction_status = 'Successful'

GROUP BY
c.customer_id,
c.customer_type,
c.plan
),

customer_rankings AS (
SELECT
customer_id,
customer_type,
plan,
successful_transactions,
total_transaction_value,

DENSE_RANK() OVER (
PARTITION BY plan
ORDER BY total_transaction_value DESC
) AS customer_rank

FROM customer_value
)

SELECT *
FROM customer_rankings

WHERE customer_rank <= 3

ORDER BY plan, customer_rank, customer_id;

-- KEY FINDINGS:
-- 1. Standard customer C24907 ranked highest overall, processing 881356.58
--
-- 2. Basic customer C23377 ranked first within Basic, processing 870011.03
--
-- 3. Premium customer C05246 ranked first within Premium, processing 830825.67
--
-- 4. Higher transaction frequency does not always into higher transaction values
--
-- 5. DENSE_RANK() and PARTITION BY were used to rank customers withing each plan
--
-- BUSINESS IMPLICATION:
-- Payflow can identify high value customers within each subscription plan for targeted retention and engagement strategies.
--
-- NOTE:
-- Top customer rankings do not establish overall superiority of any subscription plan

-- ==========================================
-- BUSINESS QUESTION 8
-- Which transaction type and payment method combinations have the highest failure rates?
-- ==========================================

SELECT
transaction_type,
payment_method,

COUNT(*) AS total_transactions,

SUM(
CASE
WHEN transaction_status = 'Failed'
THEN 1
ELSE 0
END
) AS failed_transactions,

ROUND(
SUM(
CASE
WHEN transaction_status = 'Failed'
THEN 1
ELSE 0
END
) * 100 / COUNT(*),
2
) AS failure_rate_percentage

FROM transactions

GROUP BY
transaction_type,
payment_method

HAVING COUNT(*) >= 100

ORDER BY
failure_rate_percentage DESC,
failed_transactions DESC

LIMIT 10;

-- KEY FINDINGS:
-- 1. Merchant payments thorugh wallet recorded the highest failure rate at 5.63%
--
-- 2. Bank transfers through bank accounts ranked second with a failure rate of 5.56%
--
-- 3. The top 10 combinations recorded failure rates ranging from 5.11% to 5.63%
--
-- 4. The difference between the highest and tenth ranked failure rates was only 0.52 percentage points
--
-- 5. Merchant payments appeared three times among the top 10 combinations
--
-- BUSINESS IMPLICATION:
-- Payflow could investigate payment combinations with relatively higher failure rates to identify potential operational improvements
--
-- NOTE:
-- The observed differences are relatively small
-- The results do not establish the causes of failures

-- ==========================================
-- BUSINESS QUESTION 9
-- How does transaction participation and payment performance differ across customer types and subscription plans?
-- ==========================================

WITH customer_metrics AS (
SELECT 
c.customer_id,
c.customer_type,
c.plan,

COUNT(t.transaction_id) AS total_transactions,

SUM(
CASE
WHEN t.transaction_status = 'Successful'
THEN 1
ELSE 0
END
) AS successful_transactions,

SUM(
CASE
WHEN t.transaction_status = 'Successful'
THEN t.amount
ELSE 0
END
) AS successful_transaction_value

FROM customers AS c

LEFT JOIN transactions AS t
ON c.customer_id = t.customer_id

GROUP BY
c.customer_id,
c.customer_type,
c.plan

)

SELECT
customer_type,
plan,

COUNT(*) AS registered_customers,

SUM(
CASE
WHEN total_transactions > 0
THEN 1
ELSE 0
END
) AS transacting_customers,

ROUND(
SUM(
CASE
WHEN total_transactions > 0
THEN 1
ELSE 0
END
) * 100 / COUNT(*),
2
) AS participation_rate_percentage,

ROUND(
SUM(successful_transactions) * 100 /
NULLIF(SUM(total_transactions), 0),
2
) AS success_rate_percentage,

ROUND(
SUM(successful_transaction_value),
2
) AS total_successful_value

FROM customer_metrics

GROUP BY
customer_type,
plan

ORDER BY
customer_type,
plan;

-- KEY FINDINGS:
-- 1. Individual basic customers generated the highest successful transaction value at approximately 3.17B
--
-- 2. Individual standard ranked second, processing approximately 2.02B
--
-- 3. Business premium recorded the lowest total successful transaction value at 153.78M
--
-- 4. Individual customer participation rates ranged from 87.78% to 88.02%, compared with 85.55% to 86.54% for business customers
--
-- 5. Business standard recorede the highest payment success rate at 93.20%, while business premium recorded the lowest at 92.41%
--
-- BUSINESS IMPLICATION:
-- Total transaction value is strongly associated wiht customer segment size in this dataset
-- Payflow could investigate opportunities to improve participation among business customers
--
-- NOTE: Higer total transaction value does not necessarily mean higher average customer value

-- ==========================================
-- BUSINESS QUESTION 10
-- How many customers exceed the average successful transaction value of their plan?
-- ==========================================

WITH customer_value AS (
SELECT
c.customer_id,
c.plan,
SUM(t.amount) AS successful_transaction_value

FROM customers AS c

INNER JOIN transactions AS t
ON c.customer_id = t.customer_id

WHERE t.transaction_status = 'Successful'

GROUP BY
c.customer_id,
c.plan
)

SELECT
cv.plan,

COUNT(*) AS above_average_customers,

ROUND(
AVG(cv.successful_transaction_value),
2
) AS average_value_of_above_average_customers

FROM customer_value AS cv

INNER JOIN(
SELECT
plan,
AVG(successful_transaction_value) AS plan_average

FROM customer_value

GROUP BY plan
) AS plan_averages

ON cv.plan = plan_averages.plan

WHERE
cv.successful_transaction_value > plan_averages.plan_average

GROUP BY cv.plan

ORDER BY above_average_customers DESC;

-- KEY FINDINGS:
-- 1. Basic has the largest number of customers exceeding their plan's average successful transaction value, with 5461 customers
--
-- 2. Standard has 3442 above average customers, while Premium has 1624
--
-- 3. Premium recorded the highest average value among above average customers at 470747.32
--
-- 4. Approximately 48% of customers wiht successful transactions exceed their plan's average successful transaction value across all plans
--
-- BUSINESS IMPLICATION:
-- Customer payment activity is relatively similar across subscription plans when examined using within-plan averages
--
-- NOTE:
-- Above-average customer counts are influenced by differences in plan population sizes