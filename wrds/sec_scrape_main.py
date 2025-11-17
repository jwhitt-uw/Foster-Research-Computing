# -*- coding: utf-8 -*-

import wrds
import sec_scrape

#You'll log on to WRDS here
conn = wrds.Connection()
#Put CIKs in the list below
base_path=r'path_to_folder'

#Modify the dates and form as necessary. You can manually add in CIKs or import
#frm another source.
date1 = "01/01/2020"
date2 = "12/31/2023"
form = ["10-K"]
ciks=[]
para = {'form':form, 'cik':ciks, 'date1':date1, 'date2':date2}

#Generate the query to send to WRDS. Include '::text[]' to ensure that the CIKs are 
#passed as strings rather than numbers
q = ("""
    SELECT cik,fdate,form,iname from wrdssec.forms WHERE form = ANY(%(form)s) 
    AND fdate >= %(date1)s
    AND fdate < %(date2)s
    AND cik=ANY(%(cik)s::text[])
    """)

#Send the query, return a pandas data frame
df = conn.raw_sql(q, params=para)

#This is the main part of the script- loop through the dataframe, running the
#above functions on each row
if __name__ == '__main__':
    for i,r in df.iterrows():
        print(r['iname'])
        try:
            sec_scrape.download(r)
        except:
            continue