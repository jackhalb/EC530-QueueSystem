# EC530-QueueSystem

In this project we were tasked to make a queue system for a Speech-to-Text module that will be implemented in the Healthcare System app. For my implementation I used a Flask server as the API for calling the queue system, and Redis for the queue system itself. 

To run this project, clone this repository to your local machine. Next, make sure you have all of the required python packages - for this project it is flask and redis. Simply run "pip install redis" in a bash shell, and also install it to your local machine via these instructions: 
macOS:  https://phoenixnap.com/kb/install-redis-on-mac
Windows: https://redis.io/download
Linux: https://redis.io/topics/quickstart
Also run "pip install flask" in a bash shell.

To test this project, open two bash shells and navigate both of them to where this repository is cloned. Next, in one shell, run "rq worker" to start a worker on the Redis server. In the other shell, type "flask run". Finally, to see that the queue is working, navigate to your browser and enter the URL: http://localhost:5000/task?t=[ENTER A STRING HERE]
In [ENTER A STRING HERE], you can type any string that you wish. When you load this page, and the bash shells are running, the server will respond by saying that the task was added to the queue, and tell you how many tasks are currently in the queue. To verify that a task was indeed started, navigate to the shell where you ran "rq worker" to see the task in the queue, and see it complete. 

Currently, the only tasks that are implemented is a simple sleep task, and when this finishes it will return the length of the string provided in the arguments for the API call in the URL ([ENTER A STRING HERE]). In the future, this task will be replaced with some sort of speech to text algorithm, and run in the background for the Healthcare app.
