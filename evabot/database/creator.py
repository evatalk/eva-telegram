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

print('Tabela criada com sucesso.')
# desconectando...
conn.close()
