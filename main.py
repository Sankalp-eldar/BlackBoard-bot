from bot.Bot import BlackBoard
import bot.Constants as const
from bot import opt
import logging, sys, os
import json

format = logging.Formatter(const.FORMAT)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# handler = logging.FileHandler(
#     filename='bot.log',
#      encoding='utf-8', mode='w')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(format)

logger.addHandler(handler)

def get_id():
    try:
        _id = sys.argv[1]
        pwd = sys.argv[2]
    except IndexError:
        try:
            _id = const.ID
            pwd = const.PASSWD
        except AttributeError:
            try:
                with open("info.txt", 'r') as f:
                    _id = next(f).strip()
                    pwd = next(f).strip()
            except (StopIteration, FileNotFoundError):
                print("ID or Password missing: (press Ctrl+C to stop)")
                _id = input("ID: ")
                pwd = input("Password: ")
                print("To Save info create a file named 'info.txt'\nwith first line ID, second password")
    return _id, pwd

def course_map(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main():
    try:
        _id, pwd = get_id()
    except KeyboardInterrupt:
        return
    Course = course_map(".cfg") or const.COURSE
    with BlackBoard(None, options = opt) as bb:
        if bb.check_class():
            try:
                bb.login(_id, pwd, course = Course)
                bb.begin()
            except KeyboardInterrupt:
                pass
        else:
            print("No more classes today!")

if __name__ == "__main__":
    main()
    print('\nProgram finished press Enter to exit.')
    input()

