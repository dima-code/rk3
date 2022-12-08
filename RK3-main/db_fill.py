import csv

with open('students.csv', 'wt') as csv_file:
    fieldnames = ['fio', 'id_task']
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()

    for i in (
            {'fio': 'Еселидзе Дмитрий Вахтангович', 'id_task': -1},
            {'fio': 'Петров Петр Петрович', 'id_task': -1},
            {'fio': 'Иванов Иван Иванович', 'id_task': -1},
    ):
        writer.writerow(i)
