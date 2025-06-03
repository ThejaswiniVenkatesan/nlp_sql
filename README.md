# Natural Language to SQL (TinyLlama + MySQL)

This project enables users to query a MySQL database using natural language instructions, powered by a locally running TinyLlama model.

## Features

- Converts user questions into valid SELECT-style SQL queries
- Uses llama-cpp-python to run TinyLlama fully offline
- Automatically detects relevant tables and columns based on schema match
- Cleans up hallucinated or incorrect table/column names
- Executes the generated query on a live MySQL database
- No API keys, tokens, or internet connection required

## Technology Stack

- Python 3.10+
- llama-cpp-python (for TinyLlama inference)
- MySQL
- mysql-connector-python
- TinyLlama (tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf)

## How to Use

1. Clone the repository and place the model `.gguf` file in the project folder.
2. Update the MySQL credentials in `pp.py`.
3. Run the script:
   ```bash
   python pp.py
 4.Enter queries in natural language, such as:

     Show number of working assets

    List all downtimes for asset 103

    Count parts with active status

###Current Limitations and Future Work
-Further prompt tuning is needed to improve query accuracy and consistency.
-May not handle complex or vague queries correctly.
-Supports only SELECT-style queries at the moment.
-Column name correction is basic and based on text similarity. A semantic approach can improve accuracy.
