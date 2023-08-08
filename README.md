# Assignment 4: Web scraping
This directory contains code for some webscraping tools associated with assinment 4.

I was able to run all tests for the code (found in the tests folder) from both my windows machine and an ifi linux machine without any modification. I did however add one test in test_time_planner.py (79-94).

## Requirements
The following python packages are needed in order to run the codes:

- bs4 BeautifulSoup (4.11.1)
- requests (2.28.1)
- pandas (1.5.1)
- Tabulate (0.9.0)
- requests-cache (0.9.6)
- matplotlib (3.5.3)
- pytest (7.1.2)

The versions I have used for the implementation are stated above beside each package.


You can install these packages by running the commands
```
pip install beautifulsoup4 
```
```
pip install requests 
```
```
pip install pandas
```
```
pip install tabulate
```
```
pip install requests-cache
```
``` 
pip install matplotlib
```
```
pip install pytest
```

## Usage

You can find the codes for web-scraping in the files requesting_urls.py, filter_urls.py, collect_dates.py, time_planner.py and fetch_player_statistics.py.

**requesting_urls.py** contains the code for sending an HTTP-request to a website, allowing us to get the HTML source code for this website. To use this function simply specify a url and it will return the HTML script.

**filter_urls.py** contains three functions, one for finding links, one for finding wikipedia articles and one for finding images all throughout specified HTML code (in strings). E.g. combine these functions with the get_html from requesting_urls.py for easy usage.

**collect_dates.py** contains code for identifying dates through a given text, doing so using regular expressions, (no parsing). The code will recogize dates on the following forms:

- DMY: 13 October 2020
- MDY: October 13, 2020
- YMD: 2020 October 13
- ISO: 2020-10-13

Abbreviations of the month consisting of 3 letters will also get matched. To use this code, enter desired string as argument to the function find_dates and run.

**time_planner.py** parses a table from an html text and extracts wanted columns of said table, and displays the new table with the wanted columns as markdown. This function takes a sports events page of wikipedia. Running this file will display the table as result from the url:
```
url="https://en.wikipedia.org/wiki/2020–21_FIS_Alpine_Ski_World_Cup",
"https://en.wikipedia.org/wiki/2021–22_FIS_Alpine_Ski_World_Cup",
"https://en.wikipedia.org/wiki/2022–23_FIS_Alpine_Ski_World_Cup"

```

**fetch_player_statistics.py** finds the 3 players with the highest PPG (points per game) of each team given wikipedia's playoffs site. To use this give function find_best_players a url. The NBA_player_statistics folder contains the plots as result of running 
```
find_best_players('https://en.wikipedia.org/wiki/2022_NBA_playoffs')
```

## Running the tests
You can find all test files in the tests directory. To run all tests, type following command
```
pytest -vv tests
```

Commands for running each test is stated below for each task of the assignment.

Task 1:
```
pytest tests/test_requesting_urls.py
```

Task 2 & 3:
```
pytest tests/test_filter_urls.py
```

Task 4:
```
pytest tests/test_collect_dates.py
```

Task 5 & 6 & 7:
```
pytest tests/test_time_planner.py
```

Task 8 & 9 & 10:
```
pytest tests/test_fetch_player_statistics.py
```
