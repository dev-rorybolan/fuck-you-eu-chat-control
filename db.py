from sqlite3 import connect, Connection, Cursor
from attrs import define

@define
class Database:
    conn: Connection = connect('chatapp2.db', check_same_thread=False)
    cursor: Cursor = conn.cursor()
    def __attrs_post_init__(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            username TEXT NOT NULL,
            channel TEXT NOT NULL
            );
            """
        )
        self.conn.commit()
    def post_message(self, *, msg: str, username: str, channel: str) -> None:
        self.cursor.execute(
            "insert into messages (message, username, channel) values (?, ?, ?)",
            (msg, username, channel))
        self.conn.commit()
    def load_messages(self,*, channel: str) -> list[dict[str, str]]:
        self.cursor.execute("select username, message, channel from messages where channel=?", (channel,))
        data = self.cursor.fetchall()
        return [{"username": u, "text": t, "channel": c} for (u, t, c) in data]
