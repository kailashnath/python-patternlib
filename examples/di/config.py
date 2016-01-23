from patterns.di import DIConfig
from .sqlprovider import SqlProvider
from .transaction import TransactionHandler
from .runner import TransactionRunner


diconfig = DIConfig().bind('dbConnection', SqlProvider)\
            .bind('txHandler', TransactionHandler)\
            .bind('txRunner', TransactionRunner)
