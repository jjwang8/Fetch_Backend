# Points Tracking API

This is a RESTful API built using Flask that tracks user points from various payers. It supports adding points, spending points, and retrieving the current balance for each payer.

## Requirements

To run this project, you need:

- Python 3.x
- Flask (`pip install flask`)
- Requests (`pip install requests`)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the API

1. Start the Flask API by running the `app.py` file:

   ```bash
   python app.py
   ```

   The API will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. Add Points

- **URL**: `/add`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "payer": "DANNON",
    "points": 1000,
    "timestamp": "2022-11-02T14:00:00Z"
  }
  ```
- **Response**: Status `200` on success, no response body.

### 2. Spend Points

- **URL**: `/spend`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "points": 5000
  }
  ```
- **Response**:
  ```json
  [
    { "payer": "DANNON", "points": -100 },
    { "payer": "UNILEVER", "points": -200 },
    { "MILLER COORS": "points": -4700 }
  ]
  ```

### 3. Get Points Balance

- **URL**: `/balance`
- **Method**: `GET`
- **Response**:
  ```json
  {
      "DANNON": 1000,
      "MILLER COORS": 5300,
      "UNILEVER": 0
  }
  ```

## Testing the API

To make testing easier, you can run the `test.py` script, which automates the process of adding points, spending points, and retrieving the balance, using the sample test case provided in the challenge.

### Steps to Run the Test Case

1. Make sure the Flask API is running on `http://127.0.0.1:5000/` by running the `app.py` file:

   ```bash
   python app.py
   ```
2. In another terminal, run the `test.py` script:

   ```bash
   python test.py
   ```
3. The output should look like this:

   ```bash
   Starting sample test!!!!
   Added 300 points for DANNON worked.
   Added 200 points for UNILEVER worked.
   Added -200 points for DANNON worked.
   Added 10000 points for MILLER COORS worked.
   Added 1000 points for DANNON worked.
   [
       {
           "DANNON": -100
       },
       {
           "UNILEVER": -200
       },
       {
           "MILLER COORS": -4700
       }
   ]
   Current balance:
   {
       "DANNON": 1000,
       "MILLER COORS": 5300,
       "UNILEVER": 0
   }
   ```

## Part 2

To see my responses to part 2 questions read the following file:

```bash
summary.txt
```