
###Selenium Twitter Trending Topics Scraper

This project automates the process of logging into Twitter, scraping the top 5 trending topics under the "What's Happening" section, and storing the results in a MongoDB database. The project also integrates a Flask-based web interface for running the script and displaying the results dynamically.

Features and Tasks Addressed

Read Twitter Home Page and Fetch Top 5 Trending Topics
The Selenium script logs into Twitter using your credentials and scrapes the top 5 trending topics from the "What's Happening" section.

Login with Your Own Twitter Account
The script securely logs into Twitter using the credentials provided in the configuration file. Ensure you use your own account to avoid access issues.

Proxy Support for New IP Address Requests
The project uses ProxyMesh to ensure each request originates from a different IP address. This minimizes the risk of being blocked by Twitter.

Unique ID Generation and MongoDB Integration
Every time the script runs:

A unique ID is generated for the session. The results (trending topics, date/time of the script's completion, and IP address) are stored in a MongoDB collection. 5. Dynamic HTML Page to Trigger Script and Display Results A Flask web application serves an HTML page:

A button triggers the Selenium script. Displays the top 5 trending topics along with the date/time, IP address, and a JSON extract from MongoDB. Requirements Prerequisites Python 3.8 or later Google Chrome and ChromeDriver MongoDB installed locally or accessible remotely ProxyMesh credentials Python Dependencies Install the required Python packages with:

bash Copy code pip install -r requirements.txt requirements.txt:

plaintext Copy code selenium pymongo flask uuid Project Directory Structure bash Copy code selenium-testing/ │ ├── app.py # Flask app to serve the HTML interface ├── main.py # Main Selenium script to scrape Twitter ├── templates/ │ └── index.html # HTML file for the web interface ├── requirements.txt # Python dependencies └── README.md # Project documentation How to Run the Project? Step 1: Start MongoDB Ensure MongoDB is running locally:

bash Copy code mongod Step 2: Run the Flask Application Start the Flask server:

bash Copy code python app.py Step 3: Open the Web Interface Visit http://127.0.0.1:5000 in your browser. Click "Run the Script" to execute the Selenium script. View the results dynamically updated on the page. Expected Output Web Interface Once the script completes:

Displays the top 5 trending topics. Shows the date and time of script completion. Displays the IP address (or a fake IP if unavailable). Includes a JSON extract from MongoDB. Example: plaintext Copy code These are the most happening topics as on 2024-12-30 01:02:13:

#AnnamalaiExposed
#KajalAggarwal
#RohitSharma𓃵
#ProKabaddi
The IP address used for this query was 192.168.1.100.

Here's a JSON extract of this record from the MongoDB: { "_id": { "$oid": "6771a3bd65f0c15ae2fe2746" }, "unique_id": "50f49433-a84f-4077-9696-8fdebd9a576e", "trends": [ "#AnnamalaiExposed", "#KajalAggarwal", "#RohitSharma𓃵", "#ProKabaddi" ], "end_time": "2024-12-30 01:02:13", "ip_address": "192.168.1.100" } Notes and Improvements ProxyMesh Setup: Ensure your ProxyMesh credentials are configured in main.py to rotate IP addresses. Error Handling: Includes error messages if MongoDB is unavailable or no records are found. HTML Page Improvements: The IP address defaults to "192.168.1.100" if unavailable.

