import libsql_experimental as libsql
import os
from dotenv import load_dotenv

load_dotenv()

WELCOME_CHANNEL_ID: str = os.getenv("WELCOME_CHANNEL_ID") or ""
TURSO_URL: str = os.getenv("TURSO_URL") or ""
TURSO_TOKEN: str = os.getenv("TURSO_TOKEN") or ""

def create_turso_db():
    if not TURSO_URL or not TURSO_TOKEN:
        print("URL ou token manquants !")
        return

    print(f"Connexion à la base de données avec URL: {TURSO_URL} et Token: {TURSO_TOKEN}")
 
    try:
        conn = libsql.connect(database=TURSO_URL, auth_token=TURSO_TOKEN)
        cursor = conn.cursor()

        # Créer la table des utilisateurs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            guild_id TEXT,
            xp INTEGER DEFAULT 0,
            total_xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            last_message_time INTEGER DEFAULT 0
        );
        """)

        # Créer la table des invitations
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invites (
            user_id TEXT,
            guild_id TEXT,
            last_invite_time INTEGER,
            invited_members TEXT,
            PRIMARY KEY (user_id, guild_id)
        );
        """)

        # Optionnel: Vérifier la création des tables
        cursor.execute("PRAGMA table_info(users);")
        result = cursor.fetchall()
        print("Tables après création:", result)

        # Fermer la connexion à la base de données
        conn.commit()
        conn.close()
        print("Base de données créée et fermée avec succès.")

    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données ou de l'exécution des requêtes: {e}")


# def create_local_db():
#     conn = sqlite3.connect('db/leveling.db')
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         user_id INTEGER PRIMARY KEY,
#         guild_id INTEGER,
#         xp INTEGER DEFAULT 0,
#         total_xp INTEGER DEFAULT 0,
#         level INTEGER DEFAULT 1,
#         last_message_time INTEGER DEFAULT 0
#     );
#     """)

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS invites (
#         user_id INTEGER,
#         guild_id INTEGER,
#         last_invite_time INTEGER,
#         invited_members TEXT,
#         PRIMARY KEY (user_id, guild_id)
#     )
#     """)

#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     create_turso_db()
#     print("Base de données 'leveling.db' et les tables ont été créées avec succès.")
