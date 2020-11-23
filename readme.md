# Background
The purpose of this project is to visualize running data from .gpx files.

#######################################
# Setup

## Clone github repo
git clone https://github.com/giordang/racevis.git

### cd into project repo
cd racevis

### make uploads directory
mkdir uploads

#######################################
## Mac:
### install venv, creates venv folder
python3 -m venv venv

### activate venv
source venv/bin/activate

### install dependencies
pip install -r requirements.txt

### run flask locally
flask run

########################################
## Windows
### install venv, creates venv folder
python3 -m venv venv

### activate venv
venv/Scripts/activate

### install dependencies
pip install -r requirements.txt

### run flask locally
flask run