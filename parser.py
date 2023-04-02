import requests as req
import argparse as arg
import matplotlib.pyplot as plt
import json
from datetime import datetime as dt


def init_groups_id():

    groups_id_url = "https://ruz.spbstu.ru/api/v1/ruz/faculties/122/groups"
    groups_id_json = json.loads(req.get(groups_id_url).text)
    groups = {}
    for group in groups_id_json['groups']:
        groups[group['name']] = group['id']

    return groups


def schedule_parser_init():

    parser = arg.ArgumentParser()

    parser.add_argument('group_id', help='info about this group will be shown')
    parser.add_argument('date', help='week with this day will be shown')

    return parser.parse_args()


def check_if_data_right(args, groups_id):

    act_group = groups_id.get(args.group_id, -1)
    if (act_group == -1):
        raise ValueError('Invalid group id')

    try:
        act_day = dt.strptime(args.date, '%d.%m.%Y')
    except ValueError:
        raise ValueError('Invalid date')

    return act_group, act_day


def print_week_data(schedule_json):

    print(schedule_json['week']['date_start'], '-', schedule_json['week']['date_end'])
    print('Is odd :', schedule_json['week']['is_odd'], '\n')

    for i in range(len(schedule_json['days'])):
        day = schedule_json['days'][i]['weekday']
        lessons = schedule_json['days'][i]['lessons']

        print('Date :', schedule_json['days'][i]['date'], week_names[day])
        print('_____________________________________________________')

        for lesson in lessons:
            print(lesson['time_start'], '-', lesson['time_end'])
            print(lesson['subject'], '|', lesson['typeObj']['abbr'])

            if ('auditories' in lesson):
                print(lesson['auditories'][0]['name'], 'auditory')

            if (lesson['teachers'] is not None):
                for teacher in (lesson['teachers']):
                    print(teacher['full_name'])

            print()

        print()


def get_pairs_number(schedule_json):

    week_pairs = [i for i in range(0, 6)]
    for i in range(len(schedule_json['days'])):
        day = schedule_json['days'][i]['weekday']
        lessons = schedule_json['days'][i]['lessons']
        week_pairs[day - 1] = len(lessons)

    return week_pairs


def get_schedule_json(base_url, act_group, act_day):

    schedule = req.get(base_url + str(act_group) + '?date=' + str(dt.date(act_day)))

    return json.loads(schedule.text)


def show_week_histogramm(week_pairs, week_names):

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    left = [1, 2, 3, 4, 5, 6]
    plt.bar(left, week_pairs, tick_label=weekdays,
            width=0.6, color='grey')
    plt.ylabel('Pairs number')
    plt.xlabel("Week days")
    plt.title("Week load")
    plt.show()


if __name__ == "__main__":

    args = schedule_parser_init()
    groups_id = init_groups_id()
    base_url = 'https://ruz.spbstu.ru/api/v1/ruz/scheduler/'

    week_names = {1: 'Monday', 2: 'Tuesday',
                  3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

    act_group, act_day = check_if_data_right(args, groups_id)
    schedule_json = get_schedule_json(base_url, act_group, act_day)

    week_pairs = get_pairs_number(schedule_json)
    print_week_data(schedule_json)

    show_week_histogramm(week_pairs, week_names)
