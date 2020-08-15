from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
from flask_pymongo import PyMongo
# Create an instance of our Flask app.
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/realestate_db")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    calgary_data = mongo.db.calgary_df_html.find()
    print(calgary_data)

    score_data = mongo.db.score_df_html.find()
    print(score_data)

    # Return template and data
    return render_template("index.html", calgary=[i for i in calgary_data], score=[j for j in score_data])

if __name__ == "__main__":
    app.run(debug=True)