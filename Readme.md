# Project Title

vPhrase Send Mail Django Web App

## Getting Started

You need to clone the repository and you are ready for your project. 

### Prerequisites

You should have used selenium atleast once in your unix/windows system.
Otherwise it may give you error like `geckodriver should be in execeution path` .
You can search this error(if you get error like this) on internet and `Stackoverflow`
has lots of answer for this question.

### Installing

A step by step series of examples that tell you how to get a development env running

Create a virtual environment for `python==3.6` compatibility. I have not tasted it 
with `python==3.7`, so you may encounter error or warning. For making 
Virtual environment, please follows this step

    $ sudo apt-get install python-virtualenv
    $ virtualenv --python=python3.6 myvenv

**NOTE**: If you get an error like

```
E: Unable to locate package python3-venv
```

Then instead run:

    $ sudo apt install python3.6-venv

Once you install the Virtual Environment. You need to activate it.

    source myvenv/bin/activate

You need to install the requirements now.

    pip install -r requirements.txt
        
After installations, you can run server by

    python manage.py runserver

If you find any error related to `gekodriver` or `selenium` then please check the version of `selenuim`
in your `requirements.txt` and kindly check the version of you `Mozialla Firefox`. We are trying to make it more
suitable. You can also `stackoverflow` if you encounter this type of problem. 

We need to do `makemigrations` and `migrate` for our database.

    python manage.py makemigrations
    python manage.py migrate

## Working demo on web app

![alt text](https://preview.ibb.co/fcS8ez/screencapture_127_0_0_1_8000_2018_09_15_14_25_25.png)
  
For sending mail, you need to first enter you mail address and click on `Subscribe`. 
Then you can upload the your templates i.e. `.html` file which would contain all `style and script`
file. After uploading your templates in your home page, one thumbnail would appear, with name of
your `.html` page. You need to click `Parse` for parsing it's `img`. After parsing, you can click on
`Send` button. It would send mail to all your subscribed email address.

## Working demo with Django Rest Framework

**I have used token based for authentication**

![alt text](https://preview.ibb.co/mD0pRp/Screenshot_from_2018_09_25_12_05_11.png)

Here keys are `username` and `password`. You can find all api link description in [**wiki**](https://gitlab.com/AnkurBegining1/sendmail/wikis/api)
section of gitlab.

**Uploading the templates**

![alt text](https://preview.ibb.co/mR8qz9/Screenshot_from_2018_09_25_13_06_45.png)

Here key for uploading templates is `templates`. You are only allowed to use `.html` file otherwise it would send you
`404 response`. For full documentation, please visit [**wiki**](https://gitlab.com/AnkurBegining1/sendmail/wikis/templates-upload-api)

## Running the tests

Explain how to run the automated tests for this system

**Sorry, test case is in the progress queue**

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```


