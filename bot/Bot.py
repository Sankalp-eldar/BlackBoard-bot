import os, time, logging, datetime as dt
import selenium

import bot.Constants as cons
from bot.timemanage import Timetable

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)

class BlackBoard(webdriver.Chrome):
    def __init__(self, driver_path=r"E:\Selenium driver", teardown=True, **kw):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += driver_path or os.getcwd()
        super().__init__(**kw)

        # full screen
        self.maximize_window()

        # wait x sec for it to load
        self.implicitly_wait(15)

        self.open_BB()
        self.accept_cookie()

    def __exit__(self, exc_type, exc_value, trace):
        if self.teardown:
            self.quit()

    def open_BB(self):
        self.get(cons.BASE_URL)
        self.BBTab = self.window_handles[0]

    def accept_cookie(self):
        # cookie accept...
        try:
            self.find_element_by_id(cons.CIE_A).click()
        except:
            logger.info("Cookies are already accepted!")


    def close_BB_popup(self):
        """
        BB creates some mic and vid checks.
        To be Tested and created.
        """
        try:
            self.find_element_by_css_selector(cons.mic_cam).click()
            # self.find_element_by_css_selector(cons.mic_cam[1]).click()
        except Exception as e:
            logger.debug(e)
        try:
            self.find_element_by_css_selector(cons.tutorial).click()
        except Exception as e:
            logger.debug(e)

    def click_x(self, xpath):
        self.find_element_by_xpath(xpath).click()
    def click_i(self, _id):
        self.find_element_by_id(_id).click()

    """
    Setup page:
    """
    def load_page(self):
        try:
            self.find_element_by_xpath(cons.grid_course).click()
            ActionChains(self).send_keys(Keys.PAGE_DOWN*2).perform()
        except Exception as e:
            logger.critical(f"Page loding failed!\n{e}")

    def login(self, _id, passwd, course = None, load_courses=True):
        # by_id: html tags have id, can be found using inspect

        self.find_element_by_id(cons.UID).send_keys(_id)
        self.find_element_by_id(cons.PWD).send_keys(passwd)
        self.find_element_by_id(cons.SUB).click()
        if load_courses:
            self.load_page()
        # self.fresh_load = True
        self.COURSE = course

    def create_timetable(self, filename):
        self.timetable = Timetable(filename)
        # self.get_today_course(cons.timetable)

    """
    Course interactions:
    """
    def close_course(self):
        """Just to press that X button."""
        self.find_element_by_class_name(cons.close_course).click()

    def focus_on_BB(self):
        self.switch_to.window(self.BBTab)


    def join_course(self, course):
        """
        Finds course id mapped to names
        opens-join-set_focus on new tab.
        """
        course = self.COURSE[course]

        for i in [course, cons.session, cons.join]:
            try:
                self.find_element_by_id(i).click()
            except Exception as e:
                self.close_course()
                raise e
        else:
            self.close_course()
            # get the second tab
            c = self.window_handles[1]
            #switch to tab browser
            self.switch_to.window(c)
            self.close_BB_popup()
            return




    def partial_leave_bar(self):
        """
        An incredibly important function for incredibly important task.
        Tries to leave the session and cancels at survey.
        To make sure it is possible to leave when needed.
        """
        try:
            self.find_element_by_id(cons.leave_bar).click()
            self.find_element_by_id(cons.Leave_Button).click()
            self.find_element_by_id(cons.Dont_leave_Button).click()
        except:
            return False
        return True

    def leave_course(self, wait = 10):
        """
        Leaves the on going course and sets focus on original BB window.
        """
        # Work under progress

        try:
            self.find_element_by_id(cons.leave_bar).click()
            self.find_element_by_id(cons.Leave_Button).click()
            # self.find_element_by_css_selector(cons.Leave_css).click()
            time.sleep(wait)
            self.find_element_by_id(cons.survey_skip).click()
            self.close()
        except:
            pass
        finally:
            self.focus_on_BB()



    def attend_course(self, course, duration = cons.class_dura, retry = cons.join_retry):
        for i in range(retry+1):
            try:
                self.join_course(course)
            except Exception as e:
                logger.info(f"Error While joining course: Try No.: {i} of {retry}\n")
                logger.debug("Encountered exception:", e)
            else:
                break

            # retry in 30 seconds:
            # reduce totad duration, time lost in retrying.
            logger.info("Retrying in {30} seconds...")
            time.sleep(30)
            duration -= 0.5


        # All tries failed exit the function.
        else:
            logger.warning(f"Failed to join course: Quitting: {course}")
            return False
        logger.info(f"Joined course: {course} Will remain for: {duration} mins")

        # duration -1 for leave testing!
        wait = dt.datetime.now() + dt.timedelta(minutes = duration-1)

        k = 0
        while dt.datetime.now() < wait:
            time.sleep(60)
            k += 1
            logger.info(f"In {course}: From: {k} Mins")

        # Test before leaving course.
        test = self.partial_leave_bar()
        if not test:
            logger.warning(f"Error while leaving course!!!")
        else:
            logger.info("Leaving course seem possible!")
        time.sleep(50)


        # Leave 1min after testing even if test fails.
        # return controll to BB window 
        # even if we were not able to leave.
        self.leave_course()
        logger.info(f"Left {course}")
        return True

    def check_class(self, filename = cons.timetable):
        self.create_timetable(filename)
        next_class = self.timetable.next_class_in()
        return next_class


    def begin(self, timetable = cons.timetable, duration = cons.class_dura, retry = cons.join_retry):
        self.create_timetable(timetable)
        success = True
        while 1:
            if success:
                next_class = self.timetable.next_class_in()
            else:
                next_class = self.timetable.second_next_class_in()
            if not next_class:
                logger.info("No More Classes left!")
                break
            if next_class[0] < 0:
                duration -= -next_class[0]/60
                next_class[0] = 0

            logger.info(f"Next class in {next_class[0]} seconds. Sleeping...")
            time.sleep(next_class[0])
            success = self.attend_course(next_class[1], duration = duration, retry = retry)




if __name__ == "__main__":
    pass
    # with BlackBoard(teardown=1) as bot:
    #     bot.login(cons.ID, cons.PASSWD)
    #     bot.attend_course("BEEE")
    #     bot.save_screenshot('screenshot.png')
