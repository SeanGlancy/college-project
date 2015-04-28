import mysql.connector

class UseDatabase:
    def __init__(self, configuration):
        """ Initialisation code which executes the context manager
            is CREATED. """
        #self.host = configuration['mysql.server']
        self.host = 'mysql.server'
        self.user = 'c00156721'
        self.passwd = 'dbPass'
        self.db = 'c00156721$lottoDB'

    def __enter__(self):
        """ Set-up code which executes BEFORE the body of the
            with statement. """
        self.conn = mysql.connector.connect(host=self.host,
                                            user=self.user,
                                            password=self.passwd,
                                            database=self.db,)
        self.cursor = self.conn.cursor()
        return(self.cursor)

    def __exit__(self, exc_type, exv_value, exc_traceback):

        self.cursor.close()
        self.conn.commit()
        self.conn.close()
