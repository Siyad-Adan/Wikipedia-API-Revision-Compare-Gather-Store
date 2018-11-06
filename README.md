# Wikipedia-API-Revision-Compare-Gather-Store
Script to gather 25 revisions of  a list of wikipedia page urls (or just one) entered into List_of_https.txt file (csv format) and compare each revision sequentially. Information is saved seperately into a txt file for each respective url

Ensure you have wikipedia api downloaded --> documentation: https://wikipedia-api.readthedocs.io/en/latest/
Ensure you have Beautiful Soup downloaded --> documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

STEPS on how to use
1. Enter http urls of wikipedia page you'd like to gather information for into List_of_https.txt file following csv convention
    ex: https://en.wikipedia.org/wiki/Husky_Energy,https://en.wikipedia.org/wiki/Tesla,https://en.wikipedia.org/wiki/Suncor_Energy
2. Execute  Wikipedia_Revision_Gather_Store.py file
3. txt files of revision differences for each url input saved in same directory of List_of_https.txt and Wikipedia_Revision_Gather_Store.py directory
