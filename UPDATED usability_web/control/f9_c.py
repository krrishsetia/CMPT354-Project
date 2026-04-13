from flask import request
from db import get_db
from queries.f9_q import (
    f9_low_quantity_parts_q,
    f9_parts_by_type_with_count_q,
    f9_part_usage_q,
    f9_parts_grouped_by_category_q,
)

DUMMY_LOW_PARTS = [
    (101, "Gyro Sensor", 1),
    (211, "Motor Housing", 2),
]
DUMMY_FILTERED = {
    "electronic": [(101, "Gyro Sensor", 1), (118, "Range Finder", 4)],
    "mechanical": [(205, "All-terrain wheel", 6), (211, "Motor Housing", 2)],
    "structural": [(301, "Frame Plate", 7), (302, "Support Beam", 3)],
}
DUMMY_USAGE = {
    "101": [(220, "Wheel Control Unit"), (140, "Navigation Hub")],
    "211": [],
}


def f9_parts_page_data():
    subtype = request.args.get("subtype")
    mech_type = request.args.get("mech_type")
    part_id = request.args.get("part_id")

    low_parts = []
    filtered_parts = []
    usage_rows = []
    grouped_rows = []
    error = None

    conn = get_db()
    if not conn:
        low_parts = DUMMY_LOW_PARTS
        if subtype:
            filtered_parts = DUMMY_FILTERED.get(subtype, [])
        if part_id:
            usage_rows = DUMMY_USAGE.get(str(part_id), [])
        return subtype, mech_type, part_id, low_parts, filtered_parts, usage_rows, grouped_rows, "Database connection failed. Showing demo data."

    try:
        cursor = conn.cursor()

        low_parts = f9_low_quantity_parts_q(cursor)
        grouped_rows = f9_parts_grouped_by_category_q(cursor)

        if subtype:
            filtered_parts = f9_parts_by_type_with_count_q(cursor, subtype, mech_type)

        if part_id:
            usage_rows = f9_part_usage_q(cursor, part_id)

    except Exception as e:
        error = str(e)

    finally:
        conn.close()

    return subtype, mech_type, part_id, low_parts, filtered_parts, usage_rows, grouped_rows, error
