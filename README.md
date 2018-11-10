# HomegrownRobot
A homegrown FRC robot repository

# Install on robot
1. Ensure that python 3.5 or newer is installed
2. Run `[pip executable] install robotpy-installer`
3. While connected to the internet, run `robotpy-installer download-robotpy`
4. Connect back to the robot and run `robotpy-installer install-robotpy`
5. Connect back to internet and run `robotpy-installer download-opkg python36-robotpy-cscore`
6. Connect back to the robot and run `robotpy-installer install-opkg python36-robotpy-cscore`
7. Connect back to internet and run `robotpy-installer download-opkg python36-robotpy-ctre`
8. Connect back to robot and run `robotpy-installer install-opkg python36-robotpy-ctre`


# Install dev environment
1. `[pip executable] install -r requirements.txt` 
2. Install vscode
3. Open vscode and install Python extension
4. Clone this repo into any directory, and run `code .` while in that directory

# Deploy to robot
1. Run `[python executable] robot.py deploy`

# Run unit tests
1. Run `[python executable] robot.py test`