def f8_resolve_id(cursor, table, id_col, name_col, identifier):
    identifier = str(identifier).strip()

    if identifier.isdigit():
        cursor.execute(
            f"SELECT {id_col} FROM {table} WHERE {id_col} = %s",
            (int(identifier),)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    cursor.execute(
        f"SELECT {id_col} FROM {table} WHERE {name_col} = %s",
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
        SELECT tm.RobotID, pu.`Date`, pu.Description, pu.Picture
        FROM progressupdates pu
        JOIN teammember tm
          ON pu.ID = tm.ID
        WHERE tm.RobotID = %s
        ORDER BY pu.`Date` DESC
    """, (robot_id,))
    return cursor.fetchall()


def f8_get_subassembly_info(cursor, sa_id):
    cursor.execute("""
        SELECT SATypeID, SAName, Version, SAClassification, RobotID
        FROM `sub-assembly`
        WHERE SATypeID = %s
    """, (sa_id,))
    return cursor.fetchone()


def f8_get_subassembly_history(cursor, sa_id):
    cursor.execute("SHOW COLUMNS FROM `sub-assembly-version` LIKE 'ChangeDate'")
    has_change_date = cursor.fetchone() is not None

    if has_change_date:
        cursor.execute("""
            SELECT SATypeID, Version, Description, ChangeDate
            FROM `sub-assembly-version`
            WHERE SATypeID = %s
            ORDER BY Version DESC
        """, (sa_id,))
    else:
        cursor.execute("""
            SELECT SATypeID, Version, Description, NULL AS ChangeDate
            FROM `sub-assembly-version`
            WHERE SATypeID = %s
            ORDER BY Version DESC
        """, (sa_id,))
    return cursor.fetchall()
