# AgriSense

AgriSense is a Django-based farm management web application designed for farmers to track crops, investments, sales, and overall profitability. It provides a simple dashboard to manage agricultural activities efficiently.

## Features

- Farmer registration and login
- User profile management
- Crop creation and tracking
- Expense/investment tracking per crop
- Sale tracking per crop
- Dashboard with summary metrics
- Profit calculation based on sales and expenses
- Responsive UI using Bootstrap

## Tech Stack

- Python
- Django
- SQLite
- Bootstrap 5

## Project Structure

```text
AgriSense/
├── AgriSense/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── farm/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── accounts/
│   └── farm/
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```

## Prerequisites

- Python 3.10+
- Django 5.x
- Virtual environment support

## Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd AgriSense
```

2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install django
```

4. Apply database migrations:

```bash
python3 manage.py migrate
```

5. Create a superuser (optional, for admin access):

```bash
python3 manage.py createsuperuser
```

6. Run the development server:

```bash
python3 manage.py runserver
```

7. Open the app in your browser:

```text
http://127.0.0.1:8000/
```

## Usage

1. Register a new farmer account.
2. Log in to the dashboard.
3. Add your crops.
4. Record crop-related investments/expenses.
5. Record crop sales.
6. View summary metrics and profit/loss updates from the dashboard.

## Business Logic

The application calculates farm profit using the following idea:

- Total investment = sum of all crop expenses
- Total sales revenue = sum of all crop sales revenue
- Net profit/loss = total sales revenue - total investment

Each sale revenue is calculated as:

```text
(quantity_sold * unit_price) - selling_cost
```

## Notes

This project is designed as a practical farm management demo and can be extended with features like:

- weather tracking
- harvest forecasting
- irrigation management
- inventory tracking
- PDF reports
- notifications

## License

This project is intended for educational and personal use.
