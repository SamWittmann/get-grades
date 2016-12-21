from selenium import webdriver
from threading import Timer
from datetime import datetime


"""
Created by Sam Wittmann, Rice University, December 2016
Feel free to share with other Rice people eagerly awaiting their final grades
"""
# initialize prev_grades to an empty list
prev_grades = []

# initializes the number of checks to 0
num_checks = 0


def get_grades():
    """
    Checks Esther for final grades
    """
    # create Chrome browser
    driver = webdriver.Chrome('C:\\Users\Sam\Desktop\PythonStuff\chromedriver')

    # open ESTHER
    driver.get("https://esther.rice.edu/selfserve/twbkwbis.P_WWWLogin")

    # find fields for Student ID and Password
    id_element = driver.find_element_by_name("sid")
    pw_element = driver.find_element_by_name("PIN")

    # input Student ID and password
    id_element.send_keys("ENTER STUDENT ID HERE")
    pw_element.send_keys("ENTER ESTHER PASSWORD HERE")

    # click the login button
    driver.find_element_by_xpath("/html/body/div[3]/form/p/input[1]").click()

    # go to grades page
    driver.get("https://esther.rice.edu/selfserve/!ru_bwgksrvy.main")

    # collect course titles into a list
    titles = driver.find_elements_by_class_name("complete")
    titles_list = [x.text for x in titles]

    # collect grades into a list
    grades = driver.find_elements_by_class_name("data")
    grades_list = [x.text for x in grades if x.text != "Yes"]

    # close the browser now that the required information has been collected
    driver.close()

    # the first time grades are checked, prev_grades is initialized to be different from the scraped grades so that
    # the grades are always printed the first iteration
    global prev_grades
    if num_checks == 0:
        prev_grades = list(grades_list) + ["delta"]

    # if new grades have been entered, print them
    if grades_list != prev_grades:
        for idx in range(len(titles_list)):
            print(titles_list[idx] + ": " + grades_list[idx])

    # update the previous grades
    prev_grades = grades_list

    # create and begin a timer that will check for new grades every 10 minutes
    timer = Timer(5.0, get_grades)
    timer.start()

    # increments the number of checks each time data is scraped, printing the time of the last scrape each 4 scrapes
    global num_checks
    num_checks += 1
    if num_checks % 4 == 0:
        print(datetime.now().time())

# run the script
get_grades()
