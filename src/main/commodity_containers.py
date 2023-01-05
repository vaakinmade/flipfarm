from dependency_injector import containers, providers
from src.adapters.db.commodity_repository import CommodityRepository
from src.domain.ports.commodity_service import CommodityService


class CommodityContainer(containers.DeclarativeContainer):

    db_conn = providers.Dependency()

    commodity_repository = providers.Singleton(
        CommodityRepository,
        db_conn=db_conn
    )

    commodity_service = providers.Factory(
        CommodityService,
        commodity_repo=commodity_repository
    )
