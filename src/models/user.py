from src.utils.db import db
from sqlalchemy import create_engine, text

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_as = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.String(120), unique=True, nullable=False)
    updated_at = db.Column(db.String(120), unique=True, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role_as': self.role_as,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def get_all():
        return User.query.order_by(User.id).all()

    def __repr__(self):
        return '<id {}>'.format(self.id)
    # create function that needed by controllers
    @staticmethod
    def get_by_id(id):
        return User.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_ids(ids):
        return User.query.filter(User.id.in_(ids)).all()
    
    @staticmethod
    def get_data_for_recommendation(ids):
        sql_query = text('''
            SELECT *
            FROM users
            JOIN test_results ON users.id = test_results.user_id
            JOIN test_result_details ON test_results.id = test_result_details.result_id
            JOIN question_banks ON test_result_details.question_id = question_banks.id
            WHERE users.id IN :user_ids
        ''').bindparams(user_ids=ids)

        # execute raw query
        result = db.session.execute(sql_query)

        # Fetch the results
        rows = result.fetchall()

        # Close the result
        result.close()

        return rows
