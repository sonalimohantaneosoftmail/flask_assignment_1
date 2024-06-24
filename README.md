Project Title 
- Flask Assignment 

Objective 
- Design and implement a data analysis application involving API creation, large dataset handling,
 database design, and token-based authentication.

Description
- This project is a Flask-based application that provides APIs for managing users and their transactions.

Requirements:
1. API Creation:
- Develop a RESTful API using Flask (or FastAPI).
- Implement endpoints for consuming, processing, and querying a large dataset.

2. Data Handling:
- Use the faker library to generate a large dataset, or use a publicly available dataset.
- Design APIs to perform the following operations:
- Data Ingestion: Upload and store data in the database.
- Data Querying: Fetch data based on specific filters or conditions.
- Data Analysis: Perform simple analysis such as aggregation or statistical summary.

3. Database Design:
- Use SQLAlchemy (or any ORM of your choice) to interact with a MYSQL database.
- Design a normalized database schema for the following entities:
- User: id, name, email, password, created_at
- Transaction: id, user_id, amount, timestamp, type
- Implement migrations using Alembic.

4. Authentication:
- Use JWT (JSON Web Tokens) for secure authentication.
- Implement endpoints for user registration and login:
- User Registration: POST /auth/register

5. Role-Based Access Control (RBAC):
- Define roles (e.g., Admin, User) and permissions for each role.
- Only Admins can delete data.
- Both Admins and Users can create and manage data they own.


Features 
- Added generate_fake_data.py script to generate random users and random transactions related to it in mysql database by using data/ingest_data api.
-Created api data/users to fetch users and filter users by email,name.
-Created api data/transactions to fetch transactions and filter transactions by user_id, type, date_from, date_to.
-Created api data/transactions/summary to calculate.
-Added added.is_admin.py script to set user_id=1 as the admin.
-Created api data/data/delete/user_id here if created_user.is_admin then it can delete other user only. 


Postman-Collection
-thunder-collection_flask_assignment.json

How to run
1. In 1 terminal 
-flask db init
-flask db migrate -m "Added is_admin field to the user"
-flask db upgrade
-flask run
-export FLASK_APP=run.py
-export FLASK_ENV=development
flask run

2. In other terminal
- python generate_fake_data.py
-python added_is_admin.py 




