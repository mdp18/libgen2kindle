#!/usr/bin/env python

import scrape_libgen
import mail
import math, requests, sys, os, subprocess, json, configparser
from tqdm import tqdm
from bs4 import BeautifulSoup

parser = configparser.ConfigParser()
parser.read('settings.ini')
incompatibleext = [".mobi", ".azw", ".pdf"]

def check_email_settings():
    kindle_email = parser['general']['kindle-email'].replace('"', '')
    user_email = parser['general']['your-email'].replace('"', '')
    user_password = parser['general']['your-password'].replace('"', '')
    if kindle_email != "" and user_email != "" and user_password != "":
        return True
    else:
        return False

def file_safe_name(name):
                return name.replace(":"," ").replace("/"," ").replace("\\"," ").replace("*"," ").replace("?"," ").replace('"'," ").replace("<"," ").replace(">"," ").replace("|"," ")[:255]

def convertandsend(outputname,output_path,ext_to_convert_to):
    current_ext = output_path.split(".")[-1]
    converted_path = output_path.replace(current_ext,ext_to_convert_to)
    converted_name = outputname.replace(current_ext,ext_to_convert_to)
    print("Converting to {0} format".format(ext_to_convert_to))
    process = subprocess.Popen(['Calibre2\ebook-convert',output_path,converted_path],stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)
    process.wait()
    if check_email_settings() == True:
        mail.send(converted_name, converted_path)
        print("File sent to Kindle, Please wait 5-10 minutes for it to appear on the device.")
    else:
        print("\n")
        print("Your mail settings have not been configured. Please check settings.ini \n")

def check_site(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return True
    except:
        return False

def main(search_param):

    libgen_urls = json.loads(parser['general']['libgen-urls'])

    if not search_param:
        print("Please provide a search term as argument (ex: main.py 'search term')")
    else:
        for url in libgen_urls:
            if check_site(url):
                r = requests.get(url +'/index.php?req=' + search_param)
                soup = BeautifulSoup(r.content, "html5lib")
                libgen_data = scrape_libgen.get_libgen_data(soup)
                break
            else:
                print("Could not connect to " + url)
                print("Trying next url..")
                continue
        else:
            print("Could not connect to any url")
            sys.exit()
        print("\n")
        print("Found " + str(len(libgen_data)) + " results")
        print("format: [index] [title] [author] [year(if any)] [size] [extension]")
        for x in libgen_data:
            author = libgen_data[x]["author"]
            title = libgen_data[x]["title"][:80] #limits title to 80 characters
            extension = libgen_data[x]["extension"]
            num_pages = libgen_data[x]["num_pages"]
            year_published = libgen_data[x]["year_published"]
            if year_published == '':
                year_published = ''
            else:
                year_published = "- (" + year_published + ") -"
            extension = libgen_data[x]["extension"]
            size = libgen_data[x]["size"]

            print("[%d] %s - %s %s %s %s" % (x, title, author, year_published, size, extension))

        new_search = input("Search again or [Enter] to continue: ")

        try:
            if isinstance(int(new_search), int):
                print("Wrong input")
                new_search = input("Search again or [Enter] to continue to download: ")
        except ValueError:
            new_search = new_search

        if new_search != "":
            search_term = ''.join(new_search)
            main(search_term)
        else:
            print("Please enter the index of the book you want or press any other key to search again")

            index_selection = input("Index > ")

            try:
                selection = int(index_selection)
            except ValueError:
                print("Wrong input")
                print("You had to provide the index of the book.")
                return None


            print ("\nDownloading book...")

            request_book = requests.get(scrape_libgen.get_download_url(libgen_data[selection]["download_link"]), stream=True)
            total_size = int(request_book.headers.get('content-length', 0));


            print ("Saving Book...")
            
            book_name = libgen_data[selection]["title"] + "." + libgen_data[selection]["extension"]
            extension = os.path.splitext(book_name)[1]
            book_name = file_safe_name(book_name)

            with open(book_name, 'wb') as handle:
                for block in tqdm(request_book.iter_content(4096), total=math.ceil(total_size//4096) , unit='KB', unit_scale=True):
                    handle.write(block)
            path = "./" + book_name
            print(book_name) # eg. Atomic habits.epub
            print(path) # eg. ./Atomic habits.epub
            send_mail = input("Do you wish upload to your kindle? (y/n) :> ")

            if send_mail == "y":
                if extension in incompatibleext:
                    convertandsend(book_name,path,'.epub')
                else:
                    if check_email_settings() == True:
                        mail.send(book_name, path)
                        print ("Email has been successfully sent. please give it some time to appear.")
                    else:
                        print("\n")
                        print("Mailing not configured. Find kindle_mail.py using: \n -- 'which kindle_mail.py' then open the file and edit email settings with your fav editor \n")

            else:
                print("Book saved.")

            search_again = input("Enter 'exit' or search again: ")

            if search_again != "exit":
                main(search_again)
            else:
                return None



if __name__ == '__main__':
    search_param = ' '.join(sys.argv[1:])
    main(search_param)
