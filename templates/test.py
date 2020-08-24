
import psycopg2
from flask import Flask, render_template


app = Flask(__name__)


# connect to the db
con = psycopg2.connect(
            host="localhost",
            database="realestate_db",
            user="postgres",
            password="123"
)

#
# # create cursor
# cur = con.cursor()
#
# # execute query
# cur.execute("select price, address from calgary")
#
# calgary = cur.fetchall()

# for r in rows:
#     print(f'house on {r[1]} costs {r[0]}')

#
# # close cursor
# cur.close()
#
#
# # close the connection
# con.close()
#
#

@app.route("/")
def home():

    # create cursor
    cur = con.cursor()

    # execute query
    cur.execute("SELECT cl.price, cl.address, cl.postal_code, s.walk_score, s.bike_score, s.transit_score FROM calgary AS cl JOIN score AS s ON cl.postal_code = s.postal_code")

    calgary_data = cur.fetchall()
    # print(calgary_data)

    # for r in calgary_data:
    #     print(f'house on {r[1]} costs ${r[0]} and a walkscore of {r[3]}')


    # close cursor
    cur.close()


    # close the connection
    con.close()

    # Return template and data
    return render_template("index.html", calgary_data=calgary_data)


if __name__ == "__main__":
    app.run(debug=True)

