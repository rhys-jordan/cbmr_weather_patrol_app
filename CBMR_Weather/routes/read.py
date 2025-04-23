from CBMR_Weather.routes import bp_read
from flask import render_template
from CBMR_Weather.models import User, Snow
from sqlalchemy import desc, asc

@bp_read.route("/read", methods=['GET', 'POST'])
def read():

    snow1 = Snow.query.filter(Snow.hn24 != None).order_by(desc(Snow.hn24)).first()
    hn24Greatest = snow1.hn24
    hn24Greatest_date = snow1.date
    snow2 = Snow.query.filter(Snow.past_24_temp_low != None).order_by(asc(Snow.past_24_temp_low)).first()
    temperatureColdest = snow2.past_24_temp_low
    temperatureColdest_date = snow2.date
    snow3 = Snow.query.filter(Snow.hs != None).order_by(desc(Snow.hs)).first()
    hsDeepest = snow3.hs
    hsDeepest_date = snow3.date

    stats = {
        'hn24Greatest': hn24Greatest,
        'hn24Greatest_date': hn24Greatest_date,
        'temperatureColdest': temperatureColdest,
        'temperatureColdest_date': temperatureColdest_date,
        'hsDeepest': hsDeepest,
        'hsDeepest_date': hsDeepest_date,
    }

    return render_template('read.html', stats=stats)