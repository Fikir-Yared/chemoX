from flask import Flask, render_template, request
import pubchempy as pcp

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("home.html")


@app.route("/structure")
def structure():

    return render_template("structure.html")


@app.route("/periodic_table")
def periodic_table():

    return render_template("periodic_table.html")


@app.route('/structure/molecules', methods=['GET'])
def my_form_post():

    text = request.args['molecule']

    try:
        response = pcp.get_compounds(text, 'name')
        result = response[0].isomeric_smiles
    except:
        result = "Not Available"

    return render_template("structure.html",
                           compound=result,
                           compound_name=text.capitalize())


if "__main__" == __name__:
    app.run(host="0.0.0.0", debug=True)
