__Author__ = "noduez"
#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/7/5 3:54 PM
# @File    : ushuffle_mongo.py
# @Software: PyCharm

from distutils.log import warn as printf
from random import randrange as rand
from pymongo import MongoClient, errors
import pymongo
from ch06_DB.ushuffle_db import DBNAME, randName, FIELDS, tformat, cformat

COLLECTION = 'users'

class MongoTest(object):
    def __init__(self):
        try:
            cxn = MongoClient()
        except errors.AutoReconnect:
            raise RuntimeError
        self.db = cxn[DBNAME]
        self.users = self.db[COLLECTION]

    def insert(self):
        self.users.insert(
            dict(login=who, userid=uid, projid=rand(1,5)) for who, uid in randName())

    def update(self):
        fr = rand(1,5)
        to = rand(1,5)
        i = -1
        for i, user in enumerate(self.users.find({'projid': fr})):
            self.users.update(user,
                              {'$set': {'projid': to}})
        return fr, to, i+1

    def delete(self):
        rm = rand(1,5)
        i = -1
        for i, user in enumerate(self.users.find({'projid': rm})):
            self.users.remove(user)
        return  rm, i+1

    def dbDump(self):
        printf('\n%s' % ''.join(map(cformat, FIELDS)))
        for user in self.users.find():
            printf(''.join(map(tformat, (user[k] for k in FIELDS))))

    def finish(self):
        self.db.client.close()

def main():
    printf('*** Connect to %r database' % DBNAME)

    try:
        mongo  = MongoTest()
    except RuntimeError:
        printf('\nERROR: MongoDB server unreachable, exit')
        return

    printf('\n*** Insert names into table')
    mongo.insert()
    mongo.dbDump()

    printf('\n*** Move users to a random group')
    fr, to, num = mongo.update()
    printf('\t(%d users moved from (%d) to (%d)' % (num, fr, to))
    mongo.dbDump()

    printf('\n*** Randomly delete group')
    rm, num = mongo.delete()
    printf('\t(Group #%d; %d users removed' % (rm, num))
    mongo.dbDump()

    printf('\n*** Drop users tables')
    mongo.db.drop_collection(COLLECTION)
    printf('\n Close cxns')
    mongo.finish()

if __name__ == '__main__':
    main()