def f7_team_for_robot(cursor):
    robot_id = input("Enter RobotID: ").strip()

    if not robot_id.isdigit():
        print("Invalid RobotID.")
        return

    try:
        # Team + manager
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
        """, (int(robot_id),))

        row = cursor.fetchone()

        if not row:
            print("No team found for that robot.")
            return

        print(f"\nRobotID: {row[0]}")
        print(f"RobotName: {row[1]}")
        print(f"TeamName: {row[2]}")
        print(f"ManagerName: {row[3] if row[3] is not None else 'N/A'}")

        # Team members
        cursor.execute("""
            SELECT Name
            FROM teammember
            WHERE RobotID = ?
            ORDER BY ID
        """, (int(robot_id),))

        members = cursor.fetchall()

        if not members:
            print("TeamMembers: None")
        else:
            print("TeamMembers:")
            for member in members:
                print(f"\t{member[0]}")

        #should maybe allow an optiob 

    except Exception as e:
        print("Error:", e)