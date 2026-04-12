import os
from flask import Flask, render_template, abort, request, redirect
try:
    from SQLSetup.database_conection import get_mysql_connection
except Exception:
    get_mysql_connection = None

app = Flask(__name__)

TRIGGERS = {
    "future-update": {
        "title": "No future progress updates",
        "purpose": "Prevents a team member from inserting a progress update with a date later than the current day.",
        "demo": "Try to insert a ProgressUpdates row dated tomorrow.",
    },
    "version-bump": {
        "title": "Automatic sub-assembly version bump",
        "purpose": "Related sub-assembly version increases automatically when parts are added to or removed from a sub-assembly.",
        "demo": "Insert or delete a Sub-Assembly-Parts row and show the version number change.",
    },
    "robot-name-guard": {
        "title": "Duplicate robot name guard",
        "purpose": "Stops inserts that try to reuse an existing RobotName.",
        "demo": "Try inserting another robot with the same RobotName.",
    },
    "robot-delete-audit": {
        "title": "Robot delete audit",
        "purpose": "Records deletions in RobotDeleteAudit before cascade deletes related rows.",
        "demo": "Delete a robot and then query the RobotDeleteAudit table.",
    },
}

FUNCTIONALITIES = [
    {
        "slug": "add-records",
        "number": "F1",
        "title": "Add part, sub-assembly, or robot",
        "category": "Create operation",
        "description": "Placeholder pages and forms for adding core records. This will later connect to insert queries for Part, Sub-Assembly, and Robot.",
        "demo_note": "Use this page to explain how new records enter the system before backend form handling is connected.",
        "dummy_fields": ["Entity type", "ID", "Name", "Subtype / classification", "Quantity or version"],
        "dummy_rows": [
            ["Part", "P-401", "Gyro Sensor", "Electronic", "12 in stock"],
            ["Sub-Assembly", "SA-220", "Wheel Control Unit", "Drive System", "v3"],
            ["Robot", "R-008", "Survey Rover", "Inspection", "active"],
        ],
    },
    {
        "slug": "modify-records",
        "number": "F2",
        "title": "Modify part, sub-assembly, or robot",
        "category": "Update operation",
        "description": "UI placeholder for editing existing records. This fits the assignment's update-operation demo and can later call the real update functions.",
        "demo_note": "Show how a user selects a record, edits values, and submits an update. Pair this with versioning or trigger rules in the presentation.",
        "dummy_fields": ["Target table", "Record ID", "Field to modify", "New value"],
        "dummy_rows": [
            ["Part", "P-102", "Width", "8.4 cm"],
            ["Robot", "R-002", "RobotName", "Arm Robot Mk II"],
            ["Sub-Assembly", "SA-030", "Classification", "Navigation"],
        ],
    },
    {
        "slug": "delete-records",
        "number": "F3",
        "title": "Delete part, sub-assembly, or robot",
        "category": "Delete operation with cascade",
        "description": "Dedicated page for delete flows. This is a strong place to demonstrate cascade delete and delete-audit trigger behavior.",
        "demo_note": "Use the dummy confirmation cards now; later connect them to actual delete endpoints and show cascade behavior in the database.",
        "dummy_fields": ["Entity type", "ID", "Impact summary"],
        "dummy_rows": [
            ["Robot", "R-004", "Deletes linked team relationships and records an audit row"],
            ["Sub-Assembly", "SA-108", "Removes hierarchy references"],
            ["Part", "P-211", "Removes unused part record"],
        ],
    },
    {
        "slug": "subassembly-parts",
        "number": "F4",
        "title": "Add or remove parts from a sub-assembly",
        "category": "Relationship management",
        "description": "Placeholder flow for managing the Sub-Assembly-Parts bridge table.",
        "demo_note": "This page pairs well with the version-bump trigger because adding or removing a part should affect sub-assembly version history.",
        "dummy_fields": ["Mode", "Sub-Assembly ID", "Part ID"],
        "dummy_rows": [
            ["Add", "SA-220", "P-401"],
            ["Add", "SA-220", "P-118"],
            ["Remove", "SA-117", "P-019"],
        ],
    },
    {
        "slug": "subassembly-hierarchy",
        "number": "F5",
        "title": "Manage sub-assembly hierarchy",
        "category": "Relationship management",
        "description": "Placeholder page for parent-child sub-assembly hierarchy edits.",
        "demo_note": "Use this to explain how the project models robot structure across multiple levels.",
        "dummy_fields": ["Mode", "Parent ID", "Child ID"],
        "dummy_rows": [
            ["Add child", "SA-300", "SA-220"],
            ["Add child", "SA-300", "SA-225"],
            ["Remove child", "SA-140", "SA-119"],
        ],
    },
    {
        "slug": "parts-by-type",
        "number": "F6",
        "title": "Show parts by type",
        "category": "Join query",
        "description": "Responsive read-only page for electronic, mechanical, and structural parts. This will later connect to the real join queries already prepared in the project.",
        "demo_note": "Useful for the join-query requirement because it combines base part data with subtype-specific tables.",
        "dummy_fields": ["Subtype filter", "Search term"],
        "dummy_rows": [
            ["Electronic", "Gyro Sensor", "5V", "2.0A"],
            ["Wheel", "All-terrain wheel", "11 cm", "Rubber"],
            ["Structural", "Frame Plate", "Aluminum", "Panel"],
        ],
    },
    {
        "slug": "team-for-robot",
        "number": "F7",
        "title": "Show team for a robot",
        "category": "Join query",
        "description": "Placeholder detail page for team name, manager, and members linked to a selected robot.",
        "demo_note": "This page is another strong join-query demo because it combines Robot, Team, TeamManagers, and TeamMember.",
        "dummy_fields": ["Robot ID or name"],
        "dummy_rows": [
            ["Robot", "R-002", "ArmTeam", "Manager: Godwin"],
            ["Member", "TM-11", "Ava Patel", "Controls"],
            ["Member", "TM-15", "Jae Kim", "Mechanical"],
        ],
    },
    {
        "slug": "version-history",
        "number": "F8",
        "title": "Update versions and view history",
        "category": "Update + history",
        "description": "Placeholder interface for robot/sub-assembly version updates and version history browsing.",
        "demo_note": "This page is useful when discussing controlled updates, version tracking, and integrity logic.",
        "dummy_fields": ["Entity type", "Identifier", "Change note"],
        "dummy_rows": [
            ["Robot", "R-002", "Version 3", "Arm calibration update"],
            ["Sub-Assembly", "SA-220", "Version 4", "Added new wheel sensor"],
            ["Robot", "R-004", "Version 2", "Navigation tuning"],
        ],
    },
    {
        "slug": "aggregation-reports",
        "number": "F9",
        "title": "Aggregation and group-by reports",
        "category": "Aggregation query",
        "description": "Placeholder analytics page for total robot counts, unused inventory counts, and grouped summaries by subtype.",
        "demo_note": "This directly supports the aggregation and aggregation-with-group-by requirements in the marking scheme.",
        "dummy_fields": ["Report type"],
        "dummy_rows": [
            ["Total robots", "6"],
            ["Unused wheel parts", "4"],
            ["Structural parts (grouped)", "8 names across 13 records"],
        ],
    },
    {
        "slug": "inventory-alerts",
        "number": "F10",
        "title": "Inventory alerts",
        "category": "Aggregation + decision support",
        "description": "Placeholder low-stock warning page for checking whether unused inventory counts fall below a threshold.",
        "demo_note": "This can later hook into the count-based alert logic for inventory monitoring.",
        "dummy_fields": ["Part name", "Low-stock threshold"],
        "dummy_rows": [
            ["Motor Housing", "Threshold 3", "Current unused count: 2", "LOW STOCK"],
            ["Frame Plate", "Threshold 5", "Current unused count: 7", "Sufficient"],
        ],
    },
]

FUNCTIONALITY_MAP = {item["slug"]: item for item in FUNCTIONALITIES}
STATUS_CYCLE = ["Active", "Testing", "Inspection", "Planning"]

DUMMY_ROBOTS = [
    {"id": 1, "name": "car", "team": "CarTeam", "manager": "Brendan", "updates": 2, "summary": "Robot project managed by Brendan.", "status": "Active", "trigger_id": "future-update"},
    {"id": 2, "name": "arm", "team": "ArmTeam", "manager": "Godwin", "updates": 3, "summary": "Robot project managed by Godwin.", "status": "Testing", "trigger_id": "version-bump"},
    {"id": 3, "name": "spider", "team": "SpiderTeam", "manager": "Daniel", "updates": 1, "summary": "Robot project managed by Daniel.", "status": "Inspection", "trigger_id": "robot-name-guard"},
    {"id": 4, "name": "vex", "team": "VEXTeam", "manager": "Eliana", "updates": 1, "summary": "Robot project managed by Eliana.", "status": "Planning", "trigger_id": "robot-delete-audit"},
]


def get_db():
    if get_mysql_connection is None:
        return None
    conn = get_mysql_connection(
        os.getenv("HOST"),
        os.getenv("USER"),
        os.getenv("PASSWORD"),
        os.getenv("DATABASE"),
    )
    return conn


def load_robots():
    conn = get_db()
    if conn is None:
        return DUMMY_ROBOTS

    try:
        cursor = conn.cursor()
        query = """
            SELECT
                r.RobotID AS id,
                r.RobotName AS name,
                COALESCE(t.TeamName, 'Unassigned') AS team,
                COALESCE(tm.ManagerName, 'Unassigned') AS manager,
                (
                    SELECT COUNT(*)
                    FROM ProgressUpdates pu
                    WHERE pu.ID IN (
                        SELECT tm2.ID
                        FROM TeamMember tm2
                        WHERE tm2.RobotID = r.RobotID
                    )
                ) AS updates,
                CONCAT('Robot project managed by ', COALESCE(tm.ManagerName, 'an unassigned manager'), '.') AS summary
            FROM Robot r
            LEFT JOIN Team t
                ON r.RobotID = t.RobotID
            LEFT JOIN TeamManagers tm
                ON t.RobotID = tm.RobotID
               AND t.TeamName = tm.TeamName
            ORDER BY r.RobotID
        """
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        robots = [dict(zip(columns, row)) for row in cursor.fetchall()]
        if not robots:
            return DUMMY_ROBOTS
        trigger_map = list(TRIGGERS.keys())
        for i, robot in enumerate(robots):
            robot["trigger_id"] = trigger_map[i % len(trigger_map)]
            robot["status"] = STATUS_CYCLE[i % len(STATUS_CYCLE)]
        return robots
    except Exception:
        return DUMMY_ROBOTS
    finally:
        try:
            conn.close()
        except Exception:
            pass


@app.route("/")
def index():
    robots = load_robots()
    return render_template(
        "index.html",
        robots=robots,
        triggers=TRIGGERS,
        functionalities=FUNCTIONALITIES,
    )


@app.route("/robots/<int:robot_id>")
def robot_detail(robot_id: int):
    robots = load_robots()
    robot = next((r for r in robots if int(r["id"]) == robot_id), None)
    if robot is None:
        abort(404)
    trigger = TRIGGERS[robot["trigger_id"]]
    return render_template("robot_detail.html", robot=robot, trigger=trigger)

@app.route("/entities/<entity_type>")
def api_get_entities(entity_type):
    from flask import jsonify
    conn = get_db()
    if not conn:
        return jsonify([]), 500
    try:
        cursor = conn.cursor()
        if entity_type == "robot":
            cursor.execute("SELECT RobotID, RobotName FROM Robot ORDER BY RobotID")
        elif entity_type == "sub-assembly":
            cursor.execute("SELECT SATypeID, SAName FROM `Sub-Assembly` ORDER BY SATypeID")
        elif entity_type == "part":
            cursor.execute("SELECT PartID, PartName FROM Part ORDER BY PartID")
        else:
            return jsonify([])
        rows = cursor.fetchall()
        return jsonify([{"id": r[0], "name": r[1]} for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route("/entity/<entity_type>/<int:entity_id>")
def api_get_entity_detail(entity_type, entity_id):
    from flask import jsonify
    conn = get_db()
    if not conn:
        return jsonify({}), 500
    try:
        cursor = conn.cursor()
        if entity_type == "robot":
            cursor.execute("SELECT RobotID, RobotName FROM Robot WHERE RobotID = ?", (entity_id,))
            r = cursor.fetchone()
            if not r:
                return jsonify({}), 404
            return jsonify({"id": r[0], "name": r[1]})

        elif entity_type == "sub-assembly":
            cursor.execute(
                "SELECT SATypeID, SAName, Version, SAClassification, RobotID FROM `Sub-Assembly` WHERE SATypeID = ?",
                (entity_id,)
            )
            r = cursor.fetchone()
            if not r:
                return jsonify({}), 404
            return jsonify({"id": r[0], "name": r[1], "version": r[2],
                            "classification": r[3], "robot_id": r[4]})

        elif entity_type == "part":
            cursor.execute(
                "SELECT PartID, PartName, Weight, Height, Length, Width FROM Part WHERE PartID = ?",
                (entity_id,)
            )
            r = cursor.fetchone()
            if not r:
                return jsonify({}), 404
            base = {"id": r[0], "name": r[1], "weight": r[2],
                    "height": r[3], "length": r[4], "width": r[5]}

            # Detect which subtype table this part belongs to
            cursor.execute("""
                SELECT 'battery'    FROM DUAL WHERE EXISTS (SELECT 1 FROM Battery    WHERE PartID = ?)
                UNION ALL
                SELECT 'electronic' FROM DUAL WHERE EXISTS (SELECT 1 FROM Electronic WHERE PartID = ?)
                UNION ALL
                SELECT 'structural' FROM DUAL WHERE EXISTS (SELECT 1 FROM Structural WHERE PartID = ?)
                UNION ALL
                SELECT 'wheel'      FROM DUAL WHERE EXISTS (SELECT 1 FROM Wheel      WHERE PartID = ?)
                UNION ALL
                SELECT 'motor'      FROM DUAL WHERE EXISTS (SELECT 1 FROM Motor      WHERE PartID = ?)
                UNION ALL
                SELECT 'suspension' FROM DUAL WHERE EXISTS (SELECT 1 FROM Suspension WHERE PartID = ?)
            """, (entity_id,) * 6)
            subtype_row = cursor.fetchone()
            subtype = subtype_row[0] if subtype_row else None
            base["subtype"] = subtype

            if subtype == "battery":
                cursor.execute("SELECT MaxCurrentA, MaxVoltageV, CapacitymAh FROM Battery WHERE PartID = ?", (entity_id,))
                s = cursor.fetchone()
                base.update({"max_current": s[0], "max_voltage": s[1], "capacity": s[2]})
            elif subtype == "electronic":
                cursor.execute("SELECT MaxCurrentA, MaxVoltageV FROM Electronic WHERE PartID = ?", (entity_id,))
                s = cursor.fetchone()
                base.update({"max_current": s[0], "max_voltage": s[1]})
            elif subtype == "structural":
                cursor.execute("SELECT Material, `Type` FROM Structural WHERE PartID = ?", (entity_id,))
                s = cursor.fetchone()
                base.update({"material": s[0], "type": s[1]})
            elif subtype == "wheel":
                cursor.execute("SELECT Radius, `Type` FROM Wheel WHERE PartID = ?", (entity_id,))
                s = cursor.fetchone()
                base.update({"radius": s[0], "wheel_type": s[1]})
            elif subtype == "motor":
                cursor.execute("SELECT Torque FROM Motor WHERE PartID = ?", (entity_id,))
                s = cursor.fetchone()
                base.update({"torque": s[0]})
            elif subtype == "suspension":
                cursor.execute("SELECT WeightLimit FROM Suspension WHERE PartID = ?", (entity_id,))
                s = cursor.fetchone()
                base.update({"weight_limit": s[0]})

            return jsonify(base)

        return jsonify({}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route("/functionalities")
def functionality_index():
    return render_template("functionality_index.html", functionalities=FUNCTIONALITIES)

@app.route("/functionalities/add-records", methods=["GET", "POST"])
def functionality_1():
    item = FUNCTIONALITY_MAP.get("add-records")
    
    conn = get_db()
    if item is None or conn is None:
        abort(404)
    
    if request.method == "POST":
        cursor = conn.cursor()
        entity_type = request.form.get("entity_type")
        
        
        if "part" in entity_type.lower():
            #part is going to need to be overhauled
            
            Id = request.form.get("id")
            Name = request.form.get("name")
            Weight = request.form.get("Weight")
            Length = request.form.get("Length")
            Height = request.form.get("Height")
            Width  = request.form.get("Width")
            Quantity = request.form.get("Quantity")
            
            cursor.execute(f"""INSERT INTO Part
                            (PartID, PartName, `Weight`, 
                            Height, `Length`, Width, Quantity) VALUES  
                            (?,?,?,?,?,?,?)""",
                            Id,Name,Weight,Length,Height,Width,Quantity)

            Sub_type = request.form.get("entity_subtype")
            
            if "electronic" in Sub_type.lower() and "battery" in Sub_type.lower():
                MaxVoltageV = request.form.get("MaxCurrentA")
                MaxCurrentA = request.form.get("MaxVoltageV")
                
                cursor.execute(f"""INSERT INTO Electronic
                        (PartID, MaxCurrentA,MaxVoltageV) VALUES  
                        (?,?,?)""",
                        Id,MaxCurrentA,MaxVoltageV)
                if "battery" in Sub_type.lower():
                    CapacitymAh = request.form.get("CapacitymAh")
                    
                    cursor.execute(f"""INSERT INTO Battery
                            (PartID, CapacitymAh) VALUES  
                            (?,?)""",
                            Id,CapacitymAh)
            elif "wheel" in Sub_type.lower() and "motor" in Sub_type.lower() and "suspension" in Sub_type.lower():
                cursor.execute(f"""INSERT INTO Mechanical
                            (PartID) VALUES  (?)""", Id)
                
                if "wheel" in Sub_type.lower():
                    Radius = request.form.get("radius")
                    WheelType = request.form.get("wheel-type")
                    
                    cursor.execute(f"""INSERT INTO Wheel
                            (PartID, Radius, `Sub_type`) VALUES 
                            (?,?,?)""", Id,Radius,WheelType)
                elif "motor" in Sub_type.lower():
                    Torque = request.form.get("torque")
                    
                    cursor.execute(f"""INSERT INTO Motor
                            (PartID, Torque) VALUES 
                            (?,?)""", Id,Torque)
                
                elif "suspension" in Sub_type.lower():
                    WeightLimit = request.form.get("limit")
                    
                    cursor.execute(f"""INSERT INTO Suspension
                            (PartID, WeightLimit) VALUES 
                            (?,?)""", Id,WeightLimit)
            elif "structural" in Sub_type.lower():
                Material = request.form.get("material")
                Type = request.form.get("type")
                cursor.execute(f"""INSERT INTO Structural
                            (PartID, Material, `Type`) VALUES 
                            (?,?,?)""", Id,Material,Type)
        elif "sub-assembly" in entity_type.lower():
            Id = request.form.get("id")
            Name = request.form.get("name")
            Version = request.form.get("version")
            SAClassification = request.form.get("classification")
            #this will be a list of all robots when we make a gui
            RobotId = request.form.get("robot_id")
            
            cursor.execute(f"""INSERT INTO `Sub-Assembly`
                            (SATypeID, SAName, `Version`, 
                            SAClassification, RobotID) VALUES  
                            (?,?,?,?,?)""",
                            Id,Name,Version,SAClassification,RobotId)
            
        elif "robot" in entity_type.lower():
            
            Id = request.form.get("id")
            Name = request.form.get("name")
            cursor.execute(f"""INSERT INTO Robot
                            (RobotID, RobotName) VALUES  
                            (?,?)""",
                            Id,Name)
        
        conn.commit()
        
        conn.close()
        
        return redirect("")
    
    return render_template(
        "functionality_1.html",
        item=item,
        functionalities=FUNCTIONALITIES,
    )

@app.route("/functionalities/modify-records", methods=["GET", "POST"])
def functionality_2():
    item = FUNCTIONALITY_MAP.get("modify-records")
    if not item:
        abort(404)

    if request.method == "POST":
        conn = get_db()
        if not conn:
            return "Database Connection Error", 500

        cursor = conn.cursor()
        entity_type = request.form.get("entity_type")
        entity_id   = int(request.form.get("entity_id"))

        try:
            if entity_type == "robot":
                cursor.execute(
                    "UPDATE Robot SET RobotName = ? WHERE RobotID = ?",
                    (request.form["name"], entity_id)
                )

            elif entity_type == "sub-assembly":
                cursor.execute(
                    """UPDATE `Sub-Assembly`
                       SET SAName = ?, `Version` = ?, SAClassification = ?, RobotID = ?
                       WHERE SATypeID = ?""",
                    (request.form["name"], request.form["version"],
                     request.form["classification"], request.form["robot_id"], entity_id)
                )

            elif entity_type == "part":
                cursor.execute(
                    """UPDATE Part
                       SET PartName = ?, `Weight` = ?, Height = ?, `Length` = ?, Width = ?
                       WHERE PartID = ?""",
                    (request.form["name"], request.form["weight"], request.form["height"],
                     request.form["length"], request.form["width"], entity_id)
                )
                subtype = request.form.get("subtype", "")
                if subtype == "battery":
                    cursor.execute(
                        "UPDATE Electronic SET MaxCurrentA = ?, MaxVoltageV = ? WHERE PartID = ?",
                        (request.form["max_current"], request.form["max_voltage"], entity_id)
                    )
                    cursor.execute(
                        "UPDATE Battery SET CapacitymAh = ? WHERE PartID = ?",
                        (request.form["capacity"], entity_id)
                    )
                elif subtype == "electronic":
                    cursor.execute(
                        "UPDATE Electronic SET MaxCurrentA = ?, MaxVoltageV = ? WHERE PartID = ?",
                        (request.form["max_current"], request.form["max_voltage"], entity_id)
                    )
                elif subtype == "structural":
                    cursor.execute(
                        "UPDATE Structural SET Material = ?, `Type` = ? WHERE PartID = ?",
                        (request.form["material"], request.form["type"], entity_id)
                    )
                elif subtype == "wheel":
                    cursor.execute(
                        "UPDATE Wheel SET Radius = ?, `Type` = ? WHERE PartID = ?",
                        (request.form["radius"], request.form["wheel_type"], entity_id)
                    )
                elif subtype == "motor":
                    cursor.execute(
                        "UPDATE Motor SET Torque = ? WHERE PartID = ?",
                        (request.form["torque"], entity_id)
                    )
                elif subtype == "suspension":
                    cursor.execute(
                        "UPDATE Suspension SET WeightLimit = ? WHERE PartID = ?",
                        (request.form["weight_limit"], entity_id)
                    )

            conn.commit()
        except Exception as e:
            conn.rollback()
            return f"Update failed: {e}", 500
        finally:
            conn.close()

        return redirect("/functionalities/modify-records")

    return render_template(
        "functionality_2.html",
        item=item,
        functionalities=FUNCTIONALITIES,
    )
    

@app.route("/functionalities/delete-records", methods=["GET", "POST"])
def functionality_3():
    item = FUNCTIONALITY_MAP.get("delete-records")
    if not item:
        abort(404)

    if request.method == "POST":
        conn = get_db()
        if not conn:
            return "Database Connection Error", 500

        cursor = conn.cursor()
        entity_type = request.form.get("entity_type")
        entity_id   = int(request.form.get("entity_id"))

        try:
            if entity_type == "robot":
                cursor.execute("DELETE FROM Robot WHERE RobotID = ?", (entity_id,))
            elif entity_type == "sub-assembly":
                cursor.execute("DELETE FROM `Sub-Assembly` WHERE SATypeID = ?", (entity_id,))
            elif entity_type == "part":
                cursor.execute("DELETE FROM Part WHERE PartID = ?", (entity_id,))

            conn.commit()
        except Exception as e:
            conn.rollback()
            return f"Delete failed: {e}", 500
        finally:
            conn.close()

        return redirect("/functionalities/delete-records")

    return render_template(
        "functionality_3.html",
        item=item,
        functionalities=FUNCTIONALITIES,
    )

@app.route("/functionalities/<slug>")
def functionality_detail(slug: str):
    item = FUNCTIONALITY_MAP.get(slug)
    if item is None:
        abort(404)
    related_trigger = None
    if slug in {"delete-records"}:
        related_trigger = TRIGGERS["robot-delete-audit"]
    elif slug in {"subassembly-parts", "version-history"}:
        related_trigger = TRIGGERS["version-bump"]
    elif slug in {"modify-records"}:
        related_trigger = TRIGGERS["future-update"]
    return render_template(
        "functionality_detail.html",
        item=item,
        related_trigger=related_trigger,
        functionalities=FUNCTIONALITIES,
    )
    


