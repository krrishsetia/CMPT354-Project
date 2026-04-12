from db import get_db
from queries.f8_q import (
    f8_resolve_id,
    f8_get_robot_progress_history,
    f8_get_subassembly_info,
    f8_get_subassembly_history,
)

def f8_version_history_data(entity_type, identifier):


    identifier = (identifier or "").strip()
    entity_type = entity_type or "robot"

    if not identifier:
        return history, subassembly_info, error

    conn = get_db()
    if not conn:
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