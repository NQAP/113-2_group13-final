# cafesearch

## 實作方法

### google api key環境檔設置

先在根目錄（113-2_group13-final\cafeproject）中創建.env檔案，內容為：
GOOGLE_MAPS_API_KEY=api_key的值

### mysql安裝及基本設定

1. 下載mysql/mariadb資料庫
2. 使用 `sudo mysql` 或 `mysql -u root -p` 以root權限開啟mysql/mariadb
3. 輸入`CREATE DATABASE cafe_db;` 新增dog_db database
4. 輸入`CREATE USER 'Team13'@'localhost' IDENTIFIED BY 'Team13';` 來創建一個User叫Team13 密碼是 Team13
5. `GRANT ALL PRIVILEGES ON cafe_db * TO 'Team13'@'localhost';` 讓Team13 可以獲得cafe_db的所有權限
6. 輸入 `exit` 離開資料庫，切換到當前資料夾 `cd 113-2_group13-final\cafeproject` 後執行 `python manage.py migrate` 將Table建立好
7. 執行`python import_cafe.py`自動匯入咖啡廳資訊進入mysql
8. 開啟另一個cmd，使用 `mysql -u Team13 -p` 並輸入密碼登入mysql/mariadb
9.  於mariadb中使用`use cafe_db`切換到cafe_db database
10. `select * from cafesearch_cafe`可以看到新增的咖啡廳資訊
11. 確認成功新增後回到原本的cmd按 `CTRL+D`離開shell，執行`python manage.py runserver`後於[http://localhost:8000]可以看到網頁結果