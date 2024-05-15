import logging
from datetime import datetime

import mariadb
import sys

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MariaDBPipeline:
    conn: mariadb.Connection
    hackbay_db: mariadb.Cursor

    def open_spider(self, spider):
        try:
            self.conn = mariadb.connect(
                user="hackbay_db_admin",
                password="hack_zu_dem_bay_2024",
                host="localhost",
                port=3306,
                database="hackbay2024"

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self.hackbay_db = self.conn.cursor()

    def close_spider(self, spider):
        # called when the spider is closed
        self.hackbay_db.close()
        self.conn.close()

    def process_item(self, item, spider):
        name = item["name"]
        url = item["url"]
        country = item["country"]
        description = item["description"]
        # SQL-Abfrage mit Parametern

        self.hackbay_db.execute("""
            SELECT * FROM offer
            WHERE name = ? AND url = ? AND description = ? AND country = ?
        """, (name, url, description, country))

        result = self.hackbay_db.fetchone()

        # check if the offer is already present

        if result:
            logging.info("Offer already in DB")
        if not result:
            # add the offer
            self.hackbay_db.execute("""
                INSERT INTO offer (name, url, description, country, add_date)
                VALUES (?, ?, ?, ?, NOW())
            """, (name, url, description, country))
            self.conn.commit()
            logging.info("Offer added")
