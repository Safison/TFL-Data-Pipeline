from connection import connect_to_db, close_db_connection

def seed():
    conn = connect_to_db()
    print("seed start")
    try:
        conn.run(
            "DROP TABLE IF EXISTS fact_line_status;"
        )
        conn.run(
            "DROP TABLE IF EXISTS dim_time;"
        )
        conn.run(
            "DROP TABLE IF EXISTS dim_line;"
        )
        
        conn.run(
            "CREATE TABLE dim_line (\
                line_id VARCHAR PRIMARY KEY,\
                line_name VARCHAR,\
                line_mode VARCHAR\
                );"
                )
        
        conn.run(
            "CREATE TABLE dim_time (\
                time_id VARCHAR PRIMARY KEY,\
                date DATE,\
                hour INT,\
                day_of_week VARCHAR\
                );"
                )
        conn.run(
            "CREATE TABLE fact_line_status (\
                status_id SERIAL PRIMARY KEY,\
                line_id VARCHAR REFERENCES dim_line(line_id),\
                time_id VARCHAR REFERENCES dim_time(time_id),\
                status_severity INT,\
                status_severity_description VARCHAR,\
                reason VARCHAR\
                );"
                )
    finally:
        print("Seeding Complete.")
        close_db_connection(conn)    

seed()