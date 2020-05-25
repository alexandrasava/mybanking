# MyBanking: Simple CRUD App with Python, Flask, MySQL

Exchange service API.

**MyBanking** app has a REST API that exposes 2 endpoints:
- **grab_and_save**: Accepts a currency name (3 letter code) and an amount (max 24 digits precision with 8 digits for decimals) through POST requests, calls Open Exchange Rate API to get the rate of the currency against USD in order to convert the amount into USD and saves everything into a database (the currency name, the amount, the rate of the currency against USD and the amount converted into USD).
- **last**: Returns the latest records from the database, depending on the request query string from GET requests. If it receives a currency name, it will return the latest record for that currency, if it receives a number, it will return the latest n records from the database, and if it receives both, it will return the latest n records for the currency.

**NOTE**
Actually there are more endpoints exposed, but they use the rendering feature Flask provides. Only the ones above return data in a json format (as the challenge specified). I chose this approach in order to make the frontend development part easier (since it wasn't the purpose of the challenge).

## Running the App

#### Prerequisites
- docker
- docker-compose
- MySQL

#### How To Run
1. Change `$MY_IP` from mybanking/instance/config.py with the IP address of your wireless or wired interface (run `ifconfig`)
2. `cd mybanking`
3. `sudo docker-compose up --build`

#### Testing
The endpoints can be tested both from **UI** and **curl**.
##### **UI Testing**

Paste in a web browser the following URL: *http://127.0.0.1:5000/* to view the UI. On the right side there are two links: **My Exchanges** and **Filter Exchanges**.

In order to test the **grab_and_save** endpoint, click on **My Exchanges** and then on **Exchange Amount** button (from the bottom of the page). A form will be displayed and upon submit, a new exchange will be created. All the exchanges from the database are displayed on **My Exchanges** page.

In order to test the **last** endpoint, click on **Filter Exchanges** page. Use the form in order to filter the exchanges. Upon submit, the filtered exchanges will be displayed below the form.

##### CURL Testing
For the **grab_and_save** endpoint, use the following command:

`curl -i --header "Content-Type: application/json" --request POST --data '{"currency":"EUR","amount":1234.5}' http://127.0.0.1:5000/grab_and_save`

For the **last** endpoint, use one of the following commands:

`curl -i -X GET "http://127.0.0.1:5000/last?currency=EUR&number=10"`

`curl -i -X GET "http://127.0.0.1:5000/last?currency=EUR"`

`curl -i -X GET "http://127.0.0.1:5000/last?number=5"`
