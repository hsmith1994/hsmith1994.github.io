import re  # imports the regular expression module
from PetGrooming import Pet, pets_collection  # imports the pet class and pet collection


# Allows only alphanumeric characters
def sanitize_input(user_input):
    return re.sub(r"[^a-zA-Z0-9 _-]", "", user_input)


# Displays main menu options
def display_menu():
    print("\n*** Pet Grooming Menu ***")
    print("1. Check-in pet")
    print("2. Check-out pet")
    print("3. Update checked-in pet")
    print("4. View all checked in pets")
    print("5. Exit")


# Accepts user input with basic validation and sanitization
def check_in_pet():
    # Prompts user for pet type and sanitizes the input
    pet_type = sanitize_input(input("Enter pet type (dog/cat): "))
    # Validates the pet input type
    if pet_type not in ["dog", "cat"]:
        # Exits if invalid pet type is input
        print("Invalid pet type. Must be a 'dog' or a 'cat'.")
        return

    # Prompt for pet name and sanitizes the input
    pet_name = sanitize_input(input("Enter pet name: "))
    # Exits if invalid name is input
    if not pet_name:
        print("Pet name cannot be empty.")
        return

    # Prompts for pet age and pet stay numeric inputs and converts them
    try:
        pet_age = int(input("Enter pet age: "))
        days_stay = int(input("Enter the number of days staying: "))
    # Handles invalid number inputs and exits if invalid
    except ValueError:
        print("Invalid numeric input. Please enter valid numbers for age and days staying.")
        return

    # Create and checks in the pet
    pet = Pet(pet_type, pet_name, pet_age, days_stay)
    pet.check_in()


# Finds and checks out pet by name
def check_out_pet():
    # Prompts user for name of pet they want to check out
    pet_name = sanitize_input(input("Enter the name of pet ready to be checked out: "))
    # Query the database to ensure pet is checked in
    doc = pets_collection.find_one({"pet_name": pet_name, "checked_in": True})
    # Converts the MongoDB document to find a pet object to check out
    if doc:
        pet = Pet.from_dict(doc)
        # Checks out the pet and removes it from the database
        if pet.check_out():
            pets_collection.delete_one({"pet_name": pet_name})
            print(f"Pet '{pet_name}' has been checked out and removed from the system.")
    # Breaks if no pet is checked in
    else:
        print(f"No checked-in pet named '{pet_name}' found.")


# Updates existing pet data by name
def update_pet_info():
    # Prompts user for name of pet they want to update
    pet_name = sanitize_input(input("Enter the name of the pet you want to update:"))
    # Query the database to ensure pet is checked in before updating
    doc = pets_collection.find_one({"pet_name": pet_name, "checked_in": True})
    # Exits if no matching pet is found
    if not doc:
        print(f"No checked-in pet named '{pet_name}' found.")
        return

    # Converts the MongoDB document to a pet object for updating and prompts for updating fields
    pet = Pet.from_dict(doc)
    new_name = sanitize_input(input("Enter new pet name (Leave blank to keep current): "))
    new_age = input("Enter new age (Leave blank to keep current): ")
    new_days = input("Enter new days staying (Leave blank to keep current): ")

    # Converts inputs if provided, otherwise keeps fields the same
    try:
        new_age_val = int(new_age) if new_age else None
        new_days_val = int(new_days) if new_days else None
    # Exit if the input is invalid
    except ValueError:
        print("Invalid numeric input. Please enter valid numbers for age and/or days stayed.")
        return

    # Updates the database if name is being changed
    if new_name:
        pets_collection.update_one(
            {"pet_name": pet.pet_name, "checked_in": True},
            {"$set": {"pet_name": new_name}}
        )
        pet.pet_name = new_name

    # Calls the update pet method
    pet.update_pet(new_pet_age=new_age_val, new_days_stay=new_days_val)


# Print all currently checked-in pets
def view_checked_in_pets():
    # Menu to select sorting options for viewing checked in pets
    print("\nSort by: ")
    print("1. Pet Type")
    print("2. Pet Name")
    print("3. Pet Age")
    print("4. Days staying")
    choice = input("Select a sorting option (1-4): ")

    # Maps the user input to a corresponding MongoDB field
    sort_field = {
        # Sorts by pet type
        "1": "pet_type",
        # Sorts by pet name
        "2": "pet_name",
        # Sorts by pet age
        "3": "pet_age",
        # Sorts by days staying
        "4": "days_stay"
        # Default to pet name if the choice is invalid
    }.get(choice, "pet_name")

    print("\nCurrently checked-in pets:")
    # Query the database for all checked in pets and sorts them based on user input
    for doc in pets_collection.find({"checked_in": True}).sort(sort_field):
        pet = Pet.from_dict(doc)
        print(f"{pet.pet_type.title()} named {pet.pet_name}, Age {pet.pet_age}, staying {pet.days_stay} days.")


# Main loop for user interaction
def main():
    while True:
        # Displays the available menu options
        display_menu()
        choice = input("Select an option (1-5): ")

        # Calls check in method
        if choice == "1":
            check_in_pet()
        # Calls check out method
        elif choice == "2":
            check_out_pet()
        # Calls update method
        elif choice == "3":
            update_pet_info()
        # Calls checked in pets method
        elif choice == "4":
            view_checked_in_pets()
        # Exits the loop and terminates the program
        elif choice == "5":
            print("Exiting system. Have a nice day!")
            break
        # Handles input validation
        else:
            print("Invalid choice. Please select a valid option")


# Runs the main function
if __name__ == "__main__":
    main()