from flask import Flask,render_template,request,jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/valueDisplay',methods = ["POST"])
def valueDisplay():
    data = request.get_json()
    inputValue = data.get("value","")
    updatedValue = "You Typed: " + inputValue
    if inputValue:
        return jsonify({'value':updatedValue})
    return jsonify({'value':''})

if __name__ == '__main__':
    app.run(debug = True)