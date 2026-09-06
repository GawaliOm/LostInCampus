from flask import Flask, render_template, request

app = Flask(__name__)


# Function to load homepage

@app.route("/")
def home():
    return render_template("index.html")


# Function for reporting lost item

@app.route("/report/lost", methods = ["GET", "POST"])
def reportLost():

    if request.method == "POST":
        name = request.form["name"]
        item_name = request.form["item_name"]
        email = request.form["email"]
        print("name: ", name)
        print("item name: ", item_name)
        print("email: ", email)
        return "lost report recived"
    return render_template("reportLost.html")


# Function for reporting founded item

@app.route("/report/found", methods = ["GET", "POST"])
def reportfound():

    if request.method == "POST":
        name = request.form["name"]
        item_name = request.form["item_name"]
        email = request.form["email"]
        print("name: ", name)
        print("item name: ", item_name)
        print("email: ", email)
        return "Found Report Sent"
    return render_template("reportFound.html")



if __name__ == "__main__":
    app.run(debug = True)