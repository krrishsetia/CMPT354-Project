from db import get_db
from queries.division_q import robots_with_all_required_parts_q

DUMMY_RESULTS = [
    (1, "car", 3),
    (2, "arm", 3),
]


def division_query_data(required_part_ids):
    part_ids = [p.strip() for p in (required_part_ids or []) if str(p).strip()]
    if not part_ids:
        return [], None

    clean_ids = []
    for p in part_ids:
        if not p.isdigit():
            return [], "Part IDs must be numeric."
        clean_ids.append(int(p))

    conn = get_db()
    if not conn:
        return DUMMY_RESULTS, "Database connection failed. Showing demo division-query results."

    try:
        cursor = conn.cursor()
        rows = robots_with_all_required_parts_q(cursor, clean_ids)
        return rows, None
    except Exception as e:
        return [], str(e)
    finally:
        try:
            conn.close()
        except Exception:
            pass
