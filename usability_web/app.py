import os
from flask import Flask, render_template, abort
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


@app.route("/functionalities")
def functionality_index():
    return render_template("functionality_index.html", functionalities=FUNCTIONALITIES)


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


if __name__ == "__main__":
    app.run(debug=True)
