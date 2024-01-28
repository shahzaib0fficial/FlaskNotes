from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def frontPage():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        name = request.form.get("name","Anonymous")
        return render_template("greet.html",name=name)

if __name__ == "__main__":
    app.run(debug = True, port=8000)