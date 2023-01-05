import logging

from flask import Blueprint, render_template, request, flash, g, redirect, url_for, session
from dependency_injector.wiring import inject, Provide

from src.adapters.app.blueprints.auth import login_required
from src.domain.ports import create_commodity_factory, update_commodity_factory
from src.domain.ports.commodity_service import CommodityService, CommodityDBOperationError
from src.main.containers import Container

blueprint = Blueprint('home', __name__, url_prefix='/')


@blueprint.route('/', methods=['GET'])
@inject
def index(commodity_service: CommodityService = Provide[Container.commodity_package.commodity_service]):
    current_user_avatar = session.get('email')[0].capitalize() if session.get('email') else None
    commodity = commodity_service.get_all_commodities()
    return render_template('index.html', current_user=current_user_avatar, commodity=commodity[0])
