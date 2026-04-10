def resolve_id(cursor, table, id_col, name_col, identifier, entity_name):
    if identifier.isdigit():
        cursor.execute(
            f"SELECT {id_col} FROM {table} WHERE {id_col} = ?",
            (int(identifier),)
        )
        row = cursor.fetchone()

        if not row:
            print(f"{entity_name} not found.")
            return None

        return row[0]

    cursor.execute(
        f"SELECT {id_col} FROM {table} WHERE {name_col} = ?",
        (identifier,)
    )
    rows = cursor.fetchall()

    if not rows:
        print(f"{entity_name} not found.")
        return None

    #
    if len(rows) > 1:
        print(f"Multiple matches found for {entity_name}. Please use ID.")
        return None

    return rows[0][0]


def f8_update_robot_version(cursor, conn):
    identifier = input("Enter RobotID or RobotName: ").strip()
    note = input("Enter change description: ").strip()

    robot_id = resolve_id(cursor, "robot", "RobotID", "RobotName", identifier, "Robot")
    if robot_id is None:
        return

    cursor.execute("""
        SELECT VersionNo
        FROM robot
        WHERE RobotID = ?
    """, (robot_id,))
    row = cursor.fetchone()

    if not row:
        print("Robot not found.")
        return

    current_version = row[0]
    new_version = current_version + 1

    cursor.execute("""
        UPDATE robot
        SET VersionNo = VersionNo + 1
        WHERE RobotID = ?
    """, (robot_id,))

    cursor.execute("""
        INSERT INTO robotversion (RobotID, VersionNo, Description)
        VALUES (?, ?, ?)
    """, (robot_id, new_version, note))

    conn.commit()
    print(f"Robot version updated to {new_version}.")

def f8_update_subassembly_version(cursor, conn):
    identifier = input("Enter SATypeID or SAName: ").strip()
    note = input("Enter change description: ").strip()

    sa_id = resolve_id(cursor, "subassembly", "SATypeID", "SAName", identifier, "sub-assembly")
    if sa_id is None:
        return

    cursor.execute("""
        SELECT VersionNo
        FROM subassembly
        WHERE SATypeID = ?
    """, (sa_id,))
    row = cursor.fetchone()

    if not row:
        print("Sub-assembly not found.")
        return

    current_version = row[0]
    new_version = current_version + 1

    cursor.execute("""
        UPDATE subassembly
        SET VersionNo = VersionNo + 1
        WHERE SATypeID = ?
    """, (sa_id,))

    cursor.execute("""
        INSERT INTO subassembly_version (SATypeID, VersionNo, Description)
        VALUES (?, ?, ?)
    """, (sa_id, new_version, note))

    conn.commit()
    print(f"Sub-assembly version updated to {new_version}.")

def f8_view_robot_history(cursor):
    identifier = input("Enter RobotID or RobotName: ").strip()

    robot_id = resolve_id(cursor, "robot", "RobotID", "RobotName", identifier, "Robot")
    if robot_id is None:
        return

    cursor.execute("""
        SELECT RobotID, VersionNo, Description
        FROM robotversion
        WHERE RobotID = ?
        ORDER BY VersionNo
    """, (robot_id,))

    rows = cursor.fetchall()

    if not rows:
        print("No history found for that robot.")
        return

    print(f"\nRobot {robot_id} Version History:")
    print(f"Version\t Note")
    for row in rows:
        print(f"{row[1]}\t {row[2]}")

def f8_view_subassembly_history(cursor):
    identifier = input("Enter SATypeID or SAName: ").strip()

    sa_id = resolve_id(cursor, "subassembly", "SATypeID", "SAName", identifier, "Sub-assembly")
    if sa_id is None:
        return

    cursor.execute("""
        SELECT SATypeID, VersionNo, Description
        FROM subassembly_version
        WHERE SATypeID = ?
        ORDER BY VersionNo
    """, (sa_id,))

    rows = cursor.fetchall()

    if not rows:
        print("No history found for that sub-assembly.")
        return

    print(f"\nSub-assembly {sa_id} Version History:")
    print(f"Version\t Note")
    for row in rows:
        print(f"{row[1]}\t {row[2]}")