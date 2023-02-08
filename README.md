# Import transactions to money lover web

1. Create `data/transactions.xlsx` having each sheet name as the wallet name exactly.
2. Create a folder to store browser sessions
    ```bash
    mkdir userdata
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
6. Run:
    ```bash
    conda create -n moneylover python=3.9
    conda activate moneylover
    pip install -r requirements.txt
    python import_transactions.py
    ```
7. Import the transfers manually.