# HackBay2024
Our Butter Team Solution for HackBay 2024

**Brainstorming Board**
https://app.mural.co/t/dieunik4932/m/dieunik4932/1706538421664/d532f1d64125567879562df4d05ccc87b928f48c?sender=ud20aecffb10ec34776ab5087

**Figma**
https://www.figma.com/file/LYqvwEqn4322a11Ue4Q4AH/Leitner-Solution-Prototype?type=design&node-id=0%3A1&mode=design&t=IjKQF6cuufLSTlLK-1

**DB Setup**

- sudo apt install mariadb
- sudo apt install libmariadb3 libmariadb-dev
- sudo mysql_secure_installation (answer: "Press Enter", n, n, fore every else answer yes)
- sudo mariadb
- create database hackbay2024;
- create user "hackbay_db_admin"@"localhost" identified by "hack_zu_dem_bay_2024";
- grant all PRIVILEGES on hackbay2024.* to "hackbay_db_admin"@"localhost";
- exit
- mariadb -u hackbay_db_admin -phack_zu_dem_bay_2024
- use hackbay2024;
- CREATE TABLE offer (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  url VARCHAR(255) NOT NULL,
  description TEXT,
  add_date DATE NOT NULL,
  remove_date DATE
  );