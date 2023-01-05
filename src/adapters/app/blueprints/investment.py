from flask import Blueprint, render_template, request, flash, g, redirect, url_for, session
from dependency_injector.wiring import inject, Provide

from src.adapters.app.blueprints.auth import login_required
from src.domain.ports import create_investment_factory, update_investment_factory
from src.domain.ports.investment_service import InvestmentService, calculate_percentage, Status
from src.main.containers import Container
from src.domain.utils import Money, validate_amount

blueprint = Blueprint('investment', __name__, url_prefix='/investment')


# @blueprint.route('/')
# @inject
# def index(investment_service: InvestmentService = Provide[Container.investment_package.investment_service]):
#     investment = investment_service.get_investments_by_investor_id(session.get('id'))
#     return render_template('investment/index.html', investment=investment)


@inject
def create_investment(amount: Money, commodity_id: int,
                      investment_service: InvestmentService = Provide[
                          Container.investment_package.investment_service]
                      ) -> None:
    investment_ = create_investment_factory(amount=amount,
                                            commodity_id=commodity_id,
                                            investor_id=session.get('id'),
                                            status=Status.ACTIVE.value)
    investment_service.create(investment_)


@inject
def update_investment(amount: Money, commodity_id: int,
                      investment_service: InvestmentService = Provide[
                          Container.investment_package.investment_service]
                      ) -> None:
    investment_ = investment_service.get_investment_by_investor_and_commodity_id(session.get('id'), commodity_id)
    top_up_amount = amount.add(Money(investment_.get('amount'), convert_to_pence=False))
    investment_ = update_investment_factory(id_=investment_.get('id_'),
                                            amount=top_up_amount,
                                            commodity_id=commodity_id,
                                            investor_id=session.get('id'))
    investment_service.update_investment_amount(investment_)


@blueprint.route('/user-investments', methods=('GET', 'POST'))
@login_required
@inject
def user_investments(investment_service: InvestmentService = Provide[Container.investment_package.investment_service]):
    user_id = session.get('id')
    investments_data = investment_service.get_investments_by_investor_id(user_id)

    for data in investments_data:
        return_amount = int(data['amount']) + calculate_percentage(Money(data['amount'], convert_to_pence=False),
                                                                   data['interest_yield'])
        data['return'] = Money.extract_leading_pence(return_amount)
        data['return_trailing_pence'] = Money.extract_trailing_pence(return_amount)

        amount = data['amount']
        data['amount'] = Money.extract_leading_pence(amount)
        data['amount_trailing_pence'] = Money.extract_trailing_pence(amount)

    return render_template('investment/investment_detail.html', investments_data=investments_data)
