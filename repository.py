import abc
import model

from sqlalchemy import select


class AbstractRequestRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, request: model.Request):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id) -> model.Request:
        raise NotImplementedError


class SqlAlchemyRequestRepository(AbstractRequestRepository):
    def __init__(self, session):
        self.session = session

    def add(self, request):
        self.session.add(request)

    def get(self, id):
        return self.session.scalars(
            select(model.Request).filter_by(id=id)
        ).one()

    def list(self):
        return self.session.scalars(select(model.Request)).all()



class AbstractApprovalRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, approval: model.Approval):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id) -> model.Approval:
        raise NotImplementedError


class SqlAlchemyApprovalRepository(AbstractApprovalRepository):
    def __init__(self, session):
        self.session = session

    def add(self, approval):
        self.session.add(approval)

    def get(self, id):
        return self.session.scalars(
            select(model.Approval).filter_by(id=id)
        ).one()

    def list(self):
        return self.session.scalars(select(model.Approval)).all()