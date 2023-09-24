# Stock Market - This project is Django ResAPIs which includes the logic to find the calculation for three different type of transactions.

## Introduction
Stock Market is a project where you can buy and sell your shares.You can also manage your inventory for particular comapny based on date.

## Getting Started
Follow these steps to set up the Stock Market project on your local system:

### You should have django and djnago restframework installed in your system

1. #### Clone the Repository:
    ```git clone ```

2. #### Create a Virtual Environment (Optional):

## API Endpoints
Stock Market provides the following API endpoints:

#### API Endpoints

- **Create a Transaction:**
  - Use the `/transactions/` endpoint to add BUY, SELL, or SPLIT transactions.
  - Example JSON payload for BUY:
    ```json
    {
      "company": "Company Name",
      "trade_type": "BUY",
      "quantity": 100,
      "price_per_share": 100.00,
      "trade_date": "2023-01-01"
    }
    ```
  - Example JSON payload for SELL:
    ```json
    {
      "company": "Company Name",
      "trade_type": "SELL",
      "quantity": 50,
      "price_per_share": 120.00,
      "trade_date": "2023-02-01"
    }
    ```
  - Example JSON payload for SPLIT:
    ```json
    {
      "company": "Company Name",
      "trade_type": "SPLIT",
      "split_ratio": "1:2",
      "trade_date": "2023-03-01"
    }
    ```

- **Retrieve Average Buy Price and Balance Quantity:**
  - Use the `/average_buy_price` endpoint with a specific date to get the average buy price and balance quantity after that date.

  - Example request:
    ```
    GET /average_buy_price/?company=Company Name&date=24/09/2023
    ```

- **Retrieve Inventory information:**
  - Use the `/inventory` endpoint.

  - Example request:
    ```
    GET /inventory/