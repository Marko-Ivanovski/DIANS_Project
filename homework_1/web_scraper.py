import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import psycopg2
import time
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()

def parse_number(value):
    value = value.replace(".", "")
    value = value.replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return 0.0

# Filter 1: Retrieve Firms
def retrieve_issuers(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    dropdown = soup.find("select", {"id": "Code"})

    issuers = []
    for option in dropdown.find_all("option"):
        code = option.text.strip()
        if re.match("^[A-Za-z]+$", code):  # Only alphabetical characters
            issuers.append(code)

    return issuers

# Filter 2: Check Last Date
def get_last_recorded_date(issuer_code, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Date) FROM Shares WHERE Firm_ID = %s", (issuer_code,))
    last_date = cursor.fetchone()[0]

    if last_date is None:
        last_date = datetime.now() - timedelta(days=365 * 10)
    elif isinstance(last_date, datetime):
        last_date = last_date.date()  # Convert datetime to date

    return last_date

# Filter 3: Fill in missing data
def fetch_data_by_date_range(issuer_code, start_date, conn):
    driver.get("https://www.mse.mk/mk/stats/symbolhistory/REPL")

    try:
        select_element = driver.find_element(By.ID, "Code")
        select_element.send_keys(issuer_code)
    except Exception as e:
        print(f"Error selecting issuer code {issuer_code}: {e}")
        return

    end_date = (datetime.now() - timedelta(days=1)).date()
    current_date = start_date.date() if isinstance(start_date, datetime) else start_date

    empty_data_attempts = 0

    while current_date < end_date:
        next_year_date = current_date + timedelta(days=365)
        if next_year_date > end_date:
            next_year_date = end_date

        try:
            from_date_input = driver.find_element(By.ID, "FromDate")
            to_date_input = driver.find_element(By.ID, "ToDate")
            from_date_input.clear()
            from_date_input.send_keys(current_date.strftime("%d.%m.%Y"))
            to_date_input.clear()
            to_date_input.send_keys(next_year_date.strftime("%d.%m.%Y"))
        except Exception as e:
            print(f"Error setting date range {current_date} to {next_year_date} for {issuer_code}: {e}")
            return

        try:
            show_button = driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary-sm[type='submit']")
            show_button.click()
        except Exception as e:
            print(f"Error clicking show button for {issuer_code}: {e}")
            return

        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.CSS_SELECTOR, "#resultsTable") or
                          d.find_element(By.CLASS_NAME, "col-md-12")
            )
        except Exception as e:
            print(f"Timeout or no elements found after waiting for data for {issuer_code}: {e}")
            return

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        no_data_div = soup.find("div", class_="col-md-12", string="Нема податоци")
        if no_data_div:
            print(f"No data found for date range {current_date} to {next_year_date}")
            empty_data_attempts += 1
            if empty_data_attempts > 2:  # Stop after 3 consecutive empty attempts
                print(f"No more data found for issuer {issuer_code}. Moving to the next issuer.")
                break
            current_date = next_year_date
            continue

        table = soup.find("table", {"id": "resultsTable"})
        if not table:
            empty_data_attempts += 1
            print(f"No data table found for date range {current_date} to {next_year_date}")
            if empty_data_attempts > 5:
                print(f"No more data found for issuer {issuer_code}. Moving to the next issuer.")
                break
            current_date = next_year_date
            continue

        empty_data_attempts = 0

        data_to_insert = []
        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")

            if len(cells) < 8:
                print("Skipping incomplete row:", row)
                continue

            date_str = cells[0].text.strip()

            try:
                date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()

                price_last = parse_number(cells[1].text.strip()) if cells[1].text.strip() != '' else 0.0
                max_price = parse_number(cells[2].text.strip()) if cells[2].text.strip() != '' else 0.0
                min_price = parse_number(cells[3].text.strip()) if cells[3].text.strip() != '' else 0.0
                avg_price = parse_number(cells[4].text.strip()) if cells[4].text.strip() != '' else 0.0
                percent_change = parse_number(cells[5].text.strip()) if cells[5].text.strip() != '' else 0.0
                quantity_shares = int(cells[6].text.replace(".", "")) if cells[6].text.strip() != '' else 0
                total_profit = parse_number(cells[7].text.strip()) if cells[7].text.strip() != '' else 0.0

                data = {
                    "Date": date_obj,
                    "Price_of_Last_Transaction": price_last,
                    "Max_Price": max_price,
                    "Min_Price": min_price,
                    "Average_Price": avg_price,
                    "Percent_Changed": percent_change,
                    "Quantity_of_Shares": quantity_shares,
                    "Total_Profit": total_profit
                }
                data_to_insert.append(data)

            except (ValueError, IndexError) as e:
                print(f"Error parsing row data for date {date_str} in range {current_date} to {next_year_date}: {e}")
                continue

        if data_to_insert:
            insert_data_into_db(data_to_insert, issuer_code, conn)

        current_date = next_year_date


def insert_data_into_db(data, issuer_code, conn):
    cursor = conn.cursor()

    cursor.execute("SELECT Firm_ID FROM Firms WHERE Firm_ID = %s", (issuer_code,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO Firms (Firm_ID) VALUES (%s) ON CONFLICT DO NOTHING", (issuer_code,))
        print(f"Inserted new firm: {issuer_code}")

    for entry in data:
        cursor.execute("""
            INSERT INTO Shares (
                Firm_ID, Date, Price_of_Last_Transaction, Max_Price, Min_Price, 
                Average_Price, Percent_Changed, Quantity_of_Shares, Total_Profit
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            issuer_code, entry["Date"], entry["Price_of_Last_Transaction"],
            entry["Max_Price"], entry["Min_Price"], entry["Average_Price"],
            entry["Percent_Changed"], entry["Quantity_of_Shares"], entry["Total_Profit"]
        ))
    conn.commit()

def main():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="#Jak.Password(1)",
            host="localhost",
            port="1234"
        )
    except psycopg2.OperationalError as e:
        print("Error connecting to the database:", e)
        return

    start_time = time.time()

    issuers = retrieve_issuers("https://www.mse.mk/mk/stats/symbolhistory/REPL")
    for issuer_code in issuers:
        last_date = get_last_recorded_date(issuer_code, conn)
        fetch_data_by_date_range(issuer_code, last_date, conn)


    elapsed_time = time.time() - start_time
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60

    print(f"Total time to fill the database: {int(minutes)} minutes {int(seconds)} seconds") # 33 minutes 9.00 seconds

    conn.close()
    driver.quit()

if __name__ == "__main__":
    main()