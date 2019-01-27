# DeepSpace2019
Vikings Robotics's code for DeepSpace 2019

# Basic setup
1. Install python 3.5 or newer
2. Install git
3. Install pip
4. Fork the repository that is owned by `frcteam2984`
5. Clone your forked repository to any directory
6. While in that directory, run `git remote add upstream https://github.com/FRCTeam2984/DeepSpace2019.git`

# Install dev environment
Ensure that you are in a virtual environment before running this
1. `[pip executable] install -r requirements.txt`
2. Open vscode and install Python extension
3. Run `code .`

# Install on robot
1. Run `[pip executable] install robotpy-installer`
2. While connected to the internet, run the following commands
* `robotpy-installer download-robotpy`
* `robotpy-installer download-opkg python37-robotpy-cscore python37-robotpy-ctre`
* `robotpy-installer download-pip coloredlogs`
1. Connect back to the robot and run the following commands
* `robotpy-installer install-robotpy`
* `robotpy-installer install-opkg python37-robotpy-cscore python37-robotpy-ctre`
* `robotpy-installer install-pip coloredlogs`

# Deploy to robot
1. Run `[python executable] robot.py deploy`

# Run unit tests
1. Run `[python executable] robot.py test`
