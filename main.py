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

@app.route('/', methods=['POST','GET'])
def index():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)


@app.route('/blog', methods=['POST','GET'])
def blog():
    if request.method == 'POST':
        blog_body = request.form['body'] 
        blog_name = request.form['title']
        new_blog = Blog(blog_name,blog_body)
        db.session.add(new_blog)
        db.session.commit()

        blogs = Blog.query.all()

        return render_template('blog.html',title=blog_name, body=blog_body, blogs=blogs)

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    return render_template('newpost.html')


@app.route('/blogpage')
def blogpage():
    blog_id = request.args.get('blog-id')
    return render_template('blogpage.html', id=blog_id)

if __name__ == "__main__":
    app.run()