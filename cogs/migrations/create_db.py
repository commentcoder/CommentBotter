import libsql_experimental as libsql
import os
from dotenv import load_dotenv

load_dotenv()

WELCOME_CHANNEL_ID: str = os.getenv("WELCOME_CHANNEL_ID") or ""
TURBO_URL: str = os.getenv("TURBO_URL") or ""
TURBO_TOKEN: str = os.getenv("TURBO_TOKEN") or ""

def create_turbo_db():
    if not TURBO_URL or not TURBO_TOKEN:
        print("URL ou token manquants !")
        return

    print(f"Connexion à la base de données avec URL: {TURBO_URL} et Token: {TURBO_TOKEN}")
 
    try:
        conn = libsql.connect(database=TURBO_URL, auth_token=TURBO_TOKEN)
        cursor = conn.cursor()

        # Créer la table des utilisateurs
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

        # Créer la table des invitations
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invites (
            user_id INTEGER,
            guild_id INTEGER,
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
#     create_turbo_db()
#     print("Base de données 'leveling.db' et les tables ont été créées avec succès.")
