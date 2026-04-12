# usability_web/app.py
import os
from flask import Flask, render_template, abort
from SQLSetup.database_conection import get_mysql_connection

app = Flask(__name__)

# Keep TRIGGERS as a dictionary because they are UI descriptions, not data rows
TRIGGERS = {
    "future-update": {
        "title": "No future progress updates",
        "purpose": "Prevents a team member from inserting a progress update with a date later than the current day.",
        "demo": "Try to insert a ProgressUpdates row dated tomorrow.",
    },
    "version-bump": {
        "title": "Automatic sub-assembly version bump",
        "purpose": "Related sub-assembly version increases automatically on part changes.",
        "demo": "Insert or delete a Sub-Assembly-Parts row.",
    },
    "robot-name-guard": {
        "title": "Duplicate robot name guard",
        "purpose": "Stops inserts that try to reuse an existing RobotName.",
        "demo": "Try inserting another robot with the same name.",
    },
    "robot-delete-audit": {
        "title": "Robot delete audit",
        "purpose": "Records deletions in RobotDeleteAudit before the cascade occurs.",
        "demo": "Delete a robot and check the audit table.",
    },
}

def get_db():
    return get_mysql_connection(
        os.getenv('HOST'), 
        os.getenv('USER'), 
        os.getenv('PASSWORD'), 
        os.getenv('DATABASE')
    )

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    # Query to join Robot, Team, and Manager to match your UI needs
    query = """
        SELECT 
            r.RobotID as id, 
            r.RobotName as name, 
            t.TeamName as team, 
            tm.ManagerName as manager,
            (SELECT COUNT(*) FROM ProgressUpdates pu WHERE pu.ID IN 
                (SELECT ID FROM TeamMember WHERE RobotID = r.RobotID)) as updates,
            'Robot project managed by ' + tm.ManagerName as summary
        FROM Robot r
        LEFT JOIN Team t ON r.RobotID = t.RobotID
        LEFT JOIN TeamManagers tm ON t.RobotID = tm.RobotID AND t.TeamName = tm.TeamName
    """
    cursor.execute(query)
    
    # Convert pyodbc rows to dictionaries
    columns = [column[0] for column in cursor.description]
    robots = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # Logic to map trigger_id based on your naming convention
    trigger_map = ["future-update", "version-bump", "robot-name-guard", "robot-delete-audit", "future-update", "version-bump"]
    for i, robot in enumerate(robots):
        robot['trigger_id'] = trigger_map[i % len(trigger_map)]
    
    conn.close()
    return render_template('index.html', robots=robots, triggers=TRIGGERS)

@app.route('/robots/<int:robot_id>')
def robot_detail(robot_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
                    SELECT r.RobotID as id, 
                    r.RobotName as name,
                    t.TeamName as team, 
                    tm.ManagerName as manager
                    FROM Robot r
                    LEFT JOIN Team t ON r.RobotID = t.RobotID
                    LEFT JOIN TeamManagers tm ON t.RobotID = tm.RobotID AND t.TeamName = tm.TeamName
                    WHERE r.RobotID = ?
                    """, robot_id)
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        abort(404)
        
    columns = [column[0] for column in cursor.description]
    robot = dict(zip(columns, row))
    
    robot.update({
        "status": "In Progress",
        "summary": "Full system integrity check required.",
        "trigger_id": "future-update" 
    })
    
    trigger = TRIGGERS[robot['trigger_id']]
    conn.close()
    return render_template('robot_detail.html', robot=robot, trigger=trigger)