SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS RobotDeleteAudit;
DROP TABLE IF EXISTS ProgressUpdates;
DROP TABLE IF EXISTS TeamMember;
DROP TABLE IF EXISTS TeamManagers;
DROP TABLE IF EXISTS `Sub-Assembly-Hierarchy`;
DROP TABLE IF EXISTS `Sub-Assembly-Parts`;
DROP TABLE IF EXISTS Battery;
DROP TABLE IF EXISTS Wheel;
DROP TABLE IF EXISTS Motor;
DROP TABLE IF EXISTS Suspension;
DROP TABLE IF EXISTS Electronic;
DROP TABLE IF EXISTS Mechanical;
DROP TABLE IF EXISTS Structural;
DROP TABLE IF EXISTS Part;
DROP TABLE IF EXISTS `Sub-Assembly`;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Robot;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE Robot(
    RobotID INT PRIMARY KEY,
    RobotName VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Team(
    TeamName VARCHAR(50) NOT NULL,
    RobotID INT NOT NULL,
    PRIMARY KEY (RobotID, TeamName),
    FOREIGN KEY (RobotID) REFERENCES Robot(RobotID)
    ON DELETE CASCADE
);

CREATE TABLE TeamManagers(
    ManagerName VARCHAR(50) NOT NULL,
    TeamName VARCHAR(50) NOT NULL,
    RobotID INT NOT NULL,
    PRIMARY KEY (RobotID, TeamName, ManagerName),
    FOREIGN KEY (RobotID, TeamName) REFERENCES Team(RobotID,TeamName)
    ON DELETE CASCADE
);

CREATE TABLE TeamMember(
    ID INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    TeamName VARCHAR(50) NOT NULL,
    RobotID INT NOT NULL,
    FOREIGN KEY (RobotID, TeamName) REFERENCES Team(RobotID, TeamName)
    ON DELETE CASCADE
);

CREATE TABLE ProgressUpdates(
    ID INT NOT NULL,
    `Date` DATE NOT NULL,
    Description TEXT NOT NULL,
    Picture VARCHAR(100),
    PRIMARY KEY (ID, `Date`),
    FOREIGN KEY (ID) REFERENCES TeamMember(ID)
    ON DELETE CASCADE,
    CONSTRAINT chk_progress_description_not_empty CHECK (CHAR_LENGTH(TRIM(Description)) > 0)
);

CREATE TABLE `Sub-Assembly`(
    SATypeID INT PRIMARY KEY,
    SAName VARCHAR(100) NOT NULL,
    `Version` INT NOT NULL,
    SAClassification VARCHAR(20),
    RobotID INT NOT NULL,
    UNIQUE (SAName, `Version`),
    FOREIGN KEY (RobotID) REFERENCES Robot(RobotID)
    ON DELETE CASCADE,
    CONSTRAINT chk_subassembly_version_positive CHECK (`Version` > 0)
);

CREATE TABLE Part(
    PartID INT PRIMARY KEY,
    PartName VARCHAR(100) NOT NULL UNIQUE,
    `Weight` FLOAT NOT NULL,
    Height FLOAT NOT NULL,
    `Length` FLOAT NOT NULL,
    Width FLOAT NOT NULL,
    Quantity INT NOT NULL,
    CONSTRAINT chk_part_measurements_positive CHECK (`Weight` > 0 AND Height > 0 AND `Length` > 0 AND Width > 0)
);

CREATE TABLE Structural(
    PartID INT PRIMARY KEY,
    Material VARCHAR(100),
    `Type` VARCHAR(50),
    FOREIGN KEY (PartID) REFERENCES Part(PartID)
    ON DELETE CASCADE
);

CREATE TABLE Electronic(
    PartID INT PRIMARY KEY,
    MaxCurrentA FLOAT,
    MaxVoltageV FLOAT,
    FOREIGN KEY (PartID) REFERENCES Part(PartID)
    ON DELETE CASCADE,
    CONSTRAINT chk_electronic_values_positive CHECK ((MaxCurrentA IS NULL OR MaxCurrentA > 0) AND (MaxVoltageV IS NULL OR MaxVoltageV > 0))
);

CREATE TABLE Battery(
    PartID INT PRIMARY KEY,
    CapacitymAh FLOAT,
    FOREIGN KEY (PartID) REFERENCES Electronic(PartID)
    ON DELETE CASCADE,
    CONSTRAINT chk_battery_capacity_positive CHECK (CapacitymAh IS NULL OR CapacitymAh > 0)
);

CREATE TABLE Mechanical(
    PartID INT PRIMARY KEY,
    FOREIGN KEY (PartID) REFERENCES Part(PartID)
    ON DELETE CASCADE
);

CREATE TABLE Wheel(
    PartID INT PRIMARY KEY,
    Radius FLOAT,
    `Type` VARCHAR(50),
    FOREIGN KEY (PartID) REFERENCES Mechanical(PartID)
    ON DELETE CASCADE,
    CONSTRAINT chk_wheel_radius_positive CHECK (Radius IS NULL OR Radius > 0)
);

CREATE TABLE Motor(
    PartID INT PRIMARY KEY,
    Torque FLOAT,
    FOREIGN KEY (PartID) REFERENCES Mechanical(PartID)
    ON DELETE CASCADE,
    CONSTRAINT chk_motor_torque_positive CHECK (Torque IS NULL OR Torque > 0)
);

CREATE TABLE Suspension(
    PartID INT PRIMARY KEY,
    WeightLimit FLOAT,
    FOREIGN KEY (PartID) REFERENCES Mechanical(PartID)
    ON DELETE CASCADE,
    CONSTRAINT chk_suspension_weight_limit_positive CHECK (WeightLimit IS NULL OR WeightLimit > 0)
);

CREATE TABLE `Sub-Assembly-Parts`(
    SATypeID INT,
    PartID INT,
    PRIMARY KEY (SATypeID, PartID),
    FOREIGN KEY (SATypeID) REFERENCES `Sub-Assembly`(SATypeID)
    ON DELETE CASCADE,
    FOREIGN KEY (PartID) REFERENCES Part(PartID)
    ON DELETE CASCADE
);

CREATE TABLE `Sub-Assembly-Hierarchy`(
    ParentSATypeID INT,
    ChildPartID INT,
    PRIMARY KEY (ParentSATypeID, ChildPartID),
    FOREIGN KEY (ParentSATypeID) REFERENCES `Sub-Assembly`(SATypeID)
    ON DELETE CASCADE,
    FOREIGN KEY (ChildPartID) REFERENCES `Sub-Assembly`(SATypeID)
    ON DELETE CASCADE
);

CREATE TABLE RobotDeleteAudit(
    AuditID INT AUTO_INCREMENT PRIMARY KEY,
    RobotID INT NOT NULL,
    RobotName VARCHAR(50) NOT NULL,
    DeletedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Robot (RobotID, RobotName) VALUES
(0,'dog'),(1,'car'),(2,'arm'),(3,'spider'),(4,'VEX'),(5,'FTC');

INSERT INTO Team (TeamName, RobotID) VALUES
('DogTeam',0),('CarTeam',1),('ArmTeam',2),('SpiderTeam',3),('VEXTeam',4),('FTCTeam',5);

INSERT INTO TeamManagers (ManagerName,TeamName,RobotID) VALUES
('John','DogTeam',0),('Brendan','CarTeam',1),('Godwin','ArmTeam',2),('Daniel','SpiderTeam',3),('Eliana','VEXTeam',4),('Matthew','FTCTeam',5);

INSERT INTO TeamMember (ID, Name, TeamName, RobotID) VALUES
(1, 'Alice', 'DogTeam', 0),
(2, 'Ben', 'CarTeam', 1),
(3, 'Chloe', 'ArmTeam', 2),
(4, 'David', 'SpiderTeam', 3),
(5, 'Eva', 'VEXTeam', 4),
(6, 'Felix', 'FTCTeam', 5);

INSERT INTO ProgressUpdates (ID, `Date`, Description, Picture) VALUES
(1, '2026-03-01', 'Wheel alignment completed for dog robot.', 'dog_update_1.png'),
(2, '2026-03-02', 'Battery wiring installed for car robot.', 'car_update_1.png'),
(3, '2026-03-03', 'Arm grip calibration completed.', 'arm_update_1.png'),
(4, '2026-03-04', 'Spider chassis inspection completed.', 'spider_update_1.png'),
(5, '2026-03-05', 'VEX frame cut and mounted.', 'vex_update_1.png'),
(6, '2026-03-06', 'FTC drivetrain motor tested.', 'ftc_update_1.png');

INSERT INTO `Sub-Assembly` (SATypeID, SAName, `Version`, SAClassification, RobotID) VALUES
(0,'wheel-pod',1,'wheel',1),
(1,'wheel-pod',2,'wheel',1),
(2,'chassis',1,'body',3),
(3,'legs',1,'leg',3),
(4,'hand',1,'arm',1),
(5,'ellbow',1,'arm',1);

INSERT INTO Part (PartID, PartName, `Weight`, Height, `Length`, Width, Quantity) VALUES
(100, 'Carbon Fiber Plate', 200, 2, 300, 300, 10),
(101, 'Aluminum Extrusion 2020', 500, 20, 20, 500, 10),
(102, 'Steel Bracket L', 150, 50, 50, 50, 10),
(103, 'Titanium Rod', 300, 10, 10, 400, 10),
(104, 'Polycarbonate Sheet', 400, 3, 500, 500, 10),
(200, 'LiPo 3S 5000mAh', 450, 25, 135, 45, 10),
(201, 'LiFePO4 Pack', 800, 50, 150, 60, 10),
(202, 'NiMH 7.2V', 350, 30, 100, 40, 10),
(203, 'LiPo 4S 1550mAh', 180, 35, 75, 35, 10),
(204, 'Graphene High Discharge', 500, 30, 140, 50, 10),
(205, 'Main Controller Board', 100, 15, 80, 80, 10),
(206, 'Power Distribution Board', 80, 10, 60, 60, 10),
(207, 'Radio Receiver', 20, 10, 30, 20, 10),
(208, 'Speed Controller ESC 60A', 60, 20, 40, 30, 10),
(209, 'Ultrasonic Sensor', 15, 15, 45, 20, 10),
(300, 'Mecanum Wheel Left', 400, 100, 100, 50, 10),
(301, 'Mecanum Wheel Right', 400, 100, 100, 50, 10),
(302, 'Rough Terrain Tire', 600, 120, 120, 80, 10),
(303, 'Omni Directional Pro', 350, 90, 90, 40, 10),
(304, 'Slick Racing Wheel', 300, 80, 80, 30, 10),
(305, 'Brushless Outrunner', 250, 50, 50, 60, 10),
(306, 'High Torque Servo', 70, 40, 20, 40, 10),
(307, 'DC Geared Motor', 400, 45, 45, 120, 10),
(308, 'Stepper Motor NEMA17', 350, 42, 42, 48, 10),
(309, 'Planetary Gear Motor', 550, 50, 50, 150, 10),
(310, 'Hydraulic Strut', 800, 200, 40, 40, 10),
(311, 'Coilover Spring Small', 150, 100, 30, 30, 10),
(312, 'Leaf Spring Assembly', 1200, 50, 400, 60, 10),
(313, 'Air Suspension Bag', 600, 150, 100, 100, 10),
(314, 'Torsion Bar Set', 450, 20, 500, 20, 10);

INSERT INTO Structural (PartID, Material, `Type`) VALUES
(100, 'Carbon Fiber', 'Panel'), (101, 'Aluminum', 'Frame'), (102, 'Steel', 'Joint'), (103, 'Titanium', 'Support'), (104, 'Polycarbonate', 'Shield');

INSERT INTO Electronic (PartID, MaxCurrentA, MaxVoltageV) VALUES
(200, 100, 12), (201, 80, 13), (202, 30, 7.2), (203, 120, 14.8), (204, 150, 15),
(205, 5, 5), (206, 200, 24), (207, 1, 5), (208, 60, 24), (209, 1, 5);

INSERT INTO Battery (PartID, CapacitymAh) VALUES
(200, 5000), (201, 10000), (202, 3000), (203, 1550), (204, 4500);

INSERT INTO Mechanical (PartID) SELECT PartID FROM Part WHERE PartID BETWEEN 300 AND 314;

INSERT INTO Wheel (PartID, Radius, `Type`) VALUES
(300, 50, 'Mecanum'), (301, 50, 'Mecanum'), (302, 60, 'Off-Road'), (303, 45, 'Omni'), (304, 40, 'Racing');
INSERT INTO Motor (PartID, Torque) VALUES
(305, 15), (306, 35), (307, 80), (308, 45), (309, 120);
INSERT INTO Suspension (PartID, WeightLimit) VALUES
(310, 5000), (311, 500), (312, 15000), (313, 2000), (314, 3000);

INSERT INTO `Sub-Assembly-Parts` (SATypeID, PartID) VALUES
(0, 300), (0, 305), (0, 200),
(1, 301), (1, 306), (1, 201),
(2, 100), (2, 101), (2, 102),
(3, 103), (3, 307),
(4, 104), (4, 208),
(5, 209), (5, 308);

INSERT INTO `Sub-Assembly-Hierarchy` (ParentSATypeID, ChildPartID) VALUES
(2, 0), (2, 1), (2, 4), (3, 5), (0, 4);

DELIMITER $$

CREATE TRIGGER trg_progressupdates_no_future_date_before_insert
BEFORE INSERT ON ProgressUpdates
FOR EACH ROW
BEGIN
    IF NEW.`Date` > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Progress update date cannot be in the future.';
    END IF;
END $$

CREATE TRIGGER trg_progressupdates_no_future_date_before_update
BEFORE UPDATE ON ProgressUpdates
FOR EACH ROW
BEGIN
    IF NEW.`Date` > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Progress update date cannot be in the future.';
    END IF;
END $$

CREATE TRIGGER trg_subassembly_parts_version_bump_after_insert
AFTER INSERT ON `Sub-Assembly-Parts`
FOR EACH ROW
BEGIN
    UPDATE `Sub-Assembly`
    SET `Version` = `Version` + 1
    WHERE SATypeID = NEW.SATypeID;
END $$

CREATE TRIGGER trg_subassembly_parts_version_bump_after_delete
AFTER DELETE ON `Sub-Assembly-Parts`
FOR EACH ROW
BEGIN
    UPDATE `Sub-Assembly`
    SET `Version` = `Version` + 1
    WHERE SATypeID = OLD.SATypeID;
END $$

CREATE TRIGGER trg_robot_duplicate_name_guard_before_insert
BEFORE INSERT ON Robot
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Robot r
        WHERE LOWER(r.RobotName) = LOWER(NEW.RobotName)
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Robot name already exists.';
    END IF;
END $$

CREATE TRIGGER trg_robot_delete_audit_before_delete
BEFORE DELETE ON Robot
FOR EACH ROW
BEGIN
    INSERT INTO RobotDeleteAudit (RobotID, RobotName)
    VALUES (OLD.RobotID, OLD.RobotName);
END $$

DELIMITER ;
