@staticmethod
def getAllquantity(order):
    conn = DBConnect.get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT SUM(oi.quantity) AS quantity,
               COUNT(*) AS numRows
        FROM order_items oi
        WHERE oi.order_id = %s
        GROUP BY oi.order_id
    """

    cursor.execute(query, (order.order_id,))
    row = cursor.fetchone()

    if row is None:
        order.quantity = 0
        order.numRows = 0
    else:
        order.quantity = int(row["quantity"])
        order.numRows = int(row["numRows"])

    cursor.close()
    conn.close()
E nel model.py, al posto di:
peso = (o1.quantity + o2.quantity) / diff
metti:
peso = (o1.quantity * o2.numRows + o2.quantity * o1.numRows) / diff