#!/usr/bin/env python
import subprocess
import signal
import sys
import os
import shutil
from time import sleep

def find_gradlew(script_dir):
    gradlew_path = os.path.join(script_dir, "gradlew")
    if os.path.exists(gradlew_path):
        return gradlew_path
    gradlew_path = os.path.join(script_dir, "../gradlew")
    if os.path.exists(gradlew_path):
        return gradlew_path
    raise FileNotFoundError("gradlew not found")


def main():
    print("Hello from debug.py")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(script_dir, "target")

    gradlew = find_gradlew(script_dir)

    # clean the old files...
    for d in ["renderer", "main"]:
        print(f"Cleaning target/{d} directory")
        shutil.rmtree(os.path.join(target_dir, d), ignore_errors=True)

    tasks = [':03-electron:main:jsDevelopmentExecutableCompileSync', ':03-electron:renderer:assemble']

    # Run the gradle task to compile the Kotlin/JS code
    # This will make all files before running the electron app
    subprocess.run([gradlew] + tasks,
        stdout=sys.stdout, stderr=sys.stderr, cwd=script_dir)

    # Run the gradle task to compile the Kotlin/JS code, continuously
    # This will watch for changes in the Kotlin/JS code and recompile
    # (in Background)
    gradle = subprocess.Popen([gradlew, "-t"] + tasks,
        stdout=sys.stdout, stderr=sys.stderr, cwd=script_dir)

    while True:
        print("Starting electron app")

        # start the electron app in target/ directory
        electron = subprocess.Popen(["npx", "electron", "."],
            stdout=sys.stdout, stderr=sys.stderr, cwd=target_dir)

        electron.wait()

        sleep(2)

if __name__ == "__main__":
    main()
