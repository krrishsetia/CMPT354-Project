def f4_add_or_remove_parts_from_subAssembly(cursor):
    print(f"""
      0. to exit
      1. add parts to sub-assembly
      2. remove parts from sub-assembly
      """)
    choice = int(input("what do you want do to: "))
    if choice == 0:
        pass
    elif choice == 1:
        
        while True:
            print(f"""
                    the Id of the part you wish to add
                    """)
            PartId = int(input("PartID :"))
            
            print(f"""
                    the Id of the Sub-Assembly you wish to add to
                    """)
            SATypeId = int(input("SATypeID :"))
            
            cursor.execute(f"""INSERT INTO `Sub-Assembly-Parts`
                        (SATypeID, PartID) VALUES  
                        (?,?)""",
                        SATypeId,PartId)
            print(f"""would you like to add more                      
                    1. to continue
                    2. to stop
                    """)
            # will just be a popup with yes no
            stop = int(input("choice"))
            if stop == 2:
                break
            
            
    elif choice == 2:
        while True:
            print(f"""
                    the Id of the part you wish to remove
                    """)
            PartId = int(input("PartID :"))
            
            print(f"""
                    the Id of the Sub-Assembly you wish to remove from
                    """)
            SATypeId = int(input("SATypeID :"))
            
            cursor.execute(f"""DELETE FROM `Sub-Assembly-Parts`
                        WHERE SATypeID = ? and PartID = ?  """,
                        SATypeId,PartId)
            
            print(f"""would you like to remove more                      
                    1. to continue
                    2. to stop
                    """)
            # will just be a popup with yes no
            stop = int(input("choice"))
            if stop == 2:
                break