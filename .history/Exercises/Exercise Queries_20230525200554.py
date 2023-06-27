def QueryBuilder(Data_Base, Query_Type, *Query_Tuple):
    q = ''

    if Query_Type == 'version':
        q = 'SELECT SQLITE_VERSION()'

    elif Query_Type == 'delete':
        q = f'DELETE FROM Database WHERE id={Query_Tuple[0]}'

    elif Query_Type == 'select':
        q = f'SELECT * FROM {Data_Base} WHERE {Query_Tuple[0]}'
    elif Query_Type == 'insert':
        q = f'INSERT INTO {Data_Base} (id, name, photo, html) VALUES \n({Query_Tuple})'

    elif Query_Type == 'table':
        q = f'CREATE TABLE {Data_Base}(\n{col})'

    else:
        raise ValueError(f"Invalid Query, {Query_Type} does not exist")

    return q