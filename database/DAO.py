from database.DB_connect import DBConnect
from model.categorie import Categoria
from model.products import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategorie():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from categories c """

        cursor.execute(query)

        for row in cursor:
            results.append(Categoria(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodi(category_id):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from products p 
                    where p.category_id = %s
                    order by p.product_name
                    """

        cursor.execute(query, (category_id, ))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllCoppie(anno1, anno2, id):
        #controllare in Python che i nodi rispettino la categoria
        #calcola peso arco in Python

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select a1.product_id as p1, a1.numVendite as n1, a2.product_id as p2, a2.numVendite as n2 
                    from
                        (select p.product_id, count(distinct o.order_id) as numVendite
                        from products p, order_items oi, orders o 
                        where p.product_id = oi.product_id and o.order_id = oi.order_id 
                            and o.order_date between %s and %s
                            and p.category_id = %s
                            group by p.product_id) as a1,
                        (select p.product_id, count(distinct o.order_id) as numVendite
                        from products p, order_items oi, orders o 
                        where p.product_id = oi.product_id and o.order_id = oi.order_id 
                            and o.order_date between %s and %s
                            and p.category_id = %s
                            group by p.product_id ) as a2 
                    where a1.product_id<a2.product_id
                        """

        cursor.execute(query, (anno1, anno2, id, anno1, anno2, id))

        for row in cursor:
            results.append((row["p1"], row["n1"], row["p2"], row["n2"])) #lista di tuple

        cursor.close()
        conn.close()
        return results


