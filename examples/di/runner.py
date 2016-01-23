class TransactionRunner(object):

    def begin(self):
        print 'BEGING TRANSACTION'

    def insert(self, statement):
        print statement

    def commit(self):
        print 'END TRANSACTION'

