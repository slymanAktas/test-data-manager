from db_operations.connection.oracle.connect_to_oracle import oracle


def get_seller():
    return oracle("qa").fetch_one("select * from SELLER where id = 1157832")["NICKNAME"]