import re #to work with regular expressions

# LOG_PATTERN = re.compile(
#     r"(?P<timestamp>[\d\-:\s]+)\s"
#     r"(?P<level>\w+)\s"
#     r"(?P<service>\w+)\s"
#     r"(?P<message>.*?)(?:\suser_id=(?P<user_id>\d+))?$"
# )
# #def parse_log_line(line):
#     #logic to matching log pattern
#     match=LOG_PATTERN.match(line) 
#     #if not match: #if match is not found
#         return None
#     return {
#         "timestamp": match.group("timestamp"),
#         "level": match.group("level"),
#         "service": match.group("service"),
#         "message": match.group("message")
#     }

from datetime import datetime #import datetime is a module.

LOG_PATTERN = re.compile(
    r'(?P<timestamp>\S+ \S+)\s+'
    r'(?P<level>\S+)\s+'
    r'(?P<service>\S+)\s+'
    r'(?P<message>.*)'
)

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    data = match.groupdict()
    data["timestamp"] = datetime.strptime(
        data["timestamp"], "%Y-%m-%d %H:%M:%S"
    )
    data["raw"] = line.strip()
    return data


#Groupdict()
#Strip()
#re.compile();recompile is a method in python which is used to create regex patterns
#python regex;python regular expression are used for searching matching and extract the data pattern from the given text
#r->raw data (log data). 
#?->starting of pattern code
#P<timestamp>,P<level>,P<service>,P<message> which is used to capture the names of particular data
#\s -> used to remove white spaces between the name given
#parser=>parsing the data. convert the raw data into structured data
#groupdict() -> convert raw data into structure data (dictionary)
# r'' -> raw Data
#?P<timestamp> -> named group
#s+ -> for spaces one or more
#^ -> start of line
#$ -> end of line
#\S -> non-space character