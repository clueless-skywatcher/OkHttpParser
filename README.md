# OkHttpParser
A parser for detecting HTTP requests in Android log files

Libraries used:
- json: For pretty printing JSON objects and dictionaries
- re: For matching some regular expressions to detect patterns.

About the parser:
- OkHttpParser() makes a parsing object to find necessary patterns to
find both requests and responses.
  - parse_requests() method returns a list of OkHttpRequestObject instances, each containing
  info about a particular request. All requests are parsed in sequence.
  - parse_responses() is almost the same, but returns a list of OkHttpResponseObject instances,
  containing info about responses.
