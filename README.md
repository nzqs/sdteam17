# Georgia Institute of Technology - Web Industries

Georgia Institute of Technology Spring 2019 ISYE Senior Design capstone project with Web Industries.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
To simply run the application, see [App](#App)

### Prerequisites

Python 3.6+. Can be installed for your operating system [here](https://www.python.org/downloads/).

### Development

Clone the repository with

    git clone https://github.com/nzqs/sdteam17.git

It's recommended to use a virtual environment to manage the project packages. Navigate to the project's directory.
If you are using Conda, create the environment and activate with

    conda create -n envname python=3.6
    source activate envname

Or use the venv module (Python 3.3+)

    python3 -m venv envname

Activate the virtual environment depends on platform.
Posix:

    $ source envname/bin/activate

Windows (cmd.exe or PowerShell):

    C:\> envname\Scripts\activate.bat
    PS C:\> envname\Scripts\activate.ps1


### Installing
wxPython is required to run the graphical user interface. It can be installed with pip

    pip install -U wxPython


This project also uses Google's OR-Tools. They can also be installed with pip

    pip install --upgrade --user ortools


Install the rest of the requirements with

    conda install --yes --file requirements.txt

or

    pip install -r requirements.txt

* Some packages may fail to install. Install these manually and remove them from requirements.txt

### Usage

Run the GUI application with the driver

    python driver.py


## Deliverable Instructions

### Schedule

Input an Excel Spreadsheet with the jobs to be scheduled and output a schedule that minimizes the makespan of all jobs.

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20Schedule%20tab.PNG">

Constrained programming scheduling tool

|Field|Explanation|
|:----------|--------------------------------------------|
|Schedule_Input|Input Excel File|
|write_schedule|Path to write output to|
|sheet|Name of sheet with the jobs|
|processing|Column of processing times. Populate this column from the p* tab|
|WO|Column of Work Orders|
|set|Column of sets in a Work Order|
|material|Column of the resin type or material|
|width|Column of the slit widths|
|due|Column of due dates|

Config Options

|Field|Explanation|
|:----------|--------------------------------------------|
|truncate|If Yes, will group sets together in their respective Work Orders, then schedule Work Orders as jobs. The processing time will be the sum of the processing times of the sets. If No, will schedule each set as a job. Using yes will **greatly** speed up solution time|
|start_time|When to start the first job of the schedule|
|max_run|Maximum time in seconds to run the tool. If reached, will output the best schedule found up to that point|
|output_proto|Write the model into a file|
|preprocess_times|Build minimal setups into the job duration. Keeping this ticked will speed up the tool|

Example run:

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20Schedule%20Run%20example.PNG?raw=true">

### CMF

CMF tab is for inputting historical data to fit empirical mass distributions of processing times for different materials. We use these distributions when calculating optimal allotted processing times in the p* tab.

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20CMF%20tab.PNG">

Load or modify historical data
=======
## Deliverable Instructions

### Schedule

Input an Excel Spreadsheet with the jobs to be scheduled and output a schedule that minimizes the makespan of all jobs.

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20Schedule%20tab.PNG">

Constrained programming scheduling tool:
|Field|Explanation|
|:----------|--------------------------------------------|
|Schedule_Input|Input Excel File|
|write_schedule|Path to write output to|
|sheet|Name of sheet with the jobs|
|processing|Column of processing times. Populate this column from the p* tab|
|WO|Column of Work Orders|
|set|Column of sets in a Work Order|
|material|Column of the resin type or material|
|width|Column of the slit widths|
|due|Column of due dates|

Config Options
|Field|Explanation|
|:----------|--------------------------------------------|
|truncate|If Yes, will group sets together in their respective Work Orders, then schedule Work Orders as jobs. The processing time will be the sum of the processing times of the sets. If No, will schedule each set as a job. Using yes will **greatly** speed up solution time|
|start_time|When to start the first job of the schedule|
|max_run|Maximum time in seconds to run the tool. If reached, will output the best schedule found up to that point|
|output_proto|Write the model into a file|
|preprocess_times|Build minimal setups into the job duration. Keeping this ticked will speed up the tool|

Example run:
<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20Schedule%20Run%20example.PNG?raw=true">

### CMF

CMF tab is for inputting historical data to fit empirical mass distributions of processing times for different materials. We use these distributions when calculating optimal allotted processing times in the p* tab.

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20CMF%20tab.PNG">

Load or modify historical data
|Field|Explanation|
|:----------|--------------------------------------------|
|CMF_Input|Input Excel file containing historical data|
|sheet|Name of the sheet containing historical data|
|mat_col|Column of which material or resin jobs were|
|mach_col|Column of which machine jobs were ran on|
|estim_col|Column of the estimated processing time used|
|actual_col|Column of the actual processing time each job took|

The historical data describes the processing times of previous jobs. The unique combination of Machine, Material Type, and Estimated Time determines how the distributions are grouped.

### p*

Calculate a value of p* to use in the schedule. Requires historical data to be loaded. Again, grouped by unique combination of Machine, Material Type, and Estimated Time.

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20pstar%20tab.PNG">

Required Arguments
|Field|Explanation|
|:----------|--------------------------------------------|
|theta|Dollar cost per hour of machine downtime|
|delta|Dollar cost per exceed out incident that fails testing|
|Material|The material we wish to find allotted processing time for.|
>>>>>>> 79ec28fb76bb3911058d0a75c72176b0c8a1fd39

|Field|Explanation|
|:----------|--------------------------------------------|
|CMF_Input|Input Excel file containing historical data|
|sheet|Name of the sheet containing historical data|
|mat_col|Column of which material or resin jobs were|
|mach_col|Column of which machine jobs were ran on|
|estim_col|Column of the estimated processing time used|
|actual_col|Column of the actual processing time each job took|

<<<<<<< HEAD
The historical data describes the processing times of previous jobs. The unique combination of Machine, Material Type, and Estimated Time determines how the distributions are grouped.

### p*

Calculate a value of p* to use in the schedule. Requires historical data to be loaded. Again, grouped by unique combination of Machine, Material Type, and Estimated Time.

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20pstar%20tab.PNG">

Required Arguments

|Field|Explanation|
|:----------|--------------------------------------------|
|theta|Dollar cost per hour of machine downtime|
|delta|Dollar cost per exceed out incident that fails testing|
|Material|The material we wish to find allotted processing time for.|

## Authors

=======
>>>>>>> 79ec28fb76bb3911058d0a75c72176b0c8a1fd39
* **Nicholas She**

In collaboration with
* *Suyoun Choi*
* *Camille George*
* *Jin Soo Kim*
* *Maryam Moshrefi*
* *Mallory Herrmann*

## Acknowledgments

Special thanks to our fantastic advisor
* **Dr. Gamze Tokol-Goldsman**

and other Georgia Tech ISYE faculty for their assistance and advice

* *Dr. Dima Nazzal*
* *Dr. Chen Zhou*
