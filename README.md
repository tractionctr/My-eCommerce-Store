# My eCommerce Store

A Django-based eCommerce web application featuring a vendor/buyer system, product management, shopping cart, reviews, email invoices, and a REST API.

---

## 🚀 Features

- User authentication with Buyer and Vendor roles
- Vendors can create stores and manage products
- Buyers can browse products and leave reviews
- Shopping cart and checkout system
- Email invoice sent on checkout
- REST API for products, stores, and reviews
- MariaDB database integration

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/tractionctr/My-eCommerce-Store
cd ecommerce
<<<<<<< HEAD
=======
```bash
git clone https://github.com/tractionctr/My-eCommerce-Store.git
cd My-eCommerce-Store
=======
>>>>>>> 823a32a (UI polish + flake8 fixes + Reddit feed update)
```

---

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=ecommerce
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=3306
```

---

### 5. Create database

Make sure MariaDB is running, then create the database:

```sql
CREATE DATABASE ecommerce;
```

---

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 7. Create superuser (optional)

```bash
python manage.py createsuperuser
```

---

### 8. Run development server

```bash
python manage.py runserver
```

Open:

```bash
http://127.0.0.1:8000/
```

---

## 🗄️ Database

This project uses **MariaDB** as the database backend.

---

## 🌐 Web Routes

- `/` → View products
- `/cart/` → Shopping cart
- `/checkout/` → Checkout
- `/register/` → Register account
- `/login/` → Login
- `/logout/` → Logout
- `/vendor/` → Vendor dashboard
- `/buyer/` → Buyer dashboard
- `/admin/` → Django admin panel

---

## 🔌 API Endpoints

Base URL:

```bash
/api/
```

### Products

- `GET /api/products/` → List all products
- `POST /api/products/` → Create product (vendor only)
- `GET /api/stores/<store_id>/products/` → Products by store

### Stores

- `GET /api/stores/` → List all stores
- `GET /api/vendors/<vendor_id>/stores/` → Stores by vendor

### Reviews

- `GET /api/reviews/` → List all reviews
- `GET /api/reviews/?product=<id>` → Reviews by product
- `GET /api/vendor/reviews/` → Vendor product reviews

---

## 🔐 Permissions

- Only vendors can create stores and products
- Vendors can manage their own stores/products
- Vendors can view reviews on their own products
- Buyers can browse stores, products, and leave reviews

---

## 📧 Email System

- Checkout generates and sends invoice emails
- Development uses Django console email backend

---

## 🧠 Technologies Used

- Python
- Django
- Django REST Framework
- MariaDB
- HTML/CSS

---

## 📌 Notes

- Ensure MariaDB is running before starting the server
- Create and configure your `.env` file before migrations
- Admin panel available at `/admin/`
