from flask import Flask, render_template, request, jsonify
import os
import re
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database Connection
db_password = os.environ.get("DB_PASSWORD")
host = 'localhost'
port = '3306'
username = 'root'
database_schema = os.environ.get("DB_SCHEMA")
mysql_uri = f"mysql+mysqlconnector://{username}:{db_password}@{host}:{port}/{database_schema}"
db = SQLDatabase.from_uri(mysql_uri, sample_rows_in_table_info=2)

# LLM Setup
template = """Based on the table schema below, write a SQL query that would answer the user's question:
Remember : Only provide me the sql query do not include anything else. Provide me sql query in a single line do not add line breaks.
Table Schema: {schema}
Question: {question}
SQL Query:
"""
prompt = ChatPromptTemplate.from_template(template)

llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    api_key=os.environ.get("GOOGLE_API_KEY")
)

def get_schema_from_db(database: SQLDatabase) -> str:
    """Get the schema from the database."""
    table_info = database.get_table_info()
    schema = "\n".join(table_info)
    return schema

sql_chain = (
    RunnablePassthrough.assign(schema=lambda _: get_schema_from_db(db))
    | prompt
    | llm.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

def get_sql_query_from_question(question: str) -> str:
    """Get the SQL query from the natural language question."""
    sql_query = sql_chain.invoke({"question": question})
    query = re.search(r"```sql\s*(.*?)\s*```", sql_query, re.DOTALL | re.IGNORECASE)
    if query:
        sql_query = query.group(1).strip()
    return sql_query

def execute_sql_query(sql_query: str):
    """Execute the SQL query and return the results."""
    results = db.run(sql_query)
    return results

def parse_results(results):
    """Parse SQL results into a structured format."""
    if not results:
        return {"type": "empty", "data": None}
    
    # Convert string results to list if needed
    if isinstance(results, str):
        # Try to parse the string representation
        results = results.strip()
        if results.startswith('[') and results.endswith(']'):
            # It's a list representation
            import ast
            try:
                results = ast.literal_eval(results)
            except:
                return {"type": "text", "data": results}
        else:
            return {"type": "text", "data": results}
    
    # Check if it's a list of tuples (table data)
    if isinstance(results, list):
        if len(results) == 0:
            return {"type": "empty", "data": None}
        elif len(results) == 1 and len(results[0]) == 1:
            # Single value
            return {"type": "single", "data": results[0][0]}
        elif all(isinstance(row, tuple) for row in results):
            # Table data
            return {"type": "table", "data": results}
        else:
            # List of values
            return {"type": "list", "data": results}
    
    # Single value
    return {"type": "single", "data": results}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        # Generate SQL query
        sql_query = get_sql_query_from_question(question)
        
        # Execute query
        results = execute_sql_query(sql_query)
        
        # Parse results
        parsed_results = parse_results(results)
        
        return jsonify({
            'success': True,
            'sql_query': sql_query,
            'results': parsed_results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)