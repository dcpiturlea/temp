import os
import shutil
import time


def clear_browser(browser_name):
    """
        Overview: this script delete all time browser history, cache and cookies
        Params:
        browser_name = string. Can be 'chrome' or 'edge'
    """

    browser_name = browser_name.lower()
    if browser_name == 'chrome':
        browser_exe = "chrome.exe"
        browser_company = 'google'
    elif browser_name == 'edge':
        browser_exe = "msedge.exe"
        browser_company = 'microsoft'
    else:
        err = "Please enter only 'chrome' or 'edge' browser names"
        print(err)
        time.sleep(1)
        dictionary_status = {'cache': False, 'cookies': False, 'history': False,
                             'final': False, 'error': err}
        return dictionary_status

    try:
        # kill the browser process
        os.system(f'taskkill  /im {browser_exe} /t /f')
    except Exception as ex:
        print(f"{ex}")
    time.sleep(1)

    directory_browser_settings = os.path.expandvars(
        f'%LOCALAPPDATA%\\{browser_company}\\{browser_name}\\User Data\\Default')
    directory_cache = f'{directory_browser_settings}\\cache'
    directory_cookies = f'{directory_browser_settings}\\network'
    file_history = f'{directory_browser_settings}\\history'

    is_done = False
    removed_cache = False
    removed_cookies = False
    removed_history = False
    timeout = False
    err = ""
    start = time.time()
    while is_done is False:

        # remove cache
        try:
            if not os.path.exists(directory_cache):
                removed_cache = True
            else:
                shutil.rmtree(directory_cache)
                removed_cache = True
        except Exception as ex:
            print(f'{ex}')
            err = f'{err}\n{ex}'

        # remove cookies
        try:
            if not os.path.exists(directory_cookies):
                removed_cookies = True
            else:
                shutil.rmtree(directory_cookies)
                removed_cookies = True
        except Exception as ex:
            print(f'{ex}')
            err = f'{err}\n{ex}'

        # remove history
        try:
            if not os.path.exists(file_history):
                removed_history = True
            else:
                os.remove(file_history)
                removed_history = True
        except Exception as ex:
            print(f'{ex}')
            err = f'{err}\n{ex}'

        if removed_history and removed_cache and removed_cookies:
            is_done = True
            err = ""

        # try for max 3 seconds to delete all cache/cookies/history directory
        stop = time.time()
        if stop - start >= 3:
            print("timeout")
            err = f'{err}\n"timeout'
            break
        time.sleep(0.5)

    print(f'The status is:\n'
          f'remove cache: {removed_cache}\n'
          f'remove cookies: {removed_cookies}\n'
          f'remove history: {removed_history}\n')
    print(f'The final status is {is_done}')

    dictionary_status = {'cache': removed_cache, 'cookies': removed_cookies, 'history': removed_history,
                         'final': is_done, 'error': err}

    return dictionary_status


status = clear_browser('edge')
print(status)
