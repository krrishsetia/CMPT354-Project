from db import get_db
from queries.f7_q import (
    f7_team_info_for_robot,
    f7_team_members_for_robot,
)

def f7_team_for_robot_data(robot_id_raw=None):
    """
    Returns:
        robot_id: int or None
        robot: dict or None
        members: list[str]
        error: str or None
    """

    if robot_id_raw is None or str(robot_id_raw).strip() == "":
        return None, None, [], None

    robot_id_raw = str(robot_id_raw).strip()

    if not robot_id_raw.isdigit():
        return None, None, [], "Invalid RobotID."

    robot_id = int(robot_id_raw)

    conn = get_db()
    if conn is None:
        return robot_id, None, [], "Database connection failed."

    try:
        cursor = conn.cursor()

        team_row = f7_team_info_for_robot(cursor, robot_id)

        if not team_row:
            return robot_id, None, [], "No team found for that robot."

        member_rows = f7_team_members_for_robot(cursor, robot_id)

        robot = {
            "robot_id": team_row[0],
            "robot_name": team_row[1],
            "team_name": team_row[2],
            "manager_name": team_row[3] if team_row[3] is not None else "N/A",
        }

        members = [row[0] for row in member_rows]

        return robot_id, robot, members, None

    except Exception as e:
        return robot_id, None, [], f"Error: {e}"

    finally:
        try:
            conn.close()
        except Exception:
            pass