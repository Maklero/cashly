from datetime import date
from app import create_app, models
from app.database import Database
from app.dependencies import get_database
from fastapi.testclient import TestClient

app = create_app()
client = TestClient(app)
db = Database("sqlite:///test-database.sqlite")
db.create_database()


app.dependency_overrides[get_database] = lambda: db


def test_create_expense_category():
    with db.session_factory() as session:
        session.query(models.ExpenseCategory).delete()
        session.commit()

    response = client.post(
        "/expense-categories/",
        json={
            "name": "Food", "color": "#f00"}
    )
    assert response.status_code == 201

    response_data = response.json()

    assert "id" in response_data
    assert response_data["name"] == "Food"
    assert response_data["color"] == "#f00"


def test_create_expense_category_when_name_is_already_used():
    expense_category = models.ExpenseCategory("Food", "#f00")

    with db.session_factory() as session:
        session.query(models.ExpenseCategory).delete()

        session.add(expense_category)
        session.commit()
        session.refresh(expense_category)

    response = client.post(
        "/expense-categories/",
        json={"name": "Food", "color": "#fff"}
    )

    assert response.status_code == 419

    response_data = response.json()

    assert response_data["message"] == (
        ("You have tried create expense "
         "category name but name is already used")
    )


def test_get_expense_category():
    expense_category = models.ExpenseCategory("Food", "#f00")

    with db.session_factory() as session:
        session.query(models.ExpenseCategory).delete()

        session.add(expense_category)
        session.commit()
        session.refresh(expense_category)

    expense_category_id = expense_category.id

    response = client.get(f"/expense-categories/{expense_category_id}/")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["name"] == "Food"
    assert response_data["color"] == "#f00"
    assert response_data["id"] == expense_category_id


def test_get_expense_category_not_found():
    with db.session_factory() as session:
        session.query(models.ExpenseCategory).delete()
        session.commit()

    response = client.get(f"/expense-categories/0/")

    assert response.status_code == 419

    response_data = response.json()

    assert response_data["message"] == (
        "You have tried get expense "
        "category but is not found"
    )


def test_get_all_expense_categories():
    expense_category = models.ExpenseCategory("Food", "#f00")

    with db.session_factory() as session:
        session.query(models.ExpenseCategory).delete()

        session.add(expense_category)
        session.commit()
        session.refresh(expense_category)

    response = client.get("/expense-categories/")

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 1

    assert response_data[0]["name"] == "Food"
    assert response_data[0]["color"] == "#f00"
    assert response_data[0]["id"] == expense_category.id


def test_delete_expense_category():
    expense_category = models.ExpenseCategory("Food", "#f00")

    with db.session_factory() as session:
        session.query(models.ExpenseCategory).delete()

        session.add(expense_category)
        session.commit()
        session.refresh(expense_category)

    expense_category_id = expense_category.id

    response = client.delete(f"/expense-categories/{expense_category_id}/")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["name"] == "Food"
    assert response_data["color"] == "#f00"
    assert response_data["id"] == expense_category_id


def test_update_expense_category():
    expense_category = models.ExpenseCategory("Food", "#f00")

    with db.session_factory() as session:
        session.query(models.ExpenseCategory).delete()

        session.add(expense_category)
        session.commit()
        session.refresh(expense_category)

    expense_category_id = expense_category.id

    response = client.put(
        f"/expense-categories/{expense_category_id}/",
        json={"name": "Test", "color": "#f00"}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["name"] == "Test"
    assert response_data["color"] == "#f00"
    assert response_data["id"] == expense_category_id


def test_update_expense_category_not_found():
    with db.session_factory() as session:
        session.query(models.ExpenseCategory).delete()
        session.commit()

    response = client.put(
        "/expense-categories/0/",
        json={"name": "", "color": ""}
    )

    assert response.status_code == 419

    response_data = response.json()

    assert response_data["message"] == (
        "Próbujesz edytować kategorię wydatku, "
        "która nie istnieje"
    )


def test_create_expense():
    response = client.post(
        "/expenses/", 
        json={
            "amount": 1000, 
            "realised_date": "2021-11-19"
        }
    )

    assert response.status_code == 201

    response_data = response.json()

    assert "id" in response_data
    assert response_data["amount"] == 1000
    assert response_data["expense_category"] == None
    assert response_data["realised_date"] == "2021-11-19"


def test_create_expense_with_category():
    expense_category = models.ExpenseCategory("Food", "#f00")

    with db.session_factory() as session:
        session.query(models.ExpenseCategory).delete()

        session.add(expense_category)
        session.commit()
        session.refresh(expense_category)

    expense_category_id = expense_category.id

    response = client.post(
        "/expenses/",
        json={
            "amount": 1000,
            "realised_date": "2021-11-19", 
            "expense_category_id": expense_category_id}
    )

    assert response.status_code == 201

    response_data = response.json()

    assert "id" in response_data
    assert response_data["amount"] == 1000
    assert response_data["realised_date"] == "2021-11-19"
    assert response_data["expense_category"]["name"] == "Food"
    assert response_data["expense_category"]["color"] == "#f00"
    assert response_data["expense_category"]["id"] == expense_category_id


def test_create_expense_with_category_when_category_not_found():
    response = client.post(
        "/expenses/",
        json={
            "amount": 1000, 
            "expense_category_id": "123",
            "realised_date": "2021-11-19"
        }
    )

    assert response.status_code == 419

    response_data = response.json()

    assert response_data["message"] == (
        ("You have tried create expense but "
         "expense category id is not found")
    )


def test_get_expense():
    expense = models.Expense(
        amount=1000,
        expense_category=None,
        realised_date=date.fromisoformat("2021-11-19")
    )

    with db.session_factory() as session:
        session.query(models.Expense).delete()

        session.add(expense)
        session.commit()
        session.refresh(expense)

    expense_id = expense.id

    response = client.get(f"/expenses/{expense_id}/")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == expense_id
    assert response_data["amount"] == 1000
    assert response_data["expense_category"] == None
    assert response_data["realised_date"] == "2021-11-19"


def test_get_expense_not_found():
    response = client.get(f"/expenses/123/")

    assert response.status_code == 419

    response_data = response.json()

    assert response_data["message"] == "You have tried get expense but is not found"


def test_get_expenses():
    expense = models.Expense(
        amount=1000,
        expense_category=None,
        realised_date=date.fromisoformat("2021-11-19")
    )

    with db.session_factory() as session:
        session.query(models.Expense).delete()

        session.add(expense)
        session.commit()
        session.refresh(expense)

    response = client.get("/expenses/")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data[0]["id"] == expense.id
    assert response_data[0]["amount"] == 1000
    assert response_data[0]["expense_category"] == None
    assert response_data[0]["realised_date"] == "2021-11-19"


def test_delete_expense():
    expense = models.Expense(
        amount=1000,
        expense_category=None,
        realised_date=date.fromisoformat("2021-11-19")
    )

    with db.session_factory() as session:
        session.query(models.Expense).delete()

        session.add(expense)
        session.commit()
        session.refresh(expense)

    expense_id = expense.id

    response = client.delete(f"/expenses/{expense_id}/")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == expense_id
    assert response_data["amount"] == 1000
    assert response_data["expense_category"] == None
    assert response_data["realised_date"] == "2021-11-19"


def test_delete_expense_not_found():
    response = client.delete("/expenses/123/")

    assert response.status_code == 419

    response_data = response.json()

    assert response_data["message"] == "You have tried delete expense but is not found"


def test_update_expense():
    expense = models.Expense(
        amount=1000,
        expense_category=None,
        realised_date=date.fromisoformat("2021-11-19")
    )

    with db.session_factory() as session:
        session.query(models.Expense).delete()

        session.add(expense)
        session.commit()
        session.refresh(expense)

    expense_id = expense.id

    response = client.put(
        f"/expenses/{expense_id}/",
        json={
            "amount": 500, 
            "expense_category_id": None,
            "realised_date": "2021-11-20"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["amount"] == 500
    assert response_data["id"] == expense_id
    assert response_data["expense_category"] == None
    assert response_data["realised_date"] == "2021-11-20"


def test_update_expense_not_found():
    with db.session_factory() as session:
        session.query(models.Expense).delete()
        session.commit()

    response = client.put(
        "/expenses/0/",
        json={
            "amount": 500, 
            "expense_category_id": "",
            "realised_date": "2021-11-19"
        }
    )

    assert response.status_code == 419

    response_data = response.json()

    assert response_data["message"] == "Próbujesz edytować wydatek, który nie istnieje"


def test_update_expense_when_expense_category_not_found():
    expense = models.Expense(
        amount=1000,
        expense_category=None,
        realised_date=date.fromisoformat("2021-11-19")
    )

    with db.session_factory() as session:
        session.query(models.Expense).delete()

        session.add(expense)
        session.commit()
        session.refresh(expense)

    expense_id = expense.id

    response = client.put(
        f"/expenses/{expense_id}/",
        json={
            "amount": 500, 
            "expense_category_id": "0",
            "realised_date": "2021-11-19"
        }
    )

    assert response.status_code == 419

    response_data = response.json()

    assert response_data["message"] == "Kategoria wydatku nie istnieje"
