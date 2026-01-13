# Stocks AI PoC

This project is a Proof of Concept (PoC) for ingesting, storing, and searching stock data using Azure Cosmos DB and FastAPI.

## Project Structure
```
├── ingestion.py           # Ingests all CSVs into Cosmos DB
├── poc-v1.py              # FastAPI app for search API
├── helpers.py             # Utility functions
├── entity_resolver.py     # Cosmos DB entity resolution logic
├── query_parsing.py       # Query type detection and parsing
├── response_builders.py   # API response construction
```

## Setup
1. **Clone the repository**
2. **Install dependencies**:
   - Python 3.8+
   - `pip install -r requirements.txt`
   - Azure SDKs: `azure-cosmos`, `azure-identity`, `fastapi`, `pydantic`
3. **Configure Azure Cosmos DB**:
   - Set your Cosmos DB endpoint and credentials in `poc-v1.py`.
   - Ensure your account has RBAC permissions for data ingestion and querying.
4. **Run Ingestion**:
   - Place your Kaggle stock market CSVs in the project directory.
   - Run: `python ingestion.py`
5. **Start the API**:
   - Run: `uvicorn poc-v1:app --reload`
   - Access the API at `http://localhost:8000/v1/search?q=Your+Query`

## Example Queries
- `Basilic PE`
- `Reliance market cap`
- `IT sector`
- `BEL`

## Notes
- The ingestion script is robust to missing/empty fields and handles partition key requirements.
- The API supports full-text search and returns structured responses for stock metrics, overviews, and sector constituents.
- For local development, you can use the [Azure Cosmos DB Emulator](https://learn.microsoft.com/azure/cosmos-db/emulator).

## License
MIT License
