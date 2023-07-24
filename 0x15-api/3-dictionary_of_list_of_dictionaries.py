#!/usr/bin/python3
'''
Uses a REST API to return info about an employees TODO list.
Data is exported in JSON format.
'''
import json
import requests
import sys

url = 'https://jsonplaceholder.typicode.com'


def get_users():
    '''GET information about all users
    '''
    url_path = '/users'
    response = requests.get(url + url_path)
    if response.status_code == 200:
        try:
            users = response.json()
        except json.decoder.JSONDecodeError:
            print("Error: Invalid JSON response (get_users)")
            users = None
    else:
        print("Failed to get users. Status code: {}"
              .format(response.status_code))
        return None
    return users


def get_user_todos(user_id):
    '''GET a user's to-do list
    '''
    url_path = '/users/{}/todos'.format(user_id)
    response = requests.get(url + url_path)
    if response.status_code == 200:
        try:
            todo_list = response.json()
        except json.decoder.JSONDecodeError:
            print("Error: Unable to parse JSON response")
            todo_list = None
    else:
        print("Failed to retrieve data. Status code: {}"
              .format(response.status_code))
        return None
    return todo_list


if __name__ == "__main__":
    users = get_users()
    if not users:
        print("No user found: {}".format(emp_id))
        sys.exit(0)

    json_file = "todo_all_employees.json"
    employees = {}
    for user in users:
        user_todos = get_user_todos(user.get('id'))
        user_tasks = [{"task": task.get('title'),
                       "completed": task.get('completed'),
                       "username": user.get('username'),
                       } for task in user_todos]
        employees[user.get('id')] = user_tasks

    with open(json_file, 'w') as json_file:
        json.dump(employees, json_file)
