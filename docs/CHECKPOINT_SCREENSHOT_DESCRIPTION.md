# Checkpoint screenshot description

**Suggested screenshot route**

- Open `http://127.0.0.1:8000/search?robot_id=1&part_category=All`
- This shows a meaningful query for the **Atlas Rover** robot.

**Query summary**

Retrieve all sub-assemblies and related parts for the selected robot, together with the responsible team and manager.

**Why this is meaningful**

The result demonstrates that the platform is already connected to the project data model and can join information across:

- Robot
- Team
- TeamManager
- SubAssembly
- ContainsPart
- Part
- subtype tables (Structural / Battery / Wheel / Motor / Suspension)
