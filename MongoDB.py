import pymongo as py

class MongoDBOperations:

    def __init__(self,username,password):
        self.password = password
        self.username = username
        self.url = "mongodb+srv://{}:{}@cluster0.tv8uk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(
                self.username, self.password)

    def getMongoObject(self):
        try:
            mongo_client = py.MongoClient(self.url)
            return mongo_client
        except Exception as e:
            raise  Exception("Issue with creating connection with Database : " + str(e))

    def CloseMongoDBConnection(self,client):
        try:
            client.close()
        except Exception as e:
            raise Exception("Issue with closing connection :" + str(e))

    def IsDatabasePresent(self,client,db_name):
        try:
            if db_name in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise Exception("Issue while checking database" , str(e))

    def getDatabase(self,db_name):
        try:
            client = self.getMongoObject()
            return client[db_name]
        except Exception as e:
            raise Exception("Issue with getting a database name" , str(e))

    def IsCollectionPresent(self,db_name,name):
        try:
            client = self.getMongoObject()
            database_check = self.IsDatabasePresent(client,db_name)
            if database_check:
                database = self.getDatabase(db_name)
                if name in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception("Issue with getting a collection name", str(e))

    def getCollection(self,database,name):
        try:
            return database[name]
        except Exception as e:
            raise Exception("issue while getting collection name " , str(e))

    def CreatingDatabase(self,client,name):
        try:
            if self.IsDatabasePresent(client,name):
                database = client[name]
            else:
                database = client[name]
            return database

        except Exception as e:
            raise Exception(f"Issue with creating Databse {name} : " + str(e))

    def CreatingCollection(self,db_name,name):
        try:
            status = self.IsCollectionPresent(db_name,name)
            if not status:
                database = self.getDatabase(db_name)
                return database[name]
        except Exception as e:
            raise Exception("Issue while creating a collection" , str(e))

    def insertOne(self,collection,record):
        try:
            collection.insert_one(record)
        except Exception as e:
            raise Exception("Issue while inserting record : " ,str(e))