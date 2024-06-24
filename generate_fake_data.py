

# this code is to save user in user table

# from faker import Faker
# import random
# import requests
# import json

# fake = Faker()
# breakpoint()
# def generate_fake_data(num_users=1000, num_transactions=10000):
#     users = []
#     transactions = []
#     emails =set()
    

#     while len(users) < num_users:
#         email = fake.email()
#         if email not in emails:
#             emails.add(email)
#     # for _ in range(num_users):
#             user = {
#             "name": fake.name(),
#             "email": email,
#             "password": fake.password(),
#             "created_at": fake.date_time_this_decade().isoformat()
#         }
#         # breakpoint()
#         print("user -->>",user)
#         users.append(user)
        
    
#     for _ in range(num_transactions):
#         transaction = {
#             "user_id": random.randint(1, num_users),
#             "amount": round(random.uniform(1, 1000), 2),
#             "timestamp": fake.date_time_this_year().isoformat(),
#             "type": random.choice(["credit", "debit"])
#         }
#         # breakpoint()
#         print("transaction-->>",transaction)
#         transactions.append(transaction)
    
#     return {"users": users, "transactions": transactions}

# data = generate_fake_data()
# print("data-->>",data)

# # Obtain JWT access token from the user
# access_token = input("Enter JWT token: ")

# # Set up the headers with the JWT token
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Bearer {access_token}'
# }

# # URL for the data ingestion endpoint
# url = "http://127.0.0.1:5000/data/ingest"

# # Make the POST request to ingest data
# response = requests.post(url, headers=headers, data=json.dumps(data))

# # Check the response status
# if response.status_code == 201:
#     print("Data ingested successfully")
# else:
#     print("Failed to ingest data")
#     print(response.status_code, response.text)



# This code is for saving transaction in the database
from faker import Faker
import random
import requests
import json
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from app.models import User  # Import your User model

fake = Faker()

DATABASE_URL = 'mysql+pymysql://root:ac3r@127.0.0.1:3306/flask_db'

# Set up database connection
engine = sa.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def generate_fake_data(num_transactions=10000):
    users = []
    emails = set()
    transactions = []

    # Retrieve user IDs from the database
    user_ids = [user.id for user in session.query(User).all()]

    # Generate fake transactions
    for _ in range(num_transactions):
        transaction = {
            "user_id": random.choice(user_ids),
            "amount": round(random.uniform(1, 1000), 2),
            "timestamp": fake.date_time_this_year().isoformat(),
            "type": random.choice(["credit", "debit"])
        }
        transactions.append(transaction)

    return {"transactions": transactions}

data = generate_fake_data()

access_token = input("Enter JWT token: ")

url = "http://127.0.0.1:5000/data/ingest"
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 201:
    print("Data ingested successfully")
else:
    print(f"Failed to ingest data. Status code: {response.status_code}")
    print(response.text)
