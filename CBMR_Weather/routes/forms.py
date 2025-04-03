from CBMR_Weather.routes import bp_forms
from flask_login import login_required
from flask import render_template

@bp_forms.route("/forms", methods=['GET', 'POST'])
@login_required
def forms():
    return render_template('forms.html')