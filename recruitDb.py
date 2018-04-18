import sqlite3
import os
import urllib


class DbApi:
    def getDatabase(self):

        dbName = 'recruitmentWatcher.db'
        freshDb = os.path.isfile(dbName)
        db = sqlite3.connect(dbName)

        if not freshDb:
            cursor = db.cursor()
            cursor.execute(''' CREATE TABLE terms(termId INTEGER PRIMARY KEY, term TEXT)''')
            cursor.execute(''' CREATE TABLE posts(postId INTEGER PRIMARY KEY)''')
            db.commit()

        return db


    def registerTopic(self, topicId):
        db = self.getDatabase()

        cursor = db.cursor()
        cursor.execute('''INSERT INTO posts(postId) VALUES(?)''', (topicId,) )
        db.commit()

    def checkTopic(self, topicId):
        db = self.getDatabase()

        cursor = db.cursor()
        cursor.execute( '''SELECT 1 FROM posts where postId = ?''', (topicId,) )
        results = cursor.fetchall()

        db.commit()
        #db.close()

        if results:
            return True
        else:
            return False

    def addTerm(self, message):
        db = self.getDatabase()

        print(message)
        cursor = db.cursor()
        cursor.execute('''INSERT INTO terms(term) VALUES(?)''', (message,) )
        db.commit()

    def removeTerm(self, message):
        db = self.getDatabase()

        cursor = db.cursor()
        cursor.execute('''DELETE FROM terms where termId = ?''', (message,) )
        db.commit()

    def listTermsString(self):
        db = self.getDatabase()

        cursor = db.cursor()
        cursor.execute('''SELECT * FROM terms''')
        results = cursor.fetchall()

        resultString = 'id\tterm\n'
        for result in results:
            resultString += '{0}\t{1}\n'.format(str(result[0]), result[1])

        return resultString

    def listTerms(self):
        db = self.getDatabase()

        cursor = db.cursor()
        cursor.execute('''SELECT * FROM terms''')
        results = cursor.fetchall()

        return results
