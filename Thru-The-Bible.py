#!/usr/bin/env python3
filename = ""
error_log = "0"
from datetime import datetime
import eyed3
import os
import sys
import signal
import glob
import wget
from bs4 import BeautifulSoup
import requests
import shutil
import textwrap
from random import randint
from time import sleep

def signal_handler(sig, frame):
    print('')
    if filename == "":
        sys.exit(0)
        #print(filename)
    print(colors.fg.red,"Ctrl+C Detected:   Removing Incomplete File ---->  ", filename, colors.reset)
    for file in glob.glob(filename + '*tmp'):
        #print(file)
        os.remove(file)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# colored text and background
"""Colors class:reset all colors with colors.reset
two sub classes
fg for foreground
and bg for background
use as colors.subclass.colorname.
i.e. colors.fg.red or colors.bg.green.
also, the generic bold, disable, underline, reverse, strike through, and invisible
work with the main class i.e. colors.bold"""


class colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        brown = '\033[38;5;94m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[38;5;202m'
        blue = '\033[34m'
        purple = '\033[38;5;93m'
        cyan = '\033[36m'
        grey = '\033[38;5;240m'
        lime = '\033[38;5;154m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[38;5;154m'
        lightblue = '\033[38;5;26m'
        pink = '\033[38;5;207m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


def Banner():
    content = r"""
 (Indivdual 25 Min Radio Broadcast Versions)
 Through The Bible 
 with
 Dr. J. Vernon McGee
    _               _
   .'_`\           .' `\
  (_( \ \         (_( \ \
       \ \             \ \
        \ \ ____________\ \
         \.'====. = .===='.\
         ((      ) (      ))
          \\____//^\\____//
           '----'   '----'
      __...--~~~~~-._   _.-~~~~~--...__
    //               `V'               \\ 
   //                 |                 \\ 
  //__...--~~~~~~-._  |  _.-~~~~~~--...__\\ 
 //__.....----~~~~._\ | /_.~~~~----.....__\\
====================\\|//====================
                    `---`

https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee
"""
    print(colors.fg.lightblue, content, colors.reset)


def duration_from_seconds(s):
    """Module to get the convert Seconds to a time like format."""
    s = s
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    timelapsed = "{:02d}:{:02d}:{:02d}  (hh:mm:ss)".format(int(h),int(m),int(s))
    return timelapsed


def eyed3_info():
    #global error_log
    try:

        print("\033[2A","\033[1G","\033[J")
        print('EyeD3 MP3 Tagger\n')
        print(colors.fg.purple, "Setting mp3 Tags \t[✔]\n")
        audiofile = eyed3.load(filename)
        eyed3.log.setLevel("ERROR")
        audiofile.initTag()
        audiofile.tag.artist = "Dr. J. Vernon Mcgee"
        audiofile.tag.album = "Thru The Bible"
        audiofile.tag.genre = "Christian"
        audiofile.tag.album_artist = "Dr. J. Vernon Mcgee"
        audiofile.tag.title = title
        audiofile.tag.comments.set(comment)
        audiofile.tag.artist_url = bytes("http://ttb.org", encoding='utf8')
        audiofile.tag.images.set(3, open('FRONT_COVER1.jpg','rb').read(), 'image/jpeg')
        audiofile.tag.save(filename, version=(2, 3, 0))
        print(colors.fg.cyan, "Displaying mp3 Tags \t[✔]\n")
        audiofile = eyed3.load(filename)
        print(colors.fg.grey,'File Name:......: ',colors.fg.green, filename, sep="")
        print(colors.fg.grey,'Artist..........: ',colors.fg.orange, audiofile.tag.artist, sep="")
        print(colors.fg.grey,'Title...........: ',colors.fg.orange, audiofile.tag.title, sep="")
        print(colors.fg.grey,'Album...........: ',colors.fg.orange, audiofile.tag.album, sep="")
        print(colors.fg.grey,'Album Artist....: ',colors.fg.orange, audiofile.tag.album_artist, sep="")
        print(colors.fg.grey,'Duration........: ',colors.fg.orange, duration_from_seconds(audiofile.info.time_secs), sep="")
        print(colors.fg.grey,'Filesize........: ',colors.fg.orange, "{0:.2f}".format(audiofile.info.size_bytes / 1048576),'MB', sep="")
        print(colors.fg.grey,'BitRate.........: ',colors.fg.orange, audiofile.info.bit_rate_str, sep="")
        print(colors.fg.grey,'Sample Rate.....: ',colors.fg.orange, audiofile.info.sample_freq, sep="")
        print(colors.fg.grey,'Mode............: ',colors.fg.orange, audiofile.info.mode, sep="")
        print(colors.fg.grey,'Genre...........: ',colors.fg.orange, audiofile.tag.genre, sep="")
        print(colors.fg.grey,'Website.........: ',colors.fg.orange, audiofile.tag.artist_url.decode('UTF-8'), sep="")
        print(colors.fg.grey,'Comment.........: ', sep="", end="")
        print(colors.fg.lightblue, end="")
        print(audiofile.tag.comments[0].text)
    except Exception:
        error_log = 1
        original = sys.stdout
        sys.stdout = open('Get-Vernon.log', 'a+')
        # datetime object containing current date and time
        now = datetime.now()
        # Mon 25 Nov 2021 H:M:S
        dt_string = now.strftime("%a %d %b %Y %H:%M:%S")
        print("Error Event Time:  ", dt_string)
        print("Mp3 File Error...EyeD3 Failed to set Tags for", filename)
        print('='*75)
        sys.stdout.close()
        sys.stdout = original
        print(colors.fg.red,"Mp3 File Error...EyeD3 Failed to set Tags for ",colors.fg.pink, filename, colors.reset)
        return error_log
        pass
    print(colors.reset)



def wget_cmd(mp3_url):
    #if os.path.isfile(filename):
        #os.remove(filename)
    print(colors.fg.grey,"Brief Random Delay to avoid remote server congestion ")
    sleep(randint(3,8))
    print(colors.fg.lightblue, "Downloading........", filename,colors.fg.grey)
    wget.download(mp3_url, out=filename)


def get_data_files():
    print(colors.fg.lightcyan,"Checking for Cover Art File", colors.reset)
    if os.path.isfile('FRONT_COVER1.jpg'):
        print(colors.fg.cyan,"Cover Art File Found [✔]", colors.reset)
    else:
        print(colors.fg.red,"Cover Art File not Found...[X]...A Sutiable Cover Art file named FRONT_COVER1.jpg is required.", colors.reset)
        quit()
    print(colors.fg.lightcyan,"Checking for Data Files", colors.reset)
    if os.path.isfile('vernon_mcgee-html-links.txt') and os.path.isfile('vernon_mcgee-mp3-links.txt'):
        print(colors.fg.cyan,"Data Files Found [✔]", colors.reset)
    else:
        print(colors.fg.red,"Data Files not Found...[X]...Downloading New Data Files.", colors.reset)
        if os.path.isfile('vernon_mcgee-html-links.txt'):
            os.remove('vernon_mcgee-html-links.txt')
        if os.path.isfile('vernon_mcgee-mp3-links.txt'):
            os.remove('vernon_mcgee-mp3-links.txt')

        for i in range(1, 12):
            print("Retrieving Page {} of 11".format(i))
            html_text = requests.get(
                "https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee/listen/?page={}".format(i)).text
            soup = BeautifulSoup(html_text, 'lxml')
            # link = soup.find_all(href="https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee/listen/")
            link = soup.find_all("a", {'data-action': "archive"})
            # link = soup.find_all('a',attrs={'data-action':"archive"})[]['href']
            #original_stdout = sys.stdout  # Save a reference to the original standard output

            for links in link:
                with open('vernon_mcgee-html-links.txt', 'a+') as file:
                    #sys.stdout = file  # Change the standard output to the file we created.
                    soup.find_all("a", href=True)
                    # a_file.write(str(links) + '\n')
                    file.write(links['href'] + '\n')
                    #print(links['href'])
                    #sys.stdout = original_stdout  # Reset the standard output to its original value
        src = "vernon_mcgee-html-links.txt"
        dst = "vernon_mcgee-mp3-links.txt"
        shutil.copyfile(src, dst)
        # read input file
        fin = open("vernon_mcgee-mp3-links.txt", "rt")
        # read file contents to string
        data = fin.read()
        # replace all occurrences of the required string
        data = data.replace('.html', '.mp3').replace('listen/', 'subscribe/podcast/')
        # close the input file
        fin.close()
        # open the input file in write mode
        fin = open("vernon_mcgee-mp3-links.txt", "wt")
        # overwrite the input file with the resulting data
        fin.write(data)
        # close the file
        fin.close()
        print("\033[15A","\033[1G","\033[J")


def bs4_title_cmd(html_url):
    html_text = requests.get(html_url).text
    soup = BeautifulSoup(html_text, 'lxml')
    # Get the comment & title from the HTML element
    comment = soup.find("div", class_="description").text.lstrip()
    # Wrap the text and limit the line length to 80
    comment = textwrap.fill(comment, width=80)
    # get the title from the H2 tag, strip leading white space and replace the funky double dash with a real double dash
    title = soup.find("div", class_="overlay2").h2.text.strip().replace('—', '--')
    # alternate method of getting the title
    #title = soup.head.title.text.split(' -')[0].strip().replace('—', '--')
    return comment, title


def books():
    book = ["1-chronicles", "1-corinthians", "1-john", "1-kings", "1-peter", "1-samuel", "1-thessalonians"
        , "1-timothy", "2-chronicles", "2-corinthians", "2-john", "2-kings", "2-peter", "2-samuel", "2-thessalonians"
        , "2-timothy", "3-john", "acts", "amos", "colossians", "daniel", "deuteronomy", "ecclesiastes", "ephesians"
        , "esther", "exodus", "ezekiel", "ezra", "galatians", "genesis", "habakkuk", "haggai"
        , "hebrews", "hosea", "isaiah", "james", "jeremiah", "job", "joel", "john", "jonah", "joshua", "jude", "judges"
        , "lamentations", "leviticus", "luke", "malachi", "mark", "matthew", "micah", "nahum", "nehemiah", "numbers"
        , "obadiah","philemon", "philippians", "proverbs", "psalm", "revelation", "romans", "ruth", "song-of-solomon"
        , "titus", "zechariah", "zephaniah", "guidelines"]
    return book


def menu():
    menu_banner = """
1.  1-chronicles      24. ephesians   47. luke
2.  1-corinthians     25. esther      48. malachi
3.  1-john            26. exodus      49. mark
4.  1-kings           27. ezekiel     50. matthew
5.  1-peter           28. ezra        51. micah
6.  1-samuel          29. galatians   52. nahum
7.  1-thessalonians   30. genesis     53. nehemiah
8.  1-timothy         31. habakkuk    54. numbers
9.  2-chronicles      32. haggai      55. obadiah
10. 2-corinthians     33. hebrews     56. philemon
11. 2-john            34. hosea       57. philippians
12. 2-kings           35. isaiah      58. proverbs
13. 2-peter           36. james       59. psalm
14. 2-samuel          37. jeremiah    60. revelation
15. 2-thessalonians   38. job         61. romans
16. 2-timothy         39. joel        62. ruth
17. 3-john            40. john        63. song-of-solomon
18. acts              41. jonah       64. titus
19. amos              42. joshua      65. zechariah
20. colossians        43. jude        66. zephaniah
21. daniel            44. judges      67. guidelines
22. deuteronomy       45. lamentations
23. ecclesiastes      46. leviticus
"""


    mp3_links = []
    title_links = []

    print(colors.fg.green, menu_banner, colors.reset)

    # make sure user input is a number
    user_input = False
    while not user_input:
        try:
            book_mp3 = int(input("Enter Book Number to Download  "))
            user_input = True # we only get here if the previous line didn't throw an exception
        except ValueError:
            print(colors.fg.red,"Error:", "  Book Number Expected    'CTRL+C' if you want to exit", colors.reset)

    if book_mp3 == 68: # Secret Menu Entry
        print(colors.fg.pink,"Downloading mp3's for All Books...Warning this is a 22GB Download", colors.reset)
        with open('vernon_mcgee-html-links.txt', 'r') as file:
            for line in file:
                title_links.append(line.strip())
        with open('vernon_mcgee-mp3-links.txt', 'r') as file:
            for line in file:
                mp3_links.append(line.strip())
    else:
        print(colors.fg.lightcyan,"Downloading mp3's for " + book[book_mp3 - 1].capitalize(), colors.reset)
        with open('vernon_mcgee-html-links.txt', 'r') as file:
            for line in file:
                if book[book_mp3 - 1] in line:
                    title_links.append(line.strip())
        with open('vernon_mcgee-mp3-links.txt', 'r') as file:
            for line in file:
                if book[book_mp3 - 1] in line:
                    mp3_links.append(line.strip())
    #title_links.reverse()
    #mp3_links.reverse()
    return title_links, mp3_links, book_mp3


Banner()
get_data_files()
book = books()
title_links, mp3_links, book_mp3 = menu()
end_num = len(title_links)
count = 1
while count <= end_num:

    try:
        comment, title = bs4_title_cmd(title_links[count-1])
    except AttributeError: # Data file might be old and one of the files is no loger available
        print(colors.fg.red,"Episode No Longer Available...",colors.fg.yellow + title_links[count-1], colors.fg.red, "\n Delete data files and re-run", colors.reset)
        count = count + 1 # Index the counter for the next file to be downloaded
        continue
    filename = "Through The Bible with J Vernon Mcgee - {0}"'.mp3'.format(str(title))
    if os.path.isfile(filename):
        print(colors.fg.brown, "Existing File Found......Skipping", colors.fg.orange, title, colors.reset)
        count = count + 1
        continue
    print(colors.reset, "=" * 70)
    print(colors.fg.lime,"File {} of {}".format(count, end_num))
    wget_cmd(mp3_links[count-1])
    error_log = eyed3_info()
    count = count + 1
if error_log == 1:
    print('*'*70)
    print(colors.fg.red,"Some Errors were encountered. Check Log file --->  Get-Vernon.log",colors.reset)
    print('='*70)
    log = open("Get-Vernon.log", "r")
    for line in log:
        print(line)
