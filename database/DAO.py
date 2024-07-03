from database.DB_connect import DBConnect
from model.stati import Stato


class DAO():

    @staticmethod
    def getannieavv():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select year(s.`datetime`) as anno, count(*) as avvist
                    from sighting s 
                    group by year(s.`datetime`)
                    order by anno desc
                    """

        cursor.execute(query)

        for row in cursor:
            result.append((row['anno'],row['avvist']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def tempo(id1,anno):
        conn = DBConnect.get_connection()

        result = None

        cursor = conn.cursor(dictionary=True)
        query = """select min(s.`datetime`)as t
from sighting s 
where year (s.`datetime`)=%s and s.state =%s"""

        cursor.execute(query,(anno,id1.id))

        for row in cursor:
            result = (row['t'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def verifica(id1,anno,tempo):
        conn = DBConnect.get_connection()

        result =None

        cursor = conn.cursor(dictionary=True)
        query = """select min(s.`datetime`)as t
from sighting s 
where year (s.`datetime`)=%s and s.state =%s and s.`datetime`> %s"""

        cursor.execute(query, (anno, id1.id,tempo,))

        for row in cursor:
            result = (row['t'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def nodi(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s2.*
                    from sighting s ,state s2 
                    where s.state =s2.id and year (s.`datetime`)=%s
                    group by s2.id 
                    having count(*)>=1 
                                            """

        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def arco(n1,n2,anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
            from sighting s ,sighting s2 
            where year (s.`datetime`)=%s and year (s.`datetime`)= year (s2.`datetime`)and  s.state=%s and s2.state =%s and s2.`datetime` <s.`datetime` 
            """

        cursor.execute(query, (anno,n1.id,n2.id,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result