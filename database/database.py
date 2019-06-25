import psycopg2
import os
from psycopg2.extras import RealDictCursor


class Database:

    def __init__(self):

        if app.config["ENV"] == "production":
            app.config.from_object("config.Production")
        elif app.config["ENV"] == "testing":
            app.config.from_object("config.Testing")
        else:
            app.config.from_object("config.Development")
    
    @staticmethod
    def tables():
        '''List of table to be created '''

          queries = [
              'CREATE TABLE IF NOT EXIST users(\
                    id SERIAL PRIMARY_KEY,\
                    name VARCHAR(100) NOT NULL,\
                    email VARCHAR(100) UNIQUE NOT NULL,\
                    username VARCHAR(100) NOT NULL,\
                    password VARCHAR(200) NOT NULL,\
                    created_at timestamp\
                       
              )',

              'CREATE TABLE IF NOT EXIST articles(\
                  article_id SERIAL PRIMARY_KEY,\
                  title VARCHAR(100) NOT NULL,\
                  body VARCHAR(1000) NOT NULL,\
                  author VARCHAR(200) NOT NULL,\

              )'
          ]
           return queries


    def cursor(self):
        """cursor method for executing queries
         RealDictCursor - A cursor that uses a real python dict as the base type for rows."""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        return cur

    def commit(self):
        """ saving changes to db """    
        self.connection.commit()

    def create_tables(self):
        """create all tables else return executuon error"""
        cur = self.cursor()
        try:
            for table in self.tables():
                cur.execute(table)
                self.commit()
            print('All tables created sucessfully')
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)    

    def drop_table(self):
        """drop tables else return exection error"""
        cur = self.cursor()
        table_drops = ["DROP TABLE IF EXISTS users CASCADE",
                       "DROP TABLE IF EXISTS articles CASCADE",
                      
                       ]

        try:
            for table in table_drops:
                cur.execute(table)
                self.connection.commit()
            print("All tables dropped successfully")
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)        