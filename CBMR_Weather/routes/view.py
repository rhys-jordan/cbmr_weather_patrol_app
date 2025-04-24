

from flask_login import login_required
from flask import request, redirect, url_for, send_file
import pandas as pd
from datetime import datetime
import io

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

@bp_view.route('/view/export')
@login_required
def download_excel():

    snow = Snow.query.order_by(desc(Snow.date)).all()
    snow_columns = [col.name for col in Snow.__table__.columns]
    snow_data = [{col: getattr(s, col) for col in snow_columns} for s in snow]
    snow_df = pd.DataFrame(snow_data)

    avy = Avalanche.query.order_by(desc(Avalanche.Snow_id)).all()
    avy_columns = [col.name for col in Avalanche.__table__.columns]
    avy_data = [{col: getattr(s, col) for col in avy_columns} for s in avy]
    avy_df = pd.DataFrame(avy_data)

    output = io.BytesIO()
    with pd.ExcelWriter(output) as writer:
        snow_df.to_excel(writer, index=False, sheet_name='Snow_Weather')
        avy_df.to_excel(writer, index=False, sheet_name='Avalanche')
    output.seek(0)

    fileName = "CBMR_allData_" + datetime.now().date().strftime('%Y-%m-%d') + ".xlsx"

    return send_file(output,
                     download_name=fileName,
                     as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
