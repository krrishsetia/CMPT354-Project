
def f9_low_quantity_parts_q(cursor):
    cursor.execute("""
        SELECT PartID, PartName, Quantity
        FROM part
        WHERE Quantity < 3
        ORDER BY Quantity ASC, PartName
    """)
    return cursor.fetchall()


def f9_parts_by_type_with_count_q(cursor, subtype, mech_type):
    print("QUERY subtype =", subtype, "mech_type =", mech_type)

    if subtype == "electronic":
        cursor.execute("""
            SELECT p.PartID, p.PartName, p.Quantity
            FROM part p
            JOIN electronic e ON p.PartID = e.PartID
            ORDER BY p.PartName
        """)
        rows = cursor.fetchall()
        print("electronic rows =", rows)
        return rows

    elif subtype == "mechanical":
        if mech_type == "wheel":
            cursor.execute("""
                SELECT p.PartID, p.PartName, p.Quantity
                FROM part p
                JOIN wheel w ON p.PartID = w.PartID
                ORDER BY p.PartName
            """)
            rows = cursor.fetchall()
            print("wheel rows =", rows)
            return rows

        elif mech_type == "motor":
            cursor.execute("""
                SELECT p.PartID, p.PartName, p.Quantity
                FROM part p
                JOIN motor mo ON p.PartID = mo.PartID
                ORDER BY p.PartName
            """)
            rows = cursor.fetchall()
            print("motor rows =", rows)
            return rows

        elif mech_type == "suspension":
            cursor.execute("""
                SELECT p.PartID, p.PartName, p.Quantity
                FROM part p
                JOIN suspension s ON p.PartID = s.PartID
                ORDER BY p.PartName
            """)
            rows = cursor.fetchall()
            print("suspension rows =", rows)
            return rows

        else:
            cursor.execute("""
                SELECT DISTINCT p.PartID, p.PartName, p.Quantity
                FROM part p
                LEFT JOIN mechanical m ON p.PartID = m.PartID
                LEFT JOIN wheel w ON p.PartID = w.PartID
                LEFT JOIN motor mo ON p.PartID = mo.PartID
                LEFT JOIN suspension s ON p.PartID = s.PartID
                WHERE m.PartID IS NOT NULL
                   OR w.PartID IS NOT NULL
                   OR mo.PartID IS NOT NULL
                   OR s.PartID IS NOT NULL
                ORDER BY p.PartName
            """)
            rows = cursor.fetchall()
            print("all mechanical rows =", rows)
            return rows

    elif subtype == "structural":
        cursor.execute("""
            SELECT p.PartID, p.PartName, p.Quantity
            FROM part p
            JOIN structural st ON p.PartID = st.PartID
            ORDER BY p.PartName
        """)
        rows = cursor.fetchall()
        print("structural rows =", rows)
        return rows

    print("no subtype matched")
    return []


def f9_part_usage_q(cursor, part_id):
    cursor.execute("""
        SELECT sa.SATypeID, sa.SAName
        FROM `sub-assembly` sa
        JOIN `sub-assembly-parts` sap
            ON sa.SATypeID = sap.SATypeID
        WHERE sap.PartID = %s
        ORDER BY sa.SATypeID
    """, (part_id,))
    return cursor.fetchall()