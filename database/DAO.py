from database.DB_connect import DBConnect
from model.sighting import Sighting


class DAO():

    @staticmethod
    def getYears():

        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        res = []

        query = """select distinct(year(datetime))
                    from sighting 
                    order by year(datetime) desc
        """

        cursor.execute(query)

        for row in cursor:
            res.append(row[0])

        conn.close()
        cursor.close()

        return res

    @staticmethod
    def getShapes(year):

        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        res = []

        query = """select distinct(shape)
                        from sighting 
                        where shape != 'unknown' and year(datetime) = %s and shape != ''
                        order by shape asc
            """

        cursor.execute(query, (year,))

        for row in cursor:
            res.append(row[0])

        conn.close()
        cursor.close()

        return res

    @staticmethod
    def getNodes(year, shape):

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        query = """select *
                            from sighting 
                            where shape = %s and year(datetime) = %s 
                          
                """

        cursor.execute(query, (shape, year))

        for row in cursor:
            res.append(Sighting(**row))

        conn.close()
        cursor.close()

        return res




    if __name__=='__main__':
        print(getYears())
        print(getShapes(2011))
        print(getNodes(2011, "oval"))
