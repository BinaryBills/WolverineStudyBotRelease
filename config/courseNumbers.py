#Author: BinaryBills
#Creation Date: March 1, 2023
#Date Modified: March 7, 2023
#Purpose: Contains all course numbers associated with a department! This allows for you to 
# easily add course numbers for the initialize_courses function. If you want to add a new department
#you must add it in settings.py.

def getCourseNumberList(department):
    """Given the department, returns list of course numbers.
    The logic is simple here for the programmer to easily add new courses."""
    if department == "CIS":
        CIS_LIST = ["150", "200", "275", "285", "296","298","306","310","350", "375", "427", "435","436", "450", "479"]
        return CIS_LIST
    elif department == "ENGR":
        ENGR_LIST = ["400","493"]
        return ENGR_LIST
    elif department == "IMSE":
        ENGR_LIST = ["400","350", "317"]
        return ENGR_LIST
    elif department == "GEOL":
        ENGR_LIST = ["118","218"]
        return ENGR_LIST
