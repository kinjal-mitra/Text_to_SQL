# Text-to-SQL Query Application

A Flask-based web application that converts natural language questions into SQL queries using Google's Gemini AI and executes them against a MySQL database. The application features an intuitive interface that displays results in multiple formats (single values, lists, or tables).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)
![Claude](https://simpleicons.org/?modal=icon&q=claude)
![Gemini Gemini](https://simpleicons.org/?modal=icon&q=googlegemini)


## Features

- 🤖 **AI-Powered Query Generation**: Uses Google Gemini 2.0 Flash to convert natural language to SQL
- 🎨 **Modern Responsive UI**: Beautiful gradient design that works on all devices
- 📊 **Smart Result Display**: Automatically formats results as single values, lists, or tables
- ⚡ **Real-time Execution**: Instant query generation and execution
- 🔒 **Secure Configuration**: Environment-based configuration for sensitive data
- 🎯 **Error Handling**: Comprehensive error messages for debugging

## Screenshots

### Query Interface
The main interface where users can ask questions in natural language.

### Result Display
- **Single Value**: Large highlighted display for aggregate results
- **List View**: Styled list items for multiple simple values
- **Table View**: Full table rendering with headers for complex queries

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- MySQL Server (5.7 or higher)
- Google API Key (for Gemini AI)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/text-to-sql-app.git
cd text-to-sql-app
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install from requirements file:

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

Create a MySQL database and tables:

```sql
CREATE DATABASE text_to_sql;
USE text_to_sql;

-- Example table structure
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    product VARCHAR(100),
    amount DECIMAL(10, 2),
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Insert sample data
INSERT INTO customers (name, email, city, country) VALUES
('John Doe', 'john@example.com', 'New York', 'USA'),
('Jane Smith', 'jane@example.com', 'London', 'UK'),
('Bob Johnson', 'bob@example.com', 'Toronto', 'Canada');

INSERT INTO orders (customer_id, product, amount, order_date) VALUES
(1, 'Laptop', 999.99, '2024-01-15'),
(1, 'Mouse', 29.99, '2024-01-16'),
(2, 'Keyboard', 79.99, '2024-01-17'),
(3, 'Monitor', 299.99, '2024-01-18');
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DB_USERNAME=root
DB_PASSWORD=your_mysql_password
DB_SCHEMA=your_mysql_schema_name

# Google AI Configuration
GOOGLE_API_KEY=your_google_api_key_here
```

**Getting a Google API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

## Project Structure

```
text-to-sql-app/
│
├── app.py                  # Main Flask application
├── templates/
│   └── index.html         # Frontend HTML template
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Usage

### 1. Start the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 2. Open in Browser

Navigate to `http://localhost:5000` in your web browser.

### 3. Ask Questions

Enter natural language questions such as:

- "Show me all customers"
- "What is the total revenue?"
- "List the top 5 products by sales"
- "How many orders were placed in January?"
- "Find customers from New York"
- "What is the average order amount?"

### 4. View Results

The application will:
1. Convert your question to SQL
2. Display the generated SQL query
3. Execute the query
4. Show results in an appropriate format

## Example Queries

| Natural Language Question | Expected SQL |
|--------------------------|--------------|
| "Show me all customers" | `SELECT * FROM customers` |
| "What is the total revenue?" | `SELECT SUM(amount) FROM orders` |
| "How many customers are there?" | `SELECT COUNT(*) FROM customers` |
| "List customers from USA" | `SELECT * FROM customers WHERE country = 'USA'` |
| "Show recent orders" | `SELECT * FROM orders ORDER BY order_date DESC LIMIT 10` |

## Configuration

### Database Configuration

Modify the database connection settings in `app.py`:

```python
host = 'localhost'
port = '3306'
username = 'root'
```

### LLM Model Configuration

Change the AI model in `app.py`:

```python
llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',  # Change to other Gemini models
    api_key=os.environ.get("GOOGLE_API_KEY")
)
```

## Troubleshooting

### Common Issues

**1. Database Connection Error**
```
Error: Access denied for user 'root'@'localhost'
```
**Solution**: Check your MySQL password in the `.env` file

**2. API Key Error**
```
Error: Invalid API key
```
**Solution**: Verify your Google API key is correct and active

**3. Module Not Found**
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: Install all dependencies using `pip install -r requirements.txt`

**4. Port Already in Use**
```
OSError: [Errno 48] Address already in use
```
**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use a different port
```

### Debug Mode

To enable detailed error messages, ensure debug mode is on:

```python
app.run(debug=True, port=5000)
```

## Security Considerations

- **Never commit `.env` file** to version control
- **Use strong passwords** for database access
- **Limit API key permissions** in Google Cloud Console
- **Validate user inputs** before processing
- **Use prepared statements** to prevent SQL injection
- **Implement rate limiting** for production use

## Performance Optimization

For better performance:

1. **Add database indexes** on frequently queried columns
2. **Implement caching** for common queries
3. **Use connection pooling** for database connections
4. **Optimize SQL queries** generated by the AI
5. **Set query timeouts** to prevent long-running queries

## Deployment

### Deploy to Production

For production deployment:

1. **Use a production WSGI server** (Gunicorn/uWSGI):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

2. **Set up a reverse proxy** (Nginx/Apache)
3. **Use environment-specific configurations**
4. **Enable HTTPS** with SSL certificates
5. **Implement logging** and monitoring
6. **Add authentication** for secure access

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **LangChain** for the AI framework
- **Google Gemini** for the language model
- **Flask** for the web framework
- **MySQL** for the database

## Support

For issues and questions:
- Open an issue on GitHub
- Contact: kinjalmitra03@gmail.com

## Roadmap

Future enhancements planned:

- [ ] Support for multiple databases (PostgreSQL, SQLite)
- [ ] Query history and favorites
- [ ] Export results to CSV/Excel
- [ ] Advanced filtering and sorting
- [ ] User authentication and multi-tenancy
- [ ] Query result visualization (charts/graphs)
- [ ] Natural language result explanations
- [ ] Voice input support

---

**Made with ❤️ using Flask and Google Gemini AI**