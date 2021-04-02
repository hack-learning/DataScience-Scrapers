# Complete Data Extraction-Loading Pipeline Including Continuous Deployment
<p>
    <img src="https://drive.google.com/uc?export=view&id=1llXvr17dW_N8WzrGRMVT_o2NRrjeL9qN" width="750" height="240" />
</p>


Extracting information is one of the most common duties as a Data Scientist. However a vast majority struggles deploying their pipelines. We show you here, how you can do both tasks with some useful tools.

This project was created to load up to date technology related articles periodically into a database. That information is going to be analyzed  by a Natural Language Processing API.


# About this project

Web Scraping is one of the most effective ways to get information from the web, automatically and periodically. Being Scrapy an amazing tool for this purpose.

The created scraper extracts up to date articles about technology from important news portals, using a ***Scrapy Project***. The scraper's code is stored in a cloud functions which is being triggered by a pub/sub event, executed by the scheduler every week.  

After that the information is sent to a ***Digital Ocean MySql Managed Database*** to be analyzed later by a Natural Language Processing API. 

Finally we used ***Cloud Build and Source Repos from Google Cloud*** to automates the cloud function deployment process every time you push some change to the repository.

# Prerequisites
* Create a Google Cloud account.
* Enable your billing account. 
* Enable Compute Engine, Cloud Functions, Cloud Scheduler and Cloud Pub/Sub APIs.
* Create a Digital Ocean account.
* Create an SQL Managed Database.
