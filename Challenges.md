## Challenge: Getting MediaPipe Running Reliably

One early challenge was simply getting **MediaPipe** to run correctly in my development environment.

At first, MediaPipe would not work on **Python 3.13** (compatibility issues). I then switched to **Python 3.10**, which is more commonly supported, but the installation still failed in my normal Python setup.

The fix was to create a clean, isolated virtual environment (`mp_venv`) and install MediaPipe inside it. Once MediaPipe was installed in the virtual environment, it ran successfully.

### What I learned
- Some libraries depend on specific Python versions and system-level builds.
- A virtual environment helps avoid conflicts and makes the project more reproducible.
- When working with real-world tools, setup and compatibility can be as important as writing the code itself.

### Current decision
This project will continue to use Python 3.10 in a dedicated virtual environment to keep dependencies stable.
