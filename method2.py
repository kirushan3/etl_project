from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, inspect


engine = create_engine("postgresql://postgres:123@localhost:5432/realestate_db")

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Base.classes.keys()[0]

Session = sessionmaker(bind=engine)

session = Session()


# Show name of the rows and type in the Measurement table

inspector = inspect(engine)
measurement_columns = inspector.get_table_names()
#
#
#
# for c, s in session.query(calgary, score).filter(calgary.postal_code == score.postal_code).all():
#    print ("ID: {} Name: {} Invoice No: {} Amount: {}".format(c.price, c.adress, s.walk_score, s.bike_score, s.transit_score))