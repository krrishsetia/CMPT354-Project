# Database Normalization Notes

## Functional Dependencies

The following functional dependencies are based on the schema defined in the SQL setup files for this project. The meanings are described in plain English.

### 1. Robot
**Relation:** `Robot(RobotID, RobotName)`

Functional dependencies:
- `RobotID -> RobotName`
- `RobotName -> RobotID`

Meaning in English:
- A robot ID uniquely determines the robot name.
- A robot name is unique in this system, so it also uniquely determines the robot ID.

### 2. Team
**Relation:** `Team(TeamName, RobotID)`

Functional dependency:
- `(RobotID, TeamName) -> all attributes in Team`

Meaning in English:
- The combination of robot ID and team name uniquely identifies a team record.

### 3. TeamManagers
**Relation:** `TeamManagers(ManagerName, TeamName, RobotID)`

Functional dependency:
- `(RobotID, TeamName, ManagerName) -> all attributes in TeamManagers`

Meaning in English:
- A manager record is uniquely identified by the robot, the team, and the manager name.

### 4. TeamMember
**Relation:** `TeamMember(ID, Name, TeamName, RobotID)`

Functional dependency:
- `ID -> Name, TeamName, RobotID`

Meaning in English:
- Each team member ID uniquely identifies the member's name and the team/robot they belong to.

### 5. ProgressUpdates
**Relation:** `ProgressUpdates(ID, Date, Description, Picture)`

Functional dependency:
- `(ID, Date) -> Description, Picture`

Meaning in English:
- For a given team member on a given date, there is one specific progress update record with one description and one picture.

### 6. Sub-Assembly
**Relation:** ``Sub-Assembly(SATypeID, SAName, Version, SAClassification, RobotID)``

Functional dependencies:
- `SATypeID -> SAName, Version, SAClassification, RobotID`
- `(SAName, Version) -> SATypeID, SAClassification, RobotID`

Meaning in English:
- Each sub-assembly ID uniquely determines its name, version, classification, and owning robot.
- The combination of sub-assembly name and version is also unique, so it identifies the corresponding sub-assembly record.

### 7. Part
**Relation:** `Part(PartID, PartName, Weight, Height, Length, Width, Quantity)`

Functional dependencies:
- `PartID -> PartName, Weight, Height, Length, Width, Quantity`
- `PartName -> PartID, Weight, Height, Length, Width, Quantity`

Meaning in English:
- Each part ID uniquely determines all stored information about that part.
- Part names are unique, so the part name also uniquely determines the part record.

### 8. Structural
**Relation:** `Structural(PartID, Material, Type)`

Functional dependency:
- `PartID -> Material, Type`

Meaning in English:
- Each structural part ID uniquely determines the material and structural type of that part.

### 9. Electronic
**Relation:** `Electronic(PartID, MaxCurrentA, MaxVoltageV)`

Functional dependency:
- `PartID -> MaxCurrentA, MaxVoltageV`

Meaning in English:
- Each electronic part ID uniquely determines its maximum current and maximum voltage.

### 10. Battery
**Relation:** `Battery(PartID, CapacitymAh)`

Functional dependency:
- `PartID -> CapacitymAh`

Meaning in English:
- Each battery part ID uniquely determines its capacity.

### 11. Mechanical
**Relation:** `Mechanical(PartID)`

Functional dependency:
- `PartID -> all attributes in Mechanical`

Meaning in English:
- Mechanical is a subtype relation, so the part ID alone identifies the record.

### 12. Wheel
**Relation:** `Wheel(PartID, Radius, Type)`

Functional dependency:
- `PartID -> Radius, Type`

Meaning in English:
- Each wheel part ID uniquely determines its radius and wheel type.

### 13. Motor
**Relation:** `Motor(PartID, Torque)`

Functional dependency:
- `PartID -> Torque`

Meaning in English:
- Each motor part ID uniquely determines its torque.

### 14. Suspension
**Relation:** `Suspension(PartID, WeightLimit)`

Functional dependency:
- `PartID -> WeightLimit`

Meaning in English:
- Each suspension part ID uniquely determines its weight limit.

### 15. Sub-Assembly-Parts
**Relation:** ``Sub-Assembly-Parts(SATypeID, PartID)``

Functional dependency:
- `(SATypeID, PartID) -> all attributes in Sub-Assembly-Parts`

Meaning in English:
- A row is uniquely identified by the combination of one sub-assembly and one part.

### 16. Sub-Assembly-Hierarchy
**Relation:** ``Sub-Assembly-Hierarchy(ParentSATypeID, ChildPartID)``

Functional dependency:
- `(ParentSATypeID, ChildPartID) -> all attributes in Sub-Assembly-Hierarchy`

Meaning in English:
- A hierarchy link is uniquely identified by the parent sub-assembly and child sub-assembly pair.

### 17. RobotDeleteAudit
**Relation:** `RobotDeleteAudit(AuditID, RobotID, RobotName, DeletedAt)`

Functional dependency:
- `AuditID -> RobotID, RobotName, DeletedAt`

Meaning in English:
- Each audit record ID uniquely determines the deleted robot information and deletion timestamp.

---

## Normalized Schema in 3NF / BCNF

This project separates major entities and subtype-specific attributes into different relations. This reduces redundancy and avoids update anomalies. Generic part attributes are stored in `Part`, while subtype-specific attributes are stored in their own relations such as `Structural`, `Electronic`, `Battery`, `Mechanical`, `Wheel`, `Motor`, and `Suspension`.

Most relations satisfy **BCNF** because every non-trivial functional dependency has a determinant that is a candidate key. At minimum, the schema satisfies **3NF**.

### Tables, Primary Keys, and Foreign Keys

#### Robot
- **Primary Key:** `RobotID`
- **Candidate Key:** `RobotName`

#### Team
- **Primary Key:** `(RobotID, TeamName)`
- **Foreign Key:** `RobotID -> Robot(RobotID)`

#### TeamManagers
- **Primary Key:** `(RobotID, TeamName, ManagerName)`
- **Foreign Key:** `(RobotID, TeamName) -> Team(RobotID, TeamName)`

#### TeamMember
- **Primary Key:** `ID`
- **Foreign Key:** `(RobotID, TeamName) -> Team(RobotID, TeamName)`

#### ProgressUpdates
- **Primary Key:** `(ID, Date)`
- **Foreign Key:** `ID -> TeamMember(ID)`

#### Sub-Assembly
- **Primary Key:** `SATypeID`
- **Candidate Key:** `(SAName, Version)`
- **Foreign Key:** `RobotID -> Robot(RobotID)`

#### Part
- **Primary Key:** `PartID`
- **Candidate Key:** `PartName`

#### Structural
- **Primary Key:** `PartID`
- **Foreign Key:** `PartID -> Part(PartID)`

#### Electronic
- **Primary Key:** `PartID`
- **Foreign Key:** `PartID -> Part(PartID)`

#### Battery
- **Primary Key:** `PartID`
- **Foreign Key:** `PartID -> Electronic(PartID)`

#### Mechanical
- **Primary Key:** `PartID`
- **Foreign Key:** `PartID -> Part(PartID)`

#### Wheel
- **Primary Key:** `PartID`
- **Foreign Key:** `PartID -> Mechanical(PartID)`

#### Motor
- **Primary Key:** `PartID`
- **Foreign Key:** `PartID -> Mechanical(PartID)`

#### Suspension
- **Primary Key:** `PartID`
- **Foreign Key:** `PartID -> Mechanical(PartID)`

#### Sub-Assembly-Parts
- **Primary Key:** `(SATypeID, PartID)`
- **Foreign Key:** `SATypeID -> Sub-Assembly(SATypeID)`
- **Foreign Key:** `PartID -> Part(PartID)`

#### Sub-Assembly-Hierarchy
- **Primary Key:** `(ParentSATypeID, ChildPartID)`
- **Foreign Key:** `ParentSATypeID -> Sub-Assembly(SATypeID)`
- **Foreign Key:** `ChildPartID -> Sub-Assembly(SATypeID)`

#### RobotDeleteAudit
- **Primary Key:** `AuditID`

---

## Why the Schema is in 3NF / BCNF

The schema is normalized because major entities are stored in separate relations and subtype-specific attributes are moved into subtype tables instead of being repeated in one large table. This design reduces redundancy and prevents insertion, deletion, and update anomalies.

Examples:
- `RobotID -> RobotName` in `Robot`
- `ID -> Name, TeamName, RobotID` in `TeamMember`
- `PartID -> ...` in `Part`
- `PartID -> subtype attributes` in subtype relations
- `(SATypeID, PartID) -> ...` in `Sub-Assembly-Parts`

Intersection tables such as `Sub-Assembly-Parts` and `Sub-Assembly-Hierarchy` are also normalized because their determinant is the full composite key.

Therefore, the schema is at least in **3NF**, and most relations satisfy **BCNF**.

---

## Note

Some business rules may be intended by the application, such as one team per robot or one manager per team, but these are not always enforced as unique constraints in the schema. For that reason, the functional dependency analysis above is based primarily on keys and constraints explicitly represented in the SQL schema.
