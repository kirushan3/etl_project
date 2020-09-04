from flask import Flask, render_template
from flask_pymongo import PyMongo


# Create an instance of our Flask app.
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/realestate_db")


# engine = create_engine("postgresql://postgres:123@localhost:5432/realestate_db")



# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    calgary_data = mongo.db.calgary.find()
    # for i in calgary_data:
        # print(i)
    print(calgary_data)

    score_data = mongo.db.score.find()
    print(score_data)

    # Return template and data
    return render_template("index.html", calgary=[i for i in calgary_data], score=[j for j in score_data])


if __name__ == "__main__":
    app.run(debug=True)