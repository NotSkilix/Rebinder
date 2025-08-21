# Rebinder
*NotSkilix* - May 2025

---

## Introduction
A small python project that allows the user to rebind a key to another one. \
Its main role is to fix issues such as "my 'F' keys are broken" etc...

Also contains a little interface for the user.

## Project Setup (user)
**⚠️ Currently, the application is only available through the GitHub [Release](https://github.com/NotSkilix/Rebinder/releases) page of this project, there is no other way to download this application ⚠️**.

You will be able to download the most recent version of the project by going to the bottom of the release text that contains the "latest" tag, like seen below: \
![image](https://github.com/user-attachments/assets/92deb5d8-20a2-47e2-a333-7493305b557c) \
In the end of the text explaining what's new to this version and what is set for the next one, you'll be able to find the `.exe` file, download it and run it. 

> Your antivirus might find this program dangerous and even try to block it. It is not a malware, the code is open source as you know \
> Note that build is only available since the version 0.3 and higher


## Project Setup (dev)
### Clone the project
Download the zip file from the repository or clone it using git:
```bash
git clone git@github.com:NotSkilix/Rebinder.git
```
Or with HTTPS:
````bash
https://github.com/NotSkilix/Rebinder.git
````

### Install the requirements
#### Virtual environment
It's recommended to create a virtual environment before installing the requirements. \

You can either do this manually: \
To do so, you can use the following command:
```bash
python -m venv venv
```
Then, activate the virtual environment:
```bash
venv\Scripts\activate
```

Or if you have PyCharm from JetBrains, you can create a virtual environment directly from the IDE. \
To do so, go to `File > Settings > Project: Rebinder > Python Interpreter` and select the option to create a new virtual environment. \
Then, select the location of the virtual environment and click on `OK`. 

#### The rest
Once the virtual environment is created (or not if you want it to be installed globally), you can install the requirements using the following command:
```bash
pip install -r requirements.txt
```

You are now ready to run the project. 
