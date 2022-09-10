# Library Genesis 2 Kindle

## About
I really enjoy using my kindle to read academic journals I find off of libgen.rs. However, the steps you need to take in order to get it on the kindle are far too many. This script saves you the hassle by making it extremely each to search, download, and send articles directly to your kindle.
Note: For the time being, this will only function for Windows based environments. This is due in part because of the ebook conversion tool used from the calibre binaries.

## Features
Below are a list of features that are currently implemented with additional features coming soon.
- [x] Easy to use Terminal UI.
- [x] Simple Configuration File.
- [x] Library Genesis Mirror Link Retry Function
- [x] downloaded file (PDF,Mobi,etc.) to epub conversion (Amazon is looking towards epub being a standard with mobi and azw being deprecated.)
- [x] SMTP Email Configuration
- [] pip installation
- [] bulk download and send to kindle
- [] direct download and send by libgen link



## Installation
1. Install Pipenv (https://pipenv.pypa.io/en/latest/install/)
    - If you are simply looking to use this quickly and have pip installed, you can run: ```pip install --user pipenv```
2. Run the following clone command: ``` git clone https://github.com/mdp18/libgen2kindle.git```
3. Run ```pipenv sync``` and ```pipenv shell``` to install the required dependencies and subsequently open the virtualized python shell environment.

## Configuration
### Amazon Kindle Email
In order for the application to know where to send the ebook to, it needs your Amazon provided email address that is associated with your kindle. This can be found here: https://www.amazon.com/sendtokindle/email

Once retrieved, this can be inputted into the configuration file by opening settings.ini within the root directory of the application.
### Email SMTP Provider
In order to send your downloaded ebook/journal to your kindle, you must provide an email account to send it. Within the settings file, you will see three variables:
1. Email Provider - This is your email company. For the time being, we support Gmail, Live (Hotmail,Outlook,etc.), and Yahoo.
2. Email Address - This is your email address you will be sending the ebook with.
3. Email Password - This is the password to your email account.
    - Note: For the sake of security, it is recommened you turn on 2fa and use an app-specific password feature such as what Google has. (ref: https://www.lifewire.com/get-a-password-to-access-gmail-by-pop-imap-2-1171882)
### Library Genesis Mirror Links
For the sake of keeping this application working as long as possible I have implemented the ability to choose which library genesis mirror links are used to download the ebooks. In the scenario that one of the links doesnt work, the application will automatically attempt to use the next one in the list. This list can be configured in Settings.ini.

## Usage
1. traverse into the root directory of the cloned repo: ``` cd libgen2kindle ```
2. Run the main file with the following format ```main.py "search term"```
    - Note: You will ned to ensure you use "quotations" if you have any spaces in your search term.
3. Follow prompts within terminal.

## Credits

"If it's a good idea, go ahead and do it. It's much easier to apologize than it is to get permission."
-Grace Hopper

The work I have done here is an extension of an python2 implementation of a Library Genesis 2 Kindle Utility. I have gone ahead and converted much of it to python3 to use as a template for my program with additional features added and modified. Credit goes to https://github.com/shashanoid/Gen2Kindle for work done in the past. :tada: