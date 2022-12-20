# Stylish-Automation-Test

## README 目錄
  - [專案說明](#專案說明)
  - [品牌官網與 API 文件](#品牌官網與-api-文件)
  - [開發相關應用資訊](#開發相關應用資訊)
  - [開發前準備](#開發前準備)
  - [.env 變數設定](#env-變數設定)
  - [專案結構樹](#專案結構樹)
  - [License](#license)

## 專案說明
  Stylish 是一個模擬服飾品牌，本專案針對該品牌的官網前後台基本操作行為 (UI) 及所使用的 API ，撰寫程式碼進行自動化測試。

## 品牌官網與 API 文件
  - [Stylish](http://54.201.140.239/)
  - [Swagger](https://app.swaggerhub.com/apis-docs/YINGNTY/Stylish/1.0.0)

## 開發相關應用資訊
  #### Programming Language
  - Python
  - Shell Script
  #### Framework
  - Pytest
  - Selenium
  #### Report Suite
  - Allure
  #### Database
  - MySQL

## 開發前準備
  1. 安裝 Python 環境 (建議 3.8 以上版本)
  2. 安裝所需套件： `pip install -r requirement.txt`
  3. 設定環境變數 .env ，詳細參考 [這裡](#env-變數設定)
  4. 執行本機測試檔確認程式可正常運行：
      - Windows (Git bash): `bash exec_test.sh test_api_user.py`
      - MacOS / Linux: `sh exec_test.sh test_api_user.py`

## .env 變數設定
  可參考 [.env.example](https://github.com/Allen5256/Stylish-Automation-Test/blob/master/.env.example) 檔案
  ```
  # 品牌官網首頁網址，型別為字串。
  export DOMIN = 'http://xxxxxx'
  
  # 資料庫連線設定，型別為 JSON 字串
  export DB_SETTING = '{"host": "", "port": int, "user": "", "password": "", "db": "", "charset": ""}'
  
  # 使用者登入資訊，型別為 JSON 字串，並行測試 (Parallel Test) 需因應 worker 數量增減帳號數量
  export LOGIN_INFO_0 = '{"email": "", "password": ""}'
  export LOGIN_INFO_1 = '{"email": "", "password": ""}'
  export LOGIN_INFO_2 = '{"email": "", "password": ""}'
  ```

## 專案結構樹
    ├── Stylish-Automation-Test
        │ 
        ├── api_objects  // 存放可建立 API 物件的 Python Class
            ├── __init__.py
            ├── api_utils.py  // API 共用父類別，存放 API session 常用行為及各 API 共用 Methods
            ├── group_A
                ├── A-1_api.py
                └── A-2_api.py
            └── group_B
                └── B-1_api.py
                └── B-2_api.py
        ├── page_objects  // 存放可建立 Page 物件的 Python Class
            ├── __init__.py
            ├── action_utils.py  // Page 共用父類別，存放 webdriver 常用行為及各頁面共用 Methods
            ├── common_page.py  // 前台各頁面可共用的動作 (e.g., 進入購物車)
            ├── XXX_page.py
            └── YYY_page.py
        ├── database_utils  // 存放針對資料庫進行操作的物件
            ├── __init__.py
            └── sql_object.py
        ├── test_data  // 存放測試資料檔案及資料處理相關的程式碼
            ├── __init__.py
            ├── environment_variables.py  // 讀取 .env 中的環境變數並可供其他檔案取用
            ├── get_data_from_excel.py  // Excel 資料處理的 Methods
            └── Stylish-Test Case.xlsx  // 主要測試資料的 Excel 檔
        ├── tests_web  // 各頁面 UI 的測試主程式
            ├── conftest.py
            ├── test_web_XXX.py
            └── test_web_YYY.py
        ├── tests_api  // 各 API 的測試主程式
            ├── conftest.py
            ├── test_api_A.py
            └── test_api_B.py
        ├── .env.example  // 環境變數範例檔
        ├── exec_test.sh  // 在本機執行的執行檔
        ├── pytest.ini  // Pytest 執行預設參數
        └── requirements.txt  // 專案開發所需套件
        
## License
[MIT](https://github.com/Allen5256/Stylish-Automation-Test/blob/master/license)
