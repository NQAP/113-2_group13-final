# 113-2 Web design and application final project

## 網站概述

台北市咖啡廳搜索平台

## 實行方法

1. 下載mysql/mariadb資料庫
2. 使用 `sudo mysql` 或 `mysql -u root -p` 以root權限開啟mysql/mariadb
3. 輸入`CREATE DATABASE cafe_db;` 新增cafe_db database
4. 輸入`CREATE USER 'Team13'@'localhost' IDENTIFIED BY 'Team13';` 來創建一個User叫Team13 密碼是 Team13
5. `GRANT ALL PRIVILEGES ON cafe_db.* TO 'Team13'@'localhost';` 讓Team13 可以獲得cafe_db的所有權限
6. 輸入 `exit` 離開資料庫，切換到當前資料夾 `cd 113-2_group13-final/cafeproject` 後執行 `python manage.py migrate` 將Table建立好
7. 執行`python import_cafe.py` 將資料匯入資料庫 `cafe_db` 中
8. 開啟另一個cmd，使用 `mysql -u Team13 -p` 並輸入密碼登入mysql/mariadb
9. 於mariadb中使用`use cafe_db`切換到cafe_db database
10. `select * from cafesearch_cafe`可以看到新增的cafe
11. 確認成功新增後回到原本的cmd執行`python manage.py runserver`後於[http://localhost:8000]可以看到網頁結果

## 資料夾結構

```
📦113-2_group13-final
 ┣ 📂cafeproject
 ┃ ┣ 📂cafe  //首頁、註冊、登入
 ┃ ┣ 📂cafesearch  //搜尋
 ┃ ┣ 📂cafedetail  //咖啡廳頁面、評論、新增咖啡廳
 ┃ ┣ 📂cafeproject  //settings
 ┃ ┣ 📂media  //新增咖啡廳上傳圖片暫存
 ┃ ┣ 📂static  //靜態檔(image、js、css)
 ┃ ┣ 📂templates  //模板及HTML
 ┃ ┣ 📜import_cafe.py  //新增爬蟲找到的咖啡廳
 ┃ ┣ 📜manage.py  //執行server檔案
 ┃ ┣ 📜.env  //環境檔
 ┃ ┗ 📜min_max_不限時咖啡廳.xlsx //爬蟲的檔案
 ┗ 📜Readme.md
```
