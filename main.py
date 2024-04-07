import time
import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

filename = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.txt'  # 时间作为文件名
filename = Path('查询结果') / filename
filename.parent.mkdir(parents=True, exist_ok=True)
f = open(filename, 'w', encoding='utf-8')  # 结果文件


def print_and_write(text):
    """输出并写入文件"""
    print(text)
    f.write(text + '\n')


# 读取运动员名单
files = Path('运动员名单').glob('*.txt')
file_name_map = {}
for file in files:
    names = open(file, 'r', encoding='utf-8').read().splitlines()
    file_name_map[file.stem] = names

# Chrome配置
option = webdriver.ChromeOptions()
option.add_experimental_option('useAutomationExtension', False)
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=option)

# 爬取逻辑
n = 0  # 总人数
count = 0  # 等级运动员数量
content = ''
for file, names in file_name_map.items():
    print_and_write(f'【{file}】')

    for user_name in names:
        n += 1
        driver.get(f'https://ydydj.univsport.com/index.php?c=look&a=seach_look&item=36.1&user_name={user_name}')
        # 显式等待5s，查找class为main_lista的元素
        main_lista = WebDriverWait(driver, 5).until(lambda x: x.find_element(By.CLASS_NAME, 'main_lista'))
        elements = main_lista.find_elements(By.XPATH, './*')  # 查找底下的所有元素
        if elements:
            count += 1
            for element in elements:
                # 详细版
                element.click()
                time.sleep(2)
                wza_rigys = driver.find_element(By.CLASS_NAME, 'wza_rigys')
                texts = wza_rigys.text.splitlines()
                data = {x.replace('：', ''): texts[i + 1] for i, x in enumerate(texts) if '：' in x}  # 具体等级信息
                text = ' '.join([data['姓名'], data['等级'], data['比赛名称'], data['比赛成绩'], data['授予时间']])
                print_and_write(text)
        else:
            print_and_write(user_name)
print_and_write(f'参赛{n}人，其中等级运动员{count}人，占比{count / n * 100:.2f}%')
driver.close()
f.close()
print(f'查询完毕，已导出到{filename}')
