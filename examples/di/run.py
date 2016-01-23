from examples.di.config import diconfig


if __name__ == '__main__':
    txHandler = diconfig.inject('txHandler')
    txHandler.commit('INSERT INTO examples (id, name) VALUES (3, \'di\')')

    class MockTxRunner(object):

        def __init__(self):
            self.exec_order = []

        def begin(self):
            self.exec_order.append('begin')

        def insert(self, statement):
            self.exec_order.append('insert')

        def commit(self):
            assert ['begin', 'insert'] == self.exec_order

    diconfig.bind('txRunner', MockTxRunner)

    txHandler = diconfig.inject('txHandler')
    txHandler.commit('INSERT INTO examples (id, name) VALUES (124, \'mock\')')

    print 'Test completed'

