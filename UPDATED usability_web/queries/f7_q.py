def f7_resolve_robot_id(cursor, identifier):
    identifier = str(identifier).strip()

    if identifier.isdigit():
        cursor.execute("SELECT RobotID FROM robot WHERE RobotID = %s", (int(identifier),))
        row = cursor.fetchone()
        return row[0] if row else None

    cursor.execute("SELECT RobotID FROM robot WHERE RobotName = %s", (identifier,))
    rows = cursor.fetchall()

    if not rows:
        return None
    if len(rows) > 1:
        return "MULTIPLE"
    return rows[0][0]


def f7_team_info_for_robot(cursor, robot_id):
    cursor.execute("""
        SELECT
            r.RobotID,
            r.RobotName,
            t.TeamName,
            tm.ManagerName
        FROM robot r
        JOIN team t
            ON r.RobotID = t.RobotID
        LEFT JOIN teammanagers tm
            ON t.TeamName = tm.TeamName
           AND t.RobotID = tm.RobotID
        WHERE r.RobotID = %s
    """, (robot_id,))

    return cursor.fetchone()


def f7_team_members_for_robot(cursor, robot_id):
    cursor.execute("""
        SELECT Name
        FROM teammember
        WHERE RobotID = %s
        ORDER BY ID
    """, (robot_id,))

    return cursor.fetchall()
