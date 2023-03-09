#!/bin/python3
import platform
import sys
import requests
from config import API_KEY
import os
header = {'Authorization' : 'Bearer {}'.format(API_KEY)}
url = 'https://{}.instructure.com'.format(sys.argv[1])
def clear():
    os.system('cls||clear')


def get(endpoint):
    return requests.get(url+endpoint, headers=header)

def post(endpoint, body):
    return requests.post(url+endpoint, headers=header, json=body)

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

def get_todo_count():
    return get("/api/v1/users/self/todo_item_count").json()["assignments_needing_submitting"]

def get_todo():
    return get("/api/v1/users/self/todo").json()

def get_inbox():
    return get("/api/v1/conversations").json()

def get_mail(id):
    return get("/api/v1/conversations/{}".format(id)).json()

def send_mail(address: list, subject, body):
    return post("/api/v1/conversations", {"subject": subject, "recipients": address, "body": body})

def homepage():
    selection = -1
    while selection == -1:
        selection = input("1) View grades\n2) View to do\n3) View emails\n4) Send emails\nSelection: ")
        clear()
        match selection:
            case '1':
                grades()
            case '2':
                to_do()
            case '3':
                view_emails()
            case '4':
                send_email()
            case _:
                selection = -1
        

def grades():
    courses = get_courses_data()

    for i in range(1, len(courses)+1):
        print("{}) {}".format(i, courses[i-1]["name"]))
    print("{}) <- Back".format(len(courses)+1))
    selection = -1
    while not 1 <= int(selection) <= len(courses)+1:
        selection = input("Which course would you like to see?: ")
    clear()
    if(int(selection) == len(courses)+1):
        homepage()
    print()
    print("Your grade is a {}%".format(get_grade(courses[int(selection)-1]["id"])))
    input("Press enter to return...")
    clear()
    homepage()

def to_do():
    print("{} assignments need submitting:".format(get_todo_count()))
    for i in get_todo():
        print("{}".format(i["assignment"]["name"]))
    input("Press enter to return...")
    clear()
    homepage()

def send_email():
    courses = get("/api/v1/users/self/courses?per_page=20&include=can_message").json()
    for i in range(1, len(courses)+1):
        print("{}) {}".format(i, courses[i-1]["name"]))
    print("{}) <- Back".format(len(courses)+1))
    selection = -1
    while not 1 <= int(selection) <= len(courses)+1:
        selection = input("Which course would you like to select?: ")
    clear()
    if(int(selection) == len(courses)+1):
        homepage()
    selected_id = courses[int(selection)-1]["id"]
    endpoint = "/api/v1/search/recipients?search=&per_page=50&permissions[]=send_messages_all&messageable_only=true&synthetic_contexts=true&context=course_{}_students".format(selected_id)
    students = get(endpoint).json()
    for i in range (1, len(students)+1):
        print("{}) {}".format(i, students[i-1]["name"]))
    student_id = students[int(input("Which student would you like to message?: "))-1]["id"]
    print(send_mail([student_id], input("Suject: "), input("Body: ")))
    input("Press enter to return...")
    clear()
    homepage()

def view_emails():
    term_size = os.get_terminal_size()
    inbox = get_inbox()
    selection = -1
    for i in range(1, len(inbox)+1):
        current_mail = inbox[i-1]
        print("{}) {} -- {} << {}".format(i, current_mail["subject"], current_mail["participants"][0]["full_name"], current_mail["workflow_state"]))
    
    print("{}) <- Back".format(len(inbox)+1))
    
    while not 1 <= int(selection) <= len(inbox)+1:
        selection = input("Which email would you like to see?")
    
    clear()
    if(int(selection) == len(inbox)+1):
        homepage()

    mail = get_mail(inbox[int(selection)-1]["id"])
    command = "cat temp | less"
    if platform.system() == "Windows":
        command = "type temp | more"
    
    with open('temp', 'w') as f:
        f.write(mail["subject"])
        f.write("\n")
        f.write('=' * term_size.columns)
        f.write("\n")
        f.write("\n")
        f.write("\n")

        for i in reversed(mail["messages"]):
            f.write(i["created_at"])
            f.write("\n")
            f.write(i["body"])
            f.write("\n")
            f.write("\n")
            f.write('=' * term_size.columns)
            f.write("\n")

        
    os.system(command)
    os.remove("temp")
    clear()
    homepage()

if __name__ == "__main__":
    clear()
    homepage()