from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database configuration (update with your AWS RDS details)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://admin:Surveydbs123@database-1.cee1bzde0hsf.us-east-1.rds.amazonaws.com:3306/studentdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class StudentSurvey(db.Model):
    __tablename__ = 'student_survey'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    street = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(10))
    telephone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    date_of_survey = db.Column(db.String(20))
    liked_most = db.Column(db.String(200))
    interest_source = db.Column(db.String(200))
    likelihood = db.Column(db.String(100))

# Routes
@app.route('/api/surveys', methods=['POST'])
def create_survey():
    data = request.get_json()
    survey = StudentSurvey(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        street=data.get('street'),
        city=data.get('city'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
        telephone=data.get('telephone'),
        email=data.get('email'),
        date_of_survey=data.get('date_of_survey'),
        liked_most=data.get('liked_most'),
        interest_source=data.get('interest_source'),
        likelihood=data.get('likelihood')
    )
    db.session.add(survey)
    db.session.commit()
    return jsonify({'message': 'Survey submitted successfully!'}), 201

@app.route('/api/surveys', methods=['GET'])
def get_all_surveys():
    surveys = StudentSurvey.query.all()
    output = []
    for s in surveys:
        survey_data = {
            'id': s.id,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'street': s.street,
            'city': s.city,
            'state': s.state,
            'zip_code': s.zip_code,
            'telephone': s.telephone,
            'email': s.email,
            'date_of_survey': s.date_of_survey,
            'liked_most': s.liked_most,
            'interest_source': s.interest_source,
            'likelihood': s.likelihood
        }
        output.append(survey_data)
    return jsonify(output)

@app.route('/api/surveys/<int:id>', methods=['GET'])
def get_survey(id):
    survey = StudentSurvey.query.get_or_404(id)
    return jsonify({
        'id': survey.id,
        'first_name': survey.first_name,
        'last_name': survey.last_name,
        'street': survey.street,
        'city': survey.city,
        'state': survey.state,
        'zip_code': survey.zip_code,
        'telephone': survey.telephone,
        'email': survey.email,
        'date_of_survey': survey.date_of_survey,
        'liked_most': survey.liked_most,
        'interest_source': survey.interest_source,
        'likelihood': survey.likelihood
    })

@app.route('/api/surveys/<int:id>', methods=['DELETE'])
def delete_survey(id):
    survey = StudentSurvey.query.get_or_404(id)
    db.session.delete(survey)
    db.session.commit()
    return jsonify({'message': 'Survey deleted successfully!'}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
