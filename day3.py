from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)

class Students(db.Model):
    __table_name = 'students'

    # 여기에 student 구성

@app.route('/create', methods=['GET'])
def create():
    student_id = request.args.get('student_id', None)
    student_name = request.args.get('student_name', None)
    student_phone_number = request.args.get('student_phone_number', None)
    if any([x is None for x in [student_id, student_name, student_phone_number]]):
        return abort(400)

    # 이 아래로 create 구현

    return 'OK'

@app.route('/show', methods=['GET'])
def show():
    # 이 아래로 show 구현



if __name__ ==  '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
