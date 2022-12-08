import csv
import random

from flask import render_template, request

from . import app


def get_students():
    with open('students.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


def get_students_dict():
    with open('students.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        return {row['fio']: int(row['id_task']) for row in reader}


def get_tasks():
    with open('tasks.txt') as file:
        data = file.read().strip().split('\n')

    if not data:
        return

    dct = {}
    for i in range(1, len(data), 2):
        dct[int(data[i - 1].split(' ')[-1])] = data[i]

    return dct


def get_free_tasks():
    return list(set(get_tasks().keys()) - set(map(lambda x: x[1], get_students_dict().items())))


def set_id_task(fio):
    students = get_students()
    free_tasks = get_free_tasks()
    if not free_tasks:
        return 'Нет свободных задач'

    with open('students.csv', 'wt') as csv_file:
        fieldnames = ['fio', 'id_task']
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()

        id_st = students.index({'fio': fio, 'id_task': '-1'})
        id_task = random.choice(free_tasks)
        students[id_st]['id_task'] = id_task

        for i in students:
            writer.writerow(i)

        return get_tasks()[id_task]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fio = request.form['student']
        if (id_task := get_students_dict()[fio]) == -1:
            task = set_id_task(fio)
        else:
            task = get_tasks()[id_task]

        return render_template('index.html', students=get_students(), task=task)

    return render_template('index.html', students=get_students())
