print("Hello World!" , end=" ")
print("I will print on the same line.")

print("i am" , 22 , "years old")

x, y, z = "Orange", 2 , "Cherry" #Many Values to Multiple Variables
print(x)
print(y)
print(z)


#Unpack a Collection
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)


x = "awesome" #global

def myfunc():
  x = "fantastic" #local
  print("Python is " + x)

myfunc()

print("Python is " + x)

import random #print random number
print(random.randrange(1, 10))

txt = "The best things in life are free!"
print("free" in txt)  #in used

txt = "The best things in life are free!"
print("expensive" not in txt) #not in is used

b = "Hello, World!"  #slicing
print(b[2:5])

age = 36  #fstring is used to use variable with string
txt = f"My name is John, I am {age}"
print(txt)

price = 59.34345  #placeholder and modifier
txt = f"The price is {price:.2f} dollars"
txxt = f"The price is {price} dollars"
print(txt)
print(txxt)

class InternshipTask:
    def __init__(self, task_name, hours_allocated):
        self.task_name = task_name
        self.hours_allocated = hours_allocated
        self.is_completed = False

    def mark_completed(self):
        self.is_completed = True
        print(f"✅ Task '{self.task_name}' is now marked as completed!")

    def display_info(self):
        status = "Done" in ["Done" if self.is_completed else "Pending"][0]
        print(f"Task: {self.task_name} | Hours: {self.hours_allocated}h | Status: {status}")


def calculate_total_hours(task_list):
    """Calculates total hours using a loop and exception handling."""
    total = 0
    for t in task_list:
        try:
            total += t.hours_allocated
        except TypeError:
            print("⚠️ Warning: Invalid hour format found!")
    return total


# --- Running the Script ---
if __name__ == "__main__":
    print("--- Initializing Internship Tracker ---")
    
    # Creating objects from our class
    task1 = InternshipTask("Python & Dev Foundations", 5)
    task2 = InternshipTask("Mathematics & Data Handling", 10)
    
    # Using methods
    task1.display_info()
    task2.display_info()
    
    task1.mark_completed()
    
    # Using a function with a list of objects
    all_tasks = [task1, task2]
    total_time = calculate_total_hours(all_tasks)
    print(f"\nTotal planned hours for these tasks: {total_time} hours")