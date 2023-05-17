# sqlalchemy-challenge
## Module 10 Assignment 

### This assignment involved creation of Flask API after doing some basic analysis on climate data of Hawaii using Python an SQLALchemy. 

### Analyze and Explore Climate Data
   - Using SQLALCHEMY ORM queries, Pandas and Matplotlib to do climate analysis.
   - Database used is hawaii.sqlite
   - Tables inspected creating engine connection to hawaii.sqlite - measurement and station.
   - Measurement table provided: ID, Station name, date, precipitation and temperature data
   - Station table provided: ID, Station name, latitude, longitude, elevation
   - Using automap_base function to declare a Base class.
   - Use that Base class to reflect the tables using autoload_with=engine.
   - using keys() function to view all the classes that automapping process found.
   - Saving the references to each table into Measurement and Station class respectively. 
   - Creating session (link) from Python to sqlite DB using Session(engine)
    

### Exploratory Precipitation Analysis

   - Find the most recent date from the measurement table
   - Calculate a time difference of 12 months ago from most recent date  
   - Using the calculated date query to retrieve the last 12 months of precipitation data and plot the results.
   - Saving the query results in to a Pandas Dataframe. 
   - Using matplotlib to plot the data
    ![image](https://github.com/BijoyetaK/sqlalchemy-challenge/assets/126313924/81647ecd-0c06-4bbe-8a84-dea61a02ef01)
         
   - Using Daylocator function in mdates module of matplotlib created the date plots
   - reference: #https://dataplotplus.com/change-frequency-date-x-axis-matplotlib-python/
   ![image](https://github.com/BijoyetaK/sqlalchemy-challenge/assets/126313924/37cb4778-9555-41d4-9d98-725c75d19033)         
   - precipitation summary using describe()
   
      ![image](https://github.com/BijoyetaK/sqlalchemy-challenge/assets/126313924/4f26b509-05a6-4fa7-a37e-fcb7b08baf04)
   

### Exploratory Station Analysis

   - Query the stations table to calculate the total number of stations using ORM method
   - Print the total number of stations
   - Saving the query results to a Pandas DataFrame
   
       ![image](https://github.com/BijoyetaK/sqlalchemy-challenge/assets/126313924/fe2214da-6cb8-4269-9b95-6ec1ff5b8019)
         
   - Query the measurement table to find the most active stations (i.e. which stations have the most rows?)
   - List the stations and their counts in descending order.
   - Print the most active station
   - Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
   - Create a Temperature summary dataframe
   
        ![image](https://github.com/BijoyetaK/sqlalchemy-challenge/assets/126313924/64cb2560-0668-4e01-940f-0af06c53520c)
         
   - Using the most active station id create a dataframe having the previous 12 months of temperature data
   - Plot the data temperature data in a histogram
   
        ![image](https://github.com/BijoyetaK/sqlalchemy-challenge/assets/126313924/d3df90dc-9902-44e8-aada-369ca39ad492)
         
   - Close session

  
   
### Designing Climate App(Flask API) based on the above precipitation, station and temperature analysis results

   - Two python applications:
        - appdata.py -> Python application that has all the individual functions inside the Weatherdata class.
                        Each function queries the DB to fetch required data, save them into pandas dataframe and converting into json.
                        Also contains the DataValidation class to do user input start/end dates. 
        - app.py -> Flask API that references the Weatherdata and DataValidation class and  from appdata.py to build create required routes. 
                    The routes are displayed to the user in a html table format using render_template function from flask module.
   - Available routes created for: 
        - Welcome page/homepage
        - Precipitation in the last 12 months
        - List of all Hawaii stations
        - Temperature observations of the most active station
        - Min, Avg and Max temperature for a specified start date onwards
        - Min, Avg and Max temperature from specified start date to end date inclusive,
          user input start date and end date must be in format YYYYMMDD and end date must be greater than start date.
        ![image](https://github.com/BijoyetaK/sqlalchemy-challenge/assets/126313924/94c16cc4-dbdd-470c-8a40-69a45d02c2ec)



#### references: 
     
   - https://www.quackit.com/html/html_table_generator.cfm
                 
   - https://bobbyhadz.com/blog/python-add-months-to-date#:~:text=Use%20the%20relativedelta%20class%20from,with%20different%20numbers%20of%20days.
     
   - https://dataplotplus.com/change-frequency-date-x-axis-matplotlib-python/
   
   - https://pythonbasics.org/flask-rest-api/


     
     
                 
                 
     
  
