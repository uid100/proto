#!/usr/bin/env python3

import time
import MPS7
transactions = []

class Transaction:
    def __init__(self,type,timestamp,acct,amount):
        self.__acct = acct
        self.__type = type
        self.__timestamp = timestamp
        self.__amount = amount

    def get_userID(self):
        return self.__acct    
    def get_type(self):
        return self.__type
    def get_timestamp(self):
        return self.__timestamp
    def get_amount(self):
        return self.__amount

def add_transaction(type,timestamp,acct,amount=0):
    transactions.append(Transaction(type,timestamp,acct,amount))
    return len(transactions)

def count_transactions(type):
    count = sum(1 for t in transactions if t.get_type() == type)
    return count

def sum_transactions(type):
    total = sum(t.get_amount() for t in transactions if t.get_type() == type)
    return total

def get_balance(userID):
    balance = sum(t.get_amount() for t in transactions if t.get_type() == MPS7.credit and t.get_userID() == userID)
    balance -= sum(t.get_amount() for t in transactions if t.get_type() == MPS7.debit and t.get_userID() == userID)
    return balance

if __name__ == '__main__':
    add_transaction(0,time.time(),123,199)
    add_transaction(1,time.time(),123,99)
    add_transaction(2,time.time(),123)
    add_transaction(3,time.time(),123)
    print(get_balance(123))
