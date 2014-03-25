from flask import Flask, render_template, request, session, redirect
from cdc_db import init_db, db_session
from models import NewsPost

init_db()

admin_password='cdc'

app = Flask(__name__)

@app.route("/")
def index():
    newsPosts = NewsPost.query.all()
    if len(newsPosts) > 0:
        top = newsPosts[len(newsPosts)-1]
        no_news = False
    else:
        no_news = True
        top = 0

    return render_template('index.html', NEWS=top, NO_NEWS = no_news)

@app.route("/news")
def news():
    newsPosts = reversed(NewsPost.query.all())

    return render_template('news.html', NEWSPOSTS=newsPosts, \
            NAV_ACTIVE='news')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == admin_password:
            session['admin'] = True
            return redirect("/admin")
        else:
            return render_template('login.html', INCORRECT=True)
    else:
        return render_template('login.html', INCORRECT=False);

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    splash = '';
    if 'admin' in session:
        if session['admin'] == True:
            if request.method == 'POST':
                if request.form['mode'] == 'news':
                    n = NewsPost(request.form['heading'], request.form['body'])
                    db_session.add(n)
                    db_session.commit()
                    splash='News Post Created'
            return render_template('admin.html', SPLASH=splash)
    return redirect("/login")
 
@app.route("/logout")
def logout():
    if not 'admin' in session:
        return redirect("/")
    if session['admin'] == True:
        session['admin'] = False
    return redirect("/")

@app.errorhandler(404)
def err404(e):
    return render_template('404.html'), 404

#Make this EXTREMELY SECURE
app.secret_key = 'supersecret'

if __name__ == "__main__":
#NEVER run as app.debug = True
#   app.debug = False
    app.debug = True
    app.run()
