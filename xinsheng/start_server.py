import subprocess
import time
import os

os.chdir(r'd:\xinshen')

proc = subprocess.Popen(
    ['python', 'manage.py', 'runserver', '8000'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

print(f"Started process with PID: {proc.pid}")

time.sleep(3)

if proc.poll() is None:
    print("Server is running!")
    print("Waiting for requests...")
    time.sleep(60)
else:
    print("Server exited with code:", proc.returncode)
    output = proc.stdout.read()
    print("Output:", output)