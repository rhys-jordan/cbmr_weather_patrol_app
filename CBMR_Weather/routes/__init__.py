from flask import Blueprint

bp_home = Blueprint('home', __name__)
bp_am_form = Blueprint('am_form', __name__)
bp_forms = Blueprint('forms', __name__)
bp_read = Blueprint('read', __name__)
bp_view = Blueprint('view', __name__)
bp_pm_form = Blueprint('pm_form', __name__)
bp_update_form = Blueprint('update_form', __name__)
bp_past_form = Blueprint('past_form', __name__)
bp_update_pm_form = Blueprint('update_pm_form',__name__)
bp_rankings = Blueprint('rankings',__name__)


from CBMR_Weather.routes import (home, am_form, forms, read, view, rankings,
                                 pm_form, update_form, past_data_form, update_pm_form)

from CBMR_Weather import login_manager
from CBMR_Weather.models import User
@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user
