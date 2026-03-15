from pymongo import MongoClient

MONGO_URI = "mongodb+srv://athulya:athulya123@cluster0.pmm3cw9.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client['mydatabase']

# print('Database Created')

# employees =db['Employees']

# print("collection created")

# employee_data ={
#     'Name':'Athulya',
#     'Age':21,
#     'Course':'Python'
# }





# INSERT INPUT USING FOR LOOP

# student=int(input("Enter the number of the students that you wwant to add :"))
# for i in range(1,student+1):
#     print('Student:',i)
#     admno=int(input("Enter the admno of the student:"))
#     name=input("Enter the name of the student:")
#     age=int(input("Enter the age of the student:"))
#     employee_data={
#         'Admno':admno,
#         'Name':name,
#         'Age':age,
#     }
        
#     insert_result = employees.insert_one(employee_data)






# employee_data=[
#   { 'name': "Anu",   'age': 22, 'course': "BCA" },
#   { 'name': "Rahul", 'age': 24, 'course': "MCA" },
#   { 'name': "Neha",  'age': 21, 'course': "BSc" }
# ]


# insert_result=employees.insert_many(employee_data)
# print('Document inserted', insert_result.inserted_id)






# FIND ALL

# coll = db['Employees']

# for emp in coll.find():
#     print(emp)





# FILTERATION BY SPECIFIC VALUES

# coll = db['Employees']

# for emp in coll.find({"Age":21}):
#     print(emp)



# coll = db['Employees']
# emp = coll.find_one({"Name":'Athulya'})
# print(emp)



# coll = db['Employees']

# for emp in coll.find({"Age":{"$gt":21}}):
#     print(emp)




# UPDATE ONE

# coll = db['Employees']
# coll.update_one({"Name":"Athulya"},{"$inc":{"Age":21}})
# for emp in coll.find():
#     print(emp)


# coll = db['Employees']
# coll.delete_one({"Name":"Athulya"})
# for emp in coll.find():
#     print(emp)


coll = db['Employees']
coll.delete_many({})
for emp in coll.find():
    print(emp)