#!/bin/python3
import requests
from config import API_KEY

header = {'Authorization' : 'Bearer {}'.format(API_KEY)}
def get(url):
    return requests.get(url, headers=header)
#get all courses
url = 'https://overlake.instructure.com'
courses = get(url+"/api/v1/courses").json

print("Current classes")
for i in range(0, len(courses)):
    course = ""
    course_id = i['id']
    course_grade = -1
    grades = get(url+"/api/v1/users/5415/enrollments")
    print("{} -- id: {} -- with grade: {}".format(i["name"], i['id'], grades.json()[0]["grades"]["current_score"]))
    
