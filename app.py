
import pubchempy as pcp
import chemica.engine as chemica
from chemica.substance import Substance
from chemica.structure import Structure
from chempy import chemistry
from helpers import *
import PIL
from flask import Flask, render_template, request, redirect

import sys


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("home.html")


@app.route("/structure")
def structure():

    return render_template("structure.html")


@app.route("/periodic_stable")
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


@app.route("/calc", methods=["GET", "POST"])
def index():
    """ Simple Reaction Calculator """

    if request.method == "POST":
        A_reagent = request.form.get("A")
        B_reagent = request.form.get("B")

        # Make sure there is input
        if A_reagent is None or B_reagent is None:
            print("oops")

        # Solve for products
        try:
            solved = chemica.solve(A_reagent, B_reagent)
        except Exception:
            print("oops")
        # If there is an error
        if type(solved) == str:
            print("oops")

        # Get the balanced equation and the reagent names by unpacking tuple
        # Why? balanced_eq has coef will reagents don't (except for dict values)
        balanced_equation, reagents = solved

        # Parse balanced equation
        # Get the fixed reagents
        fixed_reagents = balanced_equation.split("→")

        # Reactants
        fixed_A, fixed_B = fixed_reagents[0].split("+")
        # Products
        fixed_products = fixed_reagents[1]

        # Parse reagent names
        reactants, products = reagents
        reac_reagents = list(reactants.keys())
        prod_reagents = list(products.keys())
        # If it has more than 1 product, forcibly get an error 'message'
        if len(prod_reagents) > 1:
            prod_reagents = ["C4"]

        return render_template("predicted.html", A=fixed_A, B=fixed_B, prod=fixed_products, reac_reagents=reac_reagents, prod_reagents=prod_reagents)

    return render_template("predictor.html")


@app.route("/lewis_api/<formula>")
def lewis_api(formula):
    structure = Structure.from_formula(formula)
    return serve_pil_image(structure.lewis)


if "__main__" == __name__:
    app.run(host="0.0.0.0", debug=True)
