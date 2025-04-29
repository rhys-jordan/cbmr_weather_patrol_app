

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
    search_query = request.args.get("search", "").strip()
    search_column = request.args.get("column", "").strip()
    sort_order = request.args.get("sort_order", "asc")
    column_map = {
        "date": Snow.date,
        "season": Snow.season,
        "hs": Snow.hs,
        "hn24": Snow.hn24,
        "hn24_swe":Snow.swe,
        "hst": Snow.hst,
        "ytd_snow": Snow.ytd_snow,
        "ytd_swe": Snow.ytd_swe,
        "temperature": Snow.temperature,
        "wind_mph": Snow.wind_mph,
        "wind_direction": Snow.wind_direction,
        "peak_gust": Snow.current_peak_gust_mph,
    }

    query = Snow.query
    if search_column =='date' and sort_order =='desc':
        query = query.order_by(Snow.date.desc())
    if search_column =='date' and sort_order =='asc':
        query = query.order_by(Snow.date.asc())
    if search_query and search_column in column_map:
        column_attr = column_map[search_column]
        like_pattern = f"%{search_query}%"
        query = query.filter(db.cast(column_attr, db.String).like(like_pattern))
    if search_column in column_map:
        column_attr = column_map[search_column]
        query = query.filter(column_attr.isnot(None))
        numeric_columns = ["hs", "hn24", "hn24_swe", "hst", "ytd_snow", "ytd_swe", "temperature", "wind_mph",
                           "peak_gust"]
        if search_column in numeric_columns:
            if sort_order == "desc":
                query = query.order_by(db.cast(column_attr, db.Float).desc())
            else:
                query = query.order_by(db.cast(column_attr, db.Float).asc())
        else:
            if sort_order == "desc":
                query = query.order_by(column_attr.desc())
            else:
                query = query.order_by(column_attr.asc())
    else:
        query = query.order_by(Snow.date.desc())

    snow = query.all()
    pm_form_dates = [str(i.date) for i in Pm_form.query.all()]
    return render_template("view.html", snow=snow, search=search_query, column=search_column, sort_order=sort_order,pm_form_dates=pm_form_dates)

@bp_view.route('/view_am/<inputDate>', methods=['GET', 'POST'])
@login_required
def delete_am_data(inputDate):
    if request.method == 'GET':
        dateCheck = Snow.query.filter_by(date=inputDate).first()
        if dateCheck:
            Avalanche.query.filter_by(Snow_id=dateCheck.id).delete(synchronize_session=False)
            db.session.delete(dateCheck)
            db.session.commit()
            dateCheck_pm = Pm_form.query.filter_by(date=inputDate).first()
            if dateCheck_pm:
                db.session.delete(dateCheck_pm)
                db.session.commit()
    snow = Snow.query.order_by(desc(Snow.date)).all()
    return redirect(url_for('view.view'))

@bp_view.route('/view_pm/<inputDate>', methods=['GET', 'POST'])
@login_required
def delete_pm_data(inputDate):
    if request.method == 'GET':
        dateCheck = Pm_form.query.filter_by(date=inputDate).first()
        if dateCheck:
            db.session.delete(dateCheck)
            db.session.commit()
    snow = Snow.query.order_by(desc(Snow.date)).all()

    return redirect(url_for('view.view'))

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
