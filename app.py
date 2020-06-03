from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import save_csv


# 都道府県ID
pref = [f"pref{v:02}" for v in range(1, 48)]

# townDivからリストにする正規表現コンパイル
# <a class="preflink" id="town01101" href="#" title="中央区">中央区(415)</a>
pattern = r'<a class="preflink" id="(.*?)".*?>(.*?)\((\d*?)\)</a>'
town_a_com = re.compile(pattern)

# 起点ページ
url = ""


driver = webdriver.Chrome()

for pref_id in pref:
    driver.get(url)

    # ID指定したページ上の要素が読み込まれるまで待機（15秒でタイムアウト判定）
    WebDriverWait(driver, 15) \
        .until(EC.presence_of_element_located((By.ID, pref_id)))

    # 都道府県クリック
    driver.find_element_by_id(pref_id).click()

    # townDiv
    WebDriverWait(driver, 15) \
        .until(EC.presence_of_element_located((By.ID, "townDiv")))

    # ソースを取得
    townDiv = driver.page_source

    # リストにする
    town_lst = town_a_com.findall(townDiv)

    # リストの3番めの要素が0以外のリストを再作成
    town_lst2 = [v for v in town_lst if v[2] != "0"]

    # リストをループ
    for town in town_lst2:
        driver.get(url)

        # ID指定したページ上の要素が読み込まれるまで待機（15秒でタイムアウト判定）
        WebDriverWait(driver, 15) \
            .until(EC.presence_of_element_located((By.ID, pref_id)))

        # 都道府県クリック
        driver.find_element_by_id(pref_id).click()

        # ID指定したページ上の要素が読み込まれるまで待機（15秒でタイムアウト判定）
        WebDriverWait(driver, 15) \
            .until(EC.presence_of_element_located((By.ID, town[0])))

        driver.find_element_by_id(town[0]).click()

        # ページ上のすべての要素が読み込まれるまで待機（15秒でタイムアウト判定）
        WebDriverWait(driver, 15) \
            .until(EC.presence_of_all_elements_located)

        # 連続アクセス防止
        time.sleep(2)

        # ソースコードからCSV作成
        save_csv.save_csv(driver.page_source)


driver.close()
driver.quit()

print("終了")
