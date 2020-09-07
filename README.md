# OkHttpParser
A parser for detecting HTTP requests in Android log files

Problem description: 
While working using an Android device, we can send HTTP requests via Android using the 
OkHttp library. Our problem is to extract all the HTTP requests sent by the Android device 
via the OkHttp client, including their corresponding responses by analyzing the Android log file 
and parsing the OkHttp parts of the file.

Libraries used:
- json: For pretty printing JSON objects and dictionaries
- re: For matching some regular expressions to detect patterns.

About the parser:
- OkHttpParser() makes a parsing object to find necessary patterns to
find both requests and responses. It takes an optional "lines" variable (default = 1400) to find
requests/responses in the first "lines" number of lines in the log
  - parse() method returns a list of request-response pairs. This works for normal data but breaks
  for multipart data.
  
Downsides of the parser:
- Breaks while working with images and multipart data
