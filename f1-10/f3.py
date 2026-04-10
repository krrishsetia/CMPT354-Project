def f3_delete_part_subAssembly_robot(cursor):
    # might need to be updated
    print(f"""
    0. to exit
    1. delete a part
    2. delete a sub-assembly
    3. delete a robot
    """)
    selection = ""
    choice = int(input("what do you want do to: "))
    if choice == 0:
        pass
    elif choice == 1:
        #part is going to need to be overhauled
        selection = 'part'            
    elif choice == 2:
        selection = "`Sub-Assembly`"
        
    elif choice == 3:
        selection = 'robot'
    
    Id = int(input("ID: "))
        
    cursor.execute(f"""DELETE FROM {selection}
                        WHERE ID = ?)""",
                        Id)
    
    