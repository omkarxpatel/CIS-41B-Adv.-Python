import sqlite3
 
def QueryBuilder( Data_Base, Query_Type, Query_Tuple):
    connection = sqlite3.connect(Data_Base)
    c = connection.cursor()
    q = ''

    if Query_Type == 'version':
        q = 'SELECT SQLITE_VERSION()'

    elif Query_Type == 'select_id':
        q = f'SELECT id FROM Database WHERE name="{Query_Tuple[0]}"'

    elif Query_Type == 'select_all':
        q = 'SELECT * FROM Database'

    elif Query_Type == 'delete':
        q = f'DELETE FROM Database WHERE id={Query_Tuple[0]}'

    elif Query_Type == 'insert':
        q = 'INSERT INTO {0} (id, name, photo, html) VALUES ({1}, "{2}", "{3}", "{4}")'.format(
            Data_Base, Query_Tuple[0], Query_Tuple[1], Query_Tuple[2], Query_Tuple[3])

        c.execute(q, Query_Tuple)
        connection.commit()
        connection.close()
        exit()
    
    elif Query_Type == 'create_table':
        q = '''CREATE TABLE Database (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            photo text NOT NULL UNIQUE,
            html text NOT NULL UNIQUE)'''

    connection.close()
    return q