
# iAffirm

iAffirm is to help encourage and spread positivity with the use of affirmative words. These affirmations are human written as users can enter their daily affirmations to the api, through a landing page. The affirmations are spread through tweets by the @iAffirmbot every 5 minutes at random.

## Example

![iAffirmBot](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/9138771c-c81d-408f-93de-484e33e5348b/iAffirmBot.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210819%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210819T161143Z&X-Amz-Expires=86400&X-Amz-Signature=2fd0fd4608e65a36be6533786a1423725ec0c691f6e6ae73502da6da201dcbaf&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22iAffirmBot.png%22)

  
## Tech Stack

**Server:** Python, Flask


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`FLASK_APP`

`FLASK_ENV`

`SECRET_KEY`

`DATABASE_URL` (for production environment)

`DEV_DATABASE_URL` (for development environment)

`TEST_DATABASE_URL` (for testing environment)


  
## Run Locally

Clone the project

```bash
  git clone https://github.com/LuluNwenyi/iAffirm.git
```

Go to the project directory

```bash
  cd my-project
```

Create virtual environment

```bash
  # FOR MACOS/LINUX

  python3 -m venv venv


  # FOR WINDOWS

  py -m venv env
```

Activate virtual environment

```bash
  # FOR MACOS/LINUX

  source venv/bin/activate


  # FOR WINDOWS

  .\env\Scripts\activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Set environment variables

```bash
  export FLASK_APP=app.py
  export FLASK_ENV=development
  export DEV_DATABASE_URL='sqlite:///dev.db'
  export SECRET_KEY='mysecretkey'
```

Initiate the database

```bash
  flask db init
```

Migrate the database changes

```bash
  flask db migrate -m "commit message here"
```

Push the database changes

```bash
  flask db upgrade
```

Start the server

```bash
  flask run
```

  
## Documentation

[Documentation](http://docs.iaffirm.xyz)

  
## Authors

- [@lulunwenyi](https://www.github.com/lulunwenyi)


  
## Feedback

For feedback or ideas/contributions, email dev@lulunwenyi.com.

If you'd like to support this project, feel free to [buymeacoffee](https://www.buymeacoffee.com/lulunwenyi).