CREATE TABLE Robot(
	RobotID int IDENTITY(1,1) primary key,
	RobotName varchar(50) not null unique
);

CREATE TABLE Team(
	TeamName varchar(50),
	RobotID int,
	primary key (RobotID, TeamName),
	foreign key (RobotID) references Robot(RobotID)
)

CREATE TABLE TeamManagers(
	ManagerName varchar(50),
	TeamName varchar(50),
	RobotID int,
	primary key (RobotID, TeamName, ManagerName),
	foreign key (RobotID, TeamName) references Team(RobotID,TeamName)
)

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


INSERT INTO Robot VALUES ('0','dog'),('1','car'),('2','arm'),('3','spider'),('4','VEX'),('5','FTC');
INSERT INTO Team VALUES ('DogTeam','0'),('CarTeam','1'),('ArmTeam','2'),('SpiderTeam','3'),('VEXTeam','4'),('FTCTeam','5');
INSERT INTO TeamManagers VALUES ('John','DogTeam','0'),('Brendan','CarTeam','1'),('Godwin','ArmTeam','2'),('Daniel','SpiderTeam','3'),('Eliana','VEXTeam','4'),('Matthew','FTCTeam','5');
GO