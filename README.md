SmartMed 

SmartMed is a simple Django-based e-commerce web application for medicines.
Users can browse medicines, search for products, view details, and add items to their cart.

Features

User Registration and Login
Secure Authentication
Browse Medicines by Category

Search Medicines by:
Medicine Name
Description
Category
Product Detail Page
Add to Cart Functionality

Medicine Categories:
Tablets
Syrups
Injections
First Aid
Supplements

Technologies Used:
Backend: Django (Python)
Frontend: HTML, CSS
Database: SQLite
Authentication: Django Authentication System
Media Handling: Django Media Files


Project Structure
smartmed/
│
├── app/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── urls.py
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── tablet.html
│   ├── syrup.html
│   ├── injection.html
│   ├── product_detail.html
│
├── static/
│   ├── css/
│   ├── images/
│
├── media/
│   ├── products/
│
├── manage.py



Search Feature
Users can search medicines based on:

Medicine name

Description

Category (Tablet, Syrup, Injection, First Aid, Supplement)

The search results are displayed on the home page and clicking a product opens the product detail page.


How to Run the Project

Clone the repository

git clone https://github.com/athulyagireesh/SMARTMED_ECOM_PROJECT.git

Navigate to project folder

cd smartmed

Install dependencies

pip install django

Run migrations

python manage.py migrate

Start the server

python manage.py runserver

Open in browser

http://127.0.0.1:8000/
