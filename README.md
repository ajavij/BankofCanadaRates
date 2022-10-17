Bank of Canada Interest Rates REST API

----
  Returns the latest interest rate for several finanicial markets in json format.

* **URL**

   /bankrate/<br />
   /targetrate/<br />
   /10yearbond/<br />
   /2yearbond/<br />
   /5yearbond/<br />
   /3yearbond/<br />
   /7yearbond/<br />
   /longtermbond/<br />
   /mmfinancing/

* **Method:**

  `GET`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"Bank Of Canada Rates": {"id": 1, "InterestRate": 3.5, "Date": "2022-10-16", "FinancialMarket": "Bank rate"}}`
  ```
