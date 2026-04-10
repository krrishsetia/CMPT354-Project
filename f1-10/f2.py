def f2_modify_part_subAssembly_robot(cursor):
    print(f"""
      0. to exit
      1. modify a part
      2. modify a sub-assembly
      3. modify a robot
      (you cannot modify the ID of anything)
      """)
    selection = ""
    choice = int(input("what do you want do to: "))
    if choice == 0:
        pass
    elif choice == 1:
        #part is going to need to be overhauled
        selection = 'part'
        
        print(f"""
            if you wish to modify the base properties of a part input the following
            else input 6
            Input the Base property of the part you wish to modify
            1. Name
            2. Weight
            3. Height
            4. Length
            5. Width
            6. SubType modifications 
            """)
        property = int(input("properties: "))
        
        print(f"""
            Input the ID of the Sub-Assembly you wish to modify
            """)
        
        Id = int(input("ID: "))
        
        if property == 1:
            newName = input("New Name: ")
            cursor.execute(f"""UPDATE part
                        SET PartName = ?  
                        WHERE PartID = ?""",
                        newName,Id)
        elif property == 2:
            newWeight = int(input("New Weight: "))
            cursor.execute(f"""UPDATE part
                        SET `Weight` = ?
                        WHERE PartID = ?""",
                        newWeight,Id)
        elif property == 3:
            newHeight = input("New Height: ")
            cursor.execute(f"""UPDATE part
                        SET Height = ?  
                        WHERE PartID = ?""",
                        newHeight,Id)
        elif property == 4:
            newLength = int(input("New Length: "))
            cursor.execute(f"""UPDATE part
                        SET `Length` = ?
                        WHERE PartID = ?""",
                        newRobotId,Id)
        elif property == 5:
            newWidth = input("New Width: ")
            cursor.execute(f"""UPDATE part
                        SET Width = ?  
                        WHERE PartID = ?""",
                        newWidth,Id)
        elif property == 6:
        
            # inputs id 7 times instead of doing id,id ..., id
            parmaInput = (Id,) * 7
            
            #select 'some string' will return said string if the where statment is true
            #dual means if you find the id, print 'x' once, it for things like this
            
            cursor.execute(f""" SELECT 'Battery' FROM DUAL WHERE EXISTS (SELECT 1 FROM Battery WHERE PartID = ?)
                                UNION ALL
                                SELECT 'Electronic' FROM DUAL WHERE EXISTS (SELECT 1 FROM Electronic WHERE PartID = ?)
                                UNION ALL
                                SELECT 'Mechanical' FROM DUAL WHERE EXISTS (SELECT 1 FROM Mechanical WHERE PartID = ?)
                                UNION ALL
                                SELECT 'Structural' FROM DUAL WHERE EXISTS (SELECT 1 FROM Structural WHERE PartID = ?)
                                UNION ALL
                                SELECT 'Wheel' FROM DUAL WHERE EXISTS (SELECT 1 FROM Wheel WHERE PartID = ?)
                                UNION ALL
                                SELECT 'Motor' FROM DUAL WHERE EXISTS (SELECT 1 FROM Motor WHERE PartID = ?)
                                UNION ALL
                                SELECT 'Suspension' FROM DUAL WHERE EXISTS (SELECT 1 FROM Suspension WHERE PartID = ?);
                        """,parmaInput) 
            
            rows = cursor.fetchall()
        
        if ('Battery',) in rows:
            print(f"""
            Input the property of the Battery you wish to modify
            1. Max Current
            2. Max Voltage
            3. Capacity
            """)
            
            subProperty = int(input("properties: "))
            
            if subProperty == 1:
                newCurrent = int(input("New Max Current: "))
                cursor.execute(f"""UPDATE Electronic
                            SET MaxCurrentA = ?
                            WHERE PartID = ?""",
                            newCurrent,Id)
            elif subProperty == 2:
                newVoltage = input("New Max Voltage: ")
                cursor.execute(f"""UPDATE Electronic
                            SET MaxVoltageV = ?  
                            WHERE PartID = ?""",
                            newVoltage,Id)
            elif subProperty == 3:
                newCapacity = int(input("New CapacitymAh: "))
                cursor.execute(f"""UPDATE Battery
                            SET CapacitymAh = ?
                            WHERE PartID = ?""",
                            newCapacity,Id)
        
        elif ('Electronic',) in rows:
            print(f"""
            Input the property of the Electronic you wish to modify
            1. Max Current
            2. Max Voltage
            """)
            
            subProperty = int(input("properties: "))
            
            if subProperty == 1:
                newCurrent = int(input("New Max Current: "))
                cursor.execute(f"""UPDATE Electronic
                            SET MaxCurrentA = ?
                            WHERE PartID = ?""",
                            newCurrent,Id)
            elif subProperty == 2:
                newVoltage = input("New Max Voltage: ")
                cursor.execute(f"""UPDATE Electronic
                            SET MaxVoltageV = ?  
                            WHERE PartID = ?""",
                            newVoltage,Id)
            
        elif ('Structural',) in rows:
            print(f"""
            Input the property of the Structural part you wish to modify
            1. Material
            2. Type
            """)
            
            subProperty = int(input("properties: "))
            
            if subProperty == 1:
                newMaterial = int(input("New Material: "))
                cursor.execute(f"""UPDATE Structural
                            SET Material = ?
                            WHERE PartID = ?""",
                            newMaterial,Id)
            elif subProperty == 2:
                newType = input("New Type: ")
                cursor.execute(f"""UPDATE Structural
                            SET `Type` = ?  
                            WHERE PartID = ?""",
                            newType,Id)
        
        elif ('Wheel',) in rows:
            print(f"""
            Input the property of the Wheel you wish to modify
            1. Radius
            2. `Type`
            """)
            
            subProperty = int(input("properties: "))
            
            if subProperty == 1:
                newRadius = int(input("New Radius: "))
                cursor.execute(f"""UPDATE Wheel
                            SET Radius = ?
                            WHERE PartID = ?""",
                            newRadius,Id)
            elif subProperty == 2:
                newType = input("New Type: ")
                cursor.execute(f"""UPDATE Wheel
                            SET `Type` = ?  
                            WHERE PartID = ?""",
                            newType,Id)
        elif ('Motor',) in rows:
            print(f"""
            Input the new torque for the motor
            """)
        
            newTorque = input("New Torque: ")
            cursor.execute(f"""UPDATE Motor
                        SET Torque = ?  
                        WHERE PartID = ?""",
                        newType,Id)
        elif ('Suspension',) in rows:
            print(f"""
            Input the new weight limit for the suspension
            """)
        
            newTorque = input("New Weight Limit: ")
            cursor.execute(f"""UPDATE Suspension
                        SET WeightLimit = ?  
                        WHERE PartID = ?""",
                        newType,Id)
            
    elif choice == 2:
        selection = "`Sub-Assembly`"
        
        print(f"""
            Input the property of the Sub-Assembly you wish to modify
            1. Name
            2. Version
            3. Classification
            4. RobotID
            """)
        property = int(input("properties: "))
        
        print(f"""
            Input the ID of the Sub-Assembly you wish to modify
            """)
        
        Id = int(input("ID: "))
        
        if property == 1:
            newName = input("New Name: ")
            cursor.execute(f"""UPDATE `Sub-Assembly`
                            SET SAName = ?  
                        WHERE SATypeID = ?""",
                        newName,Id)
        elif property == 2:
            newVersion = int(input("New Version: "))
            cursor.execute(f"""UPDATE `Sub-Assembly`
                        SET `Version` = ?
                        WHERE SATypeID = ?""",
                        newVersion,Id)
        elif property == 3:
            newClassification = input("New SAClassification: ")
            cursor.execute(f"""UPDATE `Sub-Assembly`
                        SET SAClassification = ?
                        WHERE SATypeID = ?""",
                        newClassification,Id)
        elif property == 4:
            newRobotId = int(input("New RobotId: "))
            cursor.execute(f"""UPDATE `Sub-Assembly`
                        SET RobotID = ?
                        WHERE SATypeID = ?""",
                        newRobotId,Id)
            
        
    elif choice == 3:
        selection = 'robot'
        # this will be a list of all the robots and they select one and they will be able 
        
        print(f"""
            Input the ID of the robot whose name you wish to modify
            
            """)
        
        Id = int(input("ID: "))

        newName = input("New Name: ")
        cursor.execute(f"""UPDATE Robot
                        SET RobotName = ?  
                    WHERE RobotID = ?""",
                    newName,Id)
        
