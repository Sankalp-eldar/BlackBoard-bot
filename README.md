# BlackBoard-bot
A bot for interacting with Blackboard (BB) to attend my classes.

site url for BB is in Constants.py as BASE_URL, change that if needed.

Text from a readme I added while creating it:

```
Hello! This is readme for Blackboard class attending bot.

Here is how to use in case I share this:
check you have these files in one directory: 
	chromedriver.exe (hopefully you have correct version of chrome driver
							I included version 94.0.4606.81),
	timetable.csv,
	.cfg,
	main.exe

Auto Login into BB:
"info.txt" file:
- open info.txt file, create it if it does not exists.
	- you can use notepad or any text reader.
- write your bb uid in first line
- write your bb password in second line

******* Done! *******

Important:
Program leaves the class when class time ends, but you will have 10 seconds to stop it from quitting the class.
	(btw if you are paying attention then you will know 1 min before it tries to quit that it is going to quit.)
In terminal Press Ctrl+C to exit the program this will also close your bot controlled chrome window.

Note:
When you start the program it might through some errors on terminal don't mind those unless program crashes.
"INFO:bot.Bot:" kind of messeges are just information of what program is doing.

If time table changes either you can edit it carefully and accordingly or just ask me for the new one.

Extras:
- To check version of your chrome type chrome://version in chrome.
- "info.txt" file is only to remove the need of re-entering ID-password in terminal
   If you are running this program from terminal, it takes two arguments ID and password.
   If not provided it will check for info.txt file if even that is not available it will prompt for input.
- .cfg file is actually just some json data which should map: course name(as in timetable) - bb course tabs(part of url, ex: course-list-course-_340_1).
```
