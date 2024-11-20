import os
import pandas as pd
import sqlite3


class DB:
    """Class LevelsDB works with the database"""

    def __init__(self, db_path: str) -> None:
        """Create a connection and a cursor to a database with a given path.
        If the database doesn't exist yet, create it."""
        self._conn = sqlite3.connect(db_path)
        self._cur = self._conn.cursor()
        self._create_table_texts()

    def _create_table_texts(self) -> None:
        """If the table Texts doesn't exist yet, create it.
        Fields:
        - id_text INTEGER PRIMARY KEY
        - text TEXT NOT NULL
        Texts are unique"""
        self._cur.execute(
            """CREATE TABLE IF NOT EXISTS Texts(
            id_text INTEGER PRIMARY KEY,
            text TEXT NOT NULL,
            UNIQUE(text) ON CONFLICT IGNORE
            )"""
        )
        self._conn.commit()

    def add_data(self, data: list[tuple[int, str]]) -> None:
        """Add data to the table Texts."""
        self._cur.executemany(
            """INSERT OR IGNORE INTO Texts(
            id_text, text
            ) VALUES(?,?)""",
            data,
        )
        self._conn.commit()

    def get_text_by_id(self, id_text: int) -> str:
        """Return text by its id."""
        self._cur.execute(
            f"""SELECT text
            FROM Texts
            WHERE id_text = '{id_text}'"""
        )
        return self._cur.fetchone()[0]

    def __del__(self) -> None:
        """Close the cursor and the connection to the database."""
        self._cur.close()
        self._conn.close()


folder = "data"
csv_path = os.path.join(folder, "data.csv")
db_path = os.path.join(folder, "texts.db")

df = pd.read_csv(csv_path)
data = list(zip(df.index, df["review"]))

db = DB(db_path)
db.add_data(data)
print(db.get_text_by_id(1))
