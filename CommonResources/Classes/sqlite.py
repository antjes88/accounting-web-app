import sqlite3
import pandas as pd


class SqLiteDatabase:
    """Connect and interact with a sqlite database"""
    def __init__(self, db_file, db_path):
        """
        Initialise the class
        :param db_file: name of the database
        :param db_path: path of the database
        """
        self.db_file = db_path + '/' + db_file + '.db'

    def create_database(self):
        """
        create a database connection to a SQLite database. When does not exist a database, it creates a new one.
        :return:
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def create_connection(self, both=True):
        """
        create a database connection to the SQLite database
        :return: Connection object and cursor or None
        """
        cursor, conn = None, None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
        except sqlite3.Error as e:
            print(e)
        if both:
            if cursor:
                return cursor, conn
        else:
            if cursor:
                return conn

    def execute(self, statement):
        """
        Method to
        """
        conn = None
        try:
            cursor, conn = self.create_connection()
            cursor.execute(statement)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    def create_table(self, table_name, table_columns, column_type, column_constraint):
        """
        This method is to create a table in the database
        :param table_name: name of the table that is going to be created
        :param table_columns: list name of the columns
        :param column_type: list of type of the columns
        :param column_constraint: list of constraints of the columns
        :return:
        """
        # check that all list has the same length
        if (len(table_columns) != len(column_type)) | (len(table_columns) != len(column_constraint)):
            return "Error Message: Number of columns names and columns types differ."

        # creation of statement
        statement = "CREATE TABLE %s ( " % table_name
        for i in range(0, len(table_columns)):
            statement += '%s %s %s ,' % (table_columns[i], column_type[i], column_constraint[i])
        statement = statement[:-1] + ')'

        # execution of statement
        self.execute(statement)

    def insert_table(self, table_name, df, time_format=None):
        """
        This method is to insert new values on the tables. It is able to manage insertion of null values.
        :param table_name: name of the table where data is going to be inserted
        :param df: dataframe of values to insert into the table
        :param time_format: dict with key as column name and content as format desired
        :return:
        """
        # Creation of Insert into and list of tables
        base_statement = 'INSERT INTO %s (' % table_name
        for col in df.columns.values.tolist():
            base_statement += ' %s,' % col
        base_statement = base_statement[:-1] + ') VALUES ('

        # this is for nan detection to input NULL values
        nan_df = df.isna()

        if time_format:
            for key in time_format:
                df[key] = df[key].dt.strftime(time_format[key])

        # creation of insert statements
        for i in df.index.values.tolist():
            statement = base_statement
            for value in df.columns.values.tolist():
                if nan_df.loc[i, value]:
                    statement += " NULL,"
                else:
                    statement += " '%s'," % df.loc[i, value]
            statement = statement[:-1] + ')'
            self.execute(statement)

    def update_table(self, table_name, df, where_identifier):
        """
        This method is to update values in a table taking into account the where_identifier
        :param table_name: name of the table to update
        :param df: dataframe with the data to update in the table
        :param where_identifier: column identifier used to update the table
        :return:
        """
        df.reset_index(drop=True, inplace=True)
        if df.shape[0] != len(where_identifier):
            return 'Length of dataframe and where_identifier differ.'
        base_statement = 'UPDATE %s SET ' % table_name

        for i in df.index.values.tolist():
            statement = base_statement
            for col in [col_y for col_y in df.columns.values.tolist() if i != where_identifier]:
                base_statement += "%s = '%s', '" % (col, df.loc[i, col])
            base_statement = base_statement[:-2] + ("WHERE %s = '%s'" % (where_identifier, df.loc[i, where_identifier]))
            self.execute(statement)

    def delete_from_table(self, table_name, col, col_values, print_sql=False):
        """
        Method to delete rows from a table base on a column value
        :param table_name: name of the table from which data is going to be drop
        :param col: name of the column for the where clause
        :param col_values: list of values to identify the row
        :return:
        """
        base_statement = 'DELETE FROM %s WHERE %s = ' % (table_name, col)
        for value in col_values:
            statement = base_statement
            statement += ('%s' % value)
            if print_sql:
                print(statement)
            self.execute(statement)

    def drop_table(self, table_name):
        """
        This method is to drop tables from the database
        :param table_name: name of the table to drop
        :return:
        """
        self.execute("DROP TABLE IF EXISTS %s" % table_name)

    def query(self, statement, time_format=None):
        """
        Method to retrieve data from a table. It can convert dates from the format in the database to the format desired
        :param statement: sql statement
        :param time_format: list of columns to transform to datetime
        :return: data: dataframe of the sql
        """
        conn = self.create_connection(both=False)
        df = pd.read_sql_query(statement, conn)
        conn.close()

        # converting into datetime long format
        if time_format:
            for key in time_format:
                try:
                    df[key] = pd.to_datetime(df[key], format='%f')
                except ValueError:
                    df[key] = pd.to_datetime(df[key])

        return df

    def create_view(self, view_name, view_statement):
        """
        This method is to create a view
        :param view_name: name to put to the view
        :param view_statement: sql statement of the view
        :return:
        """
        statement = 'CREATE VIEW IF NOT EXISTS %s AS %s' % (view_name, view_statement)
        self.execute(statement)

    def drop_view(self, view_name):
        """
        This method is to drop a view
        :param view_name: name of the view to drop
        :return:
        """
        statement = 'DROP VIEW IF EXISTS %s' % view_name
        self.execute(statement)
