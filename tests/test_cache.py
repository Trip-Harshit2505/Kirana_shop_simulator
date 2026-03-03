from app.core.cache import SimpleCache
import time
from app.models.customer import Customer
from app.models.warehouse import Warehouse
from app.services.shipping_service import calculate_shipping
from app.core.cache import cache

# Test cases for caching functionality in warehouse_service and shipping_service

def test_cache_set_and_get():
    cache = SimpleCache()

    cache.set("key1", "value1", ttl=10)
    value = cache.get("key1")

    assert value == "value1"

def test_cache_expiry():
    cache = SimpleCache()

    cache.set("key2", "value2", ttl=1)
    time.sleep(2)

    value = cache.get("key2")

    assert value is None

def test_shipping_cache_usage(db):
    cache.store.clear()

    warehouse = Warehouse(id=1, name="W1", latitude=10, longitude=10)
    customer = Customer(id=1, name="C1", phone="123", latitude=11, longitude=11)

    db.add(warehouse)
    db.add(customer)
    db.commit()

    charge1 = calculate_shipping(
        db=db,
        warehouse_id=1,
        customer_id=1,
        delivery_speed="standard",
        weight=5,
    )

    charge2 = calculate_shipping(
        db=db,
        warehouse_id=1,
        customer_id=1,
        delivery_speed="standard",
        weight=5,
    )

    assert charge1 == charge2