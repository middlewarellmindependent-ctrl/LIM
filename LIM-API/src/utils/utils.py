def clean_string(string : str) -> str:
    return string.replace('\n', '').replace('=', '').replace(',', '').replace('.', '') 

def split_string(string : str) -> str:
    return string.replace('\n', ' ').replace('=', ' ').replace(',', ' ').replace('.', ' ').replace('!', ' ') 

