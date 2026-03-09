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
	PartID int IDENTITY(1,1) primary key,
	PartName varchar(100) not null unique,
	"Weight" int not null,
	Height int not null,
	"Length" int not null,
	Width int not null,

);

CREATE TABLE Structural(
	PartID int,
	Material varchar(100),
	"Type" varchar(50),
	foreign key (PartID) references Part(PartID)

);

CREATE TABLE Electronic(
	PartID int,
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
	PartID int,
	foreign key (PartID) references Part(PartID)

);

CREATE TABLE Wheel(
	PartID int,
	Radius int,
	"Type" varchar(50),
	foreign key (PartID) references Mechanical(PartID)

);

CREATE TABLE Motor(
	PartID int,
	Torque int,
	foreign key (PartID) references Mechanical(PartID)

);

CREATE TABLE Suspension(
	PartID int,
	WeightLimit int,
	foreign key (PartID) references Mechanical(PartID)

);



GO