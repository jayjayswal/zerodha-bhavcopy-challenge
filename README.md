# zerodha-bhavcopy-challenge

##Task
BSE publishes a "Bhavcopy" file every day here Write a Python script that:- Downloads the Equity bhavcopy zip from the above page- Extracts and parses the CSV file in it- Writes the records into Redis into appropriate data structures(Fields: code, name, open, high, low, close) Write a simple CherryPy python web application that:- Renders an HTML5 + CSS3 page that lists the top 10 stock entries from the Redis DB in a table- Has a searchbox that lets you search the entries by the 'name' field in Redis and renders it in a table- Make the page look nice! Commit the code to Github. Host the application on AWS or Heroku or a similar provider and share both the links.

## Technology Used
1. Python 3
2. Redis Database
3. AngularJs
4. Bootstrap 4 UI framework
5. JQuery

##File Structure
1. **assets:** This folder contains all required JS and CSS file. "app.js" is a angular controller file.
2. **templates:** This folder contains all html files.
3. **zips:** This folder contains all the bhav csv files.
4. **config.py:** This file contains common configurations and function which required in whole application.
4. **parser.py:** This file contains BhavCSV parser class, Which fetchs zip from the website and load it into redis.
5. **controller.py:** This file contains all the business logic and also connects to parser when required.
4. **server.py:** This file contains all the webservice endpoints. It connects to **controller.py** for business logic. 
It also initiates CherryPy web server.

