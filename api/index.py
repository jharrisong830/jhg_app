import flask
import json
from time import strptime
import requests

DATE_FORMAT = "%Y-%m-%d"


app = flask.Flask(__name__)

@app.route("/")
def home():
    return flask.render_template("pages/home.html")

@app.route("/blog")
def blog():
    with open("api/templates/pages/blog_posts/blog_database.json") as f:
        data = json.load(f)
        sorted_posts = sorted(data, reverse=True, key=get_post_date) # type: ignore
        return flask.render_template("pages/blog.html", posts=enumerate(sorted_posts))

@app.route("/roadmap")
def roadmap():
    return flask.render_template("pages/roadmap.html")

@app.route("/blog/<int:blog_id>")
def blog_post(blog_id: int):
    with open("api/templates/pages/blog_posts/blog_database.json") as f:
        metadata = {}
        data = json.load(f)
        for post in data:
            if post["blog_id"] == blog_id:
                metadata = post
        if metadata == {}: flask.abort(404)
        return flask.render_template(f"pages/blog_posts/{metadata['filename']}", title=metadata["title"], description=metadata["description"], date=metadata["date"])

@app.route("/privacy")
def privacy():
    return flask.render_template("pages/privacy.html")

def get_post_date(p: dict[str:str]):
    """returns a date object for the date of the given post"""
    return strptime(p["date"], DATE_FORMAT)





if __name__ == "__main__":
    app.run()
