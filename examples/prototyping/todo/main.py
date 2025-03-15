# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pyscript import document
from guara.transaction import Application
import transactions as transactions

# For front-end
app = Application(transactions.ToDoPrototype())


def add_task(event):
    try:
        task = document.querySelector("#task").value
        # This is the `Application` involker being used to bind the transations
        # with the front-end
        app.at(transactions.Add, task=task)
        document.querySelector("#output").innerText = f"Task '{task}' added"
    except Exception as e:
        document.querySelector("#output").innerText = str(e)


def remove_task(event):
    try:
        task = document.querySelector("#task").value
        app.at(transactions.Remove, task=task)
        document.querySelector("#output").innerText = f"Task '{task}' removed"
    except Exception as e:
        document.querySelector("#output").innerText = str(e)


def print_task_dict(event):
    document.querySelector("#output").innerText = app.at(transactions.PrintDict).result


def list_tasks(event):
    document.querySelector("#output").innerText = app.at(transactions.ListTasks).result


def get_task(event):
    index = document.querySelector("#index-input").value
    if not index:
        index = 0
    index = int(index)
    # index = int(value) - 1
    document.querySelector("#output").innerText = app.at(transactions.GetBy, index=index).result
