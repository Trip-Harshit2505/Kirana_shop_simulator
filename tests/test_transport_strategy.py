from app.services.transport_strategy import get_transport_strategy


def test_minivan_strategy():
    strategy = get_transport_strategy(50)
    charge = strategy.calculate(50, 2)
    assert charge == 50 * 2 * 3


def test_truck_strategy():
    strategy = get_transport_strategy(200)
    charge = strategy.calculate(200, 2)
    assert charge == 200 * 2 * 2


def test_aeroplane_strategy():
    strategy = get_transport_strategy(600)
    charge = strategy.calculate(600, 2)
    assert charge == 600 * 2 * 1