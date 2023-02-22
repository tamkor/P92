# To run the script

1. python -m venv venv
2. 
   1. If you are on Windows: .\venv\Scripts\activate 
   2. If you are on Linux/macOS: source ./venv/bin/activate
3. pip install -r requirements.txt
4. python main.py

# Details of the files

- main.py - An async runner of the servers.
- configs folder - If you want to configure something, like the host or port of the servers.
- servers folder - The code of gateway (http) server and the websocket server
- tests folder - The location of all the tests
- .gitignore file - to avoid unnecessary git uploads
- requirements.txt - Here are the dependencies to be able to run the project, transient ones are excluded.
