def f10_inventory_alert(cursor):
    name = input("Enter part name: ").strip()
    threshold = input("Enter low stock threshold: ").strip()

    if not name:
        print("Invalid part name.")
        return

    if not threshold.isdigit():
        print("Invalid number.")
        return

    threshold = int(threshold)

    cursor.execute("""
        SELECT COUNT(*) AS unused_count
        FROM part p
        WHERE p.PartName LIKE ?
        AND NOT EXISTS (
            SELECT 1
            FROM subassembly_parts sp
            WHERE sp.PartID = p.PartID
        )
    """, (f"%{name}%",))

    row = cursor.fetchone()
    unused_count = row[0] if row else 0

    print(f"\nUnused count for '{name}': {unused_count}")

    if unused_count < threshold:
        print(" LOW STOCK: Consider ordering more.")
    else:
        print("Stock level is sufficient.")