# Import transactions to money lover web

A selenium script to import transactions from excel file to moneylover.

## Prepare
1. Create `data/transactions.xlsx` having each sheet name as the exact wallet name.
2. Create a folder to store browser sessions
    ```bash
    mkdir chrome-data
    ```
3. Add transactions in each sheet. Columns: 
    - `Date`: Example: `31/12/2023` or `12-Jun-2022`
    - `Category`: `Expense` or `Income|Category`. Example: `Expense|Bills & Utilities`
    - `Note`: My note
    - `Description`: Can be left as in the bank statement
    - `Change` or `Withdraw` or `Deposit`: Amount. Can be positive or negative if `Change`
4. Don't put transfers into the sheets. Remember them separately. The script does not support transfers.
5. Add values in the env file:
    ```bash
    cp .env.example .env
    ```

## Run 
### Locally   
1. Run:
    ```bash
    conda create -n moneylover python=3.9
    conda activate moneylover
    pip install -r requirements.txt
    python src/import_transactions.py
    ```
2. Import the transfers manually.

### With docker (does not work on Apple chip mac)
1. Run:
    ```bash
    docker-compose up -d
    docker-compose exec selenium python src/import_transactions.py
    ```
2. See whats happening inside container: http://localhost:7900/?autoconnect=1&resize=scale&password=secret