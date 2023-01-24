import win32gui
import pygetwindow as gw
import time
import pandas as pd

# python method
def main(**student_data):
    # printing the details
    print("\nStudent details:")
    # for loop to iterate
    #for key, value in student_data.values():
        #print("{} is {}".format(key,value))
    print(list(student_data.values())[0])
# calling the function
main(Name = "Bashir", age = 21, university = 'UCA')
main(Name = "Rt", age= 20, email = "alam23@gmail.com;")