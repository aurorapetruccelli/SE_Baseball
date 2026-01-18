from database.DB_connect import DBConnect
from model.team import Team


class DAO:
    @staticmethod
    def get_year():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year from team where year>1980"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_team_year(year):
        # result =  oggetti team
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.id,t.year,t.team_code,t.name from team t where t.year=%s"""

        cursor.execute(query,(year,))

        for row in cursor:
            result.append(Team(row["id"],row["year"],row["team_code"],row["name"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_team_salario(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.id as id, sum(s.salary) as salario from team t, salary s where t.id=s.team_id and t.year=%s group by t.id"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append((row["id"],row["salario"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_coppie_team(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.id as id1,t2.id as id2 from team t1,team t2 where t1.id <>t2.id and t1.id<t2.id and t1.year=%s and t2.year=%s"""

        cursor.execute(query, (year,year,))

        for row in cursor:
            result.append((row["id1"], row["id2"]))

        cursor.close()
        conn.close()
        return result
