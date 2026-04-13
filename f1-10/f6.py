def f6_show_parts_by_type(cursor):
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
                SELECT p.PartID, p.PartName, e.MaxCurrentA, e.MaxVoltageV, e.CapacitymAh
                FROM part p
                JOIN electronic e ON p.PartID = e.PartID
            """)

            rows = cursor.fetchall()

            if not rows:
                print("No electronic parts found.")
            else:
                print(f"{'PartID':<8} {'PartName':<30} {'MaxCurrentA':<15} {'MaxVoltageV':<15} {'CapacitymAh':<15}")
                print("-" * 90)
                
                for row in rows:
                    capacity = row[4] if row[4] is not None else "N/A"
                    print(f"{row[0]:<8} {row[1]:<30} {row[2]:<15} {row[3]:<15} {str(row[4]):<15}")
                                            


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
                    SELECT DISTINCT p.PartID, p.PartName
                    FROM part p
                    LEFT JOIN mechanical m ON p.PartID = m.PartID
                    LEFT JOIN wheel w ON p.PartID = w.PartID
                    LEFT JOIN motor mo ON p.PartID = mo.PartID
                    LEFT JOIN suspension s ON p.PartID = s.PartID
                    WHERE m.PartID IS NOT NULL
                       OR w.PartID IS NOT NULL
                       OR mo.PartID IS NOT NULL
                       OR s.PartID IS NOT NULL
                    ORDER BY p.PartID
                """)

                rows = cursor.fetchall()

                if not rows:
                    print("No mechanical parts found.")
                else:
                    print(f"\nPartID\t PartName")
                    for row in rows:
                        print(f"{row[0]}\t {row[1]}")

            elif subchoice == "2":  # wheel
                cursor.execute("""
                    SELECT p.PartID, p.PartName, w.Radius, w.Type
                    FROM part p
                    JOIN wheel w ON p.PartID = w.PartID
                    ORDER BY p.PartID
                """)

                rows = cursor.fetchall()

                if not rows:
                    print("No wheel parts found.")
                else:
                    print(f"\nPartID\t PartName\t\t Radius\t Type")
                    for row in rows:
                        print(f"{row[0]}\t {row[1]}\t {row[2]}\t {row[3]}")

            elif subchoice == "3":  # motor
                cursor.execute("""
                    SELECT p.PartID, p.PartName, mo.Torque
                    FROM part p
                    JOIN motor mo ON p.PartID = mo.PartID
                    ORDER BY p.PartID
                """)

                rows = cursor.fetchall()

                if not rows:
                    print("No motor parts found.")
                else:
                    print(f"\nPartID\t PartName\t\t Torque")
                    for row in rows:
                        print(f"{row[0]}\t {row[1]}\t {row[2]}")

            elif subchoice == "4":  # suspension
                cursor.execute("""
                    SELECT p.PartID, p.PartName, s.WeightLimit
                    FROM part p
                    JOIN suspension s ON p.PartID = s.PartID
                    ORDER BY p.PartID
                """)

                rows = cursor.fetchall()

                if not rows:
                    print("No suspension parts found.")
                else:
                    print(f"\nPartID\t PartName\t\t Weight Limit")
                    for row in rows:
                        print(f"{row[0]}\t {row[1]}\t {row[2]}")
                            
                           
            else:
                print("Invalid mechanical choice.")
                return

        elif choice == "3":  # structural
            cursor.execute("""
                SELECT p.PartID, p.PartName, st.Material, st.Type
                FROM part p
                JOIN structural st ON p.PartID = st.PartID
                ORDER BY p.PartID
            """)

            rows = cursor.fetchall()

            if not rows:
                print("No structural parts found.")
            else:
                # header
                print(f"\n{'PartID':<8} {'PartName':<30} {'Material':<20} {'Type':<15}")
                print("-" * 75)

                for row in rows:
                    print(f"{row[0]:<8} {row[1]:<30} {str(row[2]):<20} {str(row[3]):<15}")

        else:
            print("Invalid choice.")
            return

    except Exception as e:
        print("Error:", e)