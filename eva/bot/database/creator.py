import sqlite3

# conectando...
conn = sqlite3.connect('eva.db')

# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE users (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        access_token VARCHAR(255) NOT NULL,
        telegram_id VARCHAR(255) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE registerstep (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        step INTEGER NOT NULL,
        telegram_id VARCHAR(255) NOT NULL
);
""")


cursor.execute("""
CREATE TABLE trials (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        telegram_id VARCHAR(255) NOT NULL,
        trials INTEGER NOT NULL,
        blocked timestamp
);
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()
