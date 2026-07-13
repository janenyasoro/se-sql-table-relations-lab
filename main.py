# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Return the first and last names and the job titles for all employees in Boston.
df_boston = pd.read_sql("""
                        SELECT e.firstName, e.lastName, e.jobTitle
                        FROM employees e
                        JOIN offices o ON e.officeCode = o.officeCode
                        WHERE o.city = 'Boston'
                        """, conn)

# STEP 2
# Are there any offices that have zero employees?
df_zero_emp = pd.read_sql("""
                        SELECT o.officeCode, o.city,o.state, COUNT(e.employeeNumber) AS employee_count
                        FROM offices o
                        LEFT JOIN employees e ON o.officeCode = e.officeCode
                        GROUP BY o.officeCode, o.city,o.state
                        HAVING COUNT(e.employeeNumber) = 0
                        """, conn)

# STEP 3
# Return employee's first and last names, along with the city and state of the office they work in.
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
# Return all of the customer's contact information (first name, last name, and phone number) 
# as well as their sales rep's employee number for any customer who has not placed an order.
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName
""", conn)

# STEP 5
# Produce a report of all the customer contacts (first and last names) along with details 
# for each of the customers' payment amounts and dates of payment.
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
    FROM customers c
    JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
# Return the employee number, first name, last name, and number of customers for employees 
# whose customers have an average credit limit over 90k.
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) as num_customers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY num_customers DESC
""", conn)

# STEP 7
# Return the product name and count the number of orders for each product as a column named numorders.
# Also return a new column, totalunits, that sums up the total quantity of product sold.
df_product_sold = pd.read_sql("""
    SELECT p.productName, 
           COUNT(DISTINCT od.orderNumber) as numorders,
           SUM(od.quantityOrdered) as totalunits
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    GROUP BY p.productName
    ORDER BY totalunits DESC
""", conn)

# STEP 8
# Return the product name, code, and the total number of different customers who have ordered each product.
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode, 
           COUNT(DISTINCT o.customerNumber) as numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productName, p.productCode
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Return the count as a column named n_customers. Also, return the office code and city.
df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city, COUNT(c.customerNumber) as n_customers
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
""", conn)

# STEP 10
# Using a subquery or CTE, select the employee number, first name, last name, 
# city of the office, and the office code for employees who sold products 
# that have been ordered by fewer than 20 customers.
df_under_20 = pd.read_sql("""
    WITH product_customers AS (
        SELECT p.productCode, COUNT(DISTINCT o.customerNumber) as num_customers
        FROM products p
        JOIN orderdetails od ON p.productCode = od.productCode
        JOIN orders o ON od.orderNumber = o.orderNumber
        GROUP BY p.productCode
        HAVING COUNT(DISTINCT o.customerNumber) < 20
    )
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders ord ON c.customerNumber = ord.customerNumber
    JOIN orderdetails od ON ord.orderNumber = od.orderNumber
    JOIN product_customers pc ON od.productCode = pc.productCode
""", conn)

# Close the connection
conn.close()