# Import the flask module for the application
from flask import Flask, request

# Import the redis module for the application
import redis
from rq import Queue

# Import the time module to include some time delay in the application
import time

# Create the application directory
app = Flask(__name__)

# Make a connection of the queue and redis
r = redis.Redis()
q = Queue(connection=r)

# Create a working task queue  
def task_in_background(t):  
 
    delay = 10 
 
    print("Running Task")  
    print(f"Simulates the {delay} seconds")  
 
    time.sleep(delay)  
 
    print(len(t))  
    print("Completed Task")  
 
    return len(t)

@app.route("/task")  
def add_task():  
 
    if request.args.get("t"):  
 
        job= q.enqueue(task_in_background, request.args.get("t"))  
 
        q_len = len(q)  
 
        return f"The task {job.id} is added into the task queue at {job.enqueued_at}. {q_len} task in the queue"  
    return "Task Queue with Flask"  
 
if __name__ == "__main__":  
    app.run()
