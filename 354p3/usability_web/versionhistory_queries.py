def f8_resolve_id(cursor, table, id_col, name_col, identifier):
    identifier = str(identifier).strip()

    if identifier.isdigit():
        cursor.execute(
            f"SELECT {id_col} FROM {table} WHERE {id_col} = ?",
            (int(identifier),)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    cursor.execute(
        f"SELECT {id_col} FROM {table} WHERE {name_col} = ?",
        (identifier,)
    )
    rows = cursor.fetchall()

    if not rows:
        return None

    if len(rows) > 1:
        return "MULTIPLE"

    return rows[0][0]


def f8_get_robot_progress_history(cursor, robot_id):
    cursor.execute("""
        SELECT ID, `Date`, Description, Picture
        FROM progressupdates
        WHERE ID = ?
        ORDER BY `Date` DESC
    """, (robot_id,))
    return cursor.fetchall()


def f8_get_subassembly_info(cursor, sa_id):
    cursor.execute("""
        SELECT SATypeID, SAName, Version, SAClassification, RobotID
        FROM `Sub-Assembly`
        WHERE SATypeID = ?
    """, (sa_id,))
    return cursor.fetchone()


def f8_get_subassembly_history(cursor, sa_id):
    cursor.execute("""
        SELECT SATypeID, Version, Description
        FROM `sub-assembly-version`
        WHERE SATypeID = ?
        ORDER BY Version DESC
    """, (sa_id,))
    return cursor.fetchall()