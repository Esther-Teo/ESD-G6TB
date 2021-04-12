# ESD-G6TB


INTRODUCTION
------------------------------------------
TutorPedia is a web application built with Flask to digitalise the entire search for tutors on finding prospective tutees. Through TutorPedia, we can reduce the manual work for both parties and tutees are able to receive more customized lesson plans and they are not bound by any tuition agencies.


FUNCTIONALITIES
------------------------------------------
======== USER ========
*Register a new account
*Log in
*Edit profile
*Create/edit children
*Create an assignment
*View/delete assignments
*View pending/accepted offers
*View notifications on dashboard (upon reception of offer)
*Make payments to tutors

======== TUTOR ========
*Register a new account
*Log in
*Edit profile
*View assignment listings
*Make offers for assignment
*View pending/accepted offers
*View notifications on dashboard (upon acceptance/rejection of offer)




REQUIREMENTS
------------------------------------------
SQLAlchemy==1.3.22
Flask==1.1.2
Flask-SQLAlchemy==2.4.4
mysql-connector-python==8.0.22
Flask-Cors==3.0.10
requests==2.25.1
pika==1.2.0
Flask-Session==0.3.2
stripe==2.56.0


INSTALLATION
------------------------------------------
 * No extra installation necessary

CONFIGURATION
------------------------------------------
======== TO SET UP ========
1. Unzip file into the root directory.
2. Load WAMP
3. Import SQL files into phpmyadmin
    How to import the required SQL:
        1.) After starting Wamp/Mamp, type “localhost/phpmyadmin”.
        2.) Click “Import” button on the navbar.
        3.) Click “Choose File”
        4.) Select the file “import.sql”
        5.) Scroll down and click “Go”
4. Go to ESD-G6TB directory in your terminal
5. Enter 'docker-compose up' command

======== CONSTRAINTS ========
 *** A user cannot create a child entity with special characters or whitespace in the childName

 *** A tutor cannot submit another offer for an assignment after their offer has been rejected

 *** All form fields must be populated before submission

 *** The maximum price range for a tutor to offer his/her services is capped at 999.99

 *** Payment settings on the payment page for the user will not be removed after payment due to recurring payments

TROUBLESHOOTING 
------------------------------------------
*If ‘docker-compose up’ does not start building the file, check if your docker engine is running. If all else fails, try to run the ‘docker-compose down —rmi all’ before trying again.


TEST DATA
------------------------------------------
User:
Email: dwightsnoot@gmail.com
pwd: gg

Tutor:
Email: esd69hrsaweek@gmail.com
pwd: 123

Email: soonhao.er@smu.edu.sg
pwd:123

Login through Google Log-In 
We have created 2 Gmail accounts to test out the Google Log In API and you can test it out too by using these login credentials)

User Email
Email: mikeyscarn69@gmail.com
pwd: ESDBestMod

Tutor Email
Email: bcoskitt@gmail.com
pwd: ESDBestMod
