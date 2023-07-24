#!/usr/bin/python3
'''
Uses a REST API to return info about an employees TODO list.
'''
import json
import requests
import sys

url = 'https://jsonplaceholder.typicode.com'


def get_user(user_id):
    '''GET information about a user

    Returns: True if user record is present
    '''
    url_path = '/users/{}'.format(user_id)
    response = requests.get(url + url_path)
    if response.status_code == 200:
        try:
            user = response.json()
        except json.decoder.JSONDecodeError:
            print("Error: Invalid JSON response (get_user)")
            user = None
    else:
        print("Failed to retrieve user. Status code: {}"
              .format(response.status_code))
        return None
    return user


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
    if len(sys.argv) < 2:
        print("Missing: Employee-ID")
        print("Usage: {} <Employee-ID>".format(sys.argv[0]))
        sys.exit(1)

    try:
        emp_id = int(sys.argv[1])
    except ValueError:
        print("Error: Employee-ID must be an integer")
        print("Usage: {} <Employee-ID>".format(sys.argv[0]))
        sys.exit(1)

    user = get_user(emp_id)
    if user:
        todo_list = get_user_todos(emp_id)
    else:
        print("No user found: {}".format(emp_id))
        sys.exit(0)

    json_file = "{}.json".format(emp_id)
    emp_tasks = []
    for task in todo_list:
        tmp_task = {"task": task.get('title'),
                    "completed": task.get('completed'),
                    "username": user.get('username'),
                    }
        emp_tasks.append(tmp_task)

    with open(json_file, 'w') as json_file:
        json.dump({emp_id: emp_tasks}, json_file)
