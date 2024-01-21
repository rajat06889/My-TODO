from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

flag = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#db.init_app(app)
#app.app_context().push()

class Todo(db.Model):
    #__tablename__ = 'Todo'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    dt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"


@app.route('/hello')
def index():
    return "Hello World!"


@app.route('/', methods=['GET', 'POST'])
def post():
    global flag 
    print(flag)
    if flag:
        with app.app_context():
            db.create_all()
        flag = False
    if request.method == 'POST':
        print("second")
        title = request.form["title"]
        descp = request.form["desc"]

        todoo = Todo(title=title, desc=descp)
        db.session.add(todoo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', alltodo = allTodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)




if __name__ == "__main__":
    app.run(debug=True, port=5000)