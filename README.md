# nlp_sql
Natural Language to SQL Generator
This project converts user-input natural language queries into SQL queries using a T5 transformer model. It dynamically matches the schema from a PostgreSQL database and returns the query results.

Features
Preprocesses natural language input
Detects relevant table and columns using fuzzy matching
Generates SQL using a T5 transformer model
Connects to PostgreSQL and executes queries

Technologies Used
Python
PostgreSQL
Hugging Face Transformers (T5)
FuzzyWuzzy (for keyword similarity)

How to Run
Ensure PostgreSQL is running and accessible.
Update the database credentials in the script.
Run the script using:
python script_name.py
