import mysql.connector
from mysql.connector import Error
import json

# def create_connection():
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='123@root',
#             database='loandata'
#         )
#         if connection.is_connected():
#             print("Connected to MySQL database")
#             return connection
#     except Error as e:
#         print(f"Error: {e}")
#         return None


# # Example usage
# if __name__ == "__main__":
#     conn = create_connection()
#     if conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM rag_documents;")
#         results = cursor.fetchall()
#         # print("Data from rag_documents table:")
#         # for row in results:
#         #     print(row)
        
#         # Store data as JSON
#         with open('json_rag_documents.json', 'w') as f:
#             json.dump(results, f)
#         print("Data stored in json_rag_documents.json")
        
#         cursor.close()
#         conn.close()
#         print("Connection closed")




import mysql.connector
import json
# STEP 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123@root",
    database="loandata"
)

cursor = conn.cursor(dictionary=True)
print("Connected to MySQL database")

# STEP 2: Fetch data
query = "SELECT * FROM Combined_Loan_Data"
cursor.execute(query)
rows = cursor.fetchall()

# STEP 3: Convert to RAG format
documents = []

for row in rows:
    doc = {
        "page_content": f"Customer {row['C_name']} has a {row['L_name']} loan dated {row['L_date']}.",  # main text
        "metadata": {
            "client_id": row["C_id"],
            "loan_type": row["L_name"],
            "date": str(row["L_date"])
        }
    }
    documents.append(doc)

# STEP 4: Save as JSON file
with open("documents.json", "w") as f:
    json.dump(documents, f, indent=4)

print("JSON file created successfully!")

# STEP 5: Close connection
cursor.close()
conn.close()