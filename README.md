# download_tools
download_tools 下载工具库，也包括爬虫的一些工具。

## 安装
### Required
```
pip install requests selenium
```

### 安装 download_tools
```
pip install download_tools
```

## 使用
### 下载文件
下载文件时，会先检查存储目录是否有同名文件，有就不下载。

####  download_url()

默认只使用requests获取，也可以selenium，需要浏览器firefox和Firefox驱动。
```
import download_tools as dt

dt.download_url('https://www.baidu.com', r'F:\test') 

# 修改名称和增加后缀
dt.download_url('https://www.baidu.com', save_dir=r'F:\test', name='baidu',suffix='html') 
```

```
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

```


####  download_str()
适用于已经获取到源代码，直接保存。当name参数为空时，使用当前日期时间做文件名。

```
import download_tools as dt

page_souce = '<p>测试</p>' dt.download_str(page_souce, r'F:\test', name='测试', suffix='html')
dt.download_str(page_souce, save_dir=r'F:\test')
```


### headers
生成headers
```
import download_tools as dt

# 随机生成header
dt.Headers().get()
# 随机生成windows平台chrome浏览器headers
dt.Headers(os='win', browser="chrome", headers=True).get()

for i in range(10):
    print(dt.Headers().get())
```
dtools.fake_headers fork from https://pypi.org/project/fake-headers/          
修改：generate()函数名修改为get()

