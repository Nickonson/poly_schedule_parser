import requests as req
import argparse as arg
import matplotlib.pyplot as plt
import json
from datetime import datetime as dt

parser = arg.ArgumentParser()

parser.add_argument('group_id', help='info about this group will be shown')
parser.add_argument('date', help='week with this day will be shown')

args = parser.parse_args()

base_url = 'https://ruz.spbstu.ru/api/v1/ruz/scheduler/'

groups = {'4831001/10001': 35287,
          '4831001/10002': 35288,
          '4831001/10003': 35289,
          '4851001/10001': 35292,
          '4851001/10002': 35293,
          '4851003/10001': 35294,
          '4851003/10002': 35295,
          '4851004/10001': 35296}

week_names = {1: 'Monday',
              2: 'Tuesday',
              3: 'Wednesday',
              4: 'Thursday',
              5: 'Friday',
              6: 'Saturday'}

act_group = groups.get(args.group_id, -1)
if (act_group == -1):
    raise ValueError('Invalid group id')

try:
    act_day = dt.strptime(args.date, '%d.%m.%Y')
except ValueError:
    raise ValueError('Invalid date')


sched = req.get(base_url + str(act_group) + '?date=' + str(dt.date(act_day)))
sched_json = json.loads(sched.text)

week_pairs = [0] * 6


print(sched_json['week']['date_start'], '-', sched_json['week']['date_end'])
print('Is odd :', sched_json['week']['is_odd'], '\n')

for i in range(len(sched_json['days'])):
    day = sched_json['days'][i]['weekday']
    lessons = sched_json['days'][i]['lessons']
    week_pairs[day - 1] = len(lessons)

    print('Date :', sched_json['days'][i]['date'], week_names[day])
    print('_____________________________________________________')

    for les in lessons:
        print(les['time_start'], '-', les['time_end'])
        print(les['subject'], '|', les['typeObj']['abbr'])

        if ('auditories' in les):
            print(les['auditories'][0]['name'], 'auditory')

        if (les['teachers'] is not None):
            for teacher in (les['teachers']):
                print(teacher['full_name'])

        print()

    print()


weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
left = [1, 2, 3, 4, 5, 6]
plt.bar(left, week_pairs, tick_label=weekdays,
        width=0.6, color='grey')

plt.ylabel('Pairs number')
plt.xlabel("Week days")
plt.title("Week load")
plt.show()
