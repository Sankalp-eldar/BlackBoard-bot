from datetime import datetime as dt
import datetime as dtp

try:
    from bot.Utility import get_today_course, find_current_course
except ModuleNotFoundError:
    from Utility import get_today_course, find_current_course


class Timetable:
    def __init__(self, filename):
        self.filename = filename
        self.get_today_course()
        self.create_stamps()

    def get_today_course(self):
        day = dt.now().strftime("%a")
        self.courses = get_today_course(day, self.filename)

    def get_current_course_name(self):
        now = dt.now()
        key = find_current_course(now, self.courses)[1]
        return self.courses[key]

    def create_stamps(self, date : dt = None):
        self.stamps = []
        if date is None:
            date = dt.now()

        for i in self.courses.keys():
            time = list(map(int, i.split(':')))
            _time = dt(date.year, date.month, date.day,
               time[0], time[1], 0)
            self.stamps.append( {'time': _time, 'key': i} )

    def second_next_class_in(self, current_time : dt = None, duration = 40):
        info = self.next_class_in(current_time, duration)
        _next = dt.now() + dtp.timedelta(minutes = duration + 0.01 - info[0])
        return self.next_class_in(_next, duration)

    def next_class_in(self, current_time : dt = None, duration = 40):
        now = current_time or dt.now()
        # now = dt(now.year, now.month, now.day, 13, 13, 20)
        dura = dtp.timedelta(minutes = duration)


        for idx, val in enumerate(self.stamps):
            i = val['time']
            if (now < i) or (i <= now < i+dura):
                index = idx
                course_name = self.courses[val['key']]
                course_time = i
                break
        else:
            return None

        wait = (course_time - now).total_seconds()

        return [wait, course_name]



if __name__ == '__main__':
    t = Timetable('hi.csv')
    cl = t.next_class_in()
    # if cl[0] < 0:
    #     cl = t.get_current_course_name()
    print(cl)
