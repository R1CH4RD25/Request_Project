import pytest
import request.domain.model as model
import request.adapters.repository as repository
import request.service_layer.services as services


class FakeRepository(repository.AbstractAssignedRepository):
    def __init__(self, requests):
        self._requests = set(requests)

    def add(self, appr):
        self._requests.add(appr)

    def get(self, id):
        return next(b for b in self._requests if b.id == id)

    def list(self):
        return list(self._requests)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_returns_allocation():
    last_id = 5007
    req = model.Request(1005, "Richard Sullivan", "Golf", "Archer City", 102, "04/06/2023", "6:30 AM")
    appr = model.Approval(1007, "Approved", 1001, 1004, "Drive Safe")
    assign = model.Assigned(last_id, 1007, 101, 1004, "03/25/2023", "Drive Safe")
    repo = FakeRepository([assign])
    session = FakeSession()

    result = services.assign(req, appr, repo, FakeSession())
    #services.assign(req, repo, FakeSession())
    assert result == last_id + 1

'''
def test_error_for_invalid_sku():
    req = model.Request("o1", "NONEXISTENTSKU", 10)
    appr = model.Approval("b1", "AREALSKU", 100, eta=None)
    repo = FakeRepository([appr])

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.assign(req, repo, FakeSession())
'''

def test_commits():
    req = model.Request(1005, "Richard Sullivan", "Golf", "Archer City", 102, "04/06/2023", "6:30 AM")
    appr = model.Approval(1007, "Approved", 1001, 1004, "Drive Safe")
    assign = model.Assigned(5007, 1007, 101, 1004, "03/25/2023", "Drive Safe")
    repo = FakeRepository([assign])
    session = FakeSession()

    services.assign(req, appr, repo, session)
    assert session.committed is True
