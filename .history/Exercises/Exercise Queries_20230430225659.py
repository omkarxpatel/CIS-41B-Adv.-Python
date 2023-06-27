import sqlite3

 def QueryBuilder( Data_Base, Query_Type, Query_Tuple):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    q = ''

    if type == 'version':
        q = 'SELECT SQLITE_VERSION()'

    elif type == 'select_id':
        q = f'SELECT id FROM Database WHERE name="{tuple[0]}"'

    elif type == 'select_all':
        q = 'SELECT * FROM Database'

    elif type == 'delete':
        q = f'DELETE FROM Database WHERE id={tuple[0]}'

    elif type == 'insert':
        q = 'INSERT INTO Database (id, name, photo, html) VALUES (?, ?, ?, ?)'

        c.execute(q, tuple)
        connection.commit()
        connection.close()
        exit()
    
    elif type == 'create_table':
        q = '''CREATE TABLE Database (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            photo text NOT NULL UNIQUE,
            html text NOT NULL UNIQUE)'''

    connection.close()
    return q