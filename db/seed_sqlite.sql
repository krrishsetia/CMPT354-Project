INSERT INTO Robot (robot_id, robot_name) VALUES
(1, 'Atlas Rover'),
(2, 'Surveyor Bot'),
(3, 'Rescue Crawler'),
(4, 'AgriCarrier'),
(5, 'Warehouse Mule');

INSERT INTO Team (team_id, team_name, robot_id) VALUES
(1, 'Mobility Team', 1),
(2, 'Exploration Team', 2),
(3, 'Emergency Systems Team', 3),
(4, 'Field Automation Team', 4),
(5, 'Logistics Team', 5);

INSERT INTO TeamManager (manager_id, manager_name, team_id) VALUES
(1, 'Hannah Lee', 1),
(2, 'Victor Chen', 2),
(3, 'Mina Patel', 3),
(4, 'Daniel Kim', 4),
(5, 'Sofia Martinez', 5);

INSERT INTO SubAssembly (subassembly_id, sa_name, version, classification, robot_id) VALUES
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

INSERT INTO Part (part_id, part_name, weight, height, length, width, part_category) VALUES
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

INSERT INTO Structural (part_id, material, structure_type) VALUES
(1, 'Aluminum', 'Frame'),
(2, 'Steel', 'Plate'),
(3, 'Carbon Fiber', 'Shell'),
(4, 'Aluminum', 'Bracket'),
(5, 'Steel', 'Tower');

INSERT INTO Electronic (part_id, max_current_a, max_voltage_v) VALUES
(6, 20, 24),
(7, 22, 24),
(8, 25, 24),
(9, 18, 24),
(10, 28, 24);

INSERT INTO Battery (part_id, capacity_mah) VALUES
(6, 6000),
(7, 6200),
(8, 6800),
(9, 5500),
(10, 7200);

INSERT INTO Mechanical (part_id) VALUES
(11),(12),(13),(14),(15),(16),(17),(18),(19),(20),(21),(22),(23),(24),(25);

INSERT INTO Wheel (part_id, radius, wheel_type) VALUES
(11, 28, 'All-Terrain'),
(12, 24, 'Omni'),
(13, 25, 'Traction'),
(14, 30, 'Mud'),
(15, 23, 'Support');

INSERT INTO Motor (part_id, torque) VALUES
(16, 210),
(17, 220),
(18, 240),
(19, 250),
(20, 260);

INSERT INTO Suspension (part_id, weight_limit) VALUES
(21, 120),
(22, 120),
(23, 180),
(24, 90),
(25, 150);

INSERT INTO ContainsPart (subassembly_id, part_id, quantity) VALUES
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
