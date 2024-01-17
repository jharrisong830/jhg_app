import flask
import json
from time import strptime

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


# preliminary json -> table converter, DO NOT PUBLISH
@app.route("/convert", methods=["GET", "POST"])
def convert():
    if flask.request.method == "GET":
        return flask.render_template("pages/convert.html", tableCells="<p class=\"text-center lead text-body-emphasis\">Enter a valid JSON object above, and it will render in HTML here!</p>")
    elif flask.request.method == "POST":
        try:
            data = flask.request.form["jsonInp"]
            jsonObj = json.loads(data)
            tableString = renderObject(jsonObj)
            return flask.render_template("pages/convert.html", tableCells=tableString)
        except:
            return flask.render_template("pages/convert.html", tableCells="<p class=\"text-center lead text-body-emphasis\">There was an error parsing your JSON text. Please try again, and insure your input has valid syntax.</p>")


def renderObject(obj) -> str:
    if isinstance(obj, dict):
        oKeys = obj.keys()
        tableString = f"<table class=\"table table-light table-hover table-bordered\"> <tr> <th>[obj]</th> {"".join([f'<th>{x}</th>' for x in oKeys])} </tr>" # adding header row
        tableString += f"<tr> <td></td> {"".join([f'<td>{renderObject(obj[x])}</td>' for x in oKeys])} </tr> </table>"
        return tableString
    elif isinstance(obj, list):
        tableString = f"<table class=\"table table-light table-hover table-bordered\"> <tr> <th>[ind]</th> <th>[elem]</th> </tr>" # adding header row
        for i in range(len(obj)):
            tableString += f"<tr> <td>{i}</td> <td>{renderObject(obj[i])}</td> </tr>"
        tableString += "</table>"
        return tableString
    else:
        return str(obj)





if __name__ == "__main__":
    app.run()
