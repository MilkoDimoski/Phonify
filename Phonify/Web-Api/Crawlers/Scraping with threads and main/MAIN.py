from idna.idnadata import scripts

from Crawlers import SETEC,ANHOCH,MOBELIX,TELEKOM,NEPTUN
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.exc import SQLAlchemyError
import urllib
import numpy as np

def main():
    scripts = [ANHOCH,SETEC,TELEKOM,NEPTUN,MOBELIX]
    # scripts = [SETEC]
    # Database connection
    database_url = "mssql+pyodbc:///?odbc_connect={}".format(urllib.parse.quote_plus(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=ETEREO\SQLEXPRESS;"
        "Database=Phonify;"
        "Trusted_Connection=yes;"
    ))

    engine = create_engine(database_url)
    metadata = MetaData()  # No need to bind here
    mobile_table = Table('Mobile', metadata, autoload_with=engine)  # Load the 'Mobile' table from the engine

    # List to store DataFrames
    dataframes = []
    final_df = pd.DataFrame()

    # Threading: Run all scraping functions concurrently
    with ThreadPoolExecutor(max_workers=len(scripts)) as executor:
        futures = {executor.submit(script.scrape): script for script in scripts}

        for future in as_completed(futures):
            script = futures[future]
            try:
                print(f"Scraping data from {script.__name__}...")
                df = future.result()  # Get the result (DataFrame)
                dataframes.append(df)
            except Exception as e:
                print(f"Error scraping data from {script.__name__}: {e}")

    # Combine all DataFrames into one
    if dataframes:
        final_df = pd.concat(dataframes, ignore_index=True)

        # Clean the price column
        final_df['price'] = final_df['price'].replace({r'[^\d.]': ''}, regex=True)  # Remove non-numeric characters
        final_df['price'] = pd.to_numeric(final_df['price'], errors='coerce')  # Convert to numeric, invalid prices become NaN
        final_df['price'] = final_df['price'].fillna(np.nan)  # Replace NaN with np.nan for compatibility

        output_file = "all_phones.csv"
        final_df.to_csv(output_file, index=False)
        print(f"All data saved to {output_file}.")
    else:
        print("No data was scraped.")

    # Insert, update, and delete phones in the database
    with engine.connect() as connection:
        # Start a transaction
        with connection.begin():
            # Get the list of phones currently in the database (based on vendor and whole_name)
            existing_phones_query = mobile_table.select()
            existing_phones = connection.execute(existing_phones_query).fetchall()

            # List of current phone identifiers (vendor + whole_name) from the database
            existing_phones_set = set((row.vendor, row.whole_name) for row in existing_phones)

            # List of phones from the new scrcape (vendor + whole_name)
            new_phones_set = set((row['vendor'], row['whole_name']) for _, row in final_df.iterrows())

            # Phones to delete (those that are in the database but not in the new data)
            phones_to_delete = existing_phones_set - new_phones_set

            # Delete old phones that are no longer scraped
            for vendor, whole_name in phones_to_delete:
                delete_query = mobile_table.delete().where(
                    mobile_table.c.vendor == vendor,
                    mobile_table.c.whole_name == whole_name
                )
                connection.execute(delete_query)
                # print(f"Deleted old phone: {whole_name} from {vendor}.")

            # Now insert or update the new phones
            # Now insert or update the new phones
            for index, row in final_df.iterrows():
                try:
                    # Check if the record already exists based on vendor and whole_name
                    query = mobile_table.select().where(
                        mobile_table.c.vendor == row['vendor'],
                        mobile_table.c.whole_name == row['whole_name']
                    )
                    existing_record = connection.execute(query).fetchone()

                    if existing_record:
                        # Update the existing record if a match is found
                        update_query = mobile_table.update().where(
                            mobile_table.c.vendor == row['vendor'],
                            mobile_table.c.whole_name == row['whole_name']
                        ).values(
                            brand=row['brand'],
                            model=row['model'],
                            price=row['price'],
                            link=row['link'],
                            updated_at=pd.to_datetime('now')  # Update the updated_at column
                        )
                        connection.execute(update_query)
                        # print(f"Updated existing phone: {row['whole_name']} from {row['vendor']}.")

                    else:
                        # Insert the new record if no match is found
                        insert_query = mobile_table.insert().values(
                            vendor=row['vendor'],
                            brand=row['brand'],
                            model=row['model'],
                            whole_name=row['whole_name'],
                            price=row['price'],
                            link=row['link'],
                            created_at=pd.to_datetime('now'),
                            updated_at=pd.to_datetime('now')
                        )
                        connection.execute(insert_query)
                        # print(f"Inserted new phone: {row['whole_name']} from {row['vendor']}.")

                except SQLAlchemyError as e:
                    print(f"Error processing record for {row['whole_name']} from {row['vendor']}: {e}")

    print("Data successfully inserted/updated/deleted in the database.")

if __name__ == "__main__":
    main()
