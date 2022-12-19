#!/bin/bash
# -*- coding: UTF-8 -*-
target=$1 # 取得 command line 後方的第一個參數
if [ "$target" = "" ]; then
        pytest --alluredir=allure_results # 如果 command line 沒帶參數，則不指定執行目標
else
        echo "target (can be module, class or method): $target"
        pytest -k "$target" --alluredir=allure_results # 如果 command line 帶了參數，則指定該目標執行
fi
test_result=$?                  # 取得測試執行指令的回傳值，用來判斷是否產生報告
is_always_generate_report=false # 是否不論執行成功與否都要產生報告，目前設為 false (有錯誤才產報告)
if [ "$test_result" = "1" ] || [ $is_always_generate_report = true ]; then
        echo "Generate Report Now..."
        allure generate allure_results -o allure_report --clean
        rm -r allure_results

        allure open allure_report
else
        rm -r allure_results
fi
