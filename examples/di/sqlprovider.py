class SqlProvider(object):
    def __init__(self, txRunner):
        self.txRunner = txRunner

    def __enter__(self):
        self.txRunner.begin()
        return self.txRunner

    def __exit__(self, *args):
        self.txRunner.commit()

