import os
from sqlalchemy import create_engine, text
import json
from dotenv import load_dotenv

load_dotenv()

class DBSaver:
    def __init__(self):
        self.db_type = os.getenv("DB_TYPE")
        db_url = os.getenv("DATABASE_URL")
        self.engine = create_engine(db_url)

    def save(self, thread_id, state):
        with self.engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO langgraph_checkpoints (thread_id, state)
                    VALUES (:thread_id, :state)
                """),
                {
                    "thread_id": thread_id,
                    "state": json.dumps(state, default=str)
                }
            )
            conn.commit()

    def load(self, thread_id):
        with self.engine.connect() as conn:

            if self.db_type == "mysql":
                query = """
                    SELECT state FROM langgraph_checkpoints
                    WHERE thread_id = :thread_id
                    ORDER BY id DESC
                    LIMIT 1
                """
            else:  # Azure SQL
                query = """
                    SELECT TOP 1 state FROM langgraph_checkpoints
                    WHERE thread_id = :thread_id
                    ORDER BY id DESC
                """

            result = conn.execute(
                text(query),
                {"thread_id": thread_id}
            ).fetchone()

            if result:
                return json.loads(result[0])
            return None