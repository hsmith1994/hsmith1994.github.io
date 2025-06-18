""""
Hunter Smith
Dr Maciosek
CS499
5/23/2025
"""
# imports pymongo
import pymongo

# Imports os required for secure credential handling
import os

# Load secure MongoDB credentials from environment variables
username = os.getenv("MONGO_USER", "groom_user")
password = os.getenv("MONGO_PASS", "Securepa$$word123")
host = "localhost"
port = 27017


# Construct MongoDB URI with authentication
uri = f"mongodb://{username}:{password}@{host}:{port}/pet_grooming"


# Connects to MongoDB securely
client = pymongo.MongoClient(uri)
db = client["pet_grooming"]
pets_collection = db["pets"]


# pet class
class Pet:
    # class constants
    dog_space = 30
    cat_space = 12
    base_fee_per_day = 25
    grooming_fee = 20

    def __init__(self, pet_type, pet_name, pet_age, days_stay, checked_in=True):
        # instance attributes
        self.pet_type = pet_type
        self.pet_name = pet_name
        self.pet_age = pet_age
        self.days_stay = days_stay
        self.amount_due = 0.0
        self.checked_in = checked_in

    # Method that converts the pet object to a dictionary data structure for MongoDB
    def to_dict(self):
        return {
            "pet_type": self.pet_type,
            "pet_name": self.pet_name,
            "pet_age": self.pet_age,
            "days_stay": self.days_stay,
            "amount_due": self.amount_due,
            "checked_in": True
        }

    # Class method that converts Mongo document into a pet object
    @classmethod
    def from_dict(cls, data):
        pet = cls(
            pet_type=data.get("pet_type", ""),
            pet_name=data.get("pet_name", ""),
            pet_age=data.get("pet_age", 0),
            days_stay=data.get("days_stay", 0),
            checked_in=data.get("checked_in", True)
        )
        pet.amount_due = data.get("amount_due", 0.0)
        return pet

    # Method that calculates amount due based on days stayed and if grooming was required
    def calculate_amount_due(self):
        self.amount_due = self.days_stay * Pet.base_fee_per_day
        if self.pet_type == "dog" and self.days_stay >= 3:
            self.amount_due += Pet.grooming_fee
        return self.amount_due

    # Method that gets current count of dogs checked in
    def get_dog_count(self):
        return pets_collection.count_documents({"pet_type": "dog", "checked_in": True})

    # Method that gets current count of cats checked in
    def get_cat_count(self):
        return pets_collection.count_documents({"pet_type": "cat", "checked_in": True})

    # Method used to check in pets
    def check_in(self):
        # Checks how many pets are currently checked in
        dog_count = self.get_dog_count()
        cat_count = self.get_cat_count()

        # Debug output
        print(f"Debug: dog_count={dog_count}, cat_count={cat_count}")

        # Checks availability based on pet type
        if self.pet_type == "dog" and dog_count >= Pet.dog_space:
            print("No space available for dogs.")
            return
        elif self.pet_type == "cat" and cat_count >= Pet.cat_space:
            print("No space available for cats.")
            return

        # Inserts new pet into the database
        pets_collection.insert_one(self.to_dict())
        print(f"{self.pet_type.title()} '{self.pet_name}' is checked in.")

    # Method that updates pet information
    def update_pet(self, new_pet_name=None, new_pet_age=None, new_days_stay=None):
        updates = {}
        if new_pet_name is not None:
            self.pet_name = new_pet_name
            updates["pet_name"] = new_pet_name
        if new_pet_age is not None:
            self.pet_age = new_pet_age
            updates["pet_age"] = new_pet_age
        if new_days_stay is not None:
            self.days_stay = new_days_stay
            updates["days_stay"] = new_days_stay

        if updates:
            pets_collection.update_one(
                {"pet_name": self.pet_name},
                {"$set": updates}
            )
            print(f"Pet '{self.pet_name}' information updated.")

    # Method used to check out pet and calculate amount due
    def check_out(self):
        self.calculate_amount_due()

        # Updates the pet record in MongoDB
        result = pets_collection.update_one(
            {"pet_name": self.pet_name, "checked_in": True},
            {"$set": {
                "checked_in": False,
                "amount_due": self.amount_due,
                "days_stay": self.days_stay
            }}
        )

        # Print checkout result
        if result.modified_count > 0:
            print(f"{self.pet_type.title()} '{self.pet_name}' is checked out.")
            print(f"Amount due: ${self.amount_due:.2f}")
            return True
        # Exits if pet name is not currently checked in
        else:
            print(f"{self.pet_name} is not currently checked in.")
            return False
