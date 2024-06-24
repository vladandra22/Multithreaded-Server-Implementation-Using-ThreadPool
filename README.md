# Multithreaded Server Implementation Using ThreadPool

The project involves developing a multithreaded server application using Flask and a ThreadPool for efficient request handling. 
Tasks, represented as tuples, are managed by pre-created threads (TaskRunners). The server processes incoming requests by adding tasks 
to the ThreadPool queue and returns JSON responses. Data management includes reading/writing job-related information to files. 
Comprehensive testing was performed using unit tests with mock data and the RapidAPI VSCode extension. The implementation addresses graceful shutdown 
issues with proper error handling and optimized resource locking mechanisms.
