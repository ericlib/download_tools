from pathlib import Path
import datetime
import time
import requests

def _save_file(content, file_path, mode='w', encoding='utf-8'):

        try:
            if 'b' in mode:
                with open(file_path, mode) as f:
                    f.write(content)
                    print("{}文件保存完成。".format(file_path))  
            else:          
                with open(file_path, mode, encoding=encoding) as f:
                    f.write(content)
                    print("{}文件保存完成。".format(file_path))
            return True
        except Exception as err:
            file_path.unlink()  # 删除文件
            print(err)
            return False


def _selenium_get_file(url, save_dir, sleep_time=0, headless=True):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    import selenium.webdriver.support.expected_conditions as EC

    op = Options()
    op.set_preference("browser.download.dir", save_dir)
    op.set_preference("browser.download.folderList",2)
    op.set_preference("browser.download.manager.showWhenStarting", False)
    op.set_preference("browser.helperApps.neverAsk.saveToDisk", "binary/octet-stream")
    op.set_preference("browser.helperApps.neverAsk.saveToDisk",
                    "text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml")
    op.headless = headless    
    driver = webdriver.Firefox(options=op)
    driver.get(url)
    time.sleep(sleep_time)
    return driver.page_source  


def _selenium_get_source(url, save_dir, sleep_time=0, headless=True):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    import selenium.webdriver.support.expected_conditions as EC
    
    op = Options()
    op.headless = headless  
    driver = webdriver.Firefox(options=op)
    driver.get(url)

    #WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.TAG_NAME,"table"))
    time.sleep(sleep_time)
    content = driver.page_source
    title =  driver.title
    driver.close()
    if '错误' in title:
        return None
    else:
        return content   

def selenium_get(url, save_dir, sleep_time=0, headless=True):
    try:
        url_type = url.rsplit('.',1)[1]
    except:
        url_type = ''
    if url_type=='' or url_type in ['html', 'htm']:
        _selenium_get_source()

def download_str(content, save_dir, name=None, suffix='txt'):
    """
    保存文本到文件，文件名存在时不保存。
    Parameters
    ----------
    content : str
        要保存的文本
    save_dir : str
        保存的文件夹路径
    name : str
        文件名，默认None为当前时间
    suffix : str
        文件后缀，默认'txt'
    Returns
    -------
    None
    Examples
    --------
    >>> download_str('hello',r'F:\test') 
    """

    if name == None:
        time_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        name = time_now

    dir = Path(save_dir)
    file_name = name + '.' + suffix
    file = dir / file_name

    if not file.exists():
        try:
            for encoding in ['utf-8','gbk']:
                result_flag = _save_file(content, file, encoding='utf-8')
                if result_flag: break
        except:
            _save_file(content, file,  mode='w')
    else:
       print("文件已存在。") 

def download_url(url, save_dir, name=None,  suffix=None, 
                headers=None ,  type='get', post_data=None,
                has_selenium='no', selenium_sleep_time=0, headless=True, sleep_time=0):
    """
    通过链接下载文件，文件名存在时不保存。
    Parameters
    ----------
    url : str
        链接
    save_dir : str
        保存的文件夹路径
    name : str
        文件名，默认None为url文件名
    suffix : str
        文件后缀，默认'txt'
    sleep_time : int
        下载一次休眠的秒数，默认0
    has_selenium : str {'both','only','no'}
        'no'不使用selenium, 'both'先requests不行再selenium，'only'只使用selenium
    selenium_sleep_time : int
        使用selenium时，等待页面加载的休眠时间，默认0
    Returns
    -------
    None
    Examples
    --------
    >>> download_url('https://www.baidu.com',r'F:\test') 
    """    

    if name == None:
        time_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        name = url.split('/')[-1].rsplit('.', 1)[0]
        if name == None : name = time_now
    if suffix == None:
        suffix = url.rsplit('.', 1)[-1]
        if suffix == None : suffix = 'txt'
        
    dir = Path(save_dir)
    file_name = name + '.' + suffix
    file = dir / file_name

    if not file.exists():
        if has_selenium != 'only':
            #请求类型
            if (type == 'get') & (post_data==None):
                res = requests.get(url, headers=headers)
            elif type == 'post':
                res = requests.post(url, data=post_data, headers=headers)
            else:
                print('未知类型，请使用get不加post_data 或 post+post_data')
                raise
                
            if res.ok:
                _save_file(res.content, file, mode='wb')
            else:
                print(res)
                if  has_selenium == 'no':
                    print('请求非200')
                    raise
                elif has_selenium == 'both':
                    # 再使用selenium下载
                    _selenium_get_file(url, save_dir, sleep_time=selenium_sleep_time, headless=headless)

                else:
                    raise  
        else:
            # 只使用selenium下载
            content = selenium_get(url, save_dir,sleep_time=selenium_sleep_time,headless=headless)
            if content != None:
                _save_file(content.encode(), file, mode='wb')
        time.sleep(sleep_time)  # 下载一次休眠时间
    else:
       print("文件已存在。")     




if __name__ == "__main__":
    download_str('file',r'test-dir')