from selenium.webdriver.chrome.options import Options
from bot.Utility import generate_course

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")

# opt.add_argument("use-fake-device-for-media-stream")
# opt.add_argument("use-fake-ui-for-media-stream")

# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1
  })

# "profile.default_content_setting_values.geolocation": 1, 
# "profile.default_content_setting_values.notifications": 1 
