

from CBMR_Weather.routes import bp_rankings
from flask import render_template

from CBMR_Weather.extensions import db
from CBMR_Weather.models import Snow


def get_month_by_ytd(month, season):
    total_month_ytd = db.session.query(Snow.ytd_snow).filter(Snow.season == season, Snow.month == month).order_by(Snow.date.desc()).first()
    if total_month_ytd is None or total_month_ytd[0] is None:
        return 0
    else:
        return total_month_ytd[0]


@bp_rankings.route("/rankings",methods=['GET', 'POST'])
def rankings():
    seasons_db = db.session.query(Snow.season).distinct()
    seasons_totals = []
    months = ['10', '11', '12', '1', '2', '3', '4']
    for s in seasons_db:
        season_monthly_totals = [s[0]]
        prev_month = 0
        for m in months:
            month_total = get_month_by_ytd(m, s[0])
            season_monthly_totals.append(month_total - prev_month)
            prev_month = month_total
        season_monthly_totals.append(prev_month)
        seasons_totals.append(season_monthly_totals)

    seasons_totals.sort(key=lambda x: x[-1], reverse=True)


    return render_template("rankings.html", ytd_snow_total = seasons_totals)