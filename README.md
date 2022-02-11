# A basic Harvest API using Python
This is a basic python API script, pluggin into Harvest. This loads time entries and estimates into individual excel files.

In order for the script to work you will need to:
  - Retrieve a Harvest token
  - Specify target locations for the excel file outputs

For API documentation refer to
https://help.getharvest.com/api-v2/

To create a API token, you must have an account with Harvest. Then follow the these steps.

1) Go to this link 
https://id.getharvest.com/developers

2) After logging in, click on "Create New Person Access Token"

3) Name the token

4) Copy and paste the code in the box titled "Testing Your Token"

It should look something like this

curl -i \
  -H 'Harvest-Account-ID: 1451470'\
  -H 'Authorization: Bearer 2666953.pt.gnaEcoAHUpHaSuMc8DGT9tZYNWW_4HdhXtykn8QMDfr9QRQXOJL676AYyq-uYGbCR8HAzBRaVRFlCs6IeqmAsQ'\
  -H 'User-Agent: Harvest API Example' \
  "https://api.harvestapp.com/api/v2/users/me.json"







