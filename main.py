import requests
from bs4 import BeautifulSoup
import re
import fs
from colorama import Fore, Style
from rich import print
import pyfiglet
import time
import os


# gotta make it look cool
if os.name == 'nt': 
    os.system('cls')
else:
    os.system('clear')

title = pyfiglet.figlet_format('AUTO-WGET', font='puffy', justify="center")
print(f'[bold magenta]{title}[/bold magenta]')
print(f'[green]Created by [/green][bold cyan]Rednotsus[/bold cyan]')
print("      ")
print("       ")
start_time = time.time()
print(f"[yellow][ AUTO-WGET ]  |  Starting auto-wget")
print(f"[yellow][ AUTO-WGET ]  |  Please enter the URL of the website you want to download from")
url = input()

print(f"[yellow][ AUTO-WGET ]  |  Scraping website...")

wget_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wget.sh')

file = open(wget_path, "a")

source = requests.get(url).text
episodes = 0

soup = BeautifulSoup(source, 'html.parser')
name_divs = soup.find_all('div', class_='centerflex name-div')

for div in name_divs:
    episodes += 1
time.sleep(0.5)
print(f"[green][ AUTO-WGET ]  |  Scraped {episodes} episodes")
print(f"[yellow][ AUTO-WGET ]  |  Generating wget script...")
print()
time.sleep(0.5)

totalmb = 0
for div in name_divs:
    a_tag = div.find('a')
    if a_tag:
        name = a_tag.text
        if "Parent Directory" not in name:
            match = re.match(r"(.*).S(\d{2})E(\d{2}).*", name, re.IGNORECASE)
            if match:
                series_name, season, episode = match.groups()
                series_name = series_name.replace('.', ' ')
                formatted_name = f"{series_name} - S{season}E{episode}"
                link = "https://vadapav.mov" + a_tag['href']
                file.write(f"wget '{link}' -O '{formatted_name}.mkv'\n")
                print(f"[green][ AUTO-WGET ]  |  Added {formatted_name}")
                time.sleep(0.025)
            size_div = div.find_next_sibling('div', class_='size-div')
            if size_div:
                mbsize = round(int(size_div.text)/1048576)
                totalmb += mbsize
gbsize = round(totalmb/1024, 2)
elapsed_time = float(time.time() - start_time)
print()
print(f"[yellow][ AUTO-WGET ]  |  Generated wget script at {os.path.dirname(os.path.abspath(__file__))}/wget.sh")
print()
time.sleep(0.5)
print(f"[green][ AUTO-WGET ]  |  Done, Completed in {elapsed_time} seconds")
print(f"[green][ AUTO-WGET ]  |  Total Size for {episodes} episodes: {gbsize} GB")
file.close()

