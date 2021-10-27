from cassandra.cluster import Cluster
cluster = Cluster(['127.0.0.1'], control_connection_timeout=10,  port=9042)
# session = cluster.connect()
# print('session', session)

import uuid

u = uuid.uuid4()
print('u', str(u))

# session.execute("CREATE KEYSPACE demo WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}")
# session.execute("CREATE TABLE demo.users (lastname text PRIMARY KEY, firstname text, email text)")
# session.execute("""
#     INSERT INTO demo.users
#     (lastname, firstname, email)
#      VALUES (%s,%s,%s)
#     """,
#     ("Brutus", "Marcus", "marcus@example.com")
# )
# session.execute("""
#     INSERT INTO demo.users
#     (lastname, firstname, email)
#      VALUES (%s,%s,%s)
#     """,
#     ("Caesar", "Julius", "caesar@example.com")
# )

# result = session.execute("""
#     SELECT * FROM demo.users WHERE lastname = %s
#     """,
#     ["Brutus"]).one()
# print('result', result)
# print(result.firstname, result.email)

# result = session.execute("""
#     SELECT * FROM demo.users WHERE lastname = %s
#     """,
#     ["Caesar"]).one()
# print(result.firstname, result.email)

# rows = session.execute('SELECT lastname, firstname, email FROM demo.users')
# for row in rows:
#     print('lastname', row.lastname, 'firstname', row.firstname, 'email', row.email)

# rows = session.execute('SELECT lastname, firstname, email FROM demo.users')
# for (lastname, firstname, email) in rows:
#     print(lastname, firstname, email)

# rows = session.execute('SELECT lastname, firstname, email FROM demo.users')
# for row in rows:
#     print(row[0], row[1], row[2])


# session.execute("""
#     UPDATE demo.users SET email =%s WHERE lastname = %s
#     """,
#     ["mb@example.com", "Brutus"])

# session.execute("""
#     UPDATE demo.users SET email =%s WHERE lastname = %s
#     """,
#     ["jc@example.com", "Caesar"])

# result = session.execute("""
#     SELECT * FROM demo.users WHERE lastname = %s
#     """,
#     ["Caesar"]).one()
# print(result.firstname, result.email)

# session.execute("""
#     DELETE FROM demo.users WHERE lastname = %s
#     """,
#     ["Brutus"])


cluster = Cluster(protocol_version = 3)
session = cluster.connect('killrvideo')

for val in session.execute("SELECT * FROM videos_by_tag"):
    # print(val[0])
    print(val)

# print('{0:12} {1:40} {2:5}'.format('Tag', 'ID', 'Title'))
# for val in session.execute("select * from videos_by_tag"):  
#     print('{0:12} {1:40} {2:5}'.format(val[0], val[2], val[3]))


# session.execute(
# "INSERT INTO videos_by_tag (tag, added_date, video_id, title)" +
# "VALUES ('cassandra', '2013-01-10', uuid(), 'Cassandra Is My Friend')")

# print('{0:12} {1:40} {2:5}'.format('Tag', 'ID', 'Title'))
# for val in session.execute("select * from videos_by_tag"):
#     print('{0:12} {1:40} {2:5}'.format(val[0], val[1], val[3]))








# import json
# from websocket import create_connection
# ws = create_connection("ws://127.0.0.1:8010/ws/7dcdbe64-0f2f-4a7c-8fdd-8d7ee35bfe99/b5ccc3ef-a907-435b-9490-03a0f5d6eab4/")
# ws.send(json.dumps({"command":"send",
#     "message":"what are u doing"}))
# result =  ws.recv()
# print (result)
# ws.close()