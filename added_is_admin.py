# update_user_to_admin.py
from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

# Update user with id 1 to be admin
user = User.query.get(1)
if user:
    user.is_admin = True
    db.session.commit()
    print(f"User {user.name} is now an admin.")
else:
    print("User not found.")
