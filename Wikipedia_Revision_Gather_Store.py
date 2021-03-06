import urllib.request
import wikipedia
import re
import json
from bs4 import BeautifulSoup

def load_https(filename):
    """
    (String) --> String[]
    
    Returns a list of string urls to be analysed for revisions from a .txt or .csv file binded to the filename string.
    
    
    >>>urls = load_https("list_of_https.txt")
    >>>urls
    >>>["https://en.wikipedia.org/wiki/Husky_Energy",https://en.wikipedia.org/wiki/Tesla,_Inc.]
    """
    file =  open(filename, "r")
    
    for line in file:
        line_ =  line.strip("\n")
        line__ = line_.split(",")
        urls = []
        for url in line__:
            urls.append(url)
            
    file.close()
    
    return urls


def get_revision_id(urls,revisionlimit):
    """
    (String[]) --> List[String[]]
    
    Returns the revision ids and when the edits were made in xml format excluding edits made by anonymous users of the url list of url strings. The revisions returned is limited by the revisionlimit integer which must be greater than or equal to zero
    
    >>> urls = load_https("list_of_https.txt")
    >>> revisions = get_revision_id(urls)
    """
    revisions = []
    
    for link in urls:
        link_revision_info = []
        url = "https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvlimit="+str(int(revisionlimit)+1)+"&titles="+ (link.split("/"))[-1] +"&rvprop=ids|timestamp&rvexcludeuser=127.0.0.1"
        next = ''
        while True:
            response = urllib.request.urlopen(url + next).read()     
            link_revision_info += re.findall('<rev [^>]*>', response.decode('utf-8'))  
            if len(link_revision_info) == (int(revisionlimit) + 1):
                break
            cont = re.search('<continue rvcontinue="([^"]+)"', response.decode('utf-8'))
            if not cont:                                      
                break
            next = "&rvcontinue=" + cont.group(1)             
        revisions.append(link_revision_info)
            
    return revisions

def get_difference_between_revisions(revision_one,timestamp_one,revision_two,timestamp_two):
    """
    (str,str,str,str) --> List[String[]]
    
    Returns a list of added and removed text between revision_one and revision_two ids
    
    >>>diff = get_difference_between_revisions(431413431,2321354)
    >>>diff
    """
    difference_holder = []
    
    added_text_holder = []
    
    removed_text_holder = []
    
    url = "https://en.wikipedia.org/w/api.php?action=compare&format=json&fromrev=" + revision_one +"&torev=" + revision_two
    
    response = urllib.request.urlopen(url).read() 
    
    link_info = (response.decode('utf-8'))
    
    j = json.loads(link_info)
    
    com = j["compare"]['*']
    
    soup = BeautifulSoup(com,'lxml')
    
    
    lister = soup.find_all('td')
    
    lsz_added = map(str,lister)
    
    lsz_removed = map(str,lister)
    
    indices_two = [i for i, text in enumerate(lsz_removed) if 'deletedline' in text]
    
    indices = [i for i, text in enumerate(lsz_added) if 'addedline' in text]
    
    for added_text in indices:
        if lister[added_text].get_text() in added_text_holder:
            break
        else:
            if lister[added_text].get_text() != "":
                edited_text = lister[added_text].get_text().split(",")
                fixed_added_text = " ".join(edited_text)
                added_text_holder.append(revision_one + "sez" + timestamp_one + "sez" + revision_two + "sez" + timestamp_two + "sez"  +"added text: " +fixed_added_text)
       
    
    for deleted_text in indices_two:
        if lister[deleted_text].get_text() in removed_text_holder:
            break
        else:
            if lister[deleted_text].get_text() != "":
                edited_text = lister[deleted_text].get_text().split(",")
                fixed_deleted_text = " ".join(edited_text)                
                removed_text_holder.append(revision_one + "sez" + timestamp_one + "sez" + revision_two + "sez" + timestamp_two + "sez" +"removed text: " + fixed_deleted_text)    
    
    difference_holder.append(added_text_holder)
    difference_holder.append(removed_text_holder)
    
    return difference_holder


def get_sequential_set_of_revisions_difference(revisions):
    """
    () --> List[List[List[Dictionary[]]]]
    
    returns a nested list of differences between sequential revisions of each url listed in txt file
    
    """
    set_of_urls_info = extract_parent_ids(revisions)
    dataset_for_url_info = []
    pos = 0
    for url in set_of_urls_info:
        for dictionary in url:
            key = []
            timestamp = []
            amount_of_compares = 0
            url_comparison_set = []
            pos = -1
            for keys in dictionary:
                pos+=1
                key.append(keys)
                timestamp.append(dictionary[keys])
            while pos >= 1 and amount_of_compares <= (len(key) - 1):
                url_comparison_set.append(get_difference_between_revisions(key[pos],timestamp[pos],key[pos - 1],timestamp[pos-1]))
                pos-=1
                amount_of_compares+=1
            
            dataset_for_url_info.append(url_comparison_set)
    
    return dataset_for_url_info

def write_revisions_to_file(urls,revisions):
    x = get_sequential_set_of_revisions_difference(revisions)
    filename = " set_of_information.csv"
    file = open(filename, 'w')
    for index in range(len(urls)): 
        file = open(filename, 'a')
        file.write((urls[index].split("/"))[-1] + " information,\n")
        file.write("Revision id 1,timestamp 1,Revision id 2,timestamp 2,\n")
        for index_two in range(len(x[index])):
            for index_three in range(len(x[index][index_two])):
                for revison in x[index][index_two][index_three]:
                    information = revison.split("sez")
                    file.write(information[0])
                    for i in range(1,len(information)):
                        file.write("," + information[i])
                    file.write(",\n")

    file.close()


  
def extract_parent_ids(revisions):
    urls = load_https('List_of_https.txt') 
    
    urls_information_ids_timestamp = []
 
    
    revision_info = get_revision_id(urls,revisions)
    
    for element in revision_info:
        information_ids_timestamp = []  
        parent_info_id = []
        timestamp_info = []
        info_dict = {}
        for index in range(len(element)):           
            parent_info_id.append(re.findall(r"[\w']+",element[index]))
            timestamp_info.append((element[index].split())[3])
            info_dict [parent_info_id[index][2]] = timestamp_info[index]
        
        information_ids_timestamp.append(info_dict)

            
        urls_information_ids_timestamp.append(information_ids_timestamp)
        
            
    return urls_information_ids_timestamp



def main():
    #revisions = input("How many revisions for the url(s)? ")
    urls = load_https('List_of_https.txt')
    write_revisions_to_file(urls,"5")
                            
if __name__ == "__main__":
    main()
