#which is used to handle the data and reuseable code which is seperate from the dask 
#loading the data
#parsing the data
#structure the data and load the data using injection files
#parser: parser is a python method which is used to convert the raw data into structured data based on the schema which we have defined(translater)
#without parser:no columns are defined 
#no filtering is done
#no anamoloy is detection or no aggregation
#with parsing: we can filter error logs
#detect the unsual patterns
#it converts raw log data to the machine readable languag
import re

LOG_PATTERN = re.compile(
    r"(?P<timestamp>[\d\-:\s]+)\s"
    r"(?P<level>\w+)\s"
    r"(?P<service>\w+)\s"
    r"(?P<message>.*?)(?:\suser_id=(?P<user_id>\d+))?$"
)
#Groupdict()
#Strip()
#re.compile();recompile is a method in python which is used to create regex patterns
#python regex;python regular expression are used for searching matching and extract the data pattern from the given text
#r->raw data (log data)
#?->starting of pattern code
#P<timestamp>,P<level>,P<service>,P<message> which is used to capture the names of particular data
#\s -> used to remove white spaces between the name given