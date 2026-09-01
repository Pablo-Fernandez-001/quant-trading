# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 22:34:51 2026

@author: pabda
"""

class bankAccount:
    """
    This class represents a bank account
    """
    def __init__(self, owner: str, initial_balance: float = 0.0) -> None :
        """
        To initialize a bank account

        Parameters
        ----------
        owner : str
            The initial owner of the bank account.
        initial_balance : float, optional
            The initial balance if the owner of the account deposit money or by default it's 0

        Returns
        -------
        None
            DESCRIPTION.

        """
        self.owner = owner
        self.__balance = initial_balance
        
    def __str__(self):
        return f"Bank account for {self.owner}"
    
    def deposit(self, quantity: float):
        """
        To deposit money into bank account

        Parameters
        ----------
        quantity : float
            Quantity of money to deposit

        Returns
        -------
        None.

        """
        self.__balance += quantity
        print(f"Have been added ${quantity} into the account, new balance ${self.__balance}")
        
    def withdraw(self, quantity: float):
        
        """
        to witdraw money of the account

        Parameters
        ----------
        quantity : float
            Quantity of money to witdraw

        Returns
        -------
        None.
        """
        
        if quantity <= self.__balance:
            self.__balance -= quantity
            print(f"We take ${quantity} of the account, your new balance it's ${self.__balance}")
        else:
            print("insufficient balance")
            
    
    def get_Balance(self):
        
        """
        to know the bank account data

        Parameters
        ----------
        Returns
        -------
        None.
        """
        
        print(f"Owner {self.owner}, Balance {self.__balance}")
        

account1 = bankAccount("Juan Pérez", 1000)
print(account1)

account2 = bankAccount("Maria Gonzáles", 1500)
print(account2)

# Operations
account1.deposit(500)
account1.withdraw(200)
account1.get_Balance()

account2.get_Balance()

# Try to know the private attribs
try:
    print(account1.__balance)
except:
    print("We can't know that attribute")
    
## Remember
# 1. The classes on pyton are templates to encapsulate data and to promote the 
#    code reuse and an organizated structure.
# 2. Self it's a reference to the current object inside the class, allowing the
#    attribute's acces and makin specific operations inside the classe's methods 


