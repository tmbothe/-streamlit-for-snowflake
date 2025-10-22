import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Snowflake Data Explorer",
    page_icon="❄️",
    layout="wide"
)

# Title and description
st.title("❄️ Snowflake Data Explorer")
st.markdown("Connect to your Snowflake database and explore your data interactively.")

# Sidebar for connection configuration
st.sidebar.header("🔧 Connection Settings")

# Check if secrets are configured
try:
    has_secrets = "snowflake" in st.secrets
except:
    has_secrets = False

if has_secrets:
    # Use secrets from .streamlit/secrets.toml
    connection_params = {
        "account": st.secrets["snowflake"]["account"],
        "user": st.secrets["snowflake"]["user"],
        "password": st.secrets["snowflake"]["password"],
        "warehouse": st.secrets["snowflake"]["warehouse"],
        "database": st.secrets["snowflake"]["database"],
        "schema": st.secrets["snowflake"]["schema"],
    }
    st.sidebar.success("✅ Using credentials from secrets.toml")
else:
    # Manual input for connection parameters
    st.sidebar.info("Enter your Snowflake credentials below:")
    connection_params = {
        "account": st.sidebar.text_input("Account", help="Your Snowflake account identifier"),
        "user": st.sidebar.text_input("User", help="Your Snowflake username"),
        "password": st.sidebar.text_input("Password", type="password", help="Your Snowflake password"),
        "warehouse": st.sidebar.text_input("Warehouse", value="COMPUTE_WH", help="Warehouse to use"),
        "database": st.sidebar.text_input("Database", help="Database name"),
        "schema": st.sidebar.text_input("Schema", value="PUBLIC", help="Schema name"),
    }

# Initialize connection state
if "conn" not in st.session_state:
    st.session_state.conn = None
if "connected" not in st.session_state:
    st.session_state.connected = False

# Function to create Snowflake connection
def init_connection():
    """Initialize connection to Snowflake"""
    try:
        conn = snowflake.connector.connect(**connection_params)
        return conn
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")
        return None

# Function to run query
def run_query(query):
    """Run a query and return results as DataFrame"""
    try:
        with st.session_state.conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return pd.DataFrame(results, columns=columns)
    except Exception as e:
        st.error(f"Query failed: {str(e)}")
        return None

# Connection button
if st.sidebar.button("🔌 Connect to Snowflake"):
    if all(connection_params.values()):
        with st.spinner("Connecting to Snowflake..."):
            st.session_state.conn = init_connection()
            if st.session_state.conn:
                st.session_state.connected = True
                st.sidebar.success("✅ Connected successfully!")
    else:
        st.sidebar.error("❌ Please fill in all connection parameters")

# Disconnect button
if st.session_state.connected:
    if st.sidebar.button("🔌 Disconnect"):
        if st.session_state.conn:
            st.session_state.conn.close()
        st.session_state.conn = None
        st.session_state.connected = False
        st.sidebar.info("Disconnected from Snowflake")

# Main content area
if st.session_state.connected:
    st.success("🎉 Connected to Snowflake!")
    
    # Tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["📊 Query Data", "📈 Visualize", "ℹ️ Database Info"])
    
    with tab1:
        st.header("Run Custom Queries")
        
        # Query input
        query = st.text_area(
            "Enter your SQL query:",
            height=150,
            placeholder="SELECT * FROM your_table LIMIT 100;",
            help="Enter a SQL query to execute on your Snowflake database"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            run_button = st.button("▶️ Run Query", type="primary")
        with col2:
            if st.button("📋 Sample Query"):
                query = "SELECT CURRENT_VERSION() AS VERSION, CURRENT_TIMESTAMP() AS CURRENT_TIME;"
        
        if run_button and query:
            with st.spinner("Running query..."):
                df = run_query(query)
                if df is not None:
                    st.success(f"✅ Query returned {len(df)} rows")
                    st.dataframe(df, use_container_width=True)
                    
                    # Download button
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv",
                    )
    
    with tab2:
        st.header("Data Visualization")
        
        # Query for visualization
        viz_query = st.text_area(
            "Enter query to visualize (must include at least 2 columns):",
            height=100,
            placeholder="SELECT category, COUNT(*) as count FROM your_table GROUP BY category;",
            key="viz_query"
        )
        
        if st.button("📊 Fetch Data for Visualization", type="primary"):
            with st.spinner("Fetching data..."):
                df = run_query(viz_query)
                if df is not None and len(df) > 0:
                    st.session_state.viz_df = df
                    st.success(f"✅ Fetched {len(df)} rows")
        
        # Visualization options
        if "viz_df" in st.session_state and st.session_state.viz_df is not None:
            df = st.session_state.viz_df
            st.dataframe(df.head(), use_container_width=True)
            
            st.subheader("Chart Options")
            chart_type = st.selectbox(
                "Select chart type:",
                ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Area Chart"]
            )
            
            cols = df.columns.tolist()
            
            col1, col2 = st.columns(2)
            with col1:
                x_axis = st.selectbox("X-axis:", cols, key="x_axis")
            with col2:
                y_axis = st.selectbox("Y-axis:", cols, index=min(1, len(cols)-1), key="y_axis")
            
            # Create visualization
            try:
                if chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                elif chart_type == "Pie Chart":
                    fig = px.pie(df, names=x_axis, values=y_axis, title=f"{y_axis} distribution")
                elif chart_type == "Area Chart":
                    fig = px.area(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating chart: {str(e)}")
    
    with tab3:
        st.header("Database Information")
        
        # Show current database info
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.subheader("📌 Connection Details")
            st.write(f"**Database:** {connection_params['database']}")
            st.write(f"**Schema:** {connection_params['schema']}")
            st.write(f"**Warehouse:** {connection_params['warehouse']}")
        
        with info_col2:
            st.subheader("🔍 Quick Stats")
            if st.button("Refresh Stats"):
                # Get database version
                version_df = run_query("SELECT CURRENT_VERSION() AS VERSION;")
                if version_df is not None:
                    st.write(f"**Snowflake Version:** {version_df['VERSION'][0]}")
                
                # Get current timestamp
                time_df = run_query("SELECT CURRENT_TIMESTAMP() AS CURRENT_TIME;")
                if time_df is not None:
                    st.write(f"**Server Time:** {time_df['CURRENT_TIME'][0]}")
        
        # List tables
        st.subheader("📋 Available Tables")
        if st.button("List Tables in Current Schema"):
            tables_query = f"SHOW TABLES IN SCHEMA {connection_params['database']}.{connection_params['schema']};"
            tables_df = run_query(tables_query)
            if tables_df is not None:
                st.dataframe(tables_df, use_container_width=True)

else:
    # Show instructions when not connected
    st.info("👈 Please configure your connection settings in the sidebar and click 'Connect to Snowflake'")
    
    st.markdown("""
    ### Getting Started
    
    1. **Configure Connection**: Enter your Snowflake credentials in the sidebar
    2. **Connect**: Click the 'Connect to Snowflake' button
    3. **Explore**: Use the tabs to query data, create visualizations, and view database information
    
    ### Using Secrets (Recommended)
    
    For better security, create a `.streamlit/secrets.toml` file with your credentials:
    
    ```toml
    [snowflake]
    account = "your_account"
    user = "your_username"
    password = "your_password"
    warehouse = "your_warehouse"
    database = "your_database"
    schema = "your_schema"
    ```
    
    ### Features
    
    - 📊 **Query Data**: Run custom SQL queries and download results
    - 📈 **Visualize**: Create interactive charts from your data
    - ℹ️ **Database Info**: View connection details and available tables
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Snowflake Data Explorer v1.0**")
st.sidebar.markdown("Built with ❤️ using Streamlit")
