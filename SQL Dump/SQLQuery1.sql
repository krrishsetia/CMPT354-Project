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
GO