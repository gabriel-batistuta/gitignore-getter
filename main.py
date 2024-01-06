import requests
from bs4 import BeautifulSoup
import os
import platform
from urllib.parse import urljoin
import warnings
from urllib.parse import unquote

def _download_file_by_url(url, file_path):
    with open(file_path, 'w') as file:
        response = requests.get(url)
        file.write(response.text)

def get_gitignore_files(url_list, folder_path):
    '''
    download the .gitgnore files by urls in a folder_path
    requires a list of url that can get in `list_gitignore_files`
    and a folder path that is where the file has been put
    '''
    for url in url_list:
        file_name = os.path.basename(url)
        if '%' in file_name:
            file_name = file_name.replace('.gitignore', '')
            file_name = unquote(file_name)
            file_name = file_name + '.gitignore'
        url='https://raw.githubusercontent.com/github/gitignore/main/' + file_name
        
        if folder_path[-1] == '/' or folder_path[-1] == r'\\':
            _download_file_by_url(url, folder_path+file_name)
        else:
            if platform.system() == 'Windows':
                _download_file_by_url(url, folder_path + r'\\' + file_name)
            else:
                _download_file_by_url(url, f'{folder_path}/{file_name}')

def filter_list_gitignore(url_list, include=None, exclude=None):
    '''
    requires a list of url that can get in `list_gitignore_files`
    and optional params include or exclude for add or remove .gitignore elements in list
    ex: ['ROS.gitgnore', 'Python.gitignore', ...]
    '''
    if include is not None:
        if type(include) == str:
            url_list = [x for x in url_list if os.path.basename(x) == include]
            return url_list
        elif type(include) == list:
            url_list = [x for x in url_list if os.path.basename(x) in include]
            return url_list
        else:
            raise ValueError("Include must be a string or a list")
        
    elif exclude is not None:
        if type(exclude) == str:
            url_list = [x for x in url_list if os.path.basename(x) != exclude]
            return url_list
        elif type(exclude) == list:
            url_list = [x for x in url_list if os.path.basename(x) not in exclude]
            return url_list
        else:
            raise ValueError("Exclude must be a string or a list")
    else:
        warnings.warn("Warning: filters were not used as parameters, returning the same list")
        return url_list

def list_gitignore_files():
    '''
    return url of elements .gitignore in root folder 'https://github.com/github/gitignore/'
    '''
    url = "https://github.com/github/gitignore/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    gitignore_files = []

    for link in soup.find_all('a', href=True):
        absolute_url = urljoin(url, link['href'])
        
        if '/blob/main/' in absolute_url and '.gitignore' in absolute_url and os.path.basename(absolute_url) != '.gitignore':
            gitignore_files.append(absolute_url)

    return gitignore_files

if __name__ == "__main__":
    gitignore_files = list_gitignore_files()
    gitignore_files = filter_list_gitignore(gitignore_files, include='Python.gitignore')
    get_gitignore_files(gitignore_files, './out')