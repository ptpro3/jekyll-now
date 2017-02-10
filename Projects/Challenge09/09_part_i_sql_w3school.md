# Challenge Set 9
## Part I: W3Schools SQL Lab 

*Introductory level SQL*

--

This challenge uses the [W3Schools SQL playground](http://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all). Please add solutions to this markdown file and submit.

1. Which customers are from the UK?
```sql
SELECT * FROM Customers WHERE Country = 'UK';
```
2. What is the name of the customer who has the most orders?
```sql
SELECT CustomerName, COUNT(*) FROM Customers C
JOIN Orders O ON C.CustomerID = O.CustomerID
GROUP BY O.CustomerID
ORDER BY 2 DESC LIMIT 1;
```
>*Ernst Handel*

3. Which supplier has the highest average product price?
```sql
SELECT SupplierName, AVG(p.Price)
FROM Suppliers s
JOIN Products p
ON s.SupplierID = p.SupplierID
GROUP BY s.SupplierID
ORDER BY 2 DESC
LIMIT 1;
```
>*Aux joyeux ecclésiastiques*

4. How many different countries are all the customers from? (*Hint:* consider [DISTINCT](http://www.w3schools.com/sql/sql_distinct.asp).)
```sql
SELECT COUNT(DISTINCT(Country)) FROM Customers;
```
> 21

5. What category appears in the most orders?
```sql
SELECT c.CategoryName, COUNT(*)
FROM OrderDetails as o
JOIN Products as p
JOIN Categories AS c
ON o.ProductID = p.ProductID
AND p.CategoryID = c.CategoryID
GROUP BY c.CategoryID
ORDER BY 2 DESC
LIMIT 1;
```
>*Dairy Products*

6. What was the total cost for each order?
```sql
SELECT
    o.OrderID,
    SUM(o.Quantity * p.Price) as Total
FROM
    OrderDetails as o
  JOIN
    Products as p
  ON
    o.ProductID = p.ProductID
GROUP BY
    o.OrderID
```

7. Which employee made the most sales (by total price)?
```sql
SELECT
    e.FirstName,
    e.LastName,
    SUM(op.Quantity * p.Price) as Total
FROM
    Employees as e
  JOIN
    Orders as o
  JOIN
    OrderDetails as op
  JOIN
    Products as p
  ON
      e.EmployeeID = o.EmployeeID
    AND
      o.OrderID = op.OrderID
    AND
      op.ProductID = p.ProductID
GROUP BY
    e.EmployeeID
ORDER BY 3 DESC
LIMIT 1;
```
>*Margaret Peacock*

8. Which employees have BS degrees? (*Hint:* look at the [LIKE](http://www.w3schools.com/sql/sql_like.asp) operator.)
```sql
SELECT * FROM Employees WHERE Notes LIKE '%BS%'
```

9. Which supplier of three or more products has the highest average product price? (*Hint:* look at the [HAVING](http://www.w3schools.com/sql/sql_having.asp) operator.)
```sql
SELECT COUNT(*), AVG(Price), SupplierName FROM Products P
JOIN Suppliers S ON P.SupplierID = S.SupplierID
GROUP BY SupplierName
HAVING COUNT(*) > 2
ORDER BY 2 DESC
LIMIT 1
```
>*Tokyo Traders*
