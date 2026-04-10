def f5_add_or_remove_subassemblyHeirarchy(cursor):
    print(f"""
    0. to exit
    1. add child sub-assembly to sub-assembly
    2. remove child sub-assembly from sub-assembly
    """)
    choice = int(input("what do you want do to: "))
    if choice == 0:
        pass
    elif choice == 1:
        
        while True:
            print(f"""
                the Id of the child sub-assembly you wish to add
                """)
            ChildId = int(input("ChildID :"))
            
            print(f"""
                the Id of the Sub-Assembly you wish to add to
                """)
            ParentId = int(input("ParentID :"))
            
            cursor.execute(f"""INSERT INTO `Sub-Assembly-Hierarchy`
                    (ParentSATypeID, ChildPartID) VALUES  
                    (?,?)""",
                    ParentId,ChildId)
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
                the Id of the child sub-assembly you wish to remove
                """)
            ChildId = int(input("ChildID :"))
            
            print(f"""
                the Id of the Sub-Assembly you wish to remove from
                """)
            ParentId = int(input("ParentID :"))
            
            cursor.execute(f"""DELETE FROM `Sub-Assembly-Hierarchy`
                    WHERE ParentSATypeID = ? and ChildPartID = ?  """,
                    ParentId,ChildId)
            
            print(f"""would you like to remove more                      
                1. to continue
                2. to stop
                """)
            # will just be a popup with yes no
            stop = int(input("choice"))
            if stop == 2:
                break
    # test code to see if it actually added the tuple    
    cursor.execute(f"""SELECT * 
                        From {selection} """)
    rows = cursor.fetchall()
    for row in rows:
        print(row)