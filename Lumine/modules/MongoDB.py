from pymongo import MongoClient


url1 = "mongodb+srv://ishikki:ishikki143@userinfo.rgkr6xj.mongodb.net/?retryWrites=true&w=majority"
url2 = "mongodb+srv://ishikki:ishikki143@guilddata.4yfxkdl.mongodb.net/?retryWrites=true&w=majority"

cluster1 = MongoClient(url1) 
cluster2 = MongoClient(url2)

db1 = cluster1['userinfo']
db2 = cluster2['guildinfo']

collection1 = db1['userinfo']
collection2 = db2['guildinfo']


#----------------------------------#######################----------------------------------
#collection1 = --- User Data   ---------post1
#collection2 = --- Guild Data  ---------post2

#post1 =                   #Post2 =
"""
_id =                      _id = 
Name =                     Guild_Name = 
level =                    Guild_Level =
Rank =                     Members =
Points =                   vault =
Gender =                   Guild_Creator =
Partner =                  Crime_Rate =
Friend =                   Guild_Rank = 
Father =                   Guild_Status =
Mother = 
Children = 
Status = (Guild name)
Bounty = 
"""
#----------------------------------#######################----------------------------------
