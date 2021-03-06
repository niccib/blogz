from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:purple@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'bb51112'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password




@app.before_request
def require_login():
    allowed_routes = ['index','blog','login','signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if len(username) < 3:
            flash('User name must be longer than 3 characters')
            return redirect('/signup')
        
        for name in username:
            if name == ' ':
                flash('Username cannot contain spaces')
                return redirect('/signup')

        if len(password) < 3:
            flash('Password must be longer than 3 characters')
            return redirect('/signup')       
        
        if password != verify:
            flash('Passwords do not match')
            return redirect('/signup')

        existing_user = User.query.filter_by(username=username).count()
        if existing_user > 0:
            flash('Username exists already')
            return redirect('/signup')


        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect("/newpost")
    else:
        return render_template('signup.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            print(session)
            return redirect('/')
        else:
            flash("User password incorrrect, or user does not exist", "error")
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # handles post requests and redirects to /blog after deleting the username 
    del session['username']
    return redirect('/blog')

@app.route('/blog', methods=['POST','GET'])
def blog():

    blog_id = request.args.get('id')
    user_id = request.args.get('user')
    users = User.query.all()
    if user_id:
        user_names = User.query.get(user_id)
        
        blogs = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('singleUser.html', blogs=blogs, user_id=user_names)

    if blog_id:
        single_blog = Blog.query.get(blog_id)
        user_name = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('blogpage.html', single_blog=single_blog, user=user_name)

    else:
        all_blogs = Blog.query.all()
        all_users = User.query.all()
        return render_template('blog.html', blogs=all_blogs, users=all_users)
        
    

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html')
    if request.method == 'POST':
        blog_body = request.form['body']
        blog_name = request.form['name']
        owner = User.query.filter_by(username=session['username']).first()
        amt_name = len(blog_name)
        amt_body = len(blog_body)
        title_error = ""
        text_error = ""
    if amt_name == 0:
        title_error = "Please enter a title for your blog"
    else:
        blog_name=blog_name

    if amt_body == 0:
        text_error="Please enter text about your blog"
    else:
        blog_body=blog_body

    if not title_error and not text_error:
        
        blog = Blog(blog_name, blog_body, owner)
        db.session.add(blog)
        db.session.commit()
        blogs = Blog.query.all()
        id = str(blog.id)
        
        return redirect('/blog?id='+ id)
    else:
        return render_template('newpost.html', name=blog_name,body=blog_body,title_error=title_error, text_error=text_error)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


    

if __name__ == "__main__":
    app.run()