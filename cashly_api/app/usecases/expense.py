from uuid import UUID
from datetime import date
from dataclasses import dataclass
from typing import List, NoReturn, Optional

from app.usecases import UseCase
from app.entities import User, Expense
from app.exceptions import ExpenseCategoryNotFoundError, ExpenseNotFoundError
from app.repositories import ExpenseRepository, ExpenseCategoryRepository


@dataclass(frozen=True)
class GetAllExpensesUseCaseInput:
  user: User


@dataclass(frozen=True)
class GetAllExpensesUseCaseOutput:
  expenses: List[Expense]


class GetAllExpensesUseCase(UseCase[GetAllExpensesUseCaseInput, GetAllExpensesUseCaseOutput]):
  def __init__(self, expense_repo: ExpenseRepository) -> None:
    self._expense_repo = expense_repo

  def execute(self, input: GetAllExpensesUseCaseInput) -> GetAllExpensesUseCaseOutput:
    return GetAllExpensesUseCaseOutput(self._expense_repo.get_all_by_user_id(input.user.id))


@dataclass(frozen=True)
class CreateExpenseUseCaseInput:
  user: User
  amount: float
  realised_date: date
  expense_category_id: Optional[UUID] = None


@dataclass(frozen=True)
class CreateExpenseUseCaseOutput:
  expense: Expense


class CreateExpenseUseCase(UseCase[CreateExpenseUseCaseInput, CreateExpenseUseCaseOutput]):
  def __init__(self, expense_repo: ExpenseRepository, expense_category_repo: ExpenseCategoryRepository) -> None:
    self._expense_repo = expense_repo
    self._expense_category_repo = expense_category_repo
    
  def execute(self, input: CreateExpenseUseCaseInput) -> CreateExpenseUseCaseOutput:
    existing_expense_category = None
    if input.expense_category_id:
      existing_expense_category = self._expense_category_repo.get_by_id_and_user_id(
        input.expense_category_id, 
        input.user.id
      )

      if not existing_expense_category:
        raise ExpenseCategoryNotFoundError()

    new_expense = Expense(
      user=input.user,
      amount=input.amount,
      realised_date=input.realised_date,
      category=existing_expense_category
    )
    self._expense_repo.add(new_expense)
    
    return CreateExpenseUseCaseOutput(new_expense)


@dataclass(frozen=True)
class UpdateExpenseUseCaseInput:
  expense_id: UUID
  user: User
  amount: float
  realised_date: date
  expense_category_id: Optional[UUID] = None


@dataclass(frozen=True)
class UpdateExpenseUseCaseOutput:
  expense: Expense


class UpdateExpenseUseCase(UseCase[UpdateExpenseUseCaseInput, UpdateExpenseUseCaseOutput]):
  def __init__(self, expense_repo: ExpenseRepository, expense_category_repo: ExpenseCategoryRepository) -> None:
    self._expense_repo = expense_repo
    self._expense_category_repo = expense_category_repo

  def execute(self, input: UpdateExpenseUseCaseInput) -> UpdateExpenseUseCaseOutput:
    existing_expense = self._expense_repo.get_by_id_and_user_id(input.expense_id, input.user.id)
    if not existing_expense:
      raise ExpenseNotFoundError()


    exisitng_expense_category = None
    if input.expense_category_id:
      exisitng_expense_category = self._expense_category_repo.get_by_id_and_user_id(input.expense_category_id, input.user.id)
      if not exisitng_expense_category:
        raise ExpenseCategoryNotFoundError()

    existing_expense.amount = input.amount
    existing_expense.realised_date = input.realised_date
    existing_expense.category = exisitng_expense_category

    self._expense_repo.save(existing_expense)


    return UpdateExpenseUseCaseOutput(existing_expense)


@dataclass(frozen=True)
class DeleteExpenseUseCaseInput:
  expense_id: UUID
  user: User


class DeleteExpenseUseCase(UseCase[DeleteExpenseUseCaseInput, NoReturn]):
  def __init__(self, expense_repo: ExpenseRepository) -> None:
    self._expense_repo = expense_repo

  def execute(self, input: DeleteExpenseUseCaseInput) -> NoReturn:
    existing_expense = self._expense_repo.get_by_id_and_user_id(input.expense_id, input.user.id)
    if not existing_expense:
      raise ExpenseNotFoundError()

    self._expense_repo.delete(existing_expense)
