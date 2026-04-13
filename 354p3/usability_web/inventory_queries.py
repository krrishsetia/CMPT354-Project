def f10_low_quantity_parts_q(cursor):
    cursor.execute("""
        SELECT PartID, PartName, Quantity
        FROM part
        WHERE Quantity < 3
        ORDER BY Quantity ASC, PartName
    """)
    return cursor.fetchall()


def f10_parts_by_type_with_count_q(cursor, subtype, mech_type):
    print("QUERY subtype =", subtype, "mech_type =", mech_type)

    if subtype == "electronic":
        cursor.execute("""
            SELECT p.PartID, p.PartName, p.Quantity
            FROM part p
            JOIN electronic e ON p.PartID = e.PartID
            ORDER BY p.PartName
        """)
        return cursor.fetchall()

    elif subtype == "mechanical":
        if mech_type == "wheel":
            cursor.execute("""
                SELECT p.PartID, p.PartName, p.Quantity
                FROM part p
                JOIN wheel w ON p.PartID = w.PartID
                ORDER BY p.PartName
            """)
            return cursor.fetchall()

        elif mech_type == "motor":
            cursor.execute("""
                SELECT p.PartID, p.PartName, p.Quantity
                FROM part p
                JOIN motor mo ON p.PartID = mo.PartID
                ORDER BY p.PartName
            """)
            return cursor.fetchall()

        elif mech_type == "suspension":
            cursor.execute("""
                SELECT p.PartID, p.PartName, p.Quantity
                FROM part p
                JOIN suspension s ON p.PartID = s.PartID
                ORDER BY p.PartName
            """)
            return cursor.fetchall()

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
            return cursor.fetchall()

    elif subtype == "structural":
        cursor.execute("""
            SELECT p.PartID, p.PartName, p.Quantity
            FROM part p
            JOIN structural st ON p.PartID = st.PartID
            ORDER BY p.PartName
        """)
        return cursor.fetchall()

    return []