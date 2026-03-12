PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS ContainsPart;
DROP TABLE IF EXISTS Wheel;
DROP TABLE IF EXISTS Motor;
DROP TABLE IF EXISTS Suspension;
DROP TABLE IF EXISTS Battery;
DROP TABLE IF EXISTS Mechanical;
DROP TABLE IF EXISTS Electronic;
DROP TABLE IF EXISTS Structural;
DROP TABLE IF EXISTS Part;
DROP TABLE IF EXISTS TeamManager;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS SubAssembly;
DROP TABLE IF EXISTS Robot;

CREATE TABLE Robot (
    robot_id INTEGER PRIMARY KEY,
    robot_name TEXT NOT NULL UNIQUE
);

CREATE TABLE Team (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT NOT NULL,
    robot_id INTEGER NOT NULL,
    UNIQUE (team_name, robot_id),
    FOREIGN KEY (robot_id) REFERENCES Robot(robot_id)
);

CREATE TABLE TeamManager (
    manager_id INTEGER PRIMARY KEY,
    manager_name TEXT NOT NULL,
    team_id INTEGER NOT NULL,
    UNIQUE (manager_name, team_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);

CREATE TABLE SubAssembly (
    subassembly_id INTEGER PRIMARY KEY,
    sa_name TEXT NOT NULL,
    version INTEGER NOT NULL,
    classification TEXT NOT NULL CHECK (classification IN ('Core', 'Power', 'Drive', 'Sensor', 'Control', 'Support')),
    robot_id INTEGER NOT NULL,
    UNIQUE (sa_name, version),
    FOREIGN KEY (robot_id) REFERENCES Robot(robot_id)
);

CREATE TABLE Part (
    part_id INTEGER PRIMARY KEY,
    part_name TEXT NOT NULL UNIQUE,
    weight INTEGER NOT NULL CHECK (weight > 0),
    height INTEGER NOT NULL CHECK (height > 0),
    length INTEGER NOT NULL CHECK (length > 0),
    width INTEGER NOT NULL CHECK (width > 0),
    part_category TEXT NOT NULL CHECK (part_category IN ('Structural', 'Electronic', 'Mechanical'))
);

CREATE TABLE Structural (
    part_id INTEGER PRIMARY KEY,
    material TEXT NOT NULL,
    structure_type TEXT NOT NULL,
    FOREIGN KEY (part_id) REFERENCES Part(part_id)
);

CREATE TABLE Electronic (
    part_id INTEGER PRIMARY KEY,
    max_current_a INTEGER NOT NULL CHECK (max_current_a > 0),
    max_voltage_v INTEGER NOT NULL CHECK (max_voltage_v > 0),
    FOREIGN KEY (part_id) REFERENCES Part(part_id)
);

CREATE TABLE Battery (
    part_id INTEGER PRIMARY KEY,
    capacity_mah INTEGER NOT NULL CHECK (capacity_mah > 0),
    FOREIGN KEY (part_id) REFERENCES Electronic(part_id)
);

CREATE TABLE Mechanical (
    part_id INTEGER PRIMARY KEY,
    FOREIGN KEY (part_id) REFERENCES Part(part_id)
);

CREATE TABLE Wheel (
    part_id INTEGER PRIMARY KEY,
    radius INTEGER NOT NULL CHECK (radius > 0),
    wheel_type TEXT NOT NULL,
    FOREIGN KEY (part_id) REFERENCES Mechanical(part_id)
);

CREATE TABLE Motor (
    part_id INTEGER PRIMARY KEY,
    torque INTEGER NOT NULL CHECK (torque > 0),
    FOREIGN KEY (part_id) REFERENCES Mechanical(part_id)
);

CREATE TABLE Suspension (
    part_id INTEGER PRIMARY KEY,
    weight_limit INTEGER NOT NULL CHECK (weight_limit > 0),
    FOREIGN KEY (part_id) REFERENCES Mechanical(part_id)
);

CREATE TABLE ContainsPart (
    subassembly_id INTEGER NOT NULL,
    part_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    PRIMARY KEY (subassembly_id, part_id),
    FOREIGN KEY (subassembly_id) REFERENCES SubAssembly(subassembly_id),
    FOREIGN KEY (part_id) REFERENCES Part(part_id)
);
