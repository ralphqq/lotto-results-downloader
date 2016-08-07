## lotto-results-downloader
This script uses Selenium and PhantomJS to scrape PCSO Lotto Draw results from the [PCSO's official website](http://www.pcso.gov.ph/index.php/games/search-lotto-results/). This script can be useful if you're trying to download lotto results spanning a considerable length of time (months or years worth of draws). I don't know why the official PCSO results page doesn't include a 'download' feature. Anyway, I hope this helps.

## Requirements
This scraper runs on Python 2.7 with the following:

1. selenium (`pip install selenium`)
2. PhantomJS ([click here to download](http://phantomjs.org/download.html))
3. dateutil (`pip install python-dateutil`)

## Running the Script
Assuming that you've already created a new virtual environment and installed the above dependencies, just cd to this project's root project directory and run:

```
$ python downloader.py
```

Then, specify the items being asked in the prompt. Make sure that the dates you enter follow some conventional date formats (e.g., '2016-07-23', 'July 23, 2016', 'Jul 26, 2016', '2016-7-23', etc.).

Also, when entering a filename for the output file, please do not include the extension, and please type either 'json' or 'csv' when prompted for the output file type.

You may also simply hit return for each item to accept the defaults.

## Output
The output will either be a JSON or CSV file (depending on your choice) containing the draw results of all PCSO Lotto Games included in the dates you've specified. The output file is saved in the project's root directory.

## Contributing
Please let me know your comments or suggestions for this project.