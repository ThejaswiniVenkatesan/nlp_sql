import re
import psycopg2
from fuzzywuzzy import fuzz
from transformers import T5ForConditionalGeneration, T5Tokenizer


# Step 1: Clean and normalize the user input query
def preprocess_input(query):
    query = re.sub(r'\s+', ' ', query.strip())
    query = re.sub(r'[^\w\s,]', '', query)
    return query.lower()


# Step 2: Identify basic SQL operation (not heavily used in generation, kept for future use)
def handle_common_operations(query):
    operations = ['count', 'sum', 'avg', 'percentage', 'max', 'min', 'total']
    for op in operations:
        if op in query:
            return op
    return 'count'


# Step 3: Connect to PostgreSQL and fetch the public schema
def fetch_schema_from_postgresql():
    conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password='2610')
    cursor = conn.cursor()

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [table[0] for table in cursor.fetchall()]

    schema = {}
    for table in tables:
        cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table,)
        )
        columns = [col[0] for col in cursor.fetchall()]
        schema[table] = columns

    cursor.close()
    conn.close()
    return schema


# Step 4: Determine the best matching table for the query
def detect_table_and_columns(query, schema):
    query_keywords = query.split()
    best_score = 0
    best_table = None

    for table, columns in schema.items():
        for column in columns:
            for keyword in query_keywords:
                score = fuzz.ratio(keyword, column)
                if score > best_score:
                    best_score = score
                    best_table = table

    return best_table or list(schema.keys())[0]


# Step 5: Generate SQL query using T5 model
def generate_sql_query(nl_query, table, columns):
    schema_hint = f"{table}({', '.join(columns)})"
    prompt = f"Convert to SQL: {nl_query}. Use table: {schema_hint}"

    inputs = tokenizer(prompt, return_tensors='pt', max_length=512, truncation=True)
    outputs = model.generate(inputs['input_ids'], max_length=100, num_beams=4, early_stopping=True)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Fallback SQL if model fails to generate a valid SELECT statement
    if not sql_query.lower().startswith("select"):
        sql_query = f"SELECT COUNT(*) FROM {table}"
    return sql_query


# Step 6: Execute the SQL query against PostgreSQL
def execute_sql_query(query):
    conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password='2610')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        print("\nQuery Result:")
        for row in results:
            print(row)
    except Exception as e:
        print("\nSQL Execution Error:")
        print(e)
    finally:
        cursor.close()
        conn.close()


# Step 7: Entry point function
def main():
    user_input = input("\nEnter your query: ")
    clean_query = preprocess_input(user_input)
    schema = fetch_schema_from_postgresql()
    selected_table = detect_table_and_columns(clean_query, schema)
    selected_columns = schema[selected_table]
    sql_query = generate_sql_query(clean_query, selected_table, selected_columns)

    print("\nGenerated SQL Query:")
    print(sql_query)
    execute_sql_query(sql_query)


# Load pretrained T5 model and tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


if __name__ == "__main__":
    main()
