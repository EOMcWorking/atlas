from src.services.database_service import (
    get_connection
)


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workflow_metrics (
            id INTEGER PRIMARY KEY,
            task TEXT,
            success INTEGER,
            duration REAL,
            timestamp REAL
        )
        """
    )

    conn.commit()

    conn.close()