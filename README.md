### Selenium Twitter Trending Topics ScraperFeatures and Tasks Addressed
## 1. Read Twitter Home Page and Fetch Top 5 Trending Topics<br>
The Selenium script logs into Twitter using your credentials and scrapes the top 5 trending topics from the "What's Happening" section.

## 2. Login with Your Own Twitter Account<br>
The script securely logs into Twitter using the credentials provided in the configuration file. Ensure you use your own account to avoid access issues.

## 3. Proxy Support for New IP Address Requests<br>
The project uses ProxyMesh to ensure each request originates from a different IP address. This minimizes the risk of being blocked by Twitter.

## 4. Unique ID Generation and MongoDB Integration<br>
Every time the script runs:

A unique ID is generated for the session.
The results (trending topics, date/time of the script's completion, and IP address) are stored in a MongoDB collection.<br>
## 5. Dynamic HTML Page to Trigger Script and Display Results<br>
A Flask web application serves an HTML page:

A button triggers the Selenium script.
Displays the top 5 trending topics along with the date/time, IP address, and a JSON extract from MongoDB.How to Run the Project?<br>
Step 1: Start MongoDB
Ensure MongoDB is running locally:

bash
```mongod```
Step 2: Run the Flask Application
Start the Flask server:

bash
```python app.py```
Step 3: Open the Web Interface
Visit http://127.0.0.1:5000 in your browser.
Click "Run the Script" to execute the Selenium script.
View the results dynamically updated on the page.
