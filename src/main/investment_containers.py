from dependency_injector import containers, providers
from src.adapters.db.investment_repository import InvestmentRepository
from src.domain.ports.investment_service import InvestmentService


class InvestmentContainer(containers.DeclarativeContainer):

    db_conn = providers.Dependency()

    investment_repository = providers.Singleton(
        InvestmentRepository,
        db_conn=db_conn
    )

    investment_service = providers.Factory(
        InvestmentService,
        investment_repo=investment_repository
    )