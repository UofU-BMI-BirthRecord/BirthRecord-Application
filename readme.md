# Automated Birth Reporting

This project is exploring the possibility of automatic data extracton from an EHR to populate a birth certificate. Currently the app pulls manufacured patient data (very small number) from the HSPC server, displays requested info, and prints out a JSON file. The eventual goal is to automate data extracton for Utah birth reporting clerks and post the extracted data to the Utah public health services and vital records department's servers. The Ut vital records department has recently set up a FHIR server to deal with death certificate information, birth certificate information may follow a similar path.

This is a multi-semester, multi-team project by the University of Utah Department of Biomedical Iformatics.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

1. clone this repository to your local machine, or save all the files in a local directiry
2. The current version of this code is in python 2, NOT python 3, but there shouldn't be any compatibility issues
3. Install all necessary packages. there may be others you need, but it's easiest to attempt to run the code and see what is not installed

`pip install flask flask_bootstrap easygui json fhirclient `


4. Run the app from the directory where this repository is cloned. Any errors may show what other packages you need to install, if no errors proceed.

`python app3.py`

 5. Open http://localhost:5000/select in your browser. This should open up the form to input days to find recent births.

note: code was written in python 2, if running python 3 there will be errors, and no output will display

### Prerequisites

Python packages required:

flask

flask_bootstrap

easygui

json

fhirchlient

## Contributing

Not currently managing contributors

## Versioning

Not currently using versioning 

## Authors

See the list of [contributors](https://uofu.box.com/s/x5y6tvqzgb2x42dcn4cqzhhttzrjs8mj) who participated in this project.

## License

This project is licensed under the Apache 2.0 license - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* List future Acknowledgements here
