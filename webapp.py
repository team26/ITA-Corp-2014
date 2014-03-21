from flask import Flask, render_template
from cdc_db import init_db, db_session
from models import NewsPost

init_db()

app = Flask(__name__)

@app.route("/")
def index():
    newsPosts = NewsPost.query.all()
    top = newsPosts[len(newsPosts)-1]
    return render_template('index.html', NEWS=top)

@app.route("/news")
def news():
    newsPosts = reversed(NewsPost.query.all())
    return render_template('news.html', NEWSPOSTS=newsPosts, NAV_ACTIVE='news')

@app.errorhandler(404)
def err404(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
#NEVER run as debug = True
#    app.debug = False
    app.debug = True
    app.run()
