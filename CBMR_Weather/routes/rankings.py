from CBMR_Weather.routes import bp_rankings
from flask import render_template



@bp_rankings.route("/rankings",methods=['GET', 'POST'])
def rankings():
    print("Put page here")
    return render_template("rankings.html")