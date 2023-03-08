#!/bin/python3
import json
import sys
import requests
from config import API_KEY

header = {'Authorization' : 'Bearer {}'.format(API_KEY)}
url = 'https://{}.instructure.com'.format(sys.argv[1])
def get(endpoint):
    return requests.get(url+endpoint, headers=header)

def get_user_id() -> int:
    return get("/api/v1/users/self").json()["id"]


def get_courses_data():
    return get("/api/v1/courses/").json()

def get_specific_course_data(id):
    for i in get_courses_data():
        if i["id"] == id:
            return i

def get_course_enrollment_all_students(id):
    return get("/api/v1/courses/{}/enrollments".format(str(id))).json()

def get_course_enrollment():
    return get("/api/v1/users/{}/enrollments".format(get_user_id())).json()

def get_grade(id):
    for i in get_course_enrollment():
        if i["course_id"] == id:
            return i["grades"]["current_score"]

def homepage():
    selection = -1
    while selection == -1:
        selection = input("1) View grades\n2) View to do\n3) View emails\nSelection: ")
        print(selection)
        match selection:
            case '1':
                grades()
            case '2':
                to_do()
            case '3':
                view_emails()
            case _:
                selection = -1

def grades():
    courses = get_courses_data()

    for i in range(1, len(courses)+1):
        print("{}) {}".format(i, courses[i-1]["name"]))

    selection = -1
    while not 1 <= int(selection) <= len(courses)+1:
        selection = input("Which course would you like to see?: ")
    print(get_grade(courses[int(selection)-1]["id"]))

def to_do():
    get()

def view_emails():
    get()

if __name__ == "__main__":
    homepage()