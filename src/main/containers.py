from dependency_injector import containers, providers

from src.main.config import get_db
from src.main.user_containers import UserContainer
from src.main.investment_containers import InvestmentContainer
from src.main.commodity_containers import CommodityContainer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.adapters.app.blueprints"])
    # db_connection = get_db()

    user_package = providers.Container(
        UserContainer,
        db_conn=get_db
    )

    investment_package = providers.Container(
        InvestmentContainer,
        db_conn=get_db
    )

    commodity_package = providers.Container(
        CommodityContainer,
        db_conn=get_db
    )
