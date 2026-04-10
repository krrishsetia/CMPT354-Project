#assuming we change the unique constraint in the part table
#standard aggregation query
def f9_count_robots(cursor):
    cursor.execute("""
        SELECT COUNT(*) AS total_robots
        FROM robot
    """)

    row = cursor.fetchone()

    print(f"Total number of robots: {row[0]}")

#aggregation group-by
def f9_inventory_unused_parts_by_name(cursor):
    cursor.execute("""
        SELECT x.SubType, x.PartName, COUNT(*) AS count_unused
        FROM (
            SELECT 'electronic' AS SubType, p.PartName, p.PartID
            FROM part p
            JOIN electronic e ON p.PartID = e.PartID

            UNION ALL

            SELECT 'mechanical' AS SubType, p.PartName, p.PartID
            FROM part p
            JOIN mechanical m ON p.PartID = m.PartID

            UNION ALL

            SELECT 'wheel' AS SubType, p.PartName, p.PartID
            FROM part p
            JOIN wheel w ON p.PartID = w.PartID

            UNION ALL

            SELECT 'motor' AS SubType, p.PartName, p.PartID
            FROM part p
            JOIN motor mo ON p.PartID = mo.PartID

            UNION ALL

            SELECT 'suspension' AS SubType, p.PartName, p.PartID
            FROM part p
            JOIN suspension s ON p.PartID = s.PartID

            UNION ALL

            SELECT 'structural' AS SubType, p.PartName, p.PartID
            FROM part p
            JOIN structural st ON p.PartID = st.PartID
        ) x
        WHERE NOT EXISTS (
            SELECT 1
            FROM subassembly_parts sp
            WHERE sp.PartID = x.PartID
        )
        GROUP BY x.SubType, x.PartName
        ORDER BY x.SubType, count_unused DESC, x.PartName
    """)

    rows = cursor.fetchall()

    if not rows:
        print("All parts are currently in use.")
    else:
        print("\nUnused parts grouped by subtype:")
        current_subtype = None

        for row in rows:
            subtype = row[0]
            part_name = row[1]
            count = row[2]

            if subtype != current_subtype:
                current_subtype = subtype
                print(f"\n{subtype.upper()}:")
            print(f"{part_name}, Count: {count}")


def f9_show_parts_by_subtype_with_count(cursor):
    subtype = input("Enter subtype: ").strip()

    if not subtype:
        print("Invalid subtype.")
        return

    cursor.execute("""
        SELECT PartName, COUNT(*) AS part_count
        FROM part
        WHERE SpecType = ?
        GROUP BY PartName
        ORDER BY PartName
    """, (subtype,))

    rows = cursor.fetchall()

    if not rows:
        print(f"No parts found for subtype '{subtype}'.")
    else:
        print(f"\nParts in subtype '{subtype}':")
        for row in rows:
            print(f"Part Name: {row[0]}, Count: {row[1]}")


def f9_show_parts_by_type_with_count(cursor):
    print("""
    Show Parts by Type
    1. electronic
    2. mechanical
    3. structural
    0. back
    """)

    choice = input("Choose: ").strip()

    if choice == "0":
        return

    try:
        if choice == "1":  # electronic
            cursor.execute("""
                SELECT p.PartName, COUNT(*) AS part_count
                FROM part p
                JOIN electronic e ON p.PartID = e.PartID
                GROUP BY p.PartName
                ORDER BY p.PartName
            """)

            rows = cursor.fetchall()

            if not rows:
                print("No electronic parts found.")
            else:
                print(f"\n{'PartName':<30} {'Count':<10}")
                print("-" * 40)
                for row in rows:
                    print(f"{row[0]:<30} {row[1]:<10}")

        elif choice == "2":  # mechanical
            print("""
            Mechanical Parts
            1. all mechanical
            2. wheel
            3. motor
            4. suspension
            0. back
            """)

            subchoice = input("Choose: ").strip()

            if subchoice == "0":
                return

            elif subchoice == "1":
                cursor.execute("""
                    SELECT p.PartName, COUNT(*) AS part_count
                    FROM part p
                    LEFT JOIN mechanical m ON p.PartID = m.PartID
                    LEFT JOIN wheel w ON p.PartID = w.PartID
                    LEFT JOIN motor mo ON p.PartID = mo.PartID
                    LEFT JOIN suspension s ON p.PartID = s.PartID
                    WHERE m.PartID IS NOT NULL
                       OR w.PartID IS NOT NULL
                       OR mo.PartID IS NOT NULL
                       OR s.PartID IS NOT NULL
                    GROUP BY p.PartName
                    ORDER BY p.PartName
                """)

                rows = cursor.fetchall()

                if not rows:
                    print("No mechanical parts found.")
                else:
                    print(f"\n{'PartName':<30} {'Count':<10}")
                    print("-" * 40)
                    for row in rows:
                        print(f"{row[0]:<30} {row[1]:<10}")

            elif subchoice == "2":  # wheel
                cursor.execute("""
                    SELECT p.PartName, COUNT(*) AS part_count
                    FROM part p
                    JOIN wheel w ON p.PartID = w.PartID
                    GROUP BY p.PartName
                    ORDER BY p.PartName
                """)

                rows = cursor.fetchall()

                if not rows:
                    print("No wheel parts found.")
                else:
                    print(f"\n{'PartName':<30} {'Count':<10}")
                    print("-" * 40)
                    for row in rows:
                        print(f"{row[0]:<30} {row[1]:<10}")

            elif subchoice == "3":  # motor
                cursor.execute("""
                    SELECT p.PartName, COUNT(*) AS part_count
                    FROM part p
                    JOIN motor mo ON p.PartID = mo.PartID
                    GROUP BY p.PartName
                    ORDER BY p.PartName
                """)

                rows = cursor.fetchall()

                if not rows:
                    print("No motor parts found.")
                else:
                    print(f"\n{'PartName':<30} {'Count':<10}")
                    print("-" * 40)
                    for row in rows:
                        print(f"{row[0]:<30} {row[1]:<10}")

            elif subchoice == "4":  # suspension
                cursor.execute("""
                    SELECT p.PartName, COUNT(*) AS part_count
                    FROM part p
                    JOIN suspension s ON p.PartID = s.PartID
                    GROUP BY p.PartName
                    ORDER BY p.PartName
                """)

                rows = cursor.fetchall()

                if not rows:
                    print("No suspension parts found.")
                else:
                    print(f"\n{'PartName':<30} {'Count':<10}")
                    print("-" * 40)
                    for row in rows:
                        print(f"{row[0]:<30} {row[1]:<10}")

            else:
                print("Invalid mechanical choice.")
                return

        elif choice == "3":  # structural
            cursor.execute("""
                SELECT p.PartName, COUNT(*) AS part_count
                FROM part p
                JOIN structural st ON p.PartID = st.PartID
                GROUP BY p.PartName
                ORDER BY p.PartName
            """)

            rows = cursor.fetchall()

            if not rows:
                print("No structural parts found.")
            else:
                print(f"\n{'PartName':<30} {'Count':<10}")
                print("-" * 40)
                for row in rows:
                    print(f"{row[0]:<30} {row[1]:<10}")

        else:
            print("Invalid choice.")
            return

    except Exception as e:
        print("Error:", e)