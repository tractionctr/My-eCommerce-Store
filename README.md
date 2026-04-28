# My eCommerce Store

A Django-based eCommerce web application featuring a vendor/buyer system, product management, shopping cart, reviews, and a REST API.

---

## 🚀 Features

* User authentication (Buyer & Vendor roles)
* Vendors can create stores and manage products
* Buyers can browse products and leave reviews
* Cart system with checkout
* Email invoice on checkout
* REST API for products, stores, and reviews

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-link>
cd ecommerce
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Configure environment variables (.env)

Create a `.env` file in the root directory:

```
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=ecommerce
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=3306
```

---

### 4. Run migrations

```
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Run the server

```
python manage.py runserver
```

---

## 🗄️ Database

This project uses **MariaDB** as the database backend.

---

## 🌐 Web Routes

* `/` → View products
* `/cart/` → View cart
* `/checkout/` → Checkout
* `/register/` → Register account
* `/login/` → Login
* `/vendor/` → Vendor dashboard
* `/buyer/` → Buyer dashboard

---

## 🔌 API Endpoints

Base URL:

```
/api/
```

### Products

* `GET /api/products/` → List all products
* `POST /api/products/` → Create product (vendor only)
* `GET /api/stores/<store_id>/products/` → Products in a specific store

---

### Stores

* `GET /api/stores/` → List all stores
* `GET /api/vendors/<vendor_id>/stores/` → Stores owned by a vendor

---

### Reviews

* `GET /api/reviews/` → List all reviews
* `GET /api/reviews/?product=<id>` → Reviews for a product
* `GET /api/vendor/reviews/` → Reviews for logged-in vendor’s products

---

## 🔐 Permissions

* Only vendors can create products and stores
* Vendors can view reviews on their own products
* Buyers can view stores and products


---

## 📧 Email System

* On checkout, an invoice is generated and sent to the user’s email

---

## 🧠 Technologies Used

* Django
* Django REST Framework
* MariaDB
* Python

---

## 📌 Notes

* Ensure MariaDB is running before starting the server
* Email backend may use console output during development
