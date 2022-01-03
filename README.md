<!-- Title -->
# Github_API_Access-Visualisation

<!-- About The Project -->
## About The Project

### Description
An implementation of measuring software engineering using analysis of code churn and refactoring, from commit data pulled from a specified Github repository


<!-- Prerequisites -->
## Prerequisites

* Python installed on the system (Python3 was used during development)
* Docker installed


<!-- Getting Started -->
## Getting Started

### Github API Token
* Step 1: Insert your API token in src/constants.py. Available at https://github.com/settings/tokens and choose whether to anonymise the user data or not

### Install Dependencies
* Step 2: Navigate to the root directory and run `./install.sh` to ensure all dependencies are installed.

### Running The Database And Webserver
* Step 3: Navigate to the root directory and run `./runServer.sh`

### Navigating To The Webpage
* Step 4: Navigate to http://localhost:8000/ in your web browser


<!-- Instructions -->
## Instructions

* Enter a repository name
* Wait for the data to be collected
* When the loading message clears, select the contributor you would like to analyse
* The number of lines added, lines deleted and total lines changed of both the contributor and the average of the team is plotted on the graph over time
* Each of these, can be toggled on or off individually by clicking on the associated label
* The individuals data can be viewed independently or overlaid with the team average using the two buttons at the top of the graph
* The exact value can be seen by hovering the cursor over any of the circles
* A summary of the overall commit statistics can also be seen at the bottom


<!-- What is being analysed? -->
## What is being analysed?

Refactoring consists of improving the structure of an existing program, to increase its efficiency or aid with understanding of the code, while preserving the external behaviour of the program.<br/>

While refactoring does not mean rewriting code, analysing the number of lines added and deleted by a developer in each commit, can be used as a good measure in determining if refactoring is taking place. By comparing a single developer's data against the other developers on the team, trends can be observed and large spikes inconsistent with the rest of the team can be a sign of a sloppy developer, as the sloppy code would require many rewrites.<br/>

Code Churn is another useful metric in analysing a software engineer. Code churn is when code is rewritten or deleted shortly after being written. Churn level is highly variable between projects, individuals and teams. As such it is important to analyse the code churn over time to determine a norm.<br/>

While rework of code is a normal part of the development process, a significant amount of rework outside the norm is often another good sign of a sloppy developer. By observing the code churn over time of a developer compared to the other developers on that team, trends can be observed in the efficiency of the developer.


<!-- How is it being analysed? -->
## How is it being analysed?

Both these methods of measuring software engineering use lines added vs lines deleted as the base metric for the analysis. This means that by plotting an individual's data against the average of the team, these two methods of measurement can be done.<br/>

When a user enters a repository, the system pulls all the commits and the list of contributors from that repository. The lines added, lines deleted and total lines changed in each commit are stored, along with the contributor’s username.<br/>

When a contributor is selected, their commits are first organised by day, meaning multiple commits on the same day are combined together. The sum of them is used to determine the number of lines added, lines deleted and total number of lines changed on each day they made a commit. This is plotted on the graph along with the average of the team.<br/>

The team average is determined by combining all commits made on the same day by any contributor other than the selected one. The sum of the total number of lines added, lines deleted and total number of lines changed on a particular day is then divided by the number of contributors who committed on the day to determine the average per person.


<!-- Additonal Information -->
## Additonal Information

### Running Tests
* Run Tests: Navigate to the root directory and run `./runscripts/runTest.sh`

<!-- Contributers -->
## Contributers
* [Cillian Fogarty](https://github.com/cillfog1)
