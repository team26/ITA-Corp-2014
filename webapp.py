from flask import Flask, render_template, request, session, redirect
from cdc_db import init_db, db_session
from models import NewsPost

init_db()

admin_password='cdc'

app = Flask(__name__)

@app.route("/")
def index():
    newsPosts = db_session.query(NewsPost).all()
    if len(newsPosts) > 0:
        top = newsPosts[len(newsPosts)-1]
        no_news = False
    else:
        no_news = True
        top = 0

    return render_template('index.html', NEWS=top, NO_NEWS = no_news)

@app.route("/news")
def news():
    newsPosts = reversed(db_session.query(NewsPost).all())

    return render_template('news.html', NEWSPOSTS=newsPosts, \
            NAV_ACTIVE='news')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == admin_password:
            session['admin'] = True
            if 'next' in request.args: 
                return redirect(request.args.get('next'))
#           return redirect('/')
        else:
            return render_template('login.html', INCORRECT=True)
    else:
        return render_template('login.html', INCORRECT=False);

@app.route("/admin_news", methods=['GET', 'POST'])
def admin_news():
    splash = '';
    if session.get('admin') == True:
        if request.method == 'POST':
            n = NewsPost(request.form.get('heading'), request.form.get('body'))
            db_session.add(n)
            db_session.commit()
            splash='News Post Created'
        return render_template('admin_news.html', SPLASH=splash)
    return redirect("/login?next=/admin_news")
 
@app.route("/admin_jobs", methods=['GET', 'POST'])
def admin_jobs():
    splash = '';
    if session.get('admin') == True:
        if request.method == 'POST':
            n = Job(request.form.get('title'), request.form('desc'), ('exp'))
            db_session.add(n)
            db_session.commit()
            splash='Job Created'
        return render_template('admin_jobs.html', SPLASH=splash)
    return redirect("/login?next=/admin_jobs")

@app.route("/logout")
def logout():
#   if session.get('admin') == True:
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
