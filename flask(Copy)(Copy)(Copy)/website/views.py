from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from .xml_utils import read_xml, add_transaction_to_xml, save_xml, read_users_from_xml, read_transactions_from_xml, generate_transaction_hash
from datetime import date, timedelta, datetime
from xml.etree import ElementTree as ET
import hashlib
from . import views

views = Blueprint('views', __name__)

# Route for the root URL
@views.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('auth.login'))

# Existing routes for other functionalities (add_expense, add_income, transactions, delete_expense, delete_income)
# ...

@views.route('/home', methods=['GET'])
@login_required
def home():
    today = date.today()
    xml_data = read_transactions_from_xml()
    if xml_data is None:  
        flash('Error reading transaction data.', category='error')
        return redirect(url_for('views.transactions'))

    user_transactions = [transaction for transaction in xml_data if transaction['user_id'] == current_user.id]

    # Calculate daily transactions
    expenses_today = [transaction for transaction in user_transactions if transaction['type'] == "expense" and transaction['date'] == str(today)]
    income_today = [transaction for transaction in user_transactions if transaction['type'] == "income" and transaction['date'] == str(today)]
    total_expenses_today = sum(float(expense['amount']) for expense in expenses_today)
    total_income_today = sum(float(income['amount']) for income in income_today)
    daily_transactions = total_income_today - total_expenses_today

    # Calculate monthly transactions
    first_day_of_month = date(today.year, today.month, 1)
    last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)
    expenses_month = [transaction for transaction in user_transactions if transaction['type'] == "expense" and first_day_of_month <= datetime.strptime(transaction['date'], '%Y-%m-%d').date() <= last_day_of_month]
    income_month = [transaction for transaction in user_transactions if transaction['type'] == "income" and first_day_of_month <= datetime.strptime(transaction['date'], '%Y-%m-%d').date() <= last_day_of_month]
    total_expenses_month = sum(float(expense['amount']) for expense in expenses_month)
    total_income_month = sum(float(income['amount']) for income in income_month)

    # Calculate monthly savings
    monthly_savings = total_income_month - total_expenses_month

    # Determine savings status
    if total_expenses_month > total_income_month:
        savings_status = "You spent more than you earned this month."
    elif total_expenses_month < total_income_month:
        savings_status = "Congratulations! You saved more than you spent this month."
    else:
        savings_status = "You spent exactly as much as you earned this month."

    # Calculate percentage of expenses and income
    total_transactions = total_expenses_month + total_income_month
    percentage_expenses = (total_expenses_month / total_transactions) * 100 if total_transactions != 0 else 0
    percentage_income = (total_income_month / total_transactions) * 100 if total_transactions != 0 else 0

    return render_template("home.html", user=current_user, daily_transactions=daily_transactions, monthly_savings=monthly_savings, savings_status=savings_status, percentage_expenses=percentage_expenses, percentage_income=percentage_income)
# Existing routes for other functionalities (add_expense, add_income, transactions, delete_expense, delete_income)
# ...

# Existing imports and code...

# Existing imports and code...



@views.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        amount = request.form.get('expenseAmount')
        description = request.form.get('expenseDescription')
        category = request.form.get('expenseCategory')

        # Add the current date to the transaction
        current_date = datetime.now().date()

        new_expense = {
            'user_id': current_user.id,
            'type': 'expense',
            'amount': amount,
            'description': description,
            'category': category,
            'date': str(current_date)  # Add the current date to the transaction
        }

        xml_data = read_xml('transactions.xml')
        if xml_data is None:
            flash('Error reading transaction data.', category='error')
            return redirect(url_for('views.transactions'))

        # Generate a unique hash for the new expense
        expense_hash = generate_transaction_hash(description, amount, str(current_date))

        # Add the new expense to the XML data with the generated hash
        add_transaction_to_xml(xml_data, new_expense, transaction_hash=expense_hash)
        save_xml('transactions.xml', xml_data)

        flash('Expense added successfully!', category='success')

        return redirect(url_for('views.home'))

    return render_template('add_expense.html', user=current_user)

@views.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    if request.method == 'POST':
        amount = request.form.get('incomeAmount')
        description = request.form.get('incomeDescription')
        category = request.form.get('incomeCategory')

        # Add the current date to the transaction
        current_date = datetime.now().date()

        new_income = {
            'user_id': current_user.id,
            'type': 'income',
            'amount': amount,
            'description': description,
            'category': category,
            'date': str(current_date)  # Add the current date to the transaction
        }

        xml_data = read_xml('transactions.xml')
        if xml_data is None:
            flash('Error reading transaction data.', category='error')
            return redirect(url_for('views.transactions'))

        # Generate a unique hash for the new income
        income_hash = generate_transaction_hash(description, amount, str(current_date))

        # Add the new income to the XML data with the generated hash
        add_transaction_to_xml(xml_data, new_income, transaction_hash=income_hash)
        save_xml('transactions.xml', xml_data)

        flash('Income added successfully!', category='success')

        return redirect(url_for('views.home'))

    return render_template('add_income.html', user=current_user)# Existing routes and code...

# Existing imports and code...



# Function to generate a unique hash for a transaction

# Your Flask routes
# Your Flask routes
@views.route('/transactions')
@login_required
def transactions():
    xml_data = read_xml('transactions.xml')
    if xml_data is None:
        flash('Error reading transaction data.', category='error')
        return redirect(url_for('views.home'))
    
    # Filter transactions based on user_id
    current_user_id = current_user.id
    transactions = xml_data.findall(f"./transaction[user_id='{current_user_id}']")
    expenses = [t for t in transactions if t.find("type").text == "expense"]
    income = [t for t in transactions if t.find("type").text == "income"]
    
    return render_template("transactions.html", expenses=expenses, income=income, user=current_user)
# views.py
@views.route('/delete_expense/<string:expense_hash>', methods=['POST'])
@login_required
def delete_expense(expense_hash):
    xml_data = read_xml('transactions.xml')
    if xml_data is None:
        flash('Error reading transaction data.', category='error')
        return redirect(url_for('views.home'))

    expense_element = xml_data.find(f"transaction[@hash='{expense_hash}']")
    if expense_element is None or expense_element.find("type").text != "expense":
        abort(404)  # Not found
    xml_data.remove(expense_element)
    save_xml('transactions.xml', xml_data)
    return redirect(url_for('views.transactions'))

@views.route('/delete_income/<string:income_hash>', methods=['POST'])
@login_required
def delete_income(income_hash):
    xml_data = read_xml('transactions.xml')
    if xml_data is None:
        flash('Error reading transaction data.', category='error')
        return redirect(url_for('views.home'))

    income_element = xml_data.find(f"transaction[@hash='{income_hash}']")
    if income_element is None or income_element.find("type").text != "income":
        abort(404)  # Not found
    xml_data.remove(income_element)
    save_xml('transactions.xml', xml_data)
    return redirect(url_for('views.transactions'))