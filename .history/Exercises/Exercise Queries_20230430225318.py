import sqlite3

def QueryBuilder(db, type, l):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    q = ''

    if type == 'version':
        q = 'SELECT SQLITE_VERSION()'

    elif type == 'select_id':
        q = f'SELECT id FROM Database WHERE name="{Query_Tuple[0]}"'

    elif type == 'select_all':
        q = 'SELECT * FROM Database'

    elif type == 'delete':
        q = f'DELETE FROM Database WHERE id={Query_Tuple[0]}'

    elif type == 'insert':
        q = 'INSERT INTO Database (id, name, photo, html) VALUES (?, ?, ?, ?)'

        c.execute(q, Query_Tuple)
        connection.commit()
        connection.close()
        return 0
    
    elif type == 'create_table':
        q = '''CREATE TABLE Database (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                photo text NOT NULL UNIQUE,
                                html text NOT NULL UNIQUE
                                )'''

    connection.close()
    return q