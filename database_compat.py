"""
Wrapper de compatibilité pour database.py
Redirige vers models/transaction_model.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models.transaction_model import TransactionModel as Database

__all__ = ['Database']
