import csv
import json
from time import sleep

from dateutil import parser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


TBL_XPATH = "//table[@id='GridView1']//tr"
BTN_XPATH = "//input[@id='btnSearch']"

URL = 'http://www.pcso.gov.ph/lotto-search/lotto-search.aspx'


class LottoResultsDownloader(object):

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.params = {}
    
    def run(self):
        try:
            self._prompt_user()
            print '\nAccessing page.'
            self.driver.get(URL)
            sleep(5)
            self._set_date_range()
            sleep(3)
            
            print 'Locating main table'
            self.rows = self.driver.find_elements_by_xpath(TBL_XPATH)
            
            if not self.rows:
                raise ValueError('No data found.')
            else:
                print 'Found %d rows.' % (len(self.rows) - 1)
                print 'Parsing main table.'
                self._parse_table()
        
        except Exception as e:
            print e
        else:
            self._save_data()
            print 'Closed.'
    
    
    def _prompt_user(self):
        """Asks user to specify certain parameters"""
        print 'Please enter the ff. Just leave blank to accept default.\n'
        self._handle_param(param='start',
                           msg='Starting date (Ex. Feb 1, 2016): ')
        self._handle_param(param='end',
                           msg='Ending date (Ex. Aug 1, 2016): ')
        self._handle_param(
            param='fname',
            msg='Output filename (do not include file ext.): '
        )
        self._handle_param(param='ftype',
                           msg='Output file type (json/csv): ')
    
    
    def _handle_param(self, param, msg):
        """Handles user inputs"""
        while True:
            try:
                if param in ['start', 'end']:
                    datestr = raw_input(msg)
                    self.params[param] = self._date_from_str(
                        date_entry=param,
                        date_str=datestr
                    )
                
                if param == 'fname':
                    fname = raw_input(msg)
                    if not fname:
                        fname = 'lotto_results'
                    
                    self.params[param] = str(fname)
                    
                if param == 'ftype':
                    ftype = raw_input((msg))
                    if not ftype:
                        ftype = 'json'
                    elif ftype.lower() not in ['json', 'csv']:
                        ftype = 'json'
                    
                    self.params[param] = ftype.lower()
            except Exception as e:
                print e
            else:
                break
    
    
    def _date_from_str(self, date_entry, date_str):
        """Converts user-specified date into correct format"""
        if not date_str:
            return None
        
        dt_obj = parser.parse(date_str)
        date_entry = date_entry.capitalize()
        
        dt_dict = {}
        dt_dict['ddl%sMonth' % date_entry] = dt_obj.strftime('%B')
        dt_dict['ddl%sYear' % date_entry] = str(dt_obj.year)
    
        # This is a particularly annoying thing on the PCSO page:
        day_key = "ddl%sDate" if date_entry == "Start" else "ddl%sDay"
        dt_dict[day_key % date_entry] = str(dt_obj.day)
        
        return dt_dict
    
    
    def _set_date_range(self):
        """Sets start and end date on the drop down boxes"""
        cond1 = self.params['start'] is not None
        cond2 = self.params['end'] is not None
    
        if cond1 or cond2:
            self._select_from_menu(self.params['start'])
            self._select_from_menu(self.params['end'])
            search_btn = self.driver.find_element_by_xpath(BTN_XPATH)
            
            if search_btn:
                search_btn.click()
    
    
    def _select_from_menu(self, date_dict):
        """Does the actual finding and selecting from dropdown box"""
        if date_dict is not None:
            for k, v in date_dict.iteritems():
                path = "//select[@id='%s']/option[@value='%s']" % (k, v)
                item = self.driver.find_element_by_xpath(path)
                
                if item:
                    item.click()
    
    
    def _parse_table(self):
        """Scrapes the table where data is displayed"""
        self.cols = []
        self.data = []
        
        for i, row in enumerate(self.rows):
            cols = row.find_elements_by_xpath('./*')
            item = {}
            
            for k, col in enumerate(cols):
                if i == 0:
                    self.cols.append(col.text)
                else:
                    item[self.cols[k]] = col.text
            
            if item:
                self.data.append(item)
    
    
    def _save_data(self):
        """Writes scraped data to file"""
        try:
            fpath = '.'.join([self.params['fname'], self.params['ftype']])
            with open(fpath, 'wb') as f:
                
                if self.params['ftype'] == 'json':
                    json.dump(self.data, f, indent=1)
                elif self.params['ftype'] == 'csv':
                    writer = csv.DictWriter(f, fieldnames=self.cols)
                    writer.writeheader()
                    
                    for row in self.data:
                        writer.writerow(row)
        
        except Exception as e:
            print e 
        else:
            print 'Finished saving data to file.'
    
    
    def __del__(self):
        if self.driver:
            self.driver.quit()
        

if __name__ == '__main__':
    d = LottoResultsDownloader()
    d.run()
