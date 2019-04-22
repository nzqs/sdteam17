# Georgia Institute of Technology - Web Industries

Georgia Institute of Technology Spring 2019 ISYE Senior Design capstone project with Web Industries.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
To simply run the application, see [App](#App)

### Prerequisites

Python 3.6+. Can be installed for your operating system [here](https://www.python.org/downloads/).

### Development

Clone the repository with
```
git clone https://github.com/nzqs/sdteam17.git
```

It's recommended to use a virtual environment to manage the project packages. Navigate to the project's directory.
If you are using Conda, create the environment and activate with
```
conda create -n envname python=3.6
source activate envname
```
Or use the venv module (Python 3.3+)
```
python3 -m venv envname
```
Activate the virtual environment depends on platform.
Posix:
```
$ source envname/bin/activate
```
Windows (cmd.exe or PowerShell):
```
C:\> envname\Scripts\activate.bat
PS C:\> envname\Scripts\activate.ps1
```

### Installing
wxPython is required to run the graphical user interface. It can be installed with pip
```
pip install -U wxPython
```

This project also uses Google's OR-Tools. They can also be installed with pip
```
pip install --upgrade --user ortools
```

Install the rest of the requirements with
```
conda install --yes --file requirements.txt
```
or
```
pip install -r requirements.txt
```
* Some packages may fail to install. Install these manually and remove them from requirements.txt

### Usage

Run the GUI application with the driver
```
python driver.py
```

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
