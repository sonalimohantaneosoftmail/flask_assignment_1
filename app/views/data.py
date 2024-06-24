from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Transaction
from flask_jwt_extended import jwt_required, get_jwt_identity

main_data = Blueprint('data', __name__, url_prefix='/data')

# @main.route('/ingest', methods=['POST'])
# @jwt_required()
# def ingest_data():
#     data = request.get_json()
#     # try:
#     for user_data in data.get('users',[]):
#             existing_user = User.query.filter_by(email=user_data['email']).first()
        
#             if existing_user is None:                
#                 user = User(
#                     name=user_data['name'],
#                     email=user_data['email'],
#                     password=user_data['password'],
#                     created_at=user_data.get('created_at', None)
#                 )
#                 db.session.add(user)
            
#     for transaction_data in data.get('transactions',[]):
#                 #there is an attempt to insert a transaction with a user_id that does not exist in the user table, violating the foreign key constraint.
#                 user_exists = User.query.filter_by(id=transaction_data['user_id']).first()
#                 if user_exists:
#                     transaction = Transaction(
#                     user_id=transaction_data['user_id'],
#                     amount=transaction_data['amount'],
#                     timestamp=transaction_data.get('timestamp', None),
#                     type=transaction_data['type']
#                         )
#                     db.session.add(transaction)
#                 else:
#                     continue
            
#     db.session.commit()
#     return jsonify(message="Data ingested successfully"), 201
    
    # except Exception as e:
    #     db.session.rollback()
    #     return jsonify({'error': str(e), 'message': 'Failed to ingest data'}), 400

   

@main_data.route('/ingest', methods=['POST'])
@jwt_required()
def ingest_data():
    data = request.get_json()
    try:
        # Add users
        users_to_insert = []
        for user_data in data.get('users', []):
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user is None:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'],
                    created_at=user_data['created_at']
                )
                users_to_insert.append(user)
        db.session.bulk_save_objects(users_to_insert)
        db.session.commit()  # Commit user additions to get their IDs

        # Fetch all user IDs
        user_ids = {user.id for user in User.query.all()}

        # Add transactions
        transactions_to_insert = []
        for transaction_data in data.get('transactions', []):
            if transaction_data['user_id'] in user_ids:
                transaction = Transaction(
                    user_id=transaction_data['user_id'],
                    amount=transaction_data['amount'],
                    timestamp=transaction_data['timestamp'],
                    type=transaction_data['type']
                )
                transactions_to_insert.append(transaction)

        db.session.bulk_save_objects(transactions_to_insert)
        db.session.commit()
        return jsonify({'message': 'Data ingested successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'message': 'Failed to ingest data'}), 400


# breakpoint()
@main_data.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    query_params = request.args
    name = query_params.get('name')
    email = query_params.get('email')
    
    users = User.query

    # if name or email:
    #     users = users.filter(User.name==name) or users.filter(User.email==email)
    if name:
        users = users.filter(User.name == name)
    if email:
        users = users.filter(User.email == email)
    
    users = users.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email, 'created_at': user.created_at} for user in users])
    



@main_data.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    query_params = request.args
    user_id = query_params.get('user_id')
    transaction_type = query_params.get('type')
    date_from = query_params.get('date_from')
    date_to = query_params.get('date_to')
    
    transactions = Transaction.query
    if user_id:
        transactions = transactions.filter(Transaction.user_id == user_id)
    if transaction_type:
        transactions = transactions.filter(Transaction.type == transaction_type)
    if date_from:
        transactions = transactions.filter(Transaction.timestamp >= date_from)
    if date_to:
        transactions = transactions.filter(Transaction.timestamp <= date_to)
    
    transactions = transactions.all()
    return jsonify([{
        'id': transaction.id,
        'user_id': transaction.user_id,
        'amount': transaction.amount,
        'timestamp': transaction.timestamp,
        'type': transaction.type
    } for transaction in transactions])

@main_data.route('/transactions/summary', methods=['GET'])
@jwt_required()
def get_transaction_summary():
    total_transactions = Transaction.query.count()
    total_amount = db.session.query(db.func.sum(Transaction.amount)).scalar()
    average_amount = db.session.query(db.func.avg(Transaction.amount)).scalar()
    
    return jsonify({
        'total_transactions': total_transactions,
        'total_amount': total_amount,
        'average_amount': average_amount
    })



@main_data.route('/data/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    breakpoint()
    current_user_id = get_jwt_identity()
    print("current_user_id-->>",current_user_id['id'])
    current_user_id_id=current_user_id['id']
    current_user = User.query.get(current_user_id_id)
    print("current_user-->>",current_user)
    print(current_user.is_admin)

    if current_user and current_user.is_admin:
        print("user_id-->>",user_id)
        user_to_delete = User.query.get(user_id)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Unauthorized to delete "}), 403




