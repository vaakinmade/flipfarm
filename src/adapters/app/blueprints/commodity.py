from typing import Tuple, Any, Optional

from flask import Blueprint, render_template, request, flash, g, redirect, url_for, session
from dependency_injector.wiring import inject, Provide

from src.adapters.app.blueprints.auth import login_required
from src.domain.ports import update_commodity_factory
from src.main.containers import Container
from src.domain.ports.commodity_service import CommodityService, get_new_raised_amount, calculate_percentage_raised
from src.domain.utils import Money, validate_amount
from src.adapters.app.blueprints.investment import create_investment, update_investment
from src.domain.ports.investment_service import Status

blueprint = Blueprint('commodity', __name__, url_prefix='/commodity')


@blueprint.route('/<id_>', methods=['GET', 'POST'])
@login_required
@inject
def view_detail(id_,
                commodity_service: CommodityService = Provide[Container.commodity_package.commodity_service]):
    error = None
    commodity_data, investment_exists = get_commodity_data(id_)

    # amount and amount_raised from commodity_data is already in pence, do not re-convert
    amount_money = Money(commodity_data.get('amount'), convert_to_pence=False)
    amount_raised_money = Money(commodity_data.get('amount_raised'), convert_to_pence=False)

    if request.method == 'POST' and request.form["investment_type"] == "pooled":
        amount, error = validate_amount(request.form['amount'], request.form['custom_amount'])

        if not error:
            amount_raised, is_funded, exceeded_max = get_new_raised_amount(amount, amount_money, amount_raised_money)
            if not exceeded_max:
                commodity_ = update_commodity_factory(id_=id_, amount_raised=amount_raised, funded=is_funded)
                commodity_service.update_amount_raised(commodity_)
                commodity_data['funded'] = is_funded

                if investment_exists:
                    create_investment(amount=Money(amount), commodity_id=commodity_data.get('id'))
                else:
                    update_investment(amount=Money(amount), commodity_id=commodity_data.get('id'))
            else:
                error = "Please enter an value that does not exceed the available amount."
                flash(error, 'Error')
        else:
            flash(error, 'Error')

    amount_left = amount_money.value - amount_raised_money.value
    commodity_data['amount_left'] = Money.extract_leading_pence(amount_left)
    commodity_data['amount'] = Money.extract_leading_pence(amount_money.value)
    commodity_data['amount_raised'] = Money.extract_leading_pence(amount_raised_money.value)

    commodity_data['amount_left_trailing_pence'] = Money.extract_trailing_pence(amount_left)
    commodity_data['amount_trailing_pence'] = Money.extract_trailing_pence(amount_money.value)
    commodity_data['amount_raised_trailing_pence'] = Money.extract_trailing_pence(amount_raised_money.value)

    commodity_data['percentage_funded'] = calculate_percentage_raised(amount_money, amount_raised_money)
    return render_template('commodity/commodity_detail.html', commodity=commodity_data, id=id_, error=error,
                           commodity_data=commodity_data)


def get_commodity_data(id_,
                       commodity_service: CommodityService = Provide[Container.commodity_package.commodity_service]):
    # first try to get the commodity and the associated investment belonging to the investor
    # if there is no investment, proceed to fetch the commodity by itself.

    commodity_data = commodity_service.get_commodity_investment_for_investor(id_, session.get('id'))
    investment_exists = True
    if not commodity_data:
        commodity_data = commodity_service.get_commodity_by_id(id_)
        investment_exists = False
    return commodity_data, investment_exists


def index(commodity_service: CommodityService = Provide[Container.commodity_package.commodity_service]):
    pass