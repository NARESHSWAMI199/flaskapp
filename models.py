from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


# we going to create a model for db like models.py in django
class BlogPost(db.Model):
    # django has a default id field but we need to create in flask but default auto increment
    id = db.Column(db.Integer, primary_key = True )
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text,nullable=False)
    author  = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)

    # something like __str__ function in djagno
    def __repr__(self):
        return "Blog post " + str(self.id)




# user Authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20),nullable=False )
    email = db.Column( db.String(120) , nullable=False)
    password = db.Column(db.Text , nullable=False)
    __table_args__ = (
        # this can be db.PrimaryKeyConstraint if you want it to be a primary key
        db.UniqueConstraint('email'),
      )
    # flask don't have any emailField in models but aslo has in forms where you can validate this 

    def __repr__(self):
        return str(self.name)



if __name__ == '__main__':
    manager.run()


    # you need some commands to create post.db
    # open python shell
    # import db 
    # from app import db
    # db.create_all() 
    # for check data
    # BlogPost.query.all()
    # for create data
    # db.session.add(BlogPost(title="and samething in all field"))
    # for save data
    # db.session.commit()