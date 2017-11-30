import re
import operator
from collections import Counter


#selecting file to parse and returns it
def ask_file():
  logfile = raw_input("Please enter a log file to parse: ")
  return logfile

#receives file and returns adapted one
def file_to_lines(logfile):
  file = open(logfile, "r")
  logs = []
  for line in file:
    if not line.isspace():
      logs.append(line.strip())
  file.close()
  return logs

#parse one line of file ,returns host ip 
def parse_ids(log):
  match = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", log)
  if match:
    return match.group(0)

#parse one line of file ,returns url 
def parse_urls(log):
  match = re.search('[GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|PATCH] (\/.*) [HTTP]', log)
  if match:
    return match.group(1)

#returns parsed ids
def ids(logfile):
  ids = []
  for log in logfile:
    ids.append(parse_ids(log))
  top_ids = sorted(dict(Counter(ids)).items(), key=operator.itemgetter(1), reverse=True)
  return top_ids

#returns parsed urls
def urls(logfile):
  urls = []
  for log in logfile:
    url = parse_urls(log)
    if url is not None:
      urls.append(url) 
  top_urls = sorted(dict(Counter(urls)).items(), key=operator.itemgetter(1), reverse=True)
  return top_urls

#makes human-readable output
def output(ip , url):
  headers = ["IP", "Request count"]
  row_format ="{:>50}" * (len(headers) + 1)
  print row_format.format("", *headers)
  for row in ip:
    print row_format.format("", *row)
  print "\n"
  headers = ["URL", "Request count"]
  row_format ="{:>50}" * (len(headers) + 1)
  print row_format.format("", *headers)
  for row in url:
    print row_format.format("", *row)

"""    final    """
def main():
  file = file_to_lines(ask_file())
  output(ids(file), urls(file))

main()
