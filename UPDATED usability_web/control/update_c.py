from db import get_db


def get_all_robots_for_update():
    conn = get_db()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT RobotID, RobotName FROM robot ORDER BY RobotID")
    rows = cursor.fetchall()
    conn.close()
    return rows


def perform_update_robot_name(robot_id_raw, new_name):
    new_name = (new_name or "").strip()

    if not str(robot_id_raw).strip().isdigit():
        return None, new_name, "invalid robot id"

    if not new_name:
        return None, new_name, "name cannot be empty"

    robot_id = int(robot_id_raw)

    conn = get_db()
    if not conn:
        return None, new_name, "Database connection failed."

    old_name = None

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT RobotName FROM robot WHERE RobotID = %s", (robot_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None, new_name, "Robot not found."
        old_name = row[0]

        print("updating robot", robot_id, "from", old_name, "to", new_name)

        cursor.execute(
            "UPDATE robot SET RobotName = %s WHERE RobotID = %s",
            (new_name, robot_id)
        )
        conn.commit()
        conn.close()
        return old_name, new_name, None

    except Exception as e:
        print("update error:", e)
        conn.close()
        return old_name, new_name, str(e)
