-- Big project for SQL
-- Link instruction: https://docs.google.com/spreadsheets/d/1WnBJsZXj_4FDi2DyfLH1jkWtfTridO2icWbWCh7PLs8/edit#gid=0


-- Query 01: calculate total visit, pageview, transaction and revenue for Jan, Feb and March 2017 order by month
#standardSQL
SELECT 
      FORMAT_DATE('%Y%m',PARSE_DATE('%Y%m%d',date)) AS month,
      SUM(totals.visits) AS visits,
      SUM(totals.pageviews) AS pageviews, 
      SUM(totals.transactions) AS transactions, 
      (SUM(totals.totalTransactionRevenue) / 1000000) AS revenue
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_2017*`
GROUP BY month
ORDER BY month
LIMIT 3
-- Query 02: Bounce rate per traffic source in July 2017
#standardSQL
SELECT trafficSource.source AS sources,
      SUM(totals.visits) AS total_visits,
      SUM(totals.bounces) AS total_no_of_bounces,
      (SUM(totals.bounces)/SUM(totals.visits) * 100) AS bounce_rate
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_201707*`
WHERE trafficSource.source IN ('google','(direct)', 'youtube.com','analytics.google.com')
GROUP  BY sources
ORDER BY  total_visits DESC

-- Query 3: Revenue by traffic source by week, by month in June 2017
(SELECT 'month' as time_type,
        FORMAT_DATE('%Y%m',PARSE_DATE('%Y%m%d',date)) AS time,
        trafficSource.source AS sources,
        (SUM(totals.totalTransactionRevenue) / 1000000) AS revenue
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_201706*`
WHERE trafficSource.source IN ('(direct)','google')
GROUP  BY sources, time
ORDER BY  revenue desc)
union all
(SELECT 'week' as time_type,
        FORMAT_DATE('%Y%W',PARSE_DATE('%Y%m%d',date)) AS time,
        trafficSource.source AS sources,
        (SUM(totals.totalTransactionRevenue) / 1000000) AS revenue
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_201706*`
WHERE trafficSource.source = '(direct)'
GROUP  BY sources, time
ORDER BY  revenue desc
limit 2)

--Query 04: Average number of product pageviews by purchaser type (purchasers vs non-purchasers) in June, July 2017. Note: totals.transactions >=1 for purchaser and totals.transactions is null for non-purchaser
#standardSQL

with
b1 as (select FORMAT_DATE('%Y%m',PARSE_DATE('%Y%m%d',date)) as month,
        sum(totals.pageviews) AS pv, 
        count(distinct fullVisitorId) as id,
from `bigquery-public-data.google_analytics_sample.ga_sessions_2017*` 
where totals.transactions >=1
and _table_suffix between '0601' and '0731'
group by month),
b2 as (select  FORMAT_DATE('%Y%m',PARSE_DATE('%Y%m%d',date)) as month,
        sum(totals.pageviews) AS npv, 
        count(distinct fullVisitorId) as nid,
from `bigquery-public-data.google_analytics_sample.ga_sessions_2017*` 
where totals.transactions is null
and _table_suffix between '0601' and '0731'
group by month)
select b1.month,
        avg(b1.pv/b1.id) AS avg_pageviews_purchase,
        avg(b2.npv/b2.nid) AS avg_pageviews_non_purchase
FROM b1
left join b2
on b1.month = b2.month
group by b1.month
order by b1.month


-- Query 05: Average number of transactions per user that made a purchase in July 2017
#standardSQL
WITH 
b1 AS (
  SELECT distinct FORMAT_DATE('%Y%m',PARSE_DATE('%Y%m%d',date)) AS month,
  FROM `bigquery-public-data.google_analytics_sample.ga_sessions_201707*`),
b2 AS (
  SELECT AVG(tt / user) AS Avg_total_transactions_per_user
  FROM (select SUM(totals.transactions) AS tt,
        count(distinct fullVisitorId) AS user  
        FROM `bigquery-public-data.google_analytics_sample.ga_sessions_201707*`
        WHERE totals.transactions >= 1))
SELECT *
FROM b1,b2

-- Query 06: Average amount of money spent per session
#standardSQL

WITH b1 AS (
  SELECT distinct FORMAT_DATE('%Y%m',PARSE_DATE('%Y%m%d',date)) AS month,
  FROM `bigquery-public-data.google_analytics_sample.ga_sessions_201707*`),
b2 as (
  SELECT ROUND(AVG(tt / vi),2) AS avg_revenue_by_user_per_visit
  FROM (select SUM(totals.totalTransactionRevenue) AS tt,
         SUM(totals.visits) AS vi  
        FROM `bigquery-public-data.google_analytics_sample.ga_sessions_201707*`
        WHERE totals.transactions IS NOT NULL))
SELECT *
FROM b1,b2

-- Query 07: Other products purchased by customers who purchased product "YouTube Men's Vintage Henley" in July 2017. Output should show product name and the quantity was ordered.
#standardSQL
select
    product.v2productname as other_purchased_product,
    sum(product.productQuantity) as quantity
from `bigquery-public-data.google_analytics_sample.ga_sessions_201707*`,
    unnest(hits) as hits,
    unnest(hits.product) as product
where fullvisitorid in (select distinct fullvisitorid
                        from `bigquery-public-data.google_analytics_sample.ga_sessions_201707*`,
                        unnest(hits) as hits,
                        unnest(hits.product) as product
                        where product.v2productname = "YouTube Men's Vintage Henley"
                        and hits.eCommerceAction.action_type = '6')
and product.v2productname != "YouTube Men's Vintage Henley"
and product.productRevenue is not null
group by other_purchased_product
order by quantity desc

--CTE:

with buyer_list as(
    SELECT
        distinct fullVisitorId
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_201707*`
    , UNNEST(hits) AS hits
    , UNNEST(hits.product) as product
    WHERE product.v2ProductName = "YouTube Men's Vintage Henley"
    AND totals.transactions>=1
    AND product.productRevenue is not null
)

SELECT
  product.v2ProductName AS other_purchased_products,
  SUM(product.productQuantity) AS quantity
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_201707*`
, UNNEST(hits) AS hits
, UNNEST(hits.product) as product
JOIN buyer_list using(fullVisitorId)
WHERE product.v2ProductName != "YouTube Men's Vintage Henley"
 and product.productRevenue is not null
GROUP BY other_purchased_products
ORDER BY quantity DESC

--Query 08: Calculate cohort map from pageview to addtocart to purchase in last 3 month. For example, 100% pageview then 40% add_to_cart and 10% purchase.
#standardSQL

with product_data as(
select
    format_date('%Y%m', parse_date('%Y%m%d',date)) as month,
    count(CASE WHEN eCommerceAction.action_type = '2' THEN product.v2ProductName END) as num_product_view,
    count(CASE WHEN eCommerceAction.action_type = '3' THEN product.v2ProductName END) as num_add_to_cart,
    count(CASE WHEN eCommerceAction.action_type = '6' THEN product.v2ProductName END) as num_purchase
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
,UNNEST(hits) as hits
,UNNEST (hits.product) as product
where _table_suffix between '20170101' and '20170331'
and eCommerceAction.action_type in ('2','3','6')
group by month
order by month
)

select
    *,
    round(num_add_to_cart/num_product_view * 100, 2) as add_to_cart_rate,
    round(num_purchase/num_product_view * 100, 2) as purchase_rate
from product_data
