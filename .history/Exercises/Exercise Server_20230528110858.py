import pandas as pd

class Server:
    def __init__(self, database_name):
        self.database_name = database_name

    def __repr__(self):
        return f"Server({self.database_name})"

    def __str__(self):
        return f"Server connected to {self.database_name}"

    def __call__(self, sql_query):
        # Process the SQL query and return the results as a DataFrame
        result = self.process_query(sql_query)
        return pd.DataFrame(result)

    def process_query(self, sql_query):
        # Simulate processing the SQL query and returning the results
        # Replace this with your actual database query processing logic
        if sql_query == "SELECT * FROM users":
            return [
                {"id": 1, "name": "John", "age": 30},
                {"id": 2, "name": "Jane", "age": 25},
                {"id": 3, "name": "Alice", "age": 35}
            ]
        elif sql_query == "SELECT * FROM orders":
            return [
                {"id": 1, "user_id": 1, "product": "A"},
                {"id": 2, "user_id": 2, "product": "B"},
                {"id": 3, "user_id": 1, "product": "C"}
            ]
        else:
            return []

# Example usage
server = Server("MyDatabase")
print(server)  # Server connected to MyDatabase

result = server("SELECT * FROM users")
print(result)
