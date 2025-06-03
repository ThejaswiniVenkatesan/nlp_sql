import re
import mysql.connector
from llama_cpp import Llama

# === CONFIG ===
MODEL_PATH = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
DB_CONFIG = {
    "host": "13.232.236.195",
    "user": "phy-thejaswini",
    "password": "Thejaphy@123",
    "database": "AIPlant40_QA"
}

# === Load model ===
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=6)
print("✅ TinyLlama model loaded!")

# === Get full DB schema ===
def get_schema():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    schema = {}
    for t in tables:
        cursor.execute(f"DESCRIBE {t}")
        schema[t] = [col[0] for col in cursor.fetchall()]
    cursor.close()
    conn.close()
    return schema

# === Find relevant tables based on fuzzy match ===
def filter_tables(input_text, schema):
    words = set(re.findall(r"\w+", input_text.lower()))
    table_scores = {}
    for table, cols in schema.items():
        all_text = f"{table} " + " ".join(cols)
        match_count = sum(1 for word in words if word in all_text.lower())
        table_scores[table] = match_count
    sorted_tables = sorted(table_scores.items(), key=lambda x: x[1], reverse=True)
    top_tables = [t for t, score in sorted_tables if score > 0]
    return top_tables[:3] if top_tables else list(schema.keys())[:3]

# === Clean SQL from LLM output ===
def clean_sql_output(text):
    lines = text.strip().splitlines()
    sql_lines = []
    for line in lines:
        if "select" in line.lower() or sql_lines:
            if any(x in line.lower() for x in ["output:", "explanation:", "instruction:"]):
                break
            sql_lines.append(line.strip())
    return " ".join(sql_lines).strip("; ")

# === Fix hallucinated column names ===
def fix_column_names(sql, column_list):
    for col in column_list:
        short = col.lower().split("_")[-1]
        pattern = rf"\b{short}\b"
        sql = re.sub(pattern, col, sql, flags=re.IGNORECASE)
    return sql

# === Fix hallucinated table names ===
def fix_table_names(sql, valid_tables):
    for table in valid_tables:
        pattern = re.compile(rf"\b{table.lower()}\b", re.IGNORECASE)
        sql = pattern.sub(table, sql)
    return sql

# === Generate SQL ===
def generate_sql(user_input, schema, selected_tables):
    selected_schema = {t: schema[t] for t in selected_tables}
    schema_prompt = "\n".join([f"{t}({', '.join(cols)})" for t, cols in selected_schema.items()])

    prompt = f"""You are a SQL generator.
Only use the exact table and column names below:
{schema_prompt}

Write SELECT-style SQL for the instruction. No INSERT, DELETE, DROP, or CREATE.
Instruction: {user_input}
SQL:"""

    result = llm(prompt, max_tokens=300, stop=["</s>", "Instruction:", "SQL:"])
    raw_text = result["choices"][0]["text"].strip()
    sql = clean_sql_output(raw_text)
    sql = fix_column_names(sql, schema[selected_tables[0]])
    sql = fix_table_names(sql, selected_tables)
    return sql

# === Run SQL on DB ===
def run_query(sql):
    if not sql.lower().startswith("select"):
        print("❌ Not a SELECT query.")
        return
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        print("\n📊 Query Result:")
        print(" | ".join(columns))
        for row in rows:
            print(" | ".join(str(cell) for cell in row))
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error executing query:\n{e}")

# === MAIN ===
if __name__ == "__main__":
    schema = get_schema()
    print("📚 Schema loaded.\n")

    while True:
        user_input = input("🧑 You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting.")
            break
        selected = filter_tables(user_input, schema)
        sql = generate_sql(user_input, schema, selected)
        if sql:
            print(f"\n✅ SQL Generated:\n{sql}")
            run_query(sql)
        else:
            print("⚠️ Could not generate SQL. Try rephrasing.")
