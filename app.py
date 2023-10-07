from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"ID: {self.id}, Name: {self.name}, Amount: ${self.amount}"

# ... [previous code for setting up Flask and SQLAlchemy]

@app.route('/expenses/')
def show_expenses():
    all_expenses = Expense.query.all()
    print(all_expenses)
    return str(all_expenses)  # Displaying the list of expenses as a string for simplicity

@app.route('/expenses/add', methods=['POST'])
def add_expense():
    name = request.form.get('name')
    amount = request.form.get('amount')
    
    # Validation
    if not name or not amount or not amount.replace('.', '', 1).isdigit():
        return "Invalid input. Please ensure you provide a name and a valid amount."

    amount = float(amount)
    new_expense = Expense(name=name, amount=amount)
    db.session.add(new_expense)
    db.session.commit()
    return f"Expense '{name}' added successfully!"

@app.route('/expenses/edit/<int:expense_id>', methods=['POST'])
def edit_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return f"No expense with ID {expense_id} found."

    name = request.form.get('name')
    amount = request.form.get('amount')
    
    # Validation
    if not name or not amount or not amount.replace('.', '', 1).isdigit():
        return "Invalid input. Please ensure you provide a name and a valid amount."

    expense.name = name
    expense.amount = float(amount)
    db.session.commit()
    return f"Expense with ID {expense_id} edited successfully!"

@app.route('/expenses/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return f"No expense with ID {expense_id} found."

    db.session.delete(expense)
    db.session.commit()
    return f"Expense with ID {expense_id} deleted successfully!"



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

