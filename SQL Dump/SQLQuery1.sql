/*
  SQL Server checkpoint dump
  - creates all tables
  - declares primary/foreign keys
  - inserts at least 5 tuples into each table
*/

IF OBJECT_ID('dbo.ContainsPart', 'U') IS NOT NULL DROP TABLE dbo.ContainsPart;
IF OBJECT_ID('dbo.Wheel', 'U') IS NOT NULL DROP TABLE dbo.Wheel;
IF OBJECT_ID('dbo.Motor', 'U') IS NOT NULL DROP TABLE dbo.Motor;
IF OBJECT_ID('dbo.Suspension', 'U') IS NOT NULL DROP TABLE dbo.Suspension;
IF OBJECT_ID('dbo.Battery', 'U') IS NOT NULL DROP TABLE dbo.Battery;
IF OBJECT_ID('dbo.Mechanical', 'U') IS NOT NULL DROP TABLE dbo.Mechanical;
IF OBJECT_ID('dbo.Electronic', 'U') IS NOT NULL DROP TABLE dbo.Electronic;
IF OBJECT_ID('dbo.Structural', 'U') IS NOT NULL DROP TABLE dbo.Structural;
IF OBJECT_ID('dbo.Part', 'U') IS NOT NULL DROP TABLE dbo.Part;
IF OBJECT_ID('dbo.TeamManager', 'U') IS NOT NULL DROP TABLE dbo.TeamManager;
IF OBJECT_ID('dbo.Team', 'U') IS NOT NULL DROP TABLE dbo.Team;
IF OBJECT_ID('dbo.SubAssembly', 'U') IS NOT NULL DROP TABLE dbo.SubAssembly;
IF OBJECT_ID('dbo.Robot', 'U') IS NOT NULL DROP TABLE dbo.Robot;
GO

CREATE TABLE dbo.Robot(
    RobotID INT PRIMARY KEY,
    RobotName VARCHAR(50) NOT NULL UNIQUE
);
GO

CREATE TABLE dbo.Team(
    TeamID INT PRIMARY KEY,
    TeamName VARCHAR(50) NOT NULL,
    RobotID INT NOT NULL,
    CONSTRAINT UQ_Team UNIQUE (TeamName, RobotID),
    CONSTRAINT FK_Team_Robot FOREIGN KEY (RobotID) REFERENCES dbo.Robot(RobotID)
);
GO

CREATE TABLE dbo.TeamManager(
    ManagerID INT PRIMARY KEY,
    ManagerName VARCHAR(50) NOT NULL,
    TeamID INT NOT NULL,
    CONSTRAINT UQ_TeamManager UNIQUE (ManagerName, TeamID),
    CONSTRAINT FK_TeamManager_Team FOREIGN KEY (TeamID) REFERENCES dbo.Team(TeamID)
);
GO

CREATE TABLE dbo.SubAssembly(
    SATypeID INT PRIMARY KEY,
    SAName VARCHAR(100) NOT NULL,
    VersionNo INT NOT NULL,
    SAClassification VARCHAR(20) NOT NULL CHECK (SAClassification IN ('Core', 'Power', 'Drive', 'Sensor', 'Control', 'Support')),
    RobotID INT NOT NULL,
    CONSTRAINT UQ_SubAssembly UNIQUE (SAName, VersionNo),
    CONSTRAINT FK_SubAssembly_Robot FOREIGN KEY (RobotID) REFERENCES dbo.Robot(RobotID)
);
GO

CREATE TABLE dbo.Part(
    PartID INT PRIMARY KEY,
    PartName VARCHAR(100) NOT NULL UNIQUE,
    Weight INT NOT NULL CHECK (Weight > 0),
    Height INT NOT NULL CHECK (Height > 0),
    Length INT NOT NULL CHECK (Length > 0),
    Width INT NOT NULL CHECK (Width > 0),
    PartCategory VARCHAR(20) NOT NULL CHECK (PartCategory IN ('Structural', 'Electronic', 'Mechanical'))
);
GO

CREATE TABLE dbo.Structural(
    PartID INT PRIMARY KEY,
    Material VARCHAR(100) NOT NULL,
    StructureType VARCHAR(50) NOT NULL,
    CONSTRAINT FK_Structural_Part FOREIGN KEY (PartID) REFERENCES dbo.Part(PartID)
);
GO

CREATE TABLE dbo.Electronic(
    PartID INT PRIMARY KEY,
    MaxCurrentA INT NOT NULL CHECK (MaxCurrentA > 0),
    MaxVoltageV INT NOT NULL CHECK (MaxVoltageV > 0),
    CONSTRAINT FK_Electronic_Part FOREIGN KEY (PartID) REFERENCES dbo.Part(PartID)
);
GO

CREATE TABLE dbo.Battery(
    PartID INT PRIMARY KEY,
    CapacitymAh INT NOT NULL CHECK (CapacitymAh > 0),
    CONSTRAINT FK_Battery_Electronic FOREIGN KEY (PartID) REFERENCES dbo.Electronic(PartID)
);
GO

CREATE TABLE dbo.Mechanical(
    PartID INT PRIMARY KEY,
    CONSTRAINT FK_Mechanical_Part FOREIGN KEY (PartID) REFERENCES dbo.Part(PartID)
);
GO

CREATE TABLE dbo.Wheel(
    PartID INT PRIMARY KEY,
    Radius INT NOT NULL CHECK (Radius > 0),
    WheelType VARCHAR(50) NOT NULL,
    CONSTRAINT FK_Wheel_Mechanical FOREIGN KEY (PartID) REFERENCES dbo.Mechanical(PartID)
);
GO

CREATE TABLE dbo.Motor(
    PartID INT PRIMARY KEY,
    Torque INT NOT NULL CHECK (Torque > 0),
    CONSTRAINT FK_Motor_Mechanical FOREIGN KEY (PartID) REFERENCES dbo.Mechanical(PartID)
);
GO

CREATE TABLE dbo.Suspension(
    PartID INT PRIMARY KEY,
    WeightLimit INT NOT NULL CHECK (WeightLimit > 0),
    CONSTRAINT FK_Suspension_Mechanical FOREIGN KEY (PartID) REFERENCES dbo.Mechanical(PartID)
);
GO

CREATE TABLE dbo.ContainsPart(
    SATypeID INT NOT NULL,
    PartID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    CONSTRAINT PK_ContainsPart PRIMARY KEY (SATypeID, PartID),
    CONSTRAINT FK_ContainsPart_SubAssembly FOREIGN KEY (SATypeID) REFERENCES dbo.SubAssembly(SATypeID),
    CONSTRAINT FK_ContainsPart_Part FOREIGN KEY (PartID) REFERENCES dbo.Part(PartID)
);
GO

INSERT INTO dbo.Robot (RobotID, RobotName) VALUES
(1, 'Atlas Rover'),
(2, 'Surveyor Bot'),
(3, 'Rescue Crawler'),
(4, 'AgriCarrier'),
(5, 'Warehouse Mule');
GO

INSERT INTO dbo.Team (TeamID, TeamName, RobotID) VALUES
(1, 'Mobility Team', 1),
(2, 'Exploration Team', 2),
(3, 'Emergency Systems Team', 3),
(4, 'Field Automation Team', 4),
(5, 'Logistics Team', 5);
GO

INSERT INTO dbo.TeamManager (ManagerID, ManagerName, TeamID) VALUES
(1, 'Hannah Lee', 1),
(2, 'Victor Chen', 2),
(3, 'Mina Patel', 3),
(4, 'Daniel Kim', 4),
(5, 'Sofia Martinez', 5);
GO

INSERT INTO dbo.SubAssembly (SATypeID, SAName, VersionNo, SAClassification, RobotID) VALUES
(1, 'Atlas Chassis', 1, 'Core', 1),
(2, 'Atlas Power Module', 1, 'Power', 1),
(3, 'Atlas Drive Unit', 1, 'Drive', 1),
(4, 'Atlas Sensor Pod', 1, 'Sensor', 1),
(5, 'Surveyor Core', 1, 'Core', 2),
(6, 'Surveyor Mobility Pack', 1, 'Drive', 2),
(7, 'Rescue Support Frame', 1, 'Support', 3),
(8, 'Agri Power Bay', 1, 'Power', 4),
(9, 'Warehouse Control Unit', 1, 'Control', 5),
(10, 'Warehouse Drive Train', 1, 'Drive', 5);
GO

INSERT INTO dbo.Part (PartID, PartName, Weight, Height, Length, Width, PartCategory) VALUES
(1, 'Aluminum Frame', 14, 20, 90, 50, 'Structural'),
(2, 'Steel Chassis Plate', 18, 6, 100, 60, 'Structural'),
(3, 'Carbon Fiber Shell', 9, 25, 80, 50, 'Structural'),
(4, 'Sensor Mount Bracket', 3, 12, 25, 12, 'Structural'),
(5, 'Shock Tower', 7, 18, 22, 18, 'Structural'),
(6, 'Lithium Battery Pack A', 11, 15, 30, 18, 'Electronic'),
(7, 'Lithium Battery Pack B', 11, 15, 30, 18, 'Electronic'),
(8, 'Lithium Battery Pack C', 12, 16, 32, 18, 'Electronic'),
(9, 'Lithium Battery Pack D', 10, 14, 28, 17, 'Electronic'),
(10, 'Lithium Battery Pack E', 13, 16, 33, 19, 'Electronic'),
(11, 'All-Terrain Wheel', 6, 55, 55, 14, 'Mechanical'),
(12, 'Omni Wheel', 5, 48, 48, 12, 'Mechanical'),
(13, 'Traction Wheel', 6, 50, 50, 13, 'Mechanical'),
(14, 'Mud Wheel', 7, 60, 60, 15, 'Mechanical'),
(15, 'Rear Support Wheel', 5, 46, 46, 12, 'Mechanical'),
(16, 'Drive Motor A', 8, 18, 30, 18, 'Mechanical'),
(17, 'Drive Motor B', 8, 18, 30, 18, 'Mechanical'),
(18, 'Drive Motor C', 9, 19, 32, 19, 'Mechanical'),
(19, 'Drive Motor D', 9, 19, 32, 19, 'Mechanical'),
(20, 'Drive Motor E', 10, 20, 34, 20, 'Mechanical'),
(21, 'Front Suspension', 7, 22, 24, 12, 'Mechanical'),
(22, 'Rear Suspension', 7, 22, 24, 12, 'Mechanical'),
(23, 'Heavy Suspension', 9, 25, 26, 14, 'Mechanical'),
(24, 'Compact Suspension', 6, 18, 20, 10, 'Mechanical'),
(25, 'Adaptive Suspension', 8, 24, 26, 13, 'Mechanical');
GO

INSERT INTO dbo.Structural (PartID, Material, StructureType) VALUES
(1, 'Aluminum', 'Frame'),
(2, 'Steel', 'Plate'),
(3, 'Carbon Fiber', 'Shell'),
(4, 'Aluminum', 'Bracket'),
(5, 'Steel', 'Tower');
GO

INSERT INTO dbo.Electronic (PartID, MaxCurrentA, MaxVoltageV) VALUES
(6, 20, 24),
(7, 22, 24),
(8, 25, 24),
(9, 18, 24),
(10, 28, 24);
GO

INSERT INTO dbo.Battery (PartID, CapacitymAh) VALUES
(6, 6000),
(7, 6200),
(8, 6800),
(9, 5500),
(10, 7200);
GO

INSERT INTO dbo.Mechanical (PartID) VALUES
(11),(12),(13),(14),(15),(16),(17),(18),(19),(20),(21),(22),(23),(24),(25);
GO

INSERT INTO dbo.Wheel (PartID, Radius, WheelType) VALUES
(11, 28, 'All-Terrain'),
(12, 24, 'Omni'),
(13, 25, 'Traction'),
(14, 30, 'Mud'),
(15, 23, 'Support');
GO

INSERT INTO dbo.Motor (PartID, Torque) VALUES
(16, 210),
(17, 220),
(18, 240),
(19, 250),
(20, 260);
GO

INSERT INTO dbo.Suspension (PartID, WeightLimit) VALUES
(21, 120),
(22, 120),
(23, 180),
(24, 90),
(25, 150);
GO

INSERT INTO dbo.ContainsPart (SATypeID, PartID, Quantity) VALUES
(1, 1, 1),
(1, 2, 1),
(1, 4, 2),
(2, 6, 1),
(2, 7, 1),
(3, 11, 2),
(3, 16, 2),
(3, 21, 1),
(3, 22, 1),
(4, 3, 1),
(4, 4, 2),
(5, 3, 1),
(5, 4, 1),
(6, 12, 2),
(6, 17, 2),
(6, 24, 1),
(7, 5, 1),
(7, 14, 2),
(7, 18, 2),
(7, 23, 2),
(8, 8, 1),
(8, 10, 1),
(9, 9, 1),
(9, 4, 1),
(10, 13, 2),
(10, 15, 2),
(10, 19, 2),
(10, 20, 1),
(10, 25, 2);
GO
