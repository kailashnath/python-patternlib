from examples.singleton.db import DbConnection


if __name__ == '__main__':
    conn_1 = DbConnection()
    conn_2 = DbConnection()
    assert conn_1 == conn_2

