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