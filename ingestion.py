import csv, os
import logging
from db import get_cosmos_container

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Cosmos DB client and container
# Make sure to set your connection string and credentials

container = get_cosmos_container()

# List of all Nifty 50 stock symbols from the dataset
def get_company_list():
    data_directory = "data_new"
    company_list = []
    with open(os.path.join(data_directory, "List-Of-All-Companies.csv"), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header if present
        for row in reader:
            if len(row) > 1:
                company_list.append(row[1].strip())
    return company_list

def process_stock_csv(csv_file_path, company_name):
    """Process a single stock CSV file and upload to Cosmos DB"""
    try:
        logger.info(f"Processing {company_name} from {csv_file_path}")
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row.get('NSE', '')
                if not symbol:
                    logger.warning(f"Skipping row with missing NSE symbol for {company_name}")
                    continue
                # Build document with all fields from CSV, remove empty fields
                doc = {k: v for k, v in row.items() if k != ''}
                doc['id'] = symbol
                doc['symbol'] = symbol
                print(doc)  # For debug
                
                try:
                    container.upsert_item(doc)
                    logger.info(f"Successfully processed data for {company_name}")
                    return 1
                except Exception as create_error:
                    logger.error(f"Error creating document for {company_name}: {create_error}")
                    return 0
        return 0
    except Exception as e:
        logger.error(f"Error processing {company_name}: {e}")
        return 0

def ingest_all_stocks_data(company_list, data_directory="data_new"):
    """Ingest all company information from the specified directory"""
    processed_stocks = 0
    
    logger.info("Starting all stocks data ingestion...")
    
    # Method 1: Try to process files based on known stock symbols
    for company_name in company_list:
        csv_file = os.path.join(data_directory, "detailed_data","detailed_data", f"{company_name}", f"{company_name}_Basic_Info.csv")
        print(csv_file)
        if os.path.exists(csv_file):
            records = process_stock_csv(csv_file, company_name)
            processed_stocks += records
        else:
            logger.warning(f"CSV file not found for {company_name}: {csv_file}")
    
    logger.info(f"Ingestion completed! Processed {processed_stocks} stocks with {len(company_list)} total records")
    return processed_stocks

if __name__ == "__main__":
    # Run the ingestion


    total_companies = get_company_list()
    print(f"Total companies retrieved: {len(total_companies)}")
    
    processed_stocks = ingest_all_stocks_data(total_companies)
    
    # print(f"\n=== INGESTION SUMMARY ===")
    # print(f"Stocks processed: {processed_stocks}")
    # print(f"Total records ingested: {total_records}")
