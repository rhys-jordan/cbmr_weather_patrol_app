from CBMR_Weather.routes import bp_view
from flask import render_template
from CBMR_Weather.models import Snow
from sqlalchemy import desc


@bp_view.route("/view",methods=['GET', 'POST'])
def view():
    snow = Snow.query.order_by(desc(Snow.date)).all()
    return render_template('view.html', snow=snow)