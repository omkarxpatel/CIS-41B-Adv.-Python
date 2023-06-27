def QueryBuilder(Data_Base, Query_Type, Query_Tuple):
    q = ''

    if Query_Type == 'version':
        q = 'SELECT SQLITE_VERSION()'

    elif Query_Type == 'delete':
        q = f'DELETE FROM Database WHERE id={Query_Tuple[0]}'

    elif Query_Type == 'select':
        q = f'SELECT * FROM {Data_Base}'
    elif Query_Type == 'insert':
        q = f'INSERT INTO {Data_Base} (id, name, photo, html) VALUES \n({Query_Tuple[0]}, {Query_Tuple[1]}, {Query_Tuple[2]}, {Query_Tuple[3]})'

    elif Query_Type == 'create_table':
        q = '''CREATE TABLE Database (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            photo text NOT NULL UNIQUE,
            html text NOT NULL UNIQUE)'''

    else:
        raise ValueError(f"Invalid Query, {Query_Type} does not exist")

    return q