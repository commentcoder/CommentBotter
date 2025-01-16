import sqlite3

def create_db():
    conn = sqlite3.connect('db/leveling.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        guild_id INTEGER,
        xp INTEGER DEFAULT 0,
        total_xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        last_message_time INTEGER DEFAULT 0
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invites (
        user_id INTEGER,
        guild_id INTEGER,
        last_invite_time INTEGER,
        invited_members TEXT,
        PRIMARY KEY (user_id, guild_id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    print("Base de données 'leveling.db' et les tables ont été créées avec succès.")
