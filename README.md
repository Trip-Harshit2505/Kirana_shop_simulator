# 📦 Jumbotail Shipping Optimization API
A scalable, extensible shipping optimization system built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, designed from the perspective of a Kirana store owner ordering products from an e-commerce platform.

This system not only calculates shipping charges but models real-world logistics constraints such as:
* Nearest warehouse selection

* Perishable goods handling

* Fragile item handling fees

* Warehouse operational filtering

* Caching for performance

* Unit testing with coverage

# 🎯 Problem Perspective
Instead of limiting implementation to the attributes mentioned in the assignment, this system was extended by thinking like a **Kirana store owner**:

* Perishable items must arrive quickly

* Fragile items need special handling

* Warehouses may be inactive

* Shipping costs should be optimized

* Repeated queries should be fast

This approach ensures the system reflects real-world e-commerce logistics behavior.

# 🏗 Architecture Overview

```
app/
 ├── api/               → FastAPI route definitions
 ├── core/              → Caching layer
 ├── db/                → Database configuration
 ├── models/            → SQLAlchemy models
 ├── schemas/           → Pydantic schemas
 ├── services/          → Business logic layer
 ├── strategies/        → Transport Strategy Pattern
 ├── utils/             → Utility functions (distance calc)
```

# 🧠 Design Decisions & Patterns

### **1️⃣ Strategy Pattern**
Used for transport cost calculation based on distance slabs.

This makes it easy to:

* Add new transport types

* Modify pricing logic

* Extend cost strategies without touching core code

### **2️⃣ Service Layer Pattern**
All business logic is separated from API routes.

This improves:

* Testability

* Maintainability

* Clean architecture adherence

### **3️⃣ Caching Abstraction Layer**
A simple in-memory TTL-based cache is implemented.

It caches:

* Nearest warehouse per seller

* Shipping cost per request combination

This reduces:

* Redundant DB queries

* Repeated distance calculations

* Strategy recalculations

The abstraction allows easy migration to Redis for distributed scaling.

# 🛒 Domain Modeling Enhancements
To reflect realistic e-commerce behavior, the following were added:

## **Product Enhancements**
* `is_fragile` → Adds handling charge

* `is_perishable` → Forces express delivery

* `min_order_quantity` → Supports bulk kirana buying

* (Optional dimensional attributes with defaults)

## **Warehouse Enhancements**
* `operational_status` → Filters inactive warehouses

## **Shipping Enhancements**
* Express delivery premium

* Fragile handling surcharge

* Perishable delivery restriction

These additions demonstrate business-aware modeling.

# **⚙️ Setup Instructions**
### **1️⃣ Clone Repository**
```
git clone <repo-url>
cd jumbotail-shipping
```
### **2️⃣ Create Virtual Environment**
```
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```
### **3️⃣ Install Dependencies**
```
pip install -r requirements.txt
```
### **4️⃣ Configure Database**

Create `.env`file:

```
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/jumbotail
```
### **5️⃣ Run Migrations**
```
alembic upgrade head
```
### **6️⃣ Run Application**
```
uvicorn app.main:app --reload
```

Access:

```
http://127.0.0.1:8000
```

Swagger Docs:

```
http://127.0.0.1:8000/docs
```

# **📌 API Endpoints**
### **Health Check**
```GET /```
### **Get Nearest Warehouse**
```
GET /warehouse/nearest/{seller_id}
```
### **Calculate Shipping**
```
POST /shipping/calculate
```

Request Body:
```json
{
  "warehouse_id": 1,
  "customer_id": 1,
  "delivery_speed": "standard",
  "weight": 5
}
```
### **Combined Seller Shipping**
```
POST /shipping/for-seller
```

Automatically:

* Finds nearest operational warehouse

* Applies perishable/fragile rules

* Calculates final shipping charge

# **🧪 Testing**
Run tests:
```python
pytest
```

# **📊 Code Coverage**
Generate coverage report:

```python
pytest --cov=app --cov-report=term --cov-report=html
```

Open detailed report:

```
htmlcov/index.html
```

**Coverage > 90%**

# **🛡 Edge Cases Covered**
* Seller not found

* Warehouse not found

* Customer not found

* No product found for seller

* Perishable restriction

* Fragile surcharge

* Cache TTL expiration

* Repeated request cache hit

# **🚀 Scalability Considerations**

The system is built to scale:

* **Cache abstraction** → Replace with Redis

* **Strategy pattern** → Add transport types easily

* **Service layer** → Extract to microservices

* **Clean separation** → Supports async migration

# **🔮 Future Improvements**

* Redis-based distributed caching

* Docker containerization

* Load testing

* Rate limiting

* Order entity with multi-item support

* Inventory stock validation

# **👨‍💻 Author**

**Harshit Tripathi**

Backend Developer | Python | FastAPI | PostgreSQL