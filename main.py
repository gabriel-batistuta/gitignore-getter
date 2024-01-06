import requests
from bs4 import BeautifulSoup
import os
import platform
import subprocess
from urllib.parse import urljoin

def get_gitignore_files(url_list, folder_path):
    '''
    download the .gitgnore files by urls in a folder_path
    requires a list of url that can get in `list_gitignore_files`
    and a folder path that is where the file has been put
    '''
    for url in url_list:
        print(url)
        file_name = os.path.basename(url)
        url='https://raw.githubusercontent.com/github/gitignore/main/' + file_name
        
        print(file_name)
        print(folder_path)
        print(folder_path[-1])
        if folder_path[-1] == '/' or folder_path[-1] == r'\\':
            subprocess.run(["wget", url, "-O", f'{folder_path}{file_name}'])
        else:
            if platform.system() == 'Windows':
                subprocess.run(["wget", url, "-O", folder_path + r'\\' + file_name])
            else:
                subprocess.run(["wget", url, "-O", f'{folder_path}/{file_name}'])

def filter_list_gitignore(url_list, include=None, exclude=None):
    '''
    requires a list of url that can get in `list_gitignore_files`
    and optional params include or exclude for add or remove .gitignore elements in list
    ex: ['ROS.gitgnore', 'Python.gitignore', ...]
    '''
    if include is not None:
        if type(include) == str:
            url_list = [x for x in url_list if os.path.basename(x[0]) == include]
            return url_list
        elif type(include) == list:
            url_list = [x for x in url_list if os.path.basename(x[0]) in include]
            return url_list
        else:
            raise ValueError("Include must be a string or a list")
        
    elif exclude is not None:
        if type(exclude) == str:
            url_list = [x for x in url_list if os.path.basename(x[0]) != exclude]
            return url_list
        elif type(exclude) == list:
            url_list = [x for x in url_list if os.path.basename(x[0]) not in exclude]
            return url_list
        else:
            raise ValueError("Exclude must be a string or a list")
    else:
        return url_list    

def list_gitignore_files(url):
    '''
    return url of elements .gitignore in root folder 'https://github.com/github/gitignore/'
    '''
    url = "https://github.com/github/gitignore/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    gitignore_files = []

    for link in soup.find_all('a', href=True):
        absolute_url = urljoin(url, link['href'])
        
        if '/blob/main/' in absolute_url and '.gitignore' in absolute_url:
            gitignore_files.append(absolute_url)

    return gitignore_files

if __name__ == "__main__":
    gitignore_files = list_gitignore_files()
    filter_list_gitignore(gitignore_files, include='Python.gitignore')
    get_gitignore_files(gitignore_files, './out')