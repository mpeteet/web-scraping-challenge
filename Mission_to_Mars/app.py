rom flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask Setup
app = Flask(__name__)

# Use Pymongo to establish Mongo connection
mongo = Pymongo(app, uri="mongodb://localhost:27017/mars_app")
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)

# Route to render an index.html template using Mongo data
@app.route("/")
def home():

    # Find more record of data from the mongo database
    mars_dictionary = mongo.db.mars_dictionary.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_dictionary)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dictionary = mongo.db.mars_dictionary
    mars_dictionary= scrape_mars.scrape()
    mars_dictionary.update({}, mars_dictionary, upsert=True)
    #mongo.db.collection.update({}, mars_dictionary, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)




