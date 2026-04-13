def robots_with_all_required_parts_q(cursor, part_ids):
    placeholders = ", ".join(["%s"] * len(part_ids))
    sql = f"""
        SELECT r.RobotID, r.RobotName, COUNT(DISTINCT sap.PartID) AS matched_required_parts
        FROM robot r
        JOIN `sub-assembly` sa
          ON sa.RobotID = r.RobotID
        JOIN `sub-assembly-parts` sap
          ON sap.SATypeID = sa.SATypeID
        WHERE sap.PartID IN ({placeholders})
        GROUP BY r.RobotID, r.RobotName
        HAVING COUNT(DISTINCT sap.PartID) = %s
        ORDER BY r.RobotID
    """
    cursor.execute(sql, (*part_ids, len(set(part_ids))))
    return cursor.fetchall()
