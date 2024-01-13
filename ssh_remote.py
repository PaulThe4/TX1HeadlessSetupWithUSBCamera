from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)

video_feed_running = False
ssh = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute_opencv', methods=['POST'])
def execute_opencv():

    global video_feed_running, ssh

    if not video_feed_running:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.1.102', username='ubuntu', password='ubuntu')
    

        # Command to run OpenCV script in shell mode
        command = '/home/ubuntu/Python-3.9.18/python /home/ubuntu/Desktop/app.py'

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        video_feed_running = True
        #return "Video feed started."
   # else:
      #  return "Video feed is already running."
    
    if not error:
        return f"OpenCV code executed successfully: {output}"
    else:
        return f"Error executing OpenCV code: {error}"

@app.route('/stop_video_feed', methods=['POST'])
def stop_video_feed():
    global video_feed_running, ssh

    
    # Close the SSH connection to stop the OpenCV process
    stop_command = 'pkill -f app.py'
    ssh.exec_command(stop_command)
    ssh.close()
    video_feed_running = False
    return "Video feed stopped."
    #else:
     #   return "Video feed is not running."

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)


