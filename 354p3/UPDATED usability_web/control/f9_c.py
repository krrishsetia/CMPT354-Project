from flask import request
from db import get_db
from queries.f9_q import (
    f9_low_quantity_parts_q,
    f9_parts_by_type_with_count_q,
    f9_part_usage_q
)

def f9_parts_page_data():
    subtype = request.args.get("subtype")
    mech_type = request.args.get("mech_type")
    part_id = request.args.get("part_id")

    low_parts = []
    filtered_parts = []
    usage_rows = []
    error = None

    conn = get_db()
    if not conn:
        return subtype, mech_type, part_id, low_parts, filtered_parts, usage_rows, "Database connection failed."

    try:
        cursor = conn.cursor()

        low_parts = f9_low_quantity_parts_q(cursor)

        if subtype:
            filtered_parts = f9_parts_by_type_with_count_q(cursor, subtype, mech_type)

        if part_id:
            usage_rows = f9_part_usage_q(cursor, part_id)

    except Exception as e:
        error = str(e)

    finally:
        conn.close()

    return subtype, mech_type, part_id, low_parts, filtered_parts, usage_rows, error