import mysql.connector

DB_CONFIG = {
    "host": "13.232.236.195",
    "user": "phy-thejaswini",
    "password": "Thejaphy@123",
    "database": "AIPlant40_QA"
}

# Read generated SQL from file
with open("query_to_run.txt", "r") as file:
    sql = file.read().strip()

# Reject unsafe queries
if not sql.lower().startswith("select"):
    print("❌ Only SELECT-type queries are allowed.")
    exit()

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    # Print headers if available
    if cursor.description:
        columns = [desc[0] for desc in cursor.description]
        print("\n Query Result:")
        print(" | ".join(columns))
    else:
        print("\n Query executed successfully. No output to display.")

    # Print rows
    for row in rows:
        print(" | ".join(str(cell) for cell in row))

    cursor.close()
    conn.close()

except Exception as e:
    print(f" Error executing query:\n{e}")
