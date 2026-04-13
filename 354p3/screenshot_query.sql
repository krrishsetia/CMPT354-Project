SELECT 
    p.PartID,
    p.PartName,
    CASE
        WHEN s.PartID IS NOT NULL THEN 'Structural'
        WHEN e.PartID IS NOT NULL THEN 'Electronic'
        WHEN m.PartID IS NOT NULL THEN 'Mechanical'
        ELSE 'Unclassified'
    END AS PartCategory,
    COUNT(sap.SATypeID) AS UsedInSubAssemblies
FROM Part p
LEFT JOIN Structural s ON p.PartID = s.PartID
LEFT JOIN Electronic e ON p.PartID = e.PartID
LEFT JOIN Mechanical m ON p.PartID = m.PartID
LEFT JOIN `Sub-Assembly-Parts` sap ON p.PartID = sap.PartID
GROUP BY p.PartID, p.PartName,
         s.PartID, e.PartID, m.PartID
ORDER BY UsedInSubAssemblies DESC, p.PartID;
