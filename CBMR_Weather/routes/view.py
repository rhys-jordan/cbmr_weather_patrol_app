from flask_login import login_required
from flask import request,redirect,url_for

# from CBMR_Weather.app import Pm_form
from CBMR_Weather.routes import bp_view
from flask import render_template
from sqlalchemy import desc
from CBMR_Weather.extensions import db
from CBMR_Weather.models import Snow, Avalanche, Pm_form


@bp_view.route("/view",methods=['GET', 'POST'])
def view():
    snow = Snow.query.order_by(desc(Snow.date)).all()
    return render_template('view.html', snow=snow)

@bp_view.route('/view_am/<inputDate>', methods=['GET', 'POST'])
@login_required
def delete_am_data(inputDate):
    if request.method == 'GET':
        dateCheck = Snow.query.filter_by(date=inputDate).first()
        if dateCheck:
            Avalanche.query.filter_by(Snow_id=dateCheck.id).delete(synchronize_session=False)
            db.session.delete(dateCheck)
            db.session.commit()
    snow = Snow.query.order_by(desc(Snow.date)).all()

    return redirect(url_for('view.view', snow=snow))

@bp_view.route('/view_pm/<inputDate>', methods=['GET', 'POST'])
@login_required
def delete_pm_data(inputDate):
    if request.method == 'GET':
        dateCheck = Pm_form.query.filter_by(date=inputDate).first()
        if dateCheck:
            db.session.delete(dateCheck)
            db.session.commit()
    snow = Snow.query.order_by(desc(Snow.date)).all()

    return redirect(url_for('view.view', snow=snow))