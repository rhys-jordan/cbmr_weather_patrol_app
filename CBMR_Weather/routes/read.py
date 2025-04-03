from CBMR_Weather.routes import bp_read
from flask import render_template

@bp_read.route("/read", methods=['GET', 'POST'])
def read():
    return render_template('read.html')