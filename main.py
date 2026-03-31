import pyodbc

def get_mysql_connection(host, user, password, database):
    drivers = [d for d in pyodbc.drivers() if 'MySQL' in d]
    if not drivers:
        raise Exception("No MySQL ODBC Driver found. Please install the MySQL Connector.")
    
    driver = drivers[0] 
    
    # 2. Build the connection string
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={host};"
        f"DATABASE={database};"
        f"USER={user};"
        f"PASSWORD={password};"
        f"OPTION=3;" # Option 3 enables dynamic cursors
    )
    
    try:
        conn = pyodbc.connect(conn_str)
        print(f"Successfully connected to {database} using {driver}")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None


#a list of all Tables for the 
table_list = [
"battery",
"electronic",
"mechanical",
"motor",
"part",
"progressupdates",
"robot",
"structural",
"`Sub-Assembly`",
"`Sub-Assembly-Hierarchy`",
"`Sub-Assembly-Parts`",
"suspension",
"team",
"teammanagers",
"teammember",
"wheel",]

# Usage
conn = get_mysql_connection('localhost', 'root', '1925', 'test')

cursor = conn.cursor()
"""
cursor.execute("select * from Part")

rows = cursor.fetchall()

for row in rows:
    print(row)"""
    
# a way to check inputs
def input_auth(input,table):
    if input.lower() in table:
        return input.lower()
    
# this while loop will be different in the final product
while True:
    # the options will be buttons
    print(f"""
      0. to exit
      1. to print all tables
      2. to print specific table
      3. add a robot, part or subassembly
      4. update a robot, part or subassembly
      
      """)
    # they will just click on the button
    user = int(input("what do you want do to: "))
    # each if statement would lead to a new different screen
    if user == 0:
        conn.close()
        break
    
    if user == 1:
        cursor.execute("SHOW TABLES")
        rows = cursor.fetchall()
        for row in rows:
            print(row[0])
    
    if user == 2:
        table = input("which table: ")
        cursor.execute(f"""SELECT * 
                           From {table} """)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            
    if user == 3:
        print(f"""
      0. to exit
      1. add a part
      2. add a sub-assembly
      3. add a robot
      """)
        selection = ""
        choice = int(input("what do you want do to: "))
        if choice == 0:
            pass
        elif choice == 1:
            #part is going to need to be overhauled
            selection = 'part'
            
            Id = int(input("ID: "))
            Name = input("Name: ")
            Weight = float(input("Weight: "))
            Length = float(input("Length: "))
            Height = float(input("Height: "))
            Width  = float(input("Width : "))
            
            cursor.execute(f"""INSERT INTO {selection}
                           (PartID, PartName, `Weight`, 
                           Height, `Length`, Width) VALUES  
                           (?,?,?,?,?,?)""",
                           Id,Name,Weight,Length,Height,Width)
            #this will be a list of all types when we make a gui
            print(f"""
                types:
                1. Electronic
                2. Battery
                3. Wheel
                4. Motor
                5. Suspension
                6. Structural
                """)
            Type = int(input("SubType: "))
            
            if Type == 1 and Type == 2:
                MaxVoltageV = float(input("Max Voltage: "))
                MaxCurrentA = float(input("Max Current: "))
                
                cursor.execute(f"""INSERT INTO Electronic
                        (PartID, MaxCurrentA,MaxVoltageV) VALUES  
                        (?,?,?)""",
                        Id,MaxCurrentA,MaxVoltageV)
                if Type == 2:
                    CapacitymAh = float(input("Capacity: "))
                    
                    cursor.execute(f"""INSERT INTO Battery
                           (PartID, CapacitymAh) VALUES  
                           (?,?)""",
                           Id,CapacitymAh)
            if Type == 3 and Type == 4 and Type == 5:
                cursor.execute(f"""INSERT INTO Mechanical
                            (PartID) VALUES  (?)""", Id)
                if Type == 3:
                    Radius = float(input("Radius: "))
                    WheelType = input("Wheel Type: ")
                    
                    cursor.execute(f"""INSERT INTO Wheel
                            (PartID, Radius, `Type`) VALUES 
                            (?,?,?)""", Id,Radius,WheelType)
                if Type == 4:
                    Torque = float(input("Torque: "))
                    
                    cursor.execute(f"""INSERT INTO Motor
                            (PartID, Torque) VALUES 
                            (?,?)""", Id,Torque)
                
                if Type == 5:
                    WeightLimit = float(input("WeightLimit: "))
                    
                    cursor.execute(f"""INSERT INTO Suspension
                            (PartID, WeightLimit) VALUES 
                            (?,?)""", Id,WeightLimit)
        elif choice == 2:
            selection = "`Sub-Assembly`"
            Id = int(input("ID: "))
            Name = input("Name: ")
            Version = int(input("Version: "))
            SAClassification = input("Classification: ")
            #this will be a list of all robots when we make a gui
            RobotId = int(input("RobotID: "))
            
            cursor.execute(f"""INSERT INTO {selection}
                           (SATypeID, SAName, `Version`, 
                           SAClassification, RobotID) VALUES  
                           (?,?,?,?,?)""",
                           Id,Name,Version,SAClassification,RobotId)
            
        elif choice == 3:
            selection = 'robot'
            
            Id = int(input("ID: "))
            Name = input("Name: ")
            cursor.execute(f"""INSERT INTO {selection}
                           (RobotID, RobotName) VALUES  
                           (?,?)""",
                           Id,Name)
            
        # test code to see if it actually added the tuple    
        cursor.execute(f"""SELECT * 
                           From {selection} """)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        
    if user == 4:
        print(f"""
      0. to exit
      1. modify a part
      2. modify a sub-assembly
      3. modify a robot
      """)
        selection = ""
        choice = int(input("what do you want do to: "))
        if choice == 0:
            pass
        elif choice == 1:
            #part is going to need to be overhauled
            selection = 'part'
            
            #this will be a list of all types when we make a gui
            print(f"""
                types:
                1. Electronic
                2. Battery
                3. Wheel
                4. Motor
                5. Suspension
                6. Structural
                """)
            Type = int(input("SubType: "))
            
            if Type == 1 and Type == 2:
                MaxVoltageV = float(input("Max Voltage: "))
                MaxCurrentA = float(input("Max Current: "))
                
                cursor.execute(f"""INSERT INTO Electronic
                        (PartID, MaxCurrentA,MaxVoltageV) VALUES  
                        (?,?,?)""",
                        Id,MaxCurrentA,MaxVoltageV)
                if Type == 2:
                    CapacitymAh = float(input("Capacity: "))
                    
                    cursor.execute(f"""INSERT INTO Battery
                           (PartID, CapacitymAh) VALUES  
                           (?,?)""",
                           Id,CapacitymAh)
            elif Type == 3 and Type == 4 and Type == 5:
                cursor.execute(f"""INSERT INTO Mechanical
                            (PartID) VALUES  (?)""", Id)
                if Type == 3:
                    Radius = float(input("Radius: "))
                    WheelType = input("Wheel Type: ")
                    
                    cursor.execute(f"""INSERT INTO Wheel
                            (PartID, Radius, `Type`) VALUES 
                            (?,?,?)""", Id,Radius,WheelType)
                elif Type == 4:
                    Torque = float(input("Torque: "))
                    
                    cursor.execute(f"""INSERT INTO Motor
                            (PartID, Torque) VALUES 
                            (?,?)""", Id,Torque)
                
                elif Type == 5:
                    WeightLimit = float(input("WeightLimit: "))
                    
                    cursor.execute(f"""INSERT INTO Suspension
                            (PartID, WeightLimit) VALUES 
                            (?,?)""", Id,WeightLimit)
        elif choice == 2:
            selection = "`Sub-Assembly`"
            Id = int(input("ID: "))
            Name = input("Name: ")
            Version = int(input("Version: "))
            SAClassification = input("Classification: ")
            #this will be a list of all robots when we make a gui
            RobotId = int(input("RobotID: "))
            
            cursor.execute(f"""INSERT INTO {selection}
                           (SATypeID, SAName, `Version`, 
                           SAClassification, RobotID) VALUES  
                           (?,?,?,?,?)""",
                           Id,Name,Version,SAClassification,RobotId)
            
        elif choice == 3:
            selection = 'robot'
            # this will be a list of all the robots and they select one and they will be able 
            print(f"""
                Input the properties of the robot you wish to modify
                1. ID
                2. Name
                3. Both
                """)
            property = int(input("properties: "))
            
            print(f"""
                Input the ID of the robot you wish to modify
                """)
            
            Id = int(input("ID: "))
            
            if property == 1:
                newID = int(input("New ID: "))
                cursor.execute(f"""UPDATE Robot
                               SET RobotID = ?  
                            WHERE RobotID = ?""",
                            newID,Id)
            elif property == 2:
                newName = input("New Name: ")
                cursor.execute(f"""UPDATE Robot
                               SET RobotName = ?  
                            WHERE RobotID = ?""",
                            newName,Id)
            elif property == 3:
                newID = int(input("New ID: "))
                newName = input("New Name: ")
                cursor.execute(f"""UPDATE Robot
                            SET RobotName = ? AND RobotID = ? 
                            WHERE RobotID = ?""",
                            newID,newName,Id)
            
        # test code to see if it actually added the tuple    
        cursor.execute(f"""SELECT * 
                           From {selection} """)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    
        
    
    
    