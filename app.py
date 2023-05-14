from flask import Flask, flash, redirect, request, jsonify, make_response, render_template, url_for

from flask_sqlalchemy import SQLAlchemy
from os import environ


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)


    def json(self):
        return {'id': self.id,'name': self.name, 'email': self.email,'age':self.age, 'gender':self.gender}

db.create_all()
#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)




@app.route('/')
def index():
    people = User.query.all()
    return render_template('person-Interaction.html', people=people)




# create 
@app.route('/submit', methods=['POST'])
def create_user():
   # try:
    name=request.form['name']
    email=request.form['email']
    age=request.form['age']
    gender=request.form['gender']
    new_user = User(name=name, email=email, age=age, gender=gender)
    db.session.add(new_user)
    db.session.commit()
    print("created")
    return redirect(url_for('index'))

# delete 
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
  try:
    user = User.query.filter_by(id=user_id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return redirect(url_for('index'))
    return ('User Not Found')
  except Exception as e:
    return ('error deleting a user')

#update 
@app.route('/update/<int:user_id>')
def update_page(user_id):
    user = User.query.get(user_id)
    return render_template('update.html', user=user, user_id=user_id)

@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return 'User not found'
    user.name = request.form['name']
    user.email = request.form['email']
    user.age = request.form['age']
    user.gender = request.form['gender']
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()



 
