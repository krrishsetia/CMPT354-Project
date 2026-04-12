def f1_add_part_subAssembly_robot(cursor):
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
        Weight = float(input("Weight  : "))
        Length = float(input("Length  : "))
        Height = float(input("Height  : "))
        Width  = float(input("Width   : "))
        Quantity = int(input("Quantity:"))
        
        cursor.execute(f"""INSERT INTO {selection}
                        (PartID, PartName, `Weight`, 
                        Height, `Length`, Width, Quantity) VALUES  
                        (?,?,?,?,?,?,?)""",
                        Id,Name,Weight,Length,Height,Width,Quantity)
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
        