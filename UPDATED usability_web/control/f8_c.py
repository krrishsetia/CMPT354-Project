from db import get_db
from queries.f8_q import (
    f8_resolve_id,
    f8_get_robot_progress_history,
    f8_get_subassembly_info,
    f8_get_subassembly_history,
)

DUMMY_ROBOT_HISTORY = [
    (2, "2026-04-01", "Arm calibration update", "arm-update-1.png"),
    (2, "2026-03-21", "Joint alignment completed", None),
]

DUMMY_SUB_INFO = (220, "Wheel Control Unit", 4, "Drive System", 2)
DUMMY_SUB_HISTORY = [
    (220, 4, "Added wheel sensor", "2026-04-05"),
    (220, 3, "Refined control routing", "2026-03-28"),
]


def f8_version_history_data(entity_type, identifier):
    history = []
    subassembly_info = None
    error = None

    identifier = (identifier or "").strip()
    entity_type = entity_type or "robot"

    if not identifier:
        return history, subassembly_info, error

    conn = get_db()
    if not conn:
        if entity_type == "robot":
            return DUMMY_ROBOT_HISTORY, None, "Database connection failed. Showing demo history."
        if entity_type == "subassembly":
            return DUMMY_SUB_HISTORY, DUMMY_SUB_INFO, "Database connection failed. Showing demo history."
        return history, subassembly_info, "Database connection failed."

    cursor = conn.cursor()

    try:
        if entity_type == "robot":
            robot_id = f8_resolve_id(
                cursor,
                "robot",
                "RobotID",
                "RobotName",
                identifier
            )

            if robot_id is None:
                error = "Robot not found."
            elif robot_id == "MULTIPLE":
                error = "Multiple robots found. Please use RobotID."
            else:
                history = f8_get_robot_progress_history(cursor, robot_id)

        elif entity_type == "subassembly":
            sa_id = f8_resolve_id(
                cursor,
                "`sub-assembly`",
                "SATypeID",
                "SAName",
                identifier
            )

            if sa_id is None:
                error = "Sub-assembly not found."
            elif sa_id == "MULTIPLE":
                error = "Multiple sub-assemblies found. Please use SATypeID."
            else:
                subassembly_info = f8_get_subassembly_info(cursor, sa_id)
                history = f8_get_subassembly_history(cursor, sa_id)

        else:
            error = "Invalid selection."

    except Exception as e:
        error = str(e)

    finally:
        cursor.close()
        conn.close()

    return history, subassembly_info, error
