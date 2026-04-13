from db import get_db


def get_all_robots_for_delete():
    conn = get_db()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT RobotID, RobotName FROM robot ORDER BY RobotID")
    rows = cursor.fetchall()
    conn.close()
    return rows


def preview_robot_delete(robot_id_raw):
    if not str(robot_id_raw).strip().isdigit():
        return None, "invalid id"

    robot_id = int(robot_id_raw)
    conn = get_db()
    if not conn:
        return None, "Database connection failed."

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT RobotID, RobotName FROM robot WHERE RobotID = %s", (robot_id,))
        row = cursor.fetchone()
        if not row:
            return None, "Robot not found."

        cursor.execute("SELECT TeamName FROM team WHERE RobotID = %s", (robot_id,))
        teams = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT ID, Name FROM teammember WHERE RobotID = %s", (robot_id,))
        members = cursor.fetchall()

        cursor.execute("SELECT SATypeID, SAName, `Version` FROM `sub-assembly` WHERE RobotID = %s", (robot_id,))
        subs = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) FROM progressupdates pu
            JOIN teammember tm ON pu.ID = tm.ID
            WHERE tm.RobotID = %s
        """, (robot_id,))
        prog_count = cursor.fetchone()[0]

        print("preview robot_id =", robot_id, "teams =", teams, "members =", members)

        preview = {
            "robot_id": row[0],
            "robot_name": row[1],
            "teams": teams,
            "members": members,
            "sub_assemblies": subs,
            "progress_count": prog_count,
        }
        return preview, None

    except Exception as e:
        print("preview error:", e)
        return None, str(e)
    finally:
        conn.close()


def perform_delete_robot(robot_id_raw):
    if not str(robot_id_raw).strip().isdigit():
        return None, None, "invalid id"

    robot_id = int(robot_id_raw)

    conn = get_db()
    if not conn:
        return None, None, "Database connection failed."

    deleted_name = None
    audit_row = None

    cursor = conn.cursor()

    cursor.execute("SELECT RobotName FROM robot WHERE RobotID = %s", (robot_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None, None, "Robot not found."
    deleted_name = row[0]

    try:
        cursor.execute("DELETE FROM robot WHERE RobotID = %s", (robot_id,))
        conn.commit()
        print("deleted robot", robot_id, deleted_name)
    except Exception as e:
        print("delete error:", e)
        conn.close()
        return deleted_name, None, str(e)

    try:
        cursor.execute("""
            SELECT AuditID, RobotID, RobotName, DeletedAt
            FROM robotdeleteaudit
            WHERE RobotID = %s
            ORDER BY AuditID DESC LIMIT 1
        """, (robot_id,))
        audit = cursor.fetchone()
        if audit:
            audit_row = {
                "audit_id": audit[0],
                "robot_id": audit[1],
                "robot_name": audit[2],
                "deleted_at": audit[3],
            }
            print("audit row =", audit_row)
    except Exception as e:
        print("audit fetch error:", e)

    conn.close()
    return deleted_name, audit_row, None
