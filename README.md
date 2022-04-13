**Running the application**

All modules required are in requirements.txt, run:

```pip install -r requirements.txt to install```

You can run the file using:

```python main.py```
(may be python3 depending on Python setup)

Application will run locally on localhost:5000.

The following endpoints are available:
 * GET localhost:5000/participants - get all participants
 * GET localhost:5000/participants/<reference_id> - get participant
 * POST localhost:5000/participants/new - create new participant
 * PATCH localhost:5000/participants/<reference_id>/update - update existing participant
 * DELETE localhost:5000/participants/<reference_id>/delete - delete participant

**Model:**

The model Participant has the following fields:
 * First name - String
 * Last name - String
 * Date of birth - Date in format DD/MM/YYYY
 * Phone number - String
 * Address line 1 - String
 * Address line 2 - String
 * Post code - String

---
**Testing the application**

All modules required are in requirements-test.txt, to install run:

```pip install -r test-requirements.txt```

To run tests:
``` pytest test_apis.py test_models.py```

---

**Rationale**

I chose Python as it is a quick language to spin a quick application up in and dependency management is easy. 
Flask allowed me to make the APIs very quickly, and I chose to use an sqlite DB to store the participants as it integrates well with Flask, the data has a standard structure and it can scale to 100,000 records.
Moving this to higher environments, this could easily be swapped to storing the data in a standalone SQL database.

Data Model - 

* Name: I made this two string fields of first name and last name. I did this because it makes updating easier as people don't often change both at once and to add ease of reading for phone operators. Also, it will be more useful in the future if the name has to be used programatically, to avoid relying on string splitting.
* Date of birth: I chose a date for the date of birth field, with the format DD/MM/YYYY. This ensures that any incorrectly formatted dates won't be input in the database and they can be reliably used and transformed if needed. However, this does mean I had to add behaviour to the APIs to validate the date coming in is in a valid format so it could be saved in the database.
* Phone number: I made this a string to ensure the number isn't manipulated by trying to store it in a numerical format. As the brief did not specify the location of the participants, I didn't add any specific requirements to the phone number, as they vary globally.
* Address: I split address into two address lines and a postcode, again for ease of updating and use, as addresses vary globally. As I am using a sql database, it didn't make sense to nest data so I chose to make three columns to store the information. This should reduce problems if address needs to be used programatically in the future. However does mean inputting data is more work, and some thought to split data.