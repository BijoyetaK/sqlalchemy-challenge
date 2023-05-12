import pandas as pd
# Python SQL toolkit and Object Relational Mapper
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
import json

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite",echo=False)

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

class Weatherdata():


    def __init__(self):

        self.station_data = None
        self.date_year_back = None
        self.precipitation_data = None
        self.most_active_station_data = None
        
        self.get_stations()

        self.get_precipitation()

  
            
    def get_stations(self):
        with Session(engine) as session:
            
            #Exploratory Station Analysis
            # Design a query to get all the station data from station table

            sel =[Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]

            station_result = session.query(*sel).all()

            cols = ['Station','Station_Name','Latitude','Longitude','Elevation']

            station_df = pd.DataFrame(station_result,columns= cols)

            #*******************************************************************************
            #Data for Route 3: Stations                                                    *
            #*******************************************************************************
            station_data = station_df.to_json(orient='records')
            self.station_data = json.loads(station_data)
            

    def get_precipitation(self):

        with Session(engine) as session:
            
            # Find the most recent date in the mmeasurement table data.
            most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
            print("Most recent date: ",most_recent_date)
        
            # Calculate a time difference of 12 months ago from '2017-08-23'(most_recent_date)
            most_recent_date_str = most_recent_date[0]
            #converting to datetime
            most_recent_date_converted = datetime.strptime(most_recent_date_str, "%Y-%m-%d")

            self.date_year_back = most_recent_date_converted - timedelta(days = 365)

            # Design a query to retrieve the last 12 months of precipitation data.
            # Perform a query to retrieve the data and precipitation scores
            # Save the query results as a Pandas DataFrame. Explicitly set the column names
            # Sort the dataframe by date

            sel =[Measurement.prcp,
                Measurement.station,
                #func.strftime("%Y-%m-%d",Measurement.date),
                Measurement.date,
                Measurement.tobs]
            prcp_result = session.query(*sel).\
                filter(Measurement.date >= self.date_year_back).\
                order_by(Measurement.date.desc()).all()

            #converting the query results to pandas dataframe
            cols = ['Precipitation','Station','Record_Date','Tobs']
            prcp_cols = ['Precipitation','Record_Date']

            measurement_df = pd.DataFrame(prcp_result,columns= cols)
            measurement_df["Precipitation"].fillna(0.00, inplace = True)
            measurement_df['Record_Date'] = measurement_df['Record_Date'].apply(lambda x:datetime.strptime(x, "%Y-%m-%d"))
            measurement_df.sort_values("Record_Date")
            prcp_df = measurement_df[prcp_cols]

            #********************************************************************************************
            #Data for Route 2: Last 12 months precipitation                                             *
            #********************************************************************************************

            precipitation_data = prcp_df.to_json(orient='records')
            self.precipitation_data = json.loads(precipitation_data)


            #***********************************************************************************************
            # Data for Route 4: dates and temperature observations of most active station for a year       *
            #***********************************************************************************************
    
            sel =[Measurement.station,
                func.count(Measurement.id)]

            station_result = session.query(*sel).\
                group_by(Measurement.station).\
                order_by(func.count(Measurement.id).desc()).all()

            most_active_station = station_result[0][0]
            
            # Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
            
            most_active_station_df = measurement_df[measurement_df['Station'] == most_active_station]

            most_active_station_df = most_active_station_df[['Station','Tobs','Record_Date']]

            most_active_station_data = most_active_station_df.to_json(orient='records')
            self.most_active_station_data = json.loads(most_active_station_data)


    def temperature_aggr_from_start_date(self,start_date):

         #***********************************************************************************************
         # Data for Route 5: for a specified start, calculate temp min, average and max, for all the    *
         #                   dates greater than or equal to the start date.                             *
         #                   Returns a JSON list of the min, avg, max temperature for a specified start *
         #                   Takes date input in the format of string(YYYYMMDD)                         *
         #***********************************************************************************************

        start_date_input = datetime.strptime(start_date,"%Y-%m-%d")
        start_date_input = start_date_input - timedelta(days = 1)
        
        with Session(engine) as session:

            
            sel =[Measurement.date,
                  func.min(Measurement.tobs),
                  func.avg(Measurement.tobs),
                  func.max(Measurement.tobs)]
            
            start_date_results = session.query(*sel).\
                filter(Measurement.date > start_date_input).\
                group_by(func.strftime("%Y-%m-%d",Measurement.date)).\
                order_by(func.strftime("%Y-%m-%d",Measurement.date)).all()
            

            cols = ['Record_Date','TMIN','TAVG','TMAX']
            start_date_df = pd.DataFrame(start_date_results,columns= cols)

            start_date_data = start_date_df.to_json(orient = 'records')
            start_date_data = json.loads(start_date_data)


        return start_date_data
    
    def temperature_aggr_between_dates(self,start_date,end_date):

       
        #***********************************************************************************************
        # Data for Route 6: for a specified start and end date calculate temp min, average and max,    *
        #                   for the dates from the user start date and end date                        *
        #                   Returns a JSON list of the min, avg, max temperature for a specified start *
        #                   and end date inclusive                                                     *
        #                   Takes date input in the format of string(YYYYMMDD)                         *
        #***********************************************************************************************

        start_date_input = datetime.strptime(start_date,"%Y-%m-%d")
        start_date_input = start_date_input - timedelta(days = 1)
        end_date_input = datetime.strptime(end_date,"%Y-%m-%d")
        
        with Session(engine) as session:

            sel =[Measurement.date,
                  func.min(Measurement.tobs),
                  func.avg(Measurement.tobs),
                  func.max(Measurement.tobs)]
            
            aggr_temp_results = session.query(*sel).filter((Measurement.date > start_date_input) & (Measurement.date <= end_date_input)).\
                group_by(func.strftime("%Y-%m-%d",Measurement.date)).\
                order_by(func.strftime("%Y-%m-%d",Measurement.date)).all()
            

            cols = ['Record_Date','TMIN','TAVG','TMAX']
            aggr_temperature_df = pd.DataFrame(aggr_temp_results,columns= cols)

            aggr_temperature_data = aggr_temperature_df.to_json(orient = 'records')
            aggr_temperature_data = json.loads(aggr_temperature_data)


            return aggr_temperature_data


#***********************************************************************************************
# Preliminary data validation for the input start and end date.                                * 
# Start or End date should be in the format of YYYYMMDD and Start Date must be earlier or      * 
# smaller than the End date                                                                    *     
# Defining a class for data validation                                                         *
#***********************************************************************************************


class DataValidation():

    #validate date range

    def validate_date_range(self,start_date,end_date):

        start_date = datetime.strptime(start_date,"%Y-%m-%d")
        end_date = datetime.strptime(end_date,"%Y-%m-%d")

        success = False if start_date > end_date else True

        return success



    def validate_date_format(self,input_date):


        return_value = {}

        try:

            input_date = datetime.strptime(input_date, "%Y%m%d")
            input_date_str = datetime.strftime(input_date,"%Y-%m-%d")

            return_value['Success'] = True

            return_value['Formatted_Date'] = input_date_str

        except:

            return_value['Success'] = False  
            return_value['Formatted_Date'] = None

        return return_value     



    









