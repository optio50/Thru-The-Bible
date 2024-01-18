#!/usr/bin/env python3
filename = ''
from datetime import datetime
import eyed3
import os
import sys
import signal
import re
import glob
import wget
from bs4 import BeautifulSoup
import requests
import shutil
import glob
import textwrap
from random import randint
from time import sleep

# Local import
from colors import colors


def Banner():
    content = r"""
 (Indivdual 25 Min Radio Broadcast Versions)
 Thru The Bible 
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
"""
    print(colors.fg.dodger_blue_1, content, colors.reset)
    print(colors.fg.dark_orange,f"""
Listen Online
https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee

Free Study Booklets
https://ttb.org/resources/electronic-booklets""")




def signal_handler(sig, frame):
    print('')
    if filename == "":
        sys.exit(0)
        # print(filename)
    print(colors.fg.red, "Ctrl+C Detected:   Removing Incomplete File ---->  ", filename, colors.reset)
    for file in glob.glob(filename + '*tmp'):
        # print(file)
        os.remove(file)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)




def duration_from_seconds(s):
    """Module to get the convert Seconds to a time like format."""
    s = s
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    timelapsed = "{:02d}:{:02d}:{:02d}  (hh:mm:ss)".format(int(h), int(m), int(s))
    return timelapsed


def eyed3_info(filename, comment, title):
    # global error_log
    try:

        print("\033[2A", "\033[1G", "\033[J")
        print('EyeD3 MP3 Tagger\n')
        print(colors.fg.purple_1b, "Setting mp3 Tags \t[✔]\n")
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
        audiofile.tag.images.set(3, open('FRONT_COVER1.jpg', 'rb').read(), 'image/jpeg')
        audiofile.tag.save(filename, version=(2, 3, 0))
        print(colors.fg.cyan, "Displaying mp3 Tags \t[✔]\n")
        audiofile = eyed3.load(filename)
        print(colors.fg.grey_19, 'File Name:......: ', colors.fg.green, filename, sep="")
        print(colors.fg.grey_19, 'Artist..........: ', colors.fg.orange_3, audiofile.tag.artist, sep="")
        print(colors.fg.grey_19, 'Title...........: ', colors.fg.orange_3, audiofile.tag.title, sep="")
        print(colors.fg.grey_19, 'Album...........: ', colors.fg.orange_3, audiofile.tag.album, sep="")
        print(colors.fg.grey_19, 'Album Artist....: ', colors.fg.orange_3, audiofile.tag.album_artist, sep="")
        print(colors.fg.grey_19, 'Duration........: ', colors.fg.orange_3, duration_from_seconds(audiofile.info.time_secs),
              sep="")
        print(colors.fg.grey_19, 'Filesize........: ', colors.fg.orange_3,
              "{0:.2f}".format(audiofile.info.size_bytes / 1048576), 'MB', sep="")
        print(colors.fg.grey_19, 'BitRate.........: ', colors.fg.orange_3, audiofile.info.bit_rate_str, sep="")
        print(colors.fg.grey_19, 'Sample Rate.....: ', colors.fg.orange_3, audiofile.info.sample_freq, sep="")
        print(colors.fg.grey_19, 'Mode............: ', colors.fg.orange_3, audiofile.info.mode, sep="")
        print(colors.fg.grey_19, 'Genre...........: ', colors.fg.orange_3, audiofile.tag.genre, sep="")
        print(colors.fg.grey_19, 'Website.........: ', colors.fg.orange_3, audiofile.tag.artist_url, sep="")
        print(colors.fg.grey_19, 'Comment.........: ', sep="", end="")
        print(colors.fg.dodger_blue_1, end="")
        print(textwrap.fill(str(audiofile.tag.comments[0].text),width=70, subsequent_indent='\t     '))
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
        print('=' * 75)
        sys.stdout.close()
        sys.stdout = original
        print(colors.fg.red, "Mp3 File Error...EyeD3 Failed to set Tags for ", colors.fg.hot_pink_1b, filename, colors.reset)
        return error_log
        pass
    print(colors.reset)




def wget_cmd(mp3_url,filename):
    #if os.path.isfile(filename):
    # os.remove(filename)
    print(colors.fg.grey_19, "Brief Random Delay to avoid remote server congestion ")
    sleep(randint(3, 8))
    print(colors.fg.dodger_blue_1, "Downloading........", filename, colors.reset)
    #print(mp3_url)
    wget.download(mp3_url, out=filename)
    print('')




def books():
    book = ["1-chronicles", "1-corinthians", "1-john", "1-kings", "1-peter", "1-samuel", "1-thessalonians"
        , "1-timothy", "2-chronicles", "2-corinthians", "2-john", "2-kings", "2-peter", "2-samuel", "2-thessalonians"
        , "2-timothy", "3-john", "acts", "amos", "colossians", "daniel", "deuteronomy", "ecclesiastes", "ephesians"
        , "esther", "exodus", "ezekiel", "ezra", "galatians", "genesis", "habakkuk", "haggai"
        , "hebrews", "hosea", "isaiah", "james", "jeremiah", "job", "joel", "john", "jonah", "joshua", "jude", "judges"
        , "lamentations", "leviticus", "luke", "malachi", "mark", "matthew", "micah", "nahum", "nehemiah", "numbers"
        , "obadiah", "philemon", "philippians", "proverbs", "psalm", "revelation", "romans", "ruth", "song-of-solomon"
        , "titus", "zechariah", "zephaniah", "guidelines"]
    return book


def menu():
    menu_banner = """
1.  1-chronicles      (12 broadcasts)       24. ephesians   (28 broadcasts)     47. luke        (29 broadcasts)
2.  1-corinthians     (24 broadcasts)       25. esther      (10 broadcasts)     48. malachi     (15 broadcasts)
3.  1-john            (25 broadcasts)       26. exodus      (36 broadcasts)     49. mark        (19 broadcasts)
4.  1-kings           (13 broadcasts)       27. ezekiel     (25 broadcasts)     50. matthew     (38 broadcasts)
5.  1-peter           (15 broadcasts)       28. ezra        (7  broadcasts)     51. micah       (17 broadcasts)
6.  1-samuel          (15 broadcasts)       29. galatians   (20 broadcasts)     52. nahum       (8  broadcasts)
7.  1-thessalonians   (14 broadcasts)       30. genesis     (55 broadcasts)     53. nehemiah    (12 broadcasts)
8.  1-timothy         (12 broadcasts)       31. habakkuk    (10 broadcasts)     54. numbers     (15 broadcasts)
9.  2-chronicles      (17 broadcasts)       32. haggai      (9  broadcasts)     55. obadiah     (5  broadcasts)
10. 2-corinthians     (17 broadcasts)       33. hebrews     (43 broadcasts)     56. philemon    (1  broadcasts)
11. 2-john            (5  broadcasts)       34. hosea       (15 broadcasts)     57. philippians (18 broadcasts)
12. 2-kings           (15 broadcasts)       35. isaiah      (49 broadcasts)     58. proverbs    (31 broadcasts)
13. 2-peter           (14 broadcasts)       36. james       (16 broadcasts)     59. psalm       (54 broadcasts)
14. 2-samuel          (15 broadcasts)       37. jeremiah    (20 broadcasts)     60. revelation  (66 broadcasts)
15. 2-thessalonians   (6  broadcasts)       38. job         (23 broadcasts)     61. romans      (36 broadcasts)
16. 2-timothy         (8  broadcasts)       39. joel        (8  broadcasts)     62. ruth        (7  broadcasts)
17. 3-john            (4  broadcasts)       40. john        (40 broadcasts)     63. solomon     (13 broadcasts)
18. acts              (35 broadcasts)       41. jonah       (11 broadcasts)     64. titus       (5  broadcasts)
19. amos              (16 broadcasts)       42. joshua      (13 broadcasts)     65. zechariah   (34 broadcasts)
20. colossians        (11 broadcasts)       43. jude        (12 broadcasts)     66. zephaniah   (7  broadcasts)
21. daniel            (30 broadcasts)       44. judges      (11 broadcasts)     67. guidelines  (10 broadcasts)
22. deuteronomy       (20 broadcasts)       45. lamentations(2  broadcasts)
23. ecclesiastes      (12 broadcasts)       46. leviticus   (30 broadcasts)


70. The complete compilation of Dr. McGee's full Notes & Outlines all in one eBook!
"""


    print(colors.fg.green, menu_banner, colors.reset)

    # make sure user input is a number
    user_input = False
    while not user_input:
        try:
            book_mp3 = int(input("Enter Book Number to Download  "))
            user_input = True  # we only get here if the previous line didn't throw an exception
        except ValueError:
            print(colors.fg.red, "Error:", "  Book Number Expected    'CTRL+C' if you want to exit", colors.reset)

    if book_mp3 == 68:  # Secret Menu Entry
        print(colors.fg.hot_pink_1b, "Downloading mp3's for All Books...Warning this is a 22GB Download", colors.reset)
        #with open('vernon_mcgee-html-links.txt', 'r') as file:
        book_mp3 = 1
        for x in book:
            get_files(book, book_mp3)
            book_mp3 += 1
    
    elif book_mp3 == 70:
        print(colors.fg.dodger_blue_1, "Downloading........Briefing the Bible\n This is the complete compilation of Dr. McGee's full Notes & Outlines you're used to, now all in one eBook!", colors.reset)
        #print(mp3_url)
        wget.download('https://ttb.org/docs/default-source/extra-materials/ttb_-briefing-the-bible_digital-book.pdf', out="1.Thru the Bible - Briefing the Bible eBook.pdf")
        print('')

    else:
        get_files(book, book_mp3)
    
def get_files(book, book_mp3):
    print(colors.fg.turquoise_4, f"Downloading mp3's for " ,f"{book[book_mp3 - 1]}", colors.reset)
    with open('vernon_mcgee-html-links.txt', 'r') as file:
        for line in file:
            thebook = book[book_mp3 - 1].lower()
            #print(thebook)
            line = line.strip()
            #print(line)
            if line.startswith(f"https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee/series/{thebook}"):
                line = line.strip()
                print("Retrieving Broadcast Page")
                print(f"Broadcast page is ",colors.fg.hot_pink_1b, f"{line}\n",colors.reset)

                html_text = requests.get(line)
                soup = BeautifulSoup(html_text.text, 'html.parser')
                #link = soup.find_all(href="https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee/listen/")
                num_of_links = []

                for link in soup.find_all('a', href=True):
                    #link = link['href'].strip()
                    if re.search(r'(https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee/listen/\w.*)', str(link)):
                        #print(link['href'])
                        num_of_links.append(link['href'])
                no_broadcasts = len(num_of_links)
                mp3_url = None
                counter = 1
                for link in soup.find_all('a', href=True):
                    if re.search(r'(https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee/listen/\w.*)', str(link)):
                        if link['href'] == mp3_url:
                            continue
                        else:
                            mp3_url = link['href']
                            html_text = requests.get(mp3_url)
                            soup = BeautifulSoup(html_text.text, 'html.parser')
                            title = soup.find('div', class_="details").h2.text.replace('—', '--')
                            comment = soup.find('div', class_="fs-16 desc epDesc").p.text
                            comment = comment.replace('\n', ' ')
                            #comment = textwrap.fill(comment, width=80)
                            mp3_url = mp3_url.replace('/listen/', '/subscribe/podcast/')
                            mp3_url = mp3_url.replace('.html', '.mp3')
                            print(colors.fg.blue_1,'=' * 80,colors.reset)
                            print(f"File {counter} of {no_broadcasts:.0f}")
                            print(colors.fg.orange_red_1,f"Title is:  {title}\nMP3 URL:", colors.fg.yellow_2, f"   {mp3_url}\n",colors.reset,sep='')
                            #print(colors.fg.dodger_blue_1,comment,'\n\n',colors.reset)
                            global filename
                            filename = f"Thru The Bible with J Vernon Mcgee - {title}.mp3"
                            if os.path.isfile(filename):
                                print(colors.fg.red, f"Existing File Found........",colors.fg.green,f"Skipping",colors.reset)
                                mp3_url = link['href']
                                counter += 1
                                continue
                            while True:
                                try:
                                    wget_cmd(mp3_url, filename)
                                except (AttributeError, ConnectionResetError):  # Data file might be old and one of the files is no loger available
                                    #print(colors.fg.red, f"Episode No Longer Available...", colors.fg.yellow, f" {title}", colors.fg.red,
                                    #      "\n Delete data file and re-run", colors.reset)
                                    #counter += 1
                                    continue
                                break
                            eyed3_info(filename, comment, title)
                            mp3_url = link['href']
                            counter += 1
                print('')
                #quit()







def get_data_files():

    if not os.path.isfile('vernon_mcgee-html-links.txt'):# and os.path.isfile('vernon_mcgee-mp3-links.txt'):
        print(colors.fg.red, "Data File not Found...[X]...Downloading New Data Files.", colors.reset)
        print("Retrieving New Data File")
        html_text = requests.get("https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee/series/")
        soup = BeautifulSoup(html_text.text, 'html.parser')
        link = soup.find_all(href="https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee/series/")

        for link in soup.find_all('a', href=True):
            with open('vernon_mcgee-html-links.txt', 'a+') as file:
                if not re.search(r'(https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee/series/\w+)', str(link)):
                #if link.get('href').startswith("https://www.oneplace.com/ministries/thru-the-bible-with-j-vernon-mcgee/series/"):
                    continue
                else:
                    file.write(f"{link['href'].lower()} \n")


Banner()
get_data_files()
book = books()
menu()
