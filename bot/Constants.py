
class_dura = 40
join_retry = 4

BASE_URL = r"https://cuchd.blackboard.com/ultra/course"
timetable = "timetable.csv"
FORMAT = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'

# ________ Login related ________
UID = "user_id"
PWD = "password"
SUB = "entry-login"

CIE_A = "agree_button"



# ________ session related  ________
# Leave buttons
leave_bar = "session-menu-open"
Leave_Button = "leave-session"

status_bar = "status-selector-toggle"
Leave_css = 'button[class="button menu-list__control status-button focus-item leave-session ng-scope"]'

survey_skip = "session-survey-skip"
Dont_leave_Button = 'back-to-session'


# to find join buttons
session = "sessions-list-dropdown"
join = "sessions-list"


# popups!?
mic_cam = '[aria-label="Cancel microphone and camera setup"]'

# mic_cam = ('[analytics-id="techcheck.audio.ok-button"]',
#     '[analytics-id="techcheck.video.fullcheck-mode.ok-button"]')

tutorial = '[ng-click="announcementModal.closeModal()"]'


# ________ Course related ________

close_course = "bb-close"
grid_course = r'//*[@id="main-content-inner"]/div/div[1]/div[1]/div/div/div[1]/div/header/bb-square-toggle/div/label[2]'

