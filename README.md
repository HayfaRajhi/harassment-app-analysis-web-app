# *Harassment Analysis Web App*
Harassment Analysis Web App is a Python and Flask-based application designed to analyze the toxicity of content using a pretrained model, [Detoxify](https://github.com/unitaryai/detoxify). 
This app processes user-provided JSON data, performs an ETL process, and displays the toxicity analysis in a tabular format on the UI. 
The application utilizes Docker for containerization, including a MongoDB instance for efficient data handling , it includes also social media scraping functionality implemented with Selenium.

## *Table of Contents*
- Features
- Technologies Used
- Architecture
- Getting Started
- Usage
- Screenshots
- Future Enhancements
- Contributing
- License
### *Features*
- ETL Process: Extract, transform, and load JSON data for analysis.
- Toxicity Analysis: Utilizes the Detoxify pretrained model to detect toxicity levels in text data.
- UI for Data Submission: Users can upload JSON files via an HTML interface.
- Results Display: Displays toxicity analysis results in a tabular format.
- Containerized Deployment: Docker containers for the Flask app and MongoDB ensure portability and scalability.
  
### *Technologies Used*
- Backend: Flask
- Machine Learning Model: Detoxify (pretrained)
- Database: MongoDB (running in a Docker container)
- Containerization: Docker and Docker Compose
- Frontend: HTML with Flask integration
- Programming Language: Python

### *Architecture*
The application has a modular architecture consisting of the following components:

- Flask API: Handles JSON file uploads, processes data, and invokes the Detoxify model for analysis.
- Instagram Scraper: Uses Selenium to collect data for toxicity analysis.
- ETL_Pipeline: Prepares the data for analysis and formats the output for the UI and utils_elt for the etl pipeline
- MongoDB Container: Stores data temporarily or permanently during analysis.
- UI: A simple HTML interface for user interaction and results visualization.


### *Getting Started*
- Prerequisites
- Install Docker
- Install Python 3.8+
- Install Google Chrome and ChromeDriver (required for Selenium)
- Clone this repository:
  * *git clone https://github.com/HayfaRajhi/harassment-app-analysis-web-app.git*
  * *cd harassment-app-analysis-web-app*

  Setup Instructions
  Install Dependencies: Install Python dependencies from requirements.txt.
  *pip install -r requirements.txt*
  Run Docker Containers: Build and start the application and database container .
  
  Start the Flask App: Access the app on `http://localhost:5000` after running the following:
  
  python app.py
  Setup Selenium: Ensure that chromedriver is in your PATH and that your browser version matches the driver version.

### *Usage*
- JSON Data Analysis
Upload JSON File: Go to `http://localhost:5000`
Upload a JSON file containing the data to be analyzed.

View Results:

Analyze the uploaded file.
Results, including toxicity levels, will be displayed in a table on the web page.

### Screenshots
Home Page
![Capture d’écran 2024-11-24 185935](https://github.com/user-attachments/assets/dc553093-284c-4a34-bc4c-eddcd00a548e)
 
Results Page
![image](https://github.com/user-attachments/assets/914a5cfc-a13a-431f-82e3-e50bc8414aef)


### Future Enhancements
+ Platform-Specific Scrapers: Add support for more platforms like Reddit or YouTube.
+ Authentication: Add user login functionality.
+ Enhanced Analytics: Include more metrics and detailed breakdowns of toxicity.
+ Batch Processing: Enable bulk uploads of JSON files.
+ Visualization: Add charts or graphs for data visualization.
+ Redis Caching: Optimize data retrieval using Redis.
+ Advanced NLP Features: Sentiment analysis, topic modeling, and keyword extraction.
+ Data Visualization: Charts and graphs for better result representation.
+ Scalable ETL Process: Improved handling of large datasets.
+ User Authentication: Secure access for personalized analysis


