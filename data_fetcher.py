from datetime import date, datetime, timedelta
from sqlite3 import Date
import requests
import os
from dateutil.relativedelta import relativedelta
import pandas as pd
from bs4 import BeautifulSoup


def get_dates(last_date: datetime):
    def get_date_range(year_range: int):
        nonlocal last_date
        first_date = last_date - relativedelta(years=1)
        DATE_FORMAT = "%d-%b-%Y"
        years = []

        for _ in range(year_range):
            last_formatted_date = last_date.strftime(DATE_FORMAT)
            first_formatted_date = first_date.strftime(DATE_FORMAT)

            years.append(
                {"first_date": first_formatted_date, "last_date": last_formatted_date}
            )
            last_date = last_date - relativedelta(years=1)
            first_date = first_date - relativedelta(years=1)

        return years

    return get_date_range


def get_agmarknet_data_and_save_csv(
    commodity,
    state,
    district,
    market,
    date_from,
    date_to,
    trend,
    commodity_head,
    state_head,
    save_dir="responses",
):
    """
    Fetches data from Agmarknet, parses it, and saves the response to a CSV file.

    Parameters:
        commodity (str): Commodity code.
        state (str): State code.
        district (str): District code.
        market (str): Market code.
        date_from (str): Start date in 'DD-MMM-YYYY' format.
        date_to (str): End date in 'DD-MMM-YYYY' format.
        trend (str): Trend parameter.
        commodity_head (str): Commodity name.
        state_head (str): State name.
        save_dir (str): Directory to save the response files.

    Returns:
        str: Path to the saved file or an error message.
    """

    # Base URL
    url = "https://agmarknet.gov.in/SearchCmmMkt.aspx"

    # Query parameters
    params = {
        "Tx_Commodity": commodity,
        "Tx_State": state,
        "Tx_District": district,
        "Tx_Market": market,
        "DateFrom": date_from,
        "DateTo": date_to,
        "Tx_Trend": trend,
        "Tx_CommodityHead": commodity_head,
        "Tx_StateHead": state_head,
    }

    try:
        # Making the GET request
        print(params)
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")
            # print(response.content)

            # Find the table
            table = soup.find("table", {"id": "cphBody_GridPriceData"})

            if table is None or table.find_all("tr") is None:
                print("data not found")
                return
            # Extract headers
            headers = []
            for th in table.find_all("th"):
                headers.append(th.text.strip())

            if table and table.find_all("tr"):
                # Extract rows
                rows = []
                for tr in table.find_all("tr")[1:]:  # Skip the header row
                    cells = tr.find_all("td")
                    row = [cell.text.strip() for cell in cells]
                    print(row, "ROW")
                    if len(row) > 1:
                        rows.append(row)
                    else:
                        print("Data Not there")
                        # print(rows, "this row")
                        return

                # Create DataFrame
                # print(rows)
                df = pd.DataFrame(rows)
                # print(df)

                # Ensure the save directory exists
                save_dir = save_dir + "/" + commodity_head + "/" + state
                os.makedirs(save_dir, exist_ok=True)

                # Sanitize dates for filename (replace '-' with '_')
                sanitized_date_from = date_from.replace("-", "_")
                sanitized_date_to = date_to.replace("-", "_")

                # Define the filename
                filename = f"response_{sanitized_date_from}_to_{sanitized_date_to}.csv"
                file_path = os.path.join(save_dir, filename)

                # Save the DataFrame to a CSV file
                df.to_csv(file_path, index=False, mode="a")

                return f"Data successfully saved to {file_path}"
            else:
                return "No table found in the response."
        else:
            return f"Failed to retrieve data. Status code: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the request: {e}"
    except IOError as e:
        return f"An error occurred while writing to the file: {e}"


def get_data_from_website():
    for year in year_ranges:
        for state, s_abbr in state_abbr.items():
            for commodity, commodity_value in commodities.items():
                print(commodity, s_abbr, district, market, year, commodity_value)

                # Call the function and print the result
                result = get_agmarknet_data_and_save_csv(
                    commodity=commodity,
                    state=s_abbr,
                    district=district,
                    market=market,
                    date_from=year["first_date"],
                    date_to=year["last_date"],
                    trend=trend,
                    commodity_head=commodity_value,
                    state_head=state,
                )
                print(result)


def append_data_from_website(from_date:date,to_date:date):
    DATE_FORMAT = "%d-%b-%Y"
    from_date_formatted = from_date.strftime(DATE_FORMAT)
    to_date_formatted = to_date.strftime(DATE_FORMAT)
    for state, s_abbr in state_abbr.items():
            for commodity, commodity_value in commodities.items():
                print(commodity, s_abbr, district, market, year, commodity_value)

                # Call the function and print the result
                result = get_agmarknet_data_and_save_csv(
                    commodity=commodity,
                    state=s_abbr,
                    district=district,
                    market=market,
                    date_from=from_date_formatted,
                    date_to=to_date_formatted,
                    trend=trend,
                    commodity_head=commodity_value,
                    state_head=state,
                )
                print(result)


state_abbr = {
    "Andaman and Nicobar": "AN",
    "Andhra Pradesh": "AP",
    "Arunachal Pradesh": "AR",
    "Assam": "AS",
    "Bihar": "BI",
    "Chandigarh": "CH",
    "Chattisgarh": "CG",
    "Dadra and Nagar Haveli": "DN",
    "Daman and Diu": "DD",
    "Goa": "GO",
    "Gujarat": "GJ",
    "Haryana": "HR",
    "Himachal Pradesh": "HP",
    "Jammu and Kashmir": "JK",
    "Jharkhand": "JR",
    "Karnataka": "KK",
    "Kerala": "KL",
    "Lakshadweep": "LD",
    "Madhya Pradesh": "MP",
    "Maharashtra": "MH",
    "Manipur": "MN",
    "Meghalaya": "MG",
    "Mizoram": "MZ",
    "Nagaland": "NG",
    "NCT of Delhi": "DL",
    "Odisha": "OR",
    "Pondicherry": "PC",
    "Punjab": "PB",
    "Rajasthan": "RJ",
    "Sikkim": "SK",
    "Tamil Nadu": "TN",
    "Telangana": "TL",
    "Tripura": "TR",
    "Uttar Pradesh": "UP",
    "Uttrakhand": "UC",
    "West Bengal": "WB",
}


# Example usage
if __name__ == "__main__":
    # Define your query parameters
    # commodity = "23"
    # state = "KK"
    district = "0"
    market = "0"
    # date_from = "01-Oct-2023"
    # date_to = "31-Aug-2024"
    trend = "0"
    # commodity_head = "Onion"
    # state_head = "Karnataka"

    # result = get_agmarknet_data_and_save_csv(
    #     commodity=commodity,
    #     state=state,
    #     district=district,
    #     market=market,
    #     date_from=date_from,
    #     date_to=date_to,
    #     trend=trend,
    #     commodity_head=commodity_head,
    #     state_head=state_head,
    # )
    # print(result)

    now = datetime.now()
    formatted_now = now.strftime("%d-%b-%Y")

    # Convert formatted date string to datetime object
    date_object = now.strptime(formatted_now, "%d-%b-%Y")

    # Subtract one year
    new_date = date_object - relativedelta(years=1)

    year_ranges = get_dates(datetime.now())(10)
    # print(year_ranges)

    # commodities = {23: "Onion"}
    commodities = {
        3: "Rice",
        1: "wheat",
        263: "Gram dal",
        260: "tur dal",
        264: "urad dal",
        265: "moong dal",
        259: "masur dal",
        267: "Groundnut oil",
        324: "mustard oil",
        273: "vanaspati",
        24: "Potato",
        23: "onion",
        78: "tomato",
        48: "Sugar",
        74: "gur",
        44: "tea",
    }

    get_data_from_website()
    append_data_from_website(datetime.now(),(today = datetime.date.today()
                                last_week = today - datetime.timedelta(weeks=1)))
