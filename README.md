# Georgia Institute of Technology - Web Industries

Georgia Institute of Technology Spring 2019 ISYE Senior Design capstone project with Web Industries.

## Table of Contents

- [Getting Started](#Getting-Started)
    - [Prerequisites](#Prerequisites)
    - [Development](#Development)
    - [Installing](#Installing)
    - [Usage](#Usage)
- [App](#App)
- [Deliverable Instructions](#Deliverable-Instructions)
    - [Schedule](#Schedule)
    - [CMF](#CMF)
    - [p\*](#p)
- [Poster](#Poster)
- [Authors](#Authors)
- [Acknowledgments](#Acknowledgments)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

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

    python3 driver.py

## App

Download the standalone executable tool [HERE](https://www.dropbox.com/s/nrdudmbdtdhb82o/Web%20Industries%20Deliverable%20final.exe?dl=0)

Please note this only supports Windows 8.1 or Windows 10.

## Deliverable Instructions

### Schedule

Input an Excel Spreadsheet with the jobs to be scheduled and output a schedule that minimizes the makespan of all jobs. Please be advised that the tool is for aiding scheduling decisions, and that discretion should still be exercised.

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20Schedule%20tab.PNG?raw=true">

**Constrained programming scheduling tool**

|  Field | Explanation |
|:----------------|------------------------------------------------------------|
| Schedule_Input | Input Excel File |
| write_schedule| Path to write output to |
| sheet | Name of sheet with the jobs |
| processing | Column of processing times. Populate this column from the [p\*](#p) tab |
| WO | Column of Work Orders |
| set | Column of sets in a Work Order |
| material | Column of the resin type or material |
| width | Column of the slit widths |
| due | Column of due dates |

**Config Options**

| Field | Explanation |
|:----------------|------------------------------------------------------------|
| truncate | If Yes, will group sets together in their respective Work Orders, then schedule Work Orders as jobs. The processing time will be the sum of the processing times of the sets. If No, will schedule each set as a job. Using yes will **greatly** speed up solution time |
| start_time | When to start the first job of the schedule |
| max_run | Maximum time in seconds to run the tool. If reached, will output the best schedule found up to that point |
| output_proto | Write the model into a file |
| preprocess_times | Build minimal setups into the job duration. Keeping this ticked will speed up the tool |

Example run:

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20Schedule%20Run%20example.PNG?raw=true">

### CMF

CMF tab is for inputting historical data to fit empirical mass distributions of processing times for different materials. We use these distributions when calculating optimal allotted processing times in the [p\*](#p) tab.

To update old data, simply upload updated data with the same unique column keys; the old data with those unique column keys will be updated, while the rest of the saved data will be preserved. To delete *all* saved data, delete the file `cmfs.pickle`.

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20CMF%20tab.PNG?raw=true">

**Load or modify historical data**

| Field| Explanation |
|:----------------|------------------------------------------------------------|
| CMF_Input | Input Excel file containing historical data |
| sheet | Name of the sheet containing historical data |
| mat_col | Column of which material or resin jobs were |
| mach_col | Column of which machine jobs were ran on |
| estim_col | Column of the estimated processing time used |
| actual_col | Column of the actual processing time each job took |

The historical data describes the processing times of previous jobs. The unique combination of Machine, Material Type, and Estimated Time determines how the distributions are grouped.

### p*

Calculate a value of p* to use in the schedule. Requires historical data to be loaded from the [CMF](#CMF) tab. Again, grouped by unique combination of Machine, Material Type, and Estimated Time.

<img src="https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/GUI%20pstar%20tab.PNG?raw=true">

**Required Arguments**

| Field | Explanation|
|:----------------|------------------------------------------------------------|
| theta | Dollar cost per hour of machine downtime |
| delta | Dollar cost per exceed out incident that fails testing |
| Material | The material we wish to find allotted processing time for. |

After calculating p\*, manually enter it into the input file of [Schedule](#Schedule). This is to ensure a human has the final review of any scheduling decisions made.

## Poster

Below is our research poster for this project.

[![](https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/Web%20Industries%20Expo%20Poster.jpg?raw=true>)](https://github.com/nzqs/sdteam17/blob/master/deliverable/resources/images/Web%20Industries%20Expo%20Poster.jpg?raw=true>)

## Authors

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
* *Dr. George Nemhauser*
