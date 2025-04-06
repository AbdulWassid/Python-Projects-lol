#Contact Book 

#Menu driven contact book
contacts = {}

while True:
    print("\nChoose an action:")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")

    choice = input("Your choice (1-5): ")
#defines the name (the key), defines the phone (the value), makes the dictionary called contacts each key has an associated value
    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        contacts[name] = phone
    elif choice == "2":
        for name, phone in contacts.items():
            print(f"{name} → {phone}")
# Uses a dictionary to search (key or name) for a contact (the phone # ) then displays it 
    elif choice == "3":
        search = input("Search name: ")
        if search in contacts:
            print(f"{search}: {contacts[search]}")
        else:
            print("Not found.")
#defines the delete option, uses del to delete the things from the contact list (the dictionary) 
    elif choice == "4":
        delete = input("Delete name: ")
        if delete in contacts:
            del contacts[delete]
            print("Deleted.")
        else:
            print("Not found.")
 # When the user selects 5 it will print Goodbye! then exit                
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")