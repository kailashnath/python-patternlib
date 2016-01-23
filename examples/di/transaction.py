

class TransactionHandler(object):
    def __init__(self, dbConnection):
        self.connection = dbConnection

    def commit(self, insertOp):
        with self.connection as tx:
            tx.insert(insertOp)

