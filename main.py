from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"<Coffee Name: {self.name}>"


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route("/random", methods=["GET"])  # "GET" by default (doesn't have to be added)
def get_random_cafe():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(all_cafes)
    print(random_cafe)
    return jsonify(cafe={"id": random_cafe.id, "name": random_cafe.name, "map_url": random_cafe.map_url,
                         "img_url": random_cafe.img_url, "location": random_cafe.location, "seats": random_cafe.seats,
                         "has_toilet": random_cafe.has_toilet, "has_wifi": random_cafe.has_wifi,
                         "has_sockets": random_cafe.has_sockets, "can_take_calls": random_cafe.can_take_calls,
                         "coffee_price": random_cafe.coffee_price
                         })


@app.route("/all")
def get_all_cafe():
    all_cafes = db.session.query(Cafe).all()
    cafes = []
    for each_cafe in all_cafes:
        cafes.append(
            {"id": each_cafe.id, "name": each_cafe.name, "map_url": each_cafe.map_url, "img_url": each_cafe.img_url,
             "location": each_cafe.location, "seats": each_cafe.seats, "has_toilet": each_cafe.has_toilet,
             "has_wifi": each_cafe.has_wifi, "has_sockets": each_cafe.has_sockets,
             "can_take_calls": each_cafe.can_take_calls,
             "coffee_price": each_cafe.coffee_price
             })
    return jsonify({"cafes": cafes})


@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe={"id": cafe.id, "name": cafe.name, "map_url": cafe.map_url,
                             "img_url": cafe.img_url, "location": cafe.location,
                             "seats": cafe.seats,
                             "has_toilet": cafe.has_toilet, "has_wifi": cafe.has_wifi,
                             "has_sockets": cafe.has_sockets, "can_take_calls": cafe.can_take_calls,
                             "coffee_price": cafe.coffee_price
                             })
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.args.get("name"),
        map_url=request.args.get("map_url"),
        img_url=request.args.get("img_url"),
        location=request.args.get("loc"),
        has_sockets=bool(request.args.get("sockets")),
        has_toilet=bool(request.args.get("toilet")),
        has_wifi=bool(request.args.get("wifi")),
        can_take_calls=bool(request.args.get("calls")),
        seats=request.args.get("seats"),
        coffee_price=request.args.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe_to_update = db.session.query(Cafe).get(cafe_id)
    if cafe_to_update:
        new_price = request.args.get("new_price")
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price"})
    else:
        return jsonify(error={"Not Found": "Sorry, cafe with that ID was not found in the database"})


## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def report_closed(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe_to_del = db.session.query(Cafe).get(cafe_id)
        if cafe_to_del:
            db.session.delete(cafe_to_del)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
