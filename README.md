# essential-meals
This is the github repo for Team 9107's Junior Design Project.
## Release Notes
Version 1.0
### New Features:
* Users can create their own recipes which can be found in the search results
* Search results uses a new API to display recipes ands nutritional information
* Calendar page allows users to create their own meal plan
* Analysis page allows users to view total sodium intake by day for the current week

### Recent Fixes:
* Added links to all of the main pages on every page of the website
* Fixed calendar events to have links to recipes so they can be easily viewed

### Known Bugs and Defects:
* Analysis page errors if no recipe has been added to the current week on the Calendar page
* Website likely does not appear very well on mobile since it has not been published online to test
* User generated recipes do not contribute towards analysis page for sodium


## Installation Guide

### Pre-reqs
* Python 3.7
* Pip

### First time setup:
1. Clone the repository to your computer
2. Navigate to the directory in terminal/command prompt
3. Type the following commands into terminal/command prompt
```
pip install virtualenv
virtualenv env
env\Scripts\activate
pip install -r requirements.txt
```
This will set up a virtual environment so external python libraries won't mess up stuff here.

### Post-First Time Use
```
env\Scripts\activate
```
And use
```
deactivate
```
To get rid of the (env) at the beginning of your terminal line
### Running the website
From the repo's directory on your computer, run the following in terminal/command prompt
```
cd essential_meals_project
python manage.py runserver
```
The website can then be viewed by going to <localhost:8000/em_website>.

### Troubleshooting

* ```
  package not installed
  ```
  Run 'pip install \<package name\>'

* Database changes are not reflected on the website
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

* "Database table is duplicated"

  ```
  python manage.py migrate --fake
  ```
