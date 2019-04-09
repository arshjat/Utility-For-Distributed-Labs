# Utility-For-Distributed-Labs

Intelligent natural language search for all of Dr. Reddy's Laboratories
(​https://www.drreddys.com/​)​ R&D data:​

**Problem Statement** : They​ ​plan to develop an application that
can help the organisation with their R&D data, which can extract the useful
information from the slides and build knowledge from it using NLP tools.
Integrating it with web application will help staff to access it anywhere any data
can be visualized with help of graphs and charts using web libraries. Such
automated application will save the time it takes to manually look through PPTs
and prepare reports.

**Solution** : This project was developed during BHacks (IIIC Allahabad's business solutions hackathon). 
This project uses :
  * Two NLP libraries - TextRazor (for keywords extraction) and DeepAI (for summarization of text).
  * Pyrebase (a firebase API for python).
  * Flask server as backend.
  * React as frontend (Future Work).
  
### How it works ?

* First a user is prompt to upload a powerpoint presentation to the server.
![Uploading a slide](https://github.com/arshjat/Utility-For-Distributed-Labs/blob/master/static/images/Screenshot%20from%202019-04-09%2020-33-02.png)

* Then the ... page is rendered and the scientists can search for all previous work done on a specific topic.
![Search page](https://github.com/arshjat/Utility-For-Distributed-Labs/blob/master/static/images/Screenshot%20from%202019-04-09%2020-33-55.png)

* Then a number of cards are shown dynamically below the search bar. (Future work in frontend)
Currently, plain data is rendered on the web page, whose glimpse can be seen at [Link](https://github.com/arshjat/Utility-For-Distributed-Labs/blob/master/static/images/Screenshot%20from%202019-04-09%2020-34-09.png)
