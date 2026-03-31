from sqlalchemy import create_engine, text
import json

class MySQLSaver:
    def __init__(self, db_url):
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
            result = conn.execute(
                text("""
                    SELECT state FROM langgraph_checkpoints
                    WHERE thread_id = :thread_id
                    ORDER BY id DESC
                    LIMIT 1
                """),
                {"thread_id": thread_id}
            ).fetchone()

            if result:
                return json.loads(result[0])
            return None