CREATE TABLE Robot(
	RobotID int IDENTITY(1,1) primary key,
	RobotName varchar(50) not null unique
);

CREATE TABLE Team(
	TeamName varchar(50),
	RobotID int,
	primary key (RobotID, TeamName),
	foreign key (RobotID) references Robot(RobotID)
);

CREATE TABLE TeamManagers(
	ManagerName varchar(50),
	TeamName varchar(50),
	RobotID int,
	primary key (RobotID, TeamName, ManagerName),
	foreign key (RobotID, TeamName) references Team(RobotID,TeamName)
);

CREATE TABLE "Sub-Assembly"(
	SATypeID int IDENTITY(1,1) primary key,
	SAName varchar(100) not null unique,
	"Version" int not null,
	SAClassification varchar(20),
	RobotID int not null,
	unique (SAName, "Version"),
	foreign key (RobotID) references Robot(RobotID)

);

CREATE TABLE Part(
	PartID int primary key,
	PartName varchar(100) not null unique,
	"Weight" int not null,
	Height int not null,
	"Length" int not null,
	Width int not null,

);

CREATE TABLE Structural(
	PartID int primary key,
	Material varchar(100),
	"Type" varchar(50),
	foreign key (PartID) references Part(PartID)

);

CREATE TABLE Electronic(
	PartID int primary key,
	MaxCurrentA int,
	MaxVoltageV int,
	foreign key (PartID) references Part(PartID)

);

CREATE TABLE Battery(
	PartID int,
	CapacitymAh int,
	foreign key (PartID) references Electronic(PartID)

);

CREATE TABLE Mechanical(
	PartID int primary key,
	foreign key (PartID) references Part(PartID)

);

CREATE TABLE Wheel(
	PartID int primary key,
	Radius int,
	"Type" varchar(50),
	foreign key (PartID) references Mechanical(PartID)

);

CREATE TABLE Motor(
	PartID int primary key,
	Torque int,
	foreign key (PartID) references Mechanical(PartID)

);

CREATE TABLE Suspension(
	PartID int primary key,
	WeightLimit int,
	foreign key (PartID) references Mechanical(PartID)

);

CREATE TABLE "Sub-Assembly-Parts"(
	SATypeID int,
	PartID int,
	primary key (SATypeID, PartID),
	foreign key (SATypeID) references "Sub-Assembly"(SATypeID),
	foreign key (PartID) references Part(PartID)
);

CREATE TABLE "Sub-Assembly-Heirarchy"(
	ParentSATypeID int,
	ChildPartID int,
	primary key (ParentSATypeID, ChildPartID),
	foreign key (ParentSATypeID) references "Sub-Assembly"(SATypeID),
	foreign key (ChildPartID) references "Sub-Assembly"(SATypeID)
);


INSERT INTO Robot VALUES ('0','dog'),('1','car'),('2','arm'),
('3','spider'),('4','VEX'),('5','FTC');

INSERT INTO Team VALUES ('DogTeam','0'),('CarTeam','1'),('ArmTeam','2'),
('SpiderTeam','3'),('VEXTeam','4'),('FTCTeam','5');

INSERT INTO TeamManagers VALUES ('John','DogTeam','0'),('Brendan','CarTeam','1'),
('Godwin','ArmTeam','2'),('Daniel','SpiderTeam','3'),('Eliana','VEXTeam','4'),('Matthew','FTCTeam','5');

INSERT INTO "Sub-Assembly" VALUES ('0','wheel-pod','1','wheel','1'), ('1','wheel-pod','2','wheel','1'), ('2','chassis','1','body','3'), 
('3','legs','1','leg','3'), ('4','hand','1','arm','1'), ('5','ellbow','1','arm','1');

INSERT INTO Part VALUES (100, 'Carbon Fiber Plate', 200, 2, 300, 300), (101, 'Aluminum Extrusion 2020', 500, 20, 20, 500), (102, 'Steel Bracket L', 150, 50, 50, 50), (103, 'Titanium Rod', 300, 10, 10, 400), (104, 'Polycarbonate Sheet', 400, 3, 500, 500);

INSERT INTO Part VALUES (200, 'LiPo 3S 5000mAh', 450, 25, 135, 45), (201, 'LiFePO4 Pack', 800, 50, 150, 60), (202, 'NiMH 7.2V', 350, 30, 100, 40), (203, 'LiPo 4S 1550mAh', 180, 35, 75, 35), (204, 'Graphene High Discharge', 500, 30, 140, 50), (205, 'Main Controller Board', 100, 15, 80, 80), (206, 'Power Distribution Board', 80, 10, 60, 60), (207, 'Radio Receiver', 20, 10, 30, 20), (208, 'Speed Controller ESC 60A', 60, 20, 40, 30), (209, 'Ultrasonic Sensor', 15, 15, 45, 20);

INSERT INTO Part VALUES (300, 'Mecanum Wheel Left', 400, 100, 100, 50), (301, 'Mecanum Wheel Right', 400, 100, 100, 50), (302, 'Rough Terrain Tire', 600, 120, 120, 80), (303, 'Omni Directional Pro', 350, 90, 90, 40), (304, 'Slick Racing Wheel', 300, 80, 80, 30), (305, 'Brushless Outrunner', 250, 50, 50, 60), (306, 'High Torque Servo', 70, 40, 20, 40), (307, 'DC Geared Motor', 400, 45, 45, 120), (308, 'Stepper Motor NEMA17', 350, 42, 42, 48), (309, 'Planetary Gear Motor', 550, 50, 50, 150), (310, 'Hydraulic Strut', 800, 200, 40, 40), (311, 'Coilover Spring Small', 150, 100, 30, 30), (312, 'Leaf Spring Assembly', 1200, 50, 400, 60), (313, 'Air Suspension Bag', 600, 150, 100, 100), (314, 'Torsion Bar Set', 450, 20, 500, 20);

INSERT INTO Structural VALUES (100, 'Carbon Fiber', 'Panel'), (101, 'Aluminum', 'Frame'), (102, 'Steel', 'Joint'), (103, 'Titanium', 'Support'), (104, 'Polycarbonate', 'Shield');

INSERT INTO Electronic VALUES (200, 100, 12), (201, 80, 13), (202, 30, 7), (203, 120, 15), (204, 150, 15), (205, 5, 5), (206, 200, 24), (207, 1, 5), (208, 60, 24), (209, 1, 5);

INSERT INTO Battery VALUES (200, 5000), (201, 10000), (202, 3000), (203, 1550), (204, 4500);

INSERT INTO Mechanical (PartID) SELECT PartID FROM Part WHERE PartID BETWEEN 300 AND 314;

INSERT INTO Wheel VALUES (300, 50, 'Mecanum'), (301, 50, 'Mecanum'), (302, 60, 'Off-Road'), (303, 45, 'Omni'), (304, 40, 'Racing');
INSERT INTO Motor VALUES (305, 15), (306, 35), (307, 80), (308, 45), (309, 120);
INSERT INTO Suspension VALUES (310, 5000), (311, 500), (312, 15000), (313, 2000), (314, 3000);

GO