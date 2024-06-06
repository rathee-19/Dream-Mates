# Dream Mates

Dream Mates is a web application designed to help users find their ideal roommates. Built with Flask and SQLite3, it allows users to register, create profiles, swipe on potential roommates based on their preferences, and view matches.

## Features

- **User Registration and Login**
  - Non-registered users are redirected to the registration page.
  - Users without profiles are redirected to the add profile page upon login.
  - Secure login to user accounts.

- **Profile Management**
  - Users can create and update their profiles with personal details and photos.

- **Swiping and Matching**
  - Users swipe left or right on potential roommates based on preferences.
  - Swiping can be done via buttons or drag-and-drop.
  - Mutual right swipes result in a match notification.

- **Viewing Matches**
  - Users can view their matches on the "UR Match" page.

- **Sign Out**
  - Secure sign-out option for users.

## Setup and Installation

### Prerequisites

- Python 3.x
- Flask
- SQLite3

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/dream-mates.git
    cd dream-mates
    ```

2. Install the required packages:

    ```sh
    pip install flask
    ```

3. Run the application:

    ```sh
    python app.py
    ```

## Project Structure


Here is a more concise README.md file for your project, Dream Mates:

markdown
Copy code
# Dream Mates

Dream Mates is a web application designed to help users find their ideal roommates. Built with Flask and SQLite3, it allows users to register, create profiles, swipe on potential roommates based on their preferences, and view matches.

## Features

- **User Registration and Login**
  - Non-registered users are redirected to the registration page.
  - Users without profiles are redirected to the add profile page upon login.
  - Secure login to user accounts.

- **Profile Management**
  - Users can create and update their profiles with personal details and photos.

- **Swiping and Matching**
  - Users swipe left or right on potential roommates based on preferences.
  - Swiping can be done via buttons or drag-and-drop.
  - Mutual right swipes result in a match notification.

- **Viewing Matches**
  - Users can view their matches on the "UR Match" page.

- **Sign Out**
  - Secure sign-out option for users.

## Setup and Installation

### Prerequisites

- Python 3.x
- Flask
- SQLite3

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/dream-mates.git
    cd dream-mates
    ```

2. Install the required packages:

    ```sh
    pip install flask
    ```

3. Run the application:

    ```sh
    python app.py
    ```

## Project Structure

```
.
├── app.py
├── templates
│ ├── start.html
│ ├── index.html
│ ├── login.html
│ ├── signup.html
│ ├── user.html
│ ├── view2.html
│ ├── viewlogin.html
│ ├── viewmatch.html
│ ├── match.html
│ ├── profile.html
│ ├── error.html
└── static
├── css
│ └── style.css
└── js
└── script.js
```

## Database Structure

### `users` Table

- `id`: INTEGER PRIMARY KEY
- `name`: TEXT
- `age`: INTEGER
- `bio`: TEXT
- `gender`: TEXT
- `address`: TEXT
- `contact`: TEXT
- `photo`: BLOB

### `swipes` Table

- `id`: INTEGER PRIMARY KEY
- `name`: TEXT
- `swipe_direction`: TEXT
- `user`: TEXT

### `matched` Table

- `name`: TEXT
- `user`: TEXT

## Key Routes

### `/`

- **GET**: Renders the start page.

### `/index`

- **GET**: Renders the main index page.

### `/submit`

- **POST**: Submits user data and saves it in the `users` table.

### `/login`

- **GET/POST**: Handles user login.

### `/sign`

- **GET/POST**: Handles user registration.

### `/user/<email>`

- **GET**: Displays user details for a given email.

### `/users/<name>`

- **GET**: Retrieves and displays user data from the database.

### `/view2/<name>`

- **GET**: Displays potential roommates for swiping.

### `/swipe_left` and `/swipe_right`

- **POST**: Records left/right swipes and handles matching.

### `/viewmatch` and `/match/<name>`

- **GET/POST**: Displays matched users.


