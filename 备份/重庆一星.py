import time,re,os,sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
user = 'zy0108'
pwd = 'zy731027'
start_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
profile = webdriver.FirefoxProfile()
profile.set_preference('permissions.default.stylesheet', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
profile.set_preference('permissions.default.image', 2)
driver = webdriver.Firefox(firefox_profile=profile, firefox_options=fireFoxOptions)
#driver = webdriver.Firefox()
driver.get('http://www.yfcp885.com/login')
wait = WebDriverWait(driver, 10)
def LogIn():
    element_user = wait.until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[2]/ul/li[1]/input'))
    )
    element_user.send_keys(user)
    element_pwd = wait.until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[2]/ul/li[2]/input'))
    )
    element_pwd.send_keys(pwd)
    element_click = wait.until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/ul/li[3]/a[1]'))
    )
    element_click.click()
    fin_driver = wait.until(
        EC.url_to_be('http://www.yfcp885.com/index')
    )
def wait_to_be_num():
    driver.get("http://www.yfcp885.com/trendChart/1000")
    wait.until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="J-chart-content"]/tr[30]/td[5]/span')) #加载第一个
    )
def GetWantBuyNumList():
    wait_to_be_num()
    WinningNum = re.compile('class="lottery-numbers">(.*?)</span>').findall(driver.page_source)
    driver.get("http://www.yfcp885.com/lottery/SSC/1000")
    temp = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    ExistNum = []
    for i in range(18, 30):
        for j in range(0, 9 ,2):
            if WinningNum[i][j] not in ExistNum:
                ExistNum.append(WinningNum[i][j])
    return set(temp).difference(set(ExistNum))
def click(x):
    time.sleep(0.5)
    driver.find_element_by_xpath(x).click()
def Operation(WantBuyNum):
    print("\a")
    print("正在打印" + str(WantBuyNum))
    method = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/ul[1]/li[1]'))
    )
    method.click()
    for i in range(1,6):
        position_xpath = '//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/ul/li/div[' + str(i) + ']/div[1]/a[' + str(int(WantBuyNum) + 1) + ']'
        click(position_xpath)
    click('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/a')
    click('/html/body/div/div[2]/div[2]/div[1]/div[2]/div[3]/p/label[2]')
    click('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div[1]/ul/li[3]')
    time.sleep(1)
    try:
        click('/html/body/div[2]/div[2]/div/div/div[2]/span')
    except: pass
    week_num = wait.until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div[1]/div[1]/div[3]/table[1]/tbody/tr[3]/td/input'))
    )
    week_num.send_keys(Keys.CONTROL + 'a')
    week_num.send_keys('6')
    rate = wait.until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div[1]/div[1]/div[3]/table[2]/tbody/tr[2]/td/input[2]'))
    )
    rate.send_keys(Keys.CONTROL + 'a')
    rate.send_keys('12')
    #times = wait.until(
    #    EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div[1]/div[1]/div[3]/table[1]/tbody/tr[4]/td/input'))
    #)
    #times.send_keys(Keys.CONTROL + 'a')
    #times.send_keys('2')
    click('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div[1]/div[1]/a')
def Buy():
    money_xpath = '//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div[2]/p/em[2]'
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH ,money_xpath))
    )
    money = driver.find_element_by_xpath(money_xpath).text
    if money == '1060.00':
        click('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/a')
        click('/html/body/div[2]/div[2]/div/div/div[2]/span[2]')
        sure_last = wait.until(
            EC.element_to_be_clickable((By.XPATH ,'/html/body/div[2]/div[2]/div/div/div[2]/span'))
        )
        sure_last.click()
        time.sleep(1)
def GetTime():
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH ,'/html/body/div/div[2]/div[1]/div[2]/em'))
    )
    time.sleep(1)
    os.system('cls')
    Time = driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[2]/em').text
    if len(Time) != 8:
        return 'error'
    sys.stdout.write('重庆一星当前时间' + Time + '\n')
    sys.stdout.flush()
    if Time == '00:00:01':
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[2]/span').click()
    return int(Time[-5] + Time[-4]) * 60 + int(Time[-2] + Time[-1])
def waitTime(nowTime ,l ,h = 120):
    while True:
        if nowTime == 'error':
            return 'error'
        elif nowTime > l and nowTime < h:
            return nowTime
        else:
            if nowTime == 120:
                driver.refresh()
            nowTime = GetTime()
def PrintLog(content):
    with open('D:\log\c_one_star' + start_time + '.txt' ,'a') as f:
        f.write(content)
def main():
    LogIn()
    while True:
        try:
            url = 'http://www.yfcp885.com/lottery/SSC/1000'
            driver.get(url)
            nowTime = waitTime(GetTime() ,90)
            if nowTime == 'error':
                continue
            elif nowTime > 90:
                WantBuyNum = GetWantBuyNumList()
                if len(WantBuyNum) == 0:
                    print("暂无符合")
                else:
                    print("剩余数字: ", end='')
                    print(WantBuyNum)
                    for Num in WantBuyNum:
                        Operation(Num)
                        Buy()
            time.sleep(40)
        except Exception as e:
            time.sleep(40)
if __name__ == '__main__':
    main()