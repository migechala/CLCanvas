#!/bin/python3
try:
    import platform
    import requests
    from config import API_KEY
    import os
    import argparse

except ImportError as e:
    print("Some modules could not be imported from stdlib('sys' and 'os')")

school = ""

parser = argparse.ArgumentParser()

parser.add_argument('-s', "--school", type=str, help='mandatory argument school')
parser.add_argument("-ve", "--view_emails", action='store', const='NoValue', nargs='?')
parser.add_argument("-se", "--send_email", action="store_true")
parser.add_argument("-vg", "--view_grades", action="store_true")
parser.add_argument("-vtd", "--view_to_do", action="store_true")

args = parser.parse_args()

header = {'Authorization' : 'Bearer {}'.format(API_KEY)}
url = 'https://{}.instructure.com'.format(args.school)

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


def view_emails():
    inbox = get_inbox()
    for i in range(1, len(inbox)+1):
        current_mail = inbox[i-1]
        print("{}) {} -- {} << {}".format(i, current_mail["subject"], current_mail["participants"][0]["full_name"], current_mail["workflow_state"]))



if args.view_emails == "NoValue":
   view_emails()

if args.view_emails != "NoValue" and args.view_emails != None:
    term_size = os.get_terminal_size()
    inbox = get_inbox()
    mail = get_mail(inbox[int(args.view_emails)-1]["id"])
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