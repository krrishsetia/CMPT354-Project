def load_f6_parts_by_type(conn, subtype, mech_type):
    try:
        cursor = conn.cursor()

        if subtype == "electronic":
            cursor.execute("""
                SELECT 
                    p.PartID,
                    p.PartName,
                    e.MaxCurrentA,
                    e.MaxVoltageV,
                    b.CapacitymAh
                FROM part p
                JOIN electronic e ON p.PartID = e.PartID
                LEFT JOIN battery b ON p.PartID = b.PartID
                ORDER BY p.PartID
            """)
            columns = [
                "PartID",
                "PartName",
                "MaxCurrentA",
                "MaxVoltageV",
                "CapacitymAh",
            ]

        elif subtype == "mechanical":
            if mech_type == "wheel":
                cursor.execute("""
                    SELECT p.PartID, p.PartName, w.Radius, w.Type
                    FROM part p
                    JOIN wheel w ON p.PartID = w.PartID
                    ORDER BY p.PartID
                """)
                columns = ["PartID", "PartName", "Radius", "Type"]

            elif mech_type == "motor":
                cursor.execute("""
                    SELECT p.PartID, p.PartName, mo.Torque
                    FROM part p
                    JOIN motor mo ON p.PartID = mo.PartID
                    ORDER BY p.PartID
                """)
                columns = ["PartID", "PartName", "Torque"]

            elif mech_type == "suspension":
                cursor.execute("""
                    SELECT p.PartID, p.PartName, s.WeightLimit
                    FROM part p
                    JOIN suspension s ON p.PartID = s.PartID
                    ORDER BY p.PartID
                """)
                columns = ["PartID", "PartName", "WeightLimit"]

            else:
                cursor.execute("""
                    SELECT DISTINCT p.PartID, p.PartName
                    FROM part p
                    LEFT JOIN mechanical m ON p.PartID = m.PartID
                    LEFT JOIN wheel w ON p.PartID = w.PartID
                    LEFT JOIN motor mo ON p.PartID = mo.PartID
                    LEFT JOIN suspension s ON p.PartID = s.PartID
                    WHERE m.PartID IS NOT NULL
                       OR w.PartID IS NOT NULL
                       OR mo.PartID IS NOT NULL
                       OR s.PartID IS NOT NULL
                    ORDER BY p.PartID
                """)
                columns = ["PartID", "PartName"]

        elif subtype == "structural":
            cursor.execute("""
                SELECT p.PartID, p.PartName
                FROM part p
                JOIN structural st ON p.PartID = st.PartID
                ORDER BY p.PartID
            """)
            columns = ["PartID", "PartName"]

        else:
            return []

        rows = cursor.fetchall()
        print("DB rows =", rows)
        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print("F6 error:", e)
        return []


def get_team_info_for_robot(cursor, robot_id):
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
        WHERE r.RobotID = ?
    """, (robot_id,))

    return cursor.fetchone()


def get_team_members_for_robot(cursor, robot_id):
    cursor.execute("""
        SELECT Name
        FROM teammember
        WHERE RobotID = ?
        ORDER BY ID
    """, (robot_id,))

    return cursor.fetchall()