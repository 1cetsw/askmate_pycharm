import csv
import os
import sys
sys.path.append("./")
DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_HEADER = ['id', 'title', 'message','image']
STATUSES = ['planning', 'todo', 'in progress', 'review', 'done']


def get_all_user_question(filename):
    dict_list = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict_list.append(row)
    return dict_list

def write_user_question(filename, mylist):
    count = len(get_all_user_question(filename))
    mylist.insert(0, count + 1)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = DATA_HEADER
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        to_write = dict(zip(DATA_HEADER, mylist))
        writer.writerow(to_write)

def change_user_question(filename, mylist):
    dict_list = get_all_user_question(filename)
    for line in dict_list:
        if line['id'] == mylist[0]:
            line['submission_time'] = mylist[1]
            line['vote_number'] = mylist[2]
            line['question_id'] = mylist[3]
            line['message'] = mylist[4]
            line['image'] = mylist[5]

    with open(filename, 'w', newline='') as csv_file:
        fieldnames = DATA_HEADER
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for dict in dict_list:
            writer.writerow({'submission_time': dict['submission_time'], 'vote_number': dict['vote_number'],
                         'question_id': dict['question_id'],
                         'message': dict['message'], 'image': dict['image']})


