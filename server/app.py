from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime  # Add this line to import datetime



from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Define the Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Create the database tables
db.create_all()


#Routes

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.json
    message = Message(body=data['body'], username=data['username'])
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.json
    message.body = data['body']
    db.session.commit()
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(port=5555)
