import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def fifty_bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    sum = add(num1, num2)
    assert sum == expected # assert Tru e means nothing is gonna happen, assert False means that an AssertionError will be raised and execution of code will stop, assert should never be used in production, use it only for testing in development.

@pytest.mark.parametrize("x, y, result", [
    (7, 2, 5),
    (9, 6, 3),
    (5, 4, 1)
])
def test_subtract(x, y, result):
    assert subtract(x, y) == result

def test_multiply():
    assert multiply(2, 5) == 10

def test_divide():
    assert divide(6, 2) == 3

def test_bank_account_initial_amount(fifty_bank_account):
    assert fifty_bank_account.balance == 50

def test_bank_account_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw_from_bank_account(fifty_bank_account):
    fifty_bank_account.withdraw(20)
    assert fifty_bank_account.balance == 30

def test_deposit_into_bank_account(fifty_bank_account):
    fifty_bank_account.deposit(10)
    assert fifty_bank_account.balance == 60

def test_collect_interest_from_bank_account(fifty_bank_account):
    fifty_bank_account.collect_interest()
    assert round(fifty_bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (250, 100, 150),
    (500, 200, 300),
    (50, 10, 40),
    (1200, 200, 1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_withdrawing_more_than_balance(fifty_bank_account):
    with pytest.raises(InsufficientFunds):
        fifty_bank_account.withdraw(200)
