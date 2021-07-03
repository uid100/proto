#!/usr/bin/env python3

transactions = []

class Transaction:
    def __init__(self,type,timestamp,acct,amount):
        __acct = acct
        __type = type
        __timestamp = timestamp
        __amount = amount

    def get_userID():
        return __acct    
    def get_type():
        return __type
    def get_timestamp():
        return __timestamp
    def get_amount():
        return __amount

def add_transaction(type,timestamp,acct,amount):
    transactions.append(Transaction(type,timestamp,acct,amount))
    return len(transactions)

def get_balance(acct):
    pass
