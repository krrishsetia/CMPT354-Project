from flask import request
from db import get_db
from queries.f6_q import load_f6_parts_by_type

def f6_parts_by_type_data():
    subtype = request.args.get("subtype")
    mech_type = request.args.get("mech_type")

    conn = get_db()
    if not conn:
        return None, None, []

    parts = load_f6_parts_by_type(conn, subtype, mech_type)

    return subtype, mech_type, parts