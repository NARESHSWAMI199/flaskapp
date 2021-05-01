import re
from flask import Flask,render_template,request,redirect,url_for,session
from models import BlogPost,User
from models import db,app
from forms import RegistraionForm,LoginForm
# from app import db
import os

# createing a sequrit key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/posts')
def posts():
        # get data from database
        blog_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html',blog_post=blog_posts)


# post delete view

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=('GET','POST'))
def edit(id):
    # you can get also if the id not exists get don't raise any type beacuse this return none
    # but get_or_404 return error
    post = BlogPost.query.get_or_404(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    return render_template('edit.html',post=post)

@app.route('/posts/new',methods = ['GET','POST'])
def newpost():
        if request.method == "POST":
            post_title = request.form['title']
            post_content = request.form['content']
            post_author = request.form['author']
            # this not save data parmantly but still save
            new_post = BlogPost(title=post_title,content=post_content,author=post_author)
            db.session.add(new_post)
            # this will actual save the data
            db.session.commit()
            return redirect('/posts')
        else:
            return render_template('new_post.html')
        
@app.route('/register',methods=('GET','POST'))
def register():
    form = RegistraionForm(request.form)
    if request.method == "POST":
        user_name = request.form['username']
        user_email = request.form['email']
        user_password = request.form['password']
        user_confirm = request.form['confirm']
        if user_confirm == user_password:
            newUser = User(name=user_name,email=user_email,password=user_password)
            db.session.add(newUser)
            db.session.commit()
            return redirect('/')
        else:
            error = {"error" : "You password are not matched"}
            return render_template("register.html",error=error)

    return render_template("register.html",form = form)


@app.route('/login',methods=('GET','POST'))
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        session.pop('user',None)
        username = request.form['username']
        password = request.form['password']

        
        


    return render_template('login.html',form=form)



if __name__ == "__main__":
    app.run(debug=True)