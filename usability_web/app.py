from flask import Flask, render_template, abort

app = Flask(__name__)

ROBOTS = [
    {
        "id": 0,
        "name": "dog",
        "team": "DogTeam",
        "manager": "John",
        "status": "Active",
        "updates": 1,
        "summary": "Quadruped project with basic wheel alignment progress update.",
        "trigger_id": "future-update",
        "trigger_name": "No future progress updates",
    },
    {
        "id": 1,
        "name": "car",
        "team": "CarTeam",
        "manager": "Brendan",
        "status": "Testing",
        "updates": 1,
        "summary": "Vehicle robot with electronics and battery-related progress data.",
        "trigger_id": "version-bump",
        "trigger_name": "Automatic sub-assembly version bump",
    },
    {
        "id": 2,
        "name": "arm",
        "team": "ArmTeam",
        "manager": "Godwin",
        "status": "Inspection",
        "updates": 1,
        "summary": "Manipulator build used to explain update history and sub-assembly integrity.",
        "trigger_id": "robot-name-guard",
        "trigger_name": "Duplicate robot name guard",
    },
    {
        "id": 3,
        "name": "spider",
        "team": "SpiderTeam",
        "manager": "Daniel",
        "status": "Active",
        "updates": 1,
        "summary": "Chassis and leg structure used to explain delete cascade and audit logging.",
        "trigger_id": "robot-delete-audit",
        "trigger_name": "Robot delete audit",
    },
    {
        "id": 4,
        "name": "VEX",
        "team": "VEXTeam",
        "manager": "Eliana",
        "status": "Testing",
        "updates": 1,
        "summary": "Competition build shown in the responsive layout and card system.",
        "trigger_id": "future-update",
        "trigger_name": "No future progress updates",
    },
    {
        "id": 5,
        "name": "FTC",
        "team": "FTCTeam",
        "manager": "Matthew",
        "status": "Planning",
        "updates": 1,
        "summary": "Drivetrain-focused example robot for mobile view preview.",
        "trigger_id": "version-bump",
        "trigger_name": "Automatic sub-assembly version bump",
    },
]

TRIGGERS = {
    "future-update": {
        "title": "No future progress updates",
        "purpose": "Prevents a team member from inserting a progress update with a date later than the current day.",
        "demo": "Try to insert a ProgressUpdates row dated tomorrow. The trigger raises an error and protects data accuracy.",
    },
    "version-bump": {
        "title": "Automatic sub-assembly version bump",
        "purpose": "Whenever a part relationship is added or removed from Sub-Assembly-Parts, the related sub-assembly version increases automatically.",
        "demo": "Insert or delete a Sub-Assembly-Parts row and then show that the related Sub-Assembly version number has increased.",
    },
    "robot-name-guard": {
        "title": "Duplicate robot name guard",
        "purpose": "Stops inserts that try to reuse an existing RobotName, reinforcing data consistency in addition to the unique constraint.",
        "demo": "Try inserting another robot with the same name. The trigger blocks the insert and returns a clear message.",
    },
    "robot-delete-audit": {
        "title": "Robot delete audit",
        "purpose": "Before deleting a robot, a trigger writes a row into RobotDeleteAudit so the deletion is recorded even when cascade removes related team data.",
        "demo": "Delete a robot and then show the audit row plus the cascade effect on Team and TeamManagers.",
    },
}


@app.route('/')
def index():
    return render_template('index.html', robots=ROBOTS, triggers=TRIGGERS)


@app.route('/robots/<int:robot_id>')
def robot_detail(robot_id: int):
    robot = next((r for r in ROBOTS if r['id'] == robot_id), None)
    if not robot:
        abort(404)
    trigger = TRIGGERS[robot['trigger_id']]
    return render_template('robot_detail.html', robot=robot, trigger=trigger)


if __name__ == '__main__':
    app.run(debug=True)
