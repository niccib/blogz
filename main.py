from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:purple@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, name, body):
        self.name = name
        self.body = body

@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)


@app.route('/blog', methods=['POST','GET'])
def blog():
    blog_id = request.args.get('id')
    if blog_id == None:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)

    else:
        single_blog = Blog.query.get(blog_id)
        return render_template('blogpage.html', single_blog=single_blog)
    

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html')
    if request.method == 'POST':
        blog_body = request.form['body']
        blog_name = request.form['name'] 
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
        
        blog = Blog(blog_name, blog_body)
        db.session.add(blog)
        db.session.commit()
        blogs = Blog.query.all()
        return render_template('blog.html',name=blog_name, body=blog_body, blogs=blogs)
    else:
        return render_template('newpost.html', name=blog_name,body=blog_body,title_error=title_error, text_error=text_error)
        


@app.route('/blogpage', methods=['POST','GET'])
def blogpage():
    blog_id = request.args.get('id')
    blog_num = Blog.query.get(blog_id)
    return render_template('blogpage.html', blog_id=blog_num)

if __name__ == "__main__":
    app.run()