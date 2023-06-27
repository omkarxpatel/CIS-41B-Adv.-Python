import pandas as pd

class Server:
    def __init__(self, database_name):
        self.database_name = database_name
        self.users = {1:{"name":"michael", "age":15, "orders":["apple", "carrot"]}, 2:{"name":"ryan", "age": 17, "orders":[]}, 3:{"name":"william", "age": 21}}
        self.ids = {"michael":1, "ryan":2, "william":3}
        

    def __repr__(self):
        return f"Server({self.database_name})"

    def __str__(self):
        return f"Server connected to {self.database_name}"

    def __call__(self, sql_query):
        result = self.process_query(sql_query)
        return pd.DataFrame(result)

    def process_query(self, sql_query):
        if sql_query == "SELECT * FROM users":
            
            for id, info in self.users.items():
                print(f"ID: {id} INFO: {info}\n")
            
                
                
        elif sql_query.startswith("SELECT * FROM users WHERE name = "):
            name = sql_query.split("=")[1].strip()
            
            if name in self.ids:
                id = self.ids[name]
                
                info = self.users[id]
                print(f"ID: {id} INFO: {info}")
            
            else:
                print(f"No user found with NAME: {name}")
                
                
        elif sql_query == "SELECT * FROM orders":
            return [
                {"id": 1, "user_id": 1, "product": "A"},
                {"id": 2, "user_id": 2, "product": "B"},
                {"id": 3, "user_id": 1, "product": "C"}
            ]
            
            
        else:
            return []

server = Server("MyDatabase")

result = server("SELECT * FROM users")
print(result)

print(); print()
result = server("SELECT * FROM users WHERE name = william")
print(result)
