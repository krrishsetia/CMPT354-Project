from db import get_db
from queries.f7_q import (
    f7_resolve_robot_id,
    f7_team_info_for_robot,
    f7_team_members_for_robot,
)

DUMMY_LOOKUPS = {
    "1": {
        "robot": {"robot_id": 1, "robot_name": "car", "team_name": "CarTeam", "manager_name": "Brendan"},
        "members": ["Alex Carter", "Sam Lee", "Priya Nair"],
    },
    "car": {
        "robot": {"robot_id": 1, "robot_name": "car", "team_name": "CarTeam", "manager_name": "Brendan"},
        "members": ["Alex Carter", "Sam Lee", "Priya Nair"],
    },
    "2": {
        "robot": {"robot_id": 2, "robot_name": "arm", "team_name": "ArmTeam", "manager_name": "Godwin"},
        "members": ["Ava Patel", "Jae Kim", "Leo Foster"],
    },
    "arm": {
        "robot": {"robot_id": 2, "robot_name": "arm", "team_name": "ArmTeam", "manager_name": "Godwin"},
        "members": ["Ava Patel", "Jae Kim", "Leo Foster"],
    },
}


def f7_team_for_robot_data(identifier_raw=None):
    if identifier_raw is None or str(identifier_raw).strip() == "":
        return None, None, [], None

    identifier = str(identifier_raw).strip()

    conn = get_db()
    if conn is None:
        dummy = DUMMY_LOOKUPS.get(identifier.lower())
        if dummy:
            robot = dummy["robot"]
            return robot["robot_id"], robot, dummy["members"], None
        return identifier, None, [], "Database connection failed. Showing demo mode only."

    try:
        cursor = conn.cursor()
        robot_id = f7_resolve_robot_id(cursor, identifier)

        if robot_id is None:
            return identifier, None, [], "Robot not found."
        if robot_id == "MULTIPLE":
            return identifier, None, [], "Multiple robots found. Please use RobotID."

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
        return identifier, None, [], f"Error: {e}"

    finally:
        try:
            conn.close()
        except Exception:
            pass
