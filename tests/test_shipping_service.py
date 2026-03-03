from app.models.customer import Customer
from app.models.warehouse import Warehouse
from app.services.shipping_service import calculate_shipping
import pytest
from fastapi import HTTPException
from app.services.warehouse_service import get_nearest_warehouse
from app.services.shipping_service import calculate_shipping
from app.services.shipping_service import calculate_shipping_for_seller


def test_shipping_calculation(db):
    warehouse = Warehouse(id=1, name="W1", latitude=10, longitude=10)
    customer = Customer(id=1, name="C1", phone="123", latitude=11, longitude=11)

    db.add(warehouse)
    db.add(customer)
    db.commit()

    charge = calculate_shipping(
        db=db,
        warehouse_id=1,
        customer_id=1,
        delivery_speed="standard",
        weight=5,
    )

    assert charge > 0

def test_seller_not_found(db):
    with pytest.raises(HTTPException) as exc:
        get_nearest_warehouse(db, seller_id=999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Seller not found"

def test_warehouse_not_found(db):
    customer = Customer(id=1, name="C1", phone="123", latitude=10, longitude=10)
    db.add(customer)
    db.commit()

    with pytest.raises(HTTPException) as exc:
        calculate_shipping(
            db=db,
            warehouse_id=999,
            customer_id=1,
            delivery_speed="standard",
            weight=5,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Warehouse not found"

def test_customer_not_found(db):
    warehouse = Warehouse(id=1, name="W1", latitude=10, longitude=10)
    db.add(warehouse)
    db.commit()

    with pytest.raises(HTTPException) as exc:
        calculate_shipping(
            db=db,
            warehouse_id=1,
            customer_id=999,
            delivery_speed="standard",
            weight=5,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Customer not found"

def test_no_product_for_seller(db):
    from app.models.seller import Seller

    seller = Seller(id=1, name="S1", latitude=10, longitude=10)
    db.add(seller)
    db.commit()

    with pytest.raises(HTTPException) as exc:
        calculate_shipping_for_seller(
            db=db,
            seller_id=1,
            customer_id=1,
            delivery_speed="standard",
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "No product found for seller"

def test_shipping_for_seller_success(db):
    from app.models.seller import Seller
    from app.models.product import Product

    seller = Seller(id=1, name="S1", latitude=10, longitude=10)
    warehouse = Warehouse(id=1, name="W1", latitude=10, longitude=10)
    customer = Customer(id=1, name="C1", phone="123", latitude=11, longitude=11)

    product = Product(
        id=1,
        name="Rice",
        weight=5,
        price=200,
        seller_id=1,
        is_fragile=False,
        is_perishable=False
    )

    db.add_all([seller, warehouse, customer, product])
    db.commit()

    warehouse_result, charge = calculate_shipping_for_seller(
        db=db,
        seller_id=1,
        customer_id=1,
        delivery_speed="standard",
    )

    assert charge > 0
    assert warehouse_result.id == 1