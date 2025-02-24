import logging

import pandas as pd
from adl_ftp_plugin.registries import FTPDecoder
from adl_ftp_plugin.utils import get_dates_to_now

logger = logging.getLogger(__name__)


class AdconSOMDecoder(FTPDecoder):
    """
    This class represents a decoder for the Adcon data format.
    """
    
    type = "adcon_som"
    compat_type = "adcon_som"
    display_name = "ADCON FTP Somalia"
    
    def get_matching_files(self, station_link, files):
        # get all the initial matching files
        matching_files = super().get_matching_files(station_link, files)
        
        # get the dates we need to check
        dates = get_dates_to_now(date_granularity=station_link.date_granularity,
                                 timezone=station_link.timezone,
                                 from_date=station_link.start_date,
                                 as_string=True,
                                 str_format="%Y%m%d")
        
        # sample filename 0-854-0-004-20250216.txt
        # filter the matching files by date
        matching_files = [file for file in matching_files if any(date in file for date in dates)]
        
        return matching_files
    
    def decode(self, file_path):
        
        """
        This method decodes the Adcon data format.
        
        :param file_path: The path to the file to decode.
        :return: A dictionary containing the decoded data.
        """
        
        # sample csv file
        # StationID,Date,Time,Time zone,Barometric Pressure,Global Radiation,Precipitation,Relative Humidity,Temperature,Dew point,Wind Direction,Wind Speed,Battery Voltage
        # 516877,24/02/2025,00:15:00,EAT,969.0,0.0,0.0,61.3,25.7,17.7,95.9,9.5,6.65
        # 516877,24/02/2025,00:30:00,EAT,969.0,0.0,0.0,62.6,25.5,17.8,101.1,8.9,6.60
        # 516877,24/02/2025,00:45:00,EAT,968.9,0.0,0.0,63.9,25.1,17.8,103.6,8.9,6.60
        
        df = pd.read_csv(file_path, dtype={"Time": str})
        
        # columns that are not data values
        non_data_val_cols = ["StationID", "Date", "Time", "Time zone"]
        
        # convert data columns to float
        for column in df.columns:
            if column not in non_data_val_cols:
                df[column] = pd.to_numeric(df[column], errors='coerce')
        
        # convert date and time columns to datetime
        # date format like 24/02/2025 Time format like 00:15:00
        date_time_str = df["Date"].astype(str) + df["Time"].astype(str)
        
        df["TIMESTAMP"] = pd.to_datetime(date_time_str, format="%d/%m/%Y%H:%M:%S")
        
        # drop the date and time columns
        df.drop(columns=["Date", "Time", "Time zone"], inplace=True)
        
        # convert the dataframe to a list of dictionaries
        records = df.to_dict(orient="records", )
        
        return {
            "values": records
        }
