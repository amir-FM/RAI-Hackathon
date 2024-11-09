class Spendings:
   
    def __init__(self):
        self.salary = 0
        self.free = 0


        self.totalSpent = 0


        self.Healthcare = 0
        self.Education = 0
        self.FoodAndDrinks = 0
        self.RestaurantsOrCoffeShops = 0
        self.Bills = 0
        self.Entertainment = 0
        self.Shopping = 0
        self.Transport = 0


        self.HealthcarePercentage = 0
        self.EducationPercentage = 0
        self.FoodAndDrinksPercentage = 0
        self.RestaurantsOrCoffeShopsPercentage = 0
        self.BillsPercentage = 0
        self.EntertainmentPercentage = 0
        self.ShoppingPercentage = 0
        self.TransportPercentage = 0
        self.freePercentage = 0



    def add_to_field(self, field_name, amount):
        # Check if the field exists in the object
        if hasattr(self, field_name):
            # Get the current value of the field
            current_value = getattr(self, field_name)
            # Add the given amount to the field
            setattr(self, field_name, current_value + amount)
            # Optionally, update the total spent field
            self.totalSpent += amount
        else:
            print(f"Field '{field_name}' does not exist in the Spendings class.")

    def str(self):
        return (f"Total Spent: {self.totalSpent}\n"
                f"Healthcare: {self.Healthcare}\n"
                f"Education: {self.Education}\n"
                f"Food and Drinks: {self.FoodAndDrinks}\n"
                f"Restaurants or Coffee Shops: {self.RestaurantsOrCoffeShops}\n"
                f"Bills: {self.Bills}\n"
                f"Entertainment: {self.Entertainment}\n"
                f"Shopping: {self.Shopping}\n"
                f"Transport: {self.Transport}")
    

    def update_percentages(self):
        # Avoid division by zero
        if self.salary > 0:
            self.HealthcarePercentage = (self.Healthcare / self.salary) * 100
            self.EducationPercentage = (self.Education / self.salary) * 100
            self.FoodAndDrinksPercentage = (self.FoodAndDrinks / self.salary) * 100
            self.RestaurantsOrCoffeShopsPercentage = (self.RestaurantsOrCoffeShops / self.salary) * 100
            self.BillsPercentage = (self.Bills / self.salary) * 100
            self.EntertainmentPercentage = (self.Entertainment / self.salary) * 100
            self.ShoppingPercentage = (self.Shopping / self.salary) * 100
            self.TransportPercentage = (self.Transport / self.salary) * 100
            self.freePercentage = (self.free / self.salary) * 100

    def percentages_str(self):
        return (f"Healt\
                hcare: {self.HealthcarePercentage:.2f}%\n"
                f"Education: {self.EducationPercentage:.2f}%\n"
                f"Food and Drinks: {self.FoodAndDrinksPercentage:.2f}%\n"
                f"Restaurants or Coffee Shops: {self.RestaurantsOrCoffeShopsPercentage:.2f}%\n"
                f"Bills: {self.BillsPercentage:.2f}%\n"
                f"Entertainment: {self.EntertainmentPercentage:.2f}%\n"
                f"Shopping: {self.ShoppingPercentage:.2f}%\n"
                f"Transport: {self.TransportPercentage:.2f}%\n"
                f"Economies: {self.freePercentage:.2f}%")
    