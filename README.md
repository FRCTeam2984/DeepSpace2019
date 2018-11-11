# HomegrownRobot
A homegrown FRC robot repository

# Basic setup
1. Install python 3.5 or newer
2. Install git
3. Install pip
4. Fork the repository that is owned by `frcteam2984`
5. Clone your forked repository to any directory
6. While in that directory, run `git remote add upstream https://github.com/FRCTeam2984/HomegrownRobot.git`

# Install dev environment
1. `[pip executable] install pyfrc`
2. `[pip executable] install pynetworktables`
3. `[pip executable] install -U robotpy-ctre`
4. Install vscode
5. Open vscode and install Python extension
6. Run `code .`

# Install on robot
1. Run `[pip executable] install robotpy-installer`
2. While connected to the internet, run the following commands
* `robotpy-installer download-robotpy`
* `robotpy-installer download-opkg python36-robotpy-cscore`
* `robotpy-installer download-opkg python36-robotpy-ctre`
3. Connect back to the robot and run the following commands
* `robotpy-installer install-robotpy`
* `robotpy-installer install-opkg python36-robotpy-cscore`
* `robotpy-installer install-opkg python36-robotpy-ctre`

# Deploy to robot
1. Run `[python executable] robot.py deploy`

# Run unit tests
1. Run `[python executable] robot.py test`
