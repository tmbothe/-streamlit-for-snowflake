# ❄️ Streamlit App for Snowflake

A powerful and interactive Streamlit application for exploring and visualizing data from Snowflake databases.

## Features

- 🔌 **Easy Connection**: Connect to your Snowflake database with a simple interface
- 📊 **Query Execution**: Run custom SQL queries and view results in an interactive table
- 📈 **Data Visualization**: Create beautiful charts (bar, line, scatter, pie, area) from your query results
- 📥 **Data Export**: Download query results as CSV files
- ℹ️ **Database Info**: View connection details and browse available tables
- 🔐 **Secure**: Support for secrets management to keep credentials safe

## Installation

1. Clone this repository:
```bash
git clone https://github.com/tmbothe/-streamlit-for-snowflake.git
cd -streamlit-for-snowflake
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Option 1: Using Secrets File (Recommended)

1. Create a `.streamlit/secrets.toml` file:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

2. Edit `.streamlit/secrets.toml` with your Snowflake credentials:
```toml
[snowflake]
account = "your_account_identifier"
user = "your_username"
password = "your_password"
warehouse = "COMPUTE_WH"
database = "your_database"
schema = "PUBLIC"
```

**Important**: Never commit `secrets.toml` to version control! It's already in `.gitignore`.

### Option 2: Manual Input

You can also enter credentials directly in the app's sidebar when you run it.

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## App Functionality

### 1. Query Data Tab
- Enter and execute custom SQL queries
- View results in an interactive table
- Download results as CSV
- Use the "Sample Query" button to test the connection

### 2. Visualize Tab
- Fetch data with a SQL query
- Select chart type (bar, line, scatter, pie, area)
- Choose X and Y axes
- Generate interactive visualizations

### 3. Database Info Tab
- View current connection details
- Check Snowflake version and server time
- List all tables in the current schema

## Requirements

- Python 3.8+
- Streamlit 1.28.0+
- snowflake-connector-python 3.0.0+
- pandas 2.0.0+
- plotly 5.0.0+

## Security Notes

- Always use the secrets.toml file for production deployments
- Never commit credentials to version control
- Use Snowflake role-based access control for database permissions
- Consider using OAuth or key-pair authentication for enhanced security

## Troubleshooting

### Connection Issues
- Verify your account identifier is correct (check Snowflake admin console)
- Ensure your IP is whitelisted in Snowflake network policies
- Check that the warehouse, database, and schema exist and you have access

### Query Errors
- Verify SQL syntax is correct for Snowflake
- Ensure you have appropriate permissions for the query
- Check that table and column names are correct

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - The fastest way to build data apps
- [Snowflake](https://www.snowflake.com/) - The Data Cloud
- [Plotly](https://plotly.com/) - Interactive graphing library
