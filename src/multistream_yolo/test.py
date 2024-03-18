from flask import Flask, render_template
from threading import Thread
import time

import queue

app = Flask(__name__)

# Variable shared between the thread and the app
shared_data = []
q = queue.Queue(4)

# Function that runs in a separate thread
def background_task():
    global shared_data
    global q
    while True:
        # Simulate some background task
        time.sleep(5)
        
        # Add data to the shared list
        shared_data.append(time.strftime("%H:%M:%S"))
        print("queue-> ",q)
        q.put(1)
        # print(shared_data)

# Start the background thread
background_thread = Thread(target=background_task)
background_thread.start()

# Flask route to display data from the shared list
@app.route('/')
def display_data():
    print("queue = ",q)
    print("queue empty = ",q.empty())
    print("queue full = ",q.full())
    print("queue value = ",q.get())
    return render_template('display_data.html', data=shared_data)

if __name__ == '__main__':
    app.run(debug=True)
