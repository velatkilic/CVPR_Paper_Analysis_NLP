from flask import Flask, request, redirect, url_for, render_template
from utils import predict
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        papers = request.form["papers"]
        return redirect(url_for("results", papers=papers))
    else:
        return render_template("home.html")

@app.route("/<papers>")
def results(papers):
    out = predict(papers)
    return render_template("results.html", out=out)

if __name__=="__main__":
    app.run(debug=True)