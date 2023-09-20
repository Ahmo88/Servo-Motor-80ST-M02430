# Create new python project:
    - Create project on Github
    - Make project clone on my pc

# Create a Virtual Environment:
    - from project root run command python -m venv env

    Activate the virtual environment:  
        - for windows run:  .\env\Scripts\activate
        - for Linux run:  source env/bin/activate


# Install Dependencies:

    Create txt file so we can install dependencies later on new machine 

     -type in terminal:  New-Item requirements.txt -type file

     inside add dependencies for example. These no need to add now it is just example:
     Flask==2.0.1
     requests==2.26.0
     numpy==1.26.0
     later add new dependencies

    Use pip to install dependencies:
     - pip install -r requirements.txt

       this will install all dependencies what we add while building a project.
