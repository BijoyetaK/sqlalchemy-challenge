# Import the dependencies.
from flask import Flask,jsonify,render_template
from datetime import datetime
import appdata

#################################################
# Flask Setup
#################################################

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

weatherdata = appdata.Weatherdata()

datavalidation = appdata.DataValidation()

#################################################
# Flask Routes
#################################################

#Homepage that list all available routes in a table format

@app.route('/')
def welcome():
   #https://www.quackit.com/html/html_table_generator.cfm
   return render_template("index.html")
 
#Route to retrieve only the last 12 months of precipitation and date

@app.route('/api/v1.0/precipitation')
def precipitation():
    try:
       output_message = {"Success": True,
                      "log_time": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.000"),
                      "Data":weatherdata.precipitation_data}
       return jsonify(output_message),200
   
    except Exception as e:
      message = "Application Error:  "+ str(e)
      output_message = {"Success": False,
                      "message": message,
                      "log_time": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.000"),
                      "status": "Error",
                      "Category": "System error",
                      "Data": None
                      }
      return jsonify(output_message),400
      
#Route to return list of all stations in the dataset

@app.route('/api/v1.0/stations')
def stations():
   try:
       output_message = {"Success": True,
                      "log_time": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.000"),
                      "Data":weatherdata.station_data}
       return jsonify(output_message), 200
   
   except Exception as e:
      message = "Application Error:  "+ str(e)
      output_message = {"Success": False,
                      "message": message,
                      "log_time": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.000"),
                      "status": "Error",
                      "Category": "System error",
                      "Data": None
                      }
      return jsonify(output_message),400
      
#Route to return dates and temperature observations for the previous year

@app.route('/api/v1.0/tobs')
def most_active_stations_tobs():
   try:
    
    output_message = {"Success": True,
                      "log_time": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.000"),
                      "Data":weatherdata.most_active_station_data}
    return jsonify(output_message), 200
   
   except Exception as e:
      message = "Application Error:  "+ str(e)
      output_message = {"Success": False,
                      "message": message,
                      "log_time": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.000"),
                      "status": "Error",
                      "Category": "System error",
                      "Data": None
                      }
      return jsonify(output_message), 400


#Route to return min, average and max temperature for all the dates greater 
#than or equal to a user sepcified start date.       

@app.route('/api/v1.0/<start>')
def measurement_from_date(start):
   
   
   try: 

    start_date_validation = datavalidation.validate_date_format(input_date=start) 

    start_dt_success = False

    if start_date_validation.get('Success'):
      start_date_str = start_date_validation.get('Formatted_Date')
      start_dt_success = True
 
    if start_dt_success:
        output_message = {"Success": True, "Data": weatherdata.temperature_aggr_from_start_date(start_date=start_date_str) }
        return jsonify(output_message), 200
    else:
        message = "Input date must be of format - 20170816 (YYYYMMDD)"
        output_message = {
                      "Success": False,
                      "message": message,
                      "input_data": start,
                      "log_time": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.000"),
                      "status": "Error",
                      "Category": "Invalid Input Date format",
                      "Data": None
                      }
        return jsonify(output_message), 400
   
   except Exception as e:
      
    message = "Error reading input "+ str(e)
    output_message = {"Success": False,
                      "message": message,
                      "input_data": start,
                      "log_time": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.000"),
                      "status": "Error",
                      "Category": "System error",
                      "Data": None
                      }
    return jsonify(output_message), 400


#Route to return min, average and max temperature for all the dates from the 
#user sepcified start date to the end date inclusive.

@app.route('/api/v1.0/<start>/<end>')
def measurement_between_dates(start,end):
   
  
   try:  
 
    start_date_validation = datavalidation.validate_date_format(input_date=start)
    end_date_validation = datavalidation.validate_date_format(input_date=end)

    start_dt_success = False
    end_dt_success = False

    date_range_success = False

    if start_date_validation.get('Success'):
      start_date_str = start_date_validation.get('Formatted_Date')
      start_dt_success = True

    if end_date_validation.get('Success'):
      end_date_str = end_date_validation.get('Formatted_Date')
      end_dt_success = True

    if start_dt_success and end_dt_success:
      date_range_success = datavalidation.validate_date_range(start_date=start_date_str,end_date=end_date_str)  

    if start_dt_success and end_dt_success and date_range_success: 

        output_message ={"Success": True, "Data": weatherdata.temperature_aggr_between_dates(start_date=start_date_str,end_date=end_date_str) }
      
        return jsonify(output_message), 200
    else:
        message = "Error valdating Input: End Date must be greater than Start date and must be of format - 20170816 (YYYYMMDD)"
        output_message = {
                        "Success": False,
                        "message": message,
                        "input_data": start,
                        "log_time": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.000"),
                        "status": "Error",
                        "Category": "Invalid Input",
                        "Data": None
                      }
        return jsonify(output_message), 400
   
   except Exception as e:

      
    message = "Error reading input "+ str(e)
    output_message = {"Success": False,
                        "message": message,
                        "input_data": start,
                        "log_time": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.000"),
                        "status": "Error",
                        "Category": "System Error",
                        "Data": None
                      }
    return jsonify(output_message), 400   


#runs on a specified host and port
if __name__ == '__main__':

   app.run(host="127.0.0.1",port=7000)