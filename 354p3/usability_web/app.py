import os
import pyodbc
from flask import Flask, render_template, abort, request, redirect, url_for
from versionhistory_queries import (
    f8_resolve_id,
    f8_get_robot_progress_history,
    f8_get_subassembly_info,
    f8_get_subassembly_history
)
from inventory_queries import (
    f10_low_quantity_parts_q,
    f10_parts_by_type_with_count_q
    )




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
        "slug": "teams",
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
        "slug": "inventory",
        "number": "F10",
        "title": "Inventory",
        "category": "Aggregation + decision support",
        "description": "View low-stock inventory and filter parts by subtype.",
        "demo_note": "Shows low-quantity parts and filtered inventory results.",
        "dummy_fields": [],
        "dummy_rows": []
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

import pyodbc
import os

def get_db():
    host = os.getenv("HOST", "localhost")
    user = os.getenv("USER", "root")
    database = os.getenv("DATABASE", "354p3")
    password = os.getenv("PASSWORD", "")

    return pyodbc.connect(
        "DRIVER={MySQL ODBC 9.6 Unicode Driver};"
        f"SERVER={host};"
        f"DATABASE={database};"
        f"USER={user};"
        f"PASSWORD={password};"
    )


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



def get_basic_part_filter_values():
    subtype = request.args.get("subtype", "").strip()
    mech_type = request.args.get("mech_type", "").strip()

    if subtype != "mechanical":
        mech_type = ""

    return subtype, mech_type

@app.route("/test-db")
def test_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE();")
    result = cursor.fetchone()

    conn.close()

    return f"Connected to: {result[0]}"



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

@app.route("/")
def home():
    return render_template(
        "index.html",
        robots=load_robots(),
        triggers=TRIGGERS,
        functionalities=FUNCTIONALITIES
    )

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
        entity_type = request.form.get("entity_type", "").strip()
        sub_type = request.form.get("entity_subtype", "").strip()

        try:
            if entity_type.lower() == "robot":
                name = request.form.get("name", "").strip()
                selected_team_name = request.form.get("team_name", "").strip()
                new_team_name = request.form.get("new_team_name", "").strip()

                if not name:
                    return "Robot name is required.", 400

                team_name = new_team_name if new_team_name else selected_team_name

                if not team_name:
                    return "You must select a team or create a new one.", 400

                cursor.execute(
                    "SELECT COUNT(*) FROM Robot WHERE RobotName = ?",
                    (name,)
                )
                existing_count = cursor.fetchone()[0]

                if existing_count > 0:
                    return f"Robot '{name}' already exists.", 400

                cursor.execute("SELECT COALESCE(MAX(RobotID), 0) + 1 FROM Robot")
                next_id = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO Robot (RobotID, RobotName) VALUES (?, ?)",
                    (next_id, name)
                )

                cursor.execute(
                    "SELECT COUNT(*) FROM team WHERE TeamName = ?",
                    (team_name,)
                )
                team_exists = cursor.fetchone()[0]

                if team_exists == 0:
                    cursor.execute(
                        "INSERT INTO team (TeamName, RobotID) VALUES (?, ?)",
                        (team_name, next_id)
                    )
                else:
                    cursor.execute(
                        "UPDATE team SET RobotID = ? WHERE TeamName = ?",
                        (next_id, team_name)
                    )

            elif entity_type.lower() == "sub-assembly":
                name = request.form.get("name", "").strip()
                version = request.form.get("version", "").strip()
                classification = request.form.get("classification", "").strip()
                robot_id = request.form.get("robot_id", "").strip()

                if not name or not version or not classification or not robot_id:
                    return "All sub-assembly fields are required.", 400

                cursor.execute("SELECT COALESCE(MAX(SATypeID), 0) + 1 FROM `Sub-Assembly`")
                next_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO `Sub-Assembly`
                    (SATypeID, SAName, `Version`, SAClassification, RobotID)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (next_id, name, version, classification, robot_id)
                )

            elif entity_type.lower() == "part":
                name = request.form.get("name", "").strip()
                weight = request.form.get("Weight", "").strip()
                length = request.form.get("Length", "").strip()
                height = request.form.get("Height", "").strip()
                width = request.form.get("Width", "").strip()
                quantity = request.form.get("Quantity", "").strip()

                if not name or not weight or not length or not height or not width or not quantity:
                    return "All part fields are required.", 400

                cursor.execute("SELECT COALESCE(MAX(PartID), 0) + 1 FROM Part")
                next_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO Part
                    (PartID, PartName, Weight, Height, Length, Width, Quantity)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (next_id, name, weight, height, length, width, quantity)
                )

                if "electronic" in sub_type.lower() or "battery" in sub_type.lower():
                    max_current_a = request.form.get("MaxCurrentA", "").strip()
                    max_voltage_v = request.form.get("MaxVoltageV", "").strip()

                    cursor.execute(
                        """
                        INSERT INTO Electronic (PartID, MaxCurrentA, MaxVoltageV)
                        VALUES (?, ?, ?)
                        """,
                        (next_id, max_current_a, max_voltage_v)
                    )

                    if "battery" in sub_type.lower():
                        capacity_mah = request.form.get("CapacitymAh", "").strip()
                        cursor.execute(
                            """
                            INSERT INTO Battery (PartID, CapacitymAh)
                            VALUES (?, ?)
                            """,
                            (next_id, capacity_mah)
                        )

                elif (
                    "wheel" in sub_type.lower()
                    or "motor" in sub_type.lower()
                    or "suspension" in sub_type.lower()
                ):
                    cursor.execute(
                        "INSERT INTO Mechanical (PartID) VALUES (?)",
                        (next_id,)
                    )

                    if "wheel" in sub_type.lower():
                        radius = request.form.get("radius", "").strip()
                        wheel_type = request.form.get("wheel-type", "").strip()

                        cursor.execute(
                            """
                            INSERT INTO Wheel (PartID, Radius, `Sub_type`)
                            VALUES (?, ?, ?)
                            """,
                            (next_id, radius, wheel_type)
                        )

                    elif "motor" in sub_type.lower():
                        torque = request.form.get("torque", "").strip()
                        cursor.execute(
                            "INSERT INTO Motor (PartID, Torque) VALUES (?, ?)",
                            (next_id, torque)
                        )

                    elif "suspension" in sub_type.lower():
                        weight_limit = request.form.get("limit", "").strip()
                        cursor.execute(
                            "INSERT INTO Suspension (PartID, WeightLimit) VALUES (?, ?)",
                            (next_id, weight_limit)
                        )

                elif "structural" in sub_type.lower():
                    material = request.form.get("material", "").strip()
                    type_value = request.form.get("type", "").strip()

                    cursor.execute(
                        "INSERT INTO Structural (PartID, Material, `Type`) VALUES (?, ?, ?)",
                        (next_id, material, type_value)
                    )

            else:
                return "Invalid entity type.", 400

            conn.commit()
            return redirect("/functionalities/add-records")

        except Exception as e:
            conn.rollback()
            return f"Insert failed: {e}", 500

        finally:
            conn.close()

    cursor = conn.cursor()
    cursor.execute("SELECT TeamName FROM team ORDER BY TeamName")
    teams = cursor.fetchall()
    conn.close()

    return render_template(
        "functionality_1.html",
        item=item,
        functionalities=FUNCTIONALITIES,
        teams=teams
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
    
@app.route("/functionalities/subassembly-parts", methods=["GET", "POST"])
def functionality_4():
    item = FUNCTIONALITY_MAP.get("subassembly-parts")
    if not item:
        abort(404)

    if request.method == "POST":
        conn = get_db()
        if not conn:
            return "Database Connection Error", 500

        cursor = conn.cursor()
        # The form sends parallel lists: modes[], sa_ids[], part_ids[]
        modes    = request.form.getlist("mode[]")
        sa_ids   = request.form.getlist("sa_id[]")
        part_ids = request.form.getlist("part_id[]")

        try:
            for mode, sa_id, part_id in zip(modes, sa_ids, part_ids):
                if mode == "add":
                    cursor.execute(
                        "INSERT INTO `Sub-Assembly-Parts` (SATypeID, PartID) VALUES (?, ?)",
                        (int(sa_id), int(part_id))
                    )
                elif mode == "remove":
                    cursor.execute(
                        "DELETE FROM `Sub-Assembly-Parts` WHERE SATypeID = ? AND PartID = ?",
                        (int(sa_id), int(part_id))
                    )
            conn.commit()
        except Exception as e:
            conn.rollback()
            return f"Operation failed: {e}", 500
        finally:
            conn.close()

        return redirect("/functionalities/subassembly-parts")

    return render_template(
        "functionality_4.html",
        item=item,
        functionalities=FUNCTIONALITIES,
    )

@app.route("/functionalities/subassembly-hierarchy", methods=["GET", "POST"])
def functionality_5():
    item = FUNCTIONALITY_MAP.get("subassembly-hierarchy")
    if not item:
        abort(404)

    if request.method == "POST":
        conn = get_db()
        if not conn:
            return "Database Connection Error", 500

        cursor = conn.cursor()
        modes      = request.form.getlist("mode[]")
        parent_ids = request.form.getlist("parent_id[]")
        child_ids  = request.form.getlist("child_id[]")

        try:
            for mode, parent_id, child_id in zip(modes, parent_ids, child_ids):
                if mode == "add":
                    cursor.execute(
                        "INSERT INTO `Sub-Assembly-Hierarchy` (ParentSATypeID, ChildPartID) VALUES (?, ?)",
                        (int(parent_id), int(child_id))
                    )
                elif mode == "remove":
                    cursor.execute(
                        "DELETE FROM `Sub-Assembly-Hierarchy` WHERE ParentSATypeID = ? AND ChildPartID = ?",
                        (int(parent_id), int(child_id))
                    )
            conn.commit()
        except Exception as e:
            conn.rollback()
            return f"Operation failed: {e}", 500
        finally:
            conn.close()

        return redirect("/functionalities/subassembly-hierarchy")

    return render_template(
        "functionality_5.html",
        item=item,
        functionalities=FUNCTIONALITIES,
    )


@app.route("/functionalities/teams", methods=["GET", "POST"])
def functionality_7():
    item = FUNCTIONALITY_MAP.get("teams")
    if not item:
        abort(404)

    conn = get_db()
    if not conn:
        return "Database Connection Error", 500

    cursor = conn.cursor()

    error = None
    success = None

    if request.method == "POST":
        form_type = request.form.get("form_type", "").strip()

        try:
            if form_type == "add_team":
                team_name = request.form.get("team_name", "").strip()
                robot_id = request.form.get("robot_id", "").strip()

                if not team_name or not robot_id:
                    error = "Please enter both Team Name and Robot ID."
                else:
                    robot_id = int(robot_id)

                    cursor.execute("""
                        SELECT RobotID
                        FROM Robot
                        WHERE RobotID = ?
                    """, (robot_id,))
                    robot = cursor.fetchone()

                    if not robot:
                        error = "Robot ID not found."
                    else:
                        cursor.execute("""
                            INSERT INTO Team (TeamName, RobotID)
                            VALUES (?, ?)
                        """, (team_name, robot_id))
                        conn.commit()
                        success = "Team added successfully."

            elif form_type == "add_member":
                member_name = request.form.get("member_name", "").strip()
                team_name = request.form.get("member_team_name", "").strip()

                if not member_name or not team_name:
                    error = "Please enter both Member Name and Team Name."
                else:
                    # Find RobotID from TeamName
                    cursor.execute("""
                        SELECT RobotID
                        FROM Team
                        WHERE TeamName = ?
                    """, (team_name,))
                    team_row = cursor.fetchone()

                    if not team_row:
                        error = "Team name not found."
                    else:
                        robot_id = team_row[0]

                        # Auto-generate next TeamMember ID
                        cursor.execute("""
                            SELECT COALESCE(MAX(ID), 0) + 1
                            FROM TeamMember
                        """)
                        new_member_id = cursor.fetchone()[0]

                        cursor.execute("""
                            INSERT INTO TeamMember (ID, Name, TeamName, RobotID)
                            VALUES (?, ?, ?, ?)
                        """, (new_member_id, member_name, team_name, robot_id))
                        conn.commit()
                        success = f"Team member added successfully with ID {new_member_id}."

            else:
                error = "Invalid form submission."

        except ValueError:
            conn.rollback()
            error = "Robot ID must be a number."

        except Exception as e:
            conn.rollback()
            msg = str(e).lower()

            if "duplicate" in msg or "unique" in msg:
                if form_type == "add_team":
                    error = "Team names must be unique."
                elif form_type == "add_member":
                    error = "Member ID must be unique."
                else:
                    error = "Duplicate value error."
            else:
                error = f"Failed to submit form: {e}"

    try:
        cursor.execute("""
            SELECT r.RobotID, r.RobotName, t.TeamName
            FROM Robot r
            JOIN Team t ON r.RobotID = t.RobotID
            ORDER BY r.RobotID
        """)
        rows = cursor.fetchall()

        cursor.execute("""
            SELECT TeamName
            FROM Team
            ORDER BY TeamName
        """)
        team_names = cursor.fetchall()

    except Exception as e:
        conn.close()
        return f"Query failed: {e}", 500

    conn.close()

    return render_template(
        "functionality_7.html",
        item=item,
        functionalities=FUNCTIONALITIES,
        rows=rows,
        team_names=team_names,
        error=error,
        success=success,
    )


@app.route("/functionalities/teams/<int:robot_id>")
def functionality_7_detail(robot_id):
    item = FUNCTIONALITY_MAP.get("teams")
    if not item:
        abort(404)

    conn = get_db()
    if not conn:
        return "Database Connection Error", 500

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT r.RobotID, r.RobotName, t.TeamName
            FROM Robot r
            JOIN Team t ON r.RobotID = t.RobotID
            WHERE r.RobotID = ?
        """, (robot_id,))
        robot_team = cursor.fetchone()

        if not robot_team:
            conn.close()
            abort(404)

        cursor.execute("""
            SELECT ManagerName
            FROM TeamManagers
            WHERE RobotID = ?
        """, (robot_id,))
        managers = cursor.fetchall()

        cursor.execute("""
            SELECT ID, Name
            FROM TeamMember
            WHERE RobotID = ?
            ORDER BY ID
        """, (robot_id,))
        members = cursor.fetchall()

        cursor.execute("""
            SELECT `Date`, Description, Picture
            FROM ProgressUpdates
            WHERE ID = ?
            ORDER BY `Date` DESC
        """, (robot_id,))
        updates = cursor.fetchall()

    except Exception as e:
        conn.close()
        return f"Query failed: {e}", 500

    conn.close()

    return render_template(
        "functionality_7_detail.html",
        item=item,
        functionalities=FUNCTIONALITIES,
        robot_team=robot_team,
        managers=managers,
        members=members,
        updates=updates,
    )

@app.route("/functionalities/version-history", methods=["GET"])
def functionality_8():
    item = FUNCTIONALITY_MAP.get("version-history")

    conn = get_db()
    if item is None or conn is None:
        abort(404)

    entity_type = request.args.get("entity_type", "").strip().lower()
    identifier = request.args.get("identifier", "").strip()

    history = []
    current_info = None
    error = None

    try:
        cursor = conn.cursor()

        if entity_type and identifier:
            if entity_type == "robot":
                robot_id = f8_resolve_id(
                    cursor,
                    "Robot",
                    "RobotID",
                    "RobotName",
                    identifier
                )

                if robot_id is None:
                    error = "Robot not found."
                elif robot_id == "MULTIPLE":
                    error = "Multiple robots matched that name. Please use RobotID."
                else:
                    history = f8_get_robot_progress_history(cursor, robot_id)

            elif entity_type == "sub-assembly":
                sa_id = f8_resolve_id(
                    cursor,
                    "`Sub-Assembly`",
                    "SATypeID",
                    "SAName",
                    identifier
                )

                if sa_id is None:
                    error = "Sub-assembly not found."
                elif sa_id == "MULTIPLE":
                    error = "Multiple sub-assemblies matched that name. Please use SATypeID."
                else:
                    current_info = f8_get_subassembly_info(cursor, sa_id)
                    history = f8_get_subassembly_history(cursor, sa_id)

            else:
                error = "Invalid entity type."

    except Exception as e:
        error = f"Lookup failed: {e}"

    finally:
        conn.close()

    return render_template(
        "functionality_8.html",
        item=item,
        functionalities=FUNCTIONALITIES,
        entity_type=entity_type,
        identifier=identifier,
        history=history,
        current_info=current_info,
        error=error
    )

@app.route("/functionalities/<slug>")
def functionality_detail(slug: str):
    item = FUNCTIONALITY_MAP.get(slug)
    if item is None:
        abort(404)

    # defaults
    subtype = ""
    mech_type = ""
    parts = []
    low_parts = []

    if slug == "inventory":
        subtype, mech_type = get_basic_part_filter_values()

        conn = get_db()
        if conn:
            try:
                cursor = conn.cursor()

                # show low inventory automatically when inventory page is opened
                low_parts = f10_low_quantity_parts_q(cursor)

                # show filtered parts
                if subtype:
                    parts = f10_parts_by_type_with_count_q(cursor, subtype, mech_type)
                else:
                    cursor.execute("""
                        SELECT PartID, PartName, Quantity
                        FROM Part
                        ORDER BY PartName
                    """)
                    parts = cursor.fetchall()

            except Exception as e:
                print("Inventory page error:", e)
                low_parts = []
                parts = []
            finally:
                conn.close()

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
        subtype=subtype,
        mech_type=mech_type,
        parts=parts,
        low_parts=low_parts,
        related_trigger=related_trigger,
        functionalities=FUNCTIONALITIES,
    )

if __name__ == "__main__":
    app.run(debug=True)
    


