# Design and implementation of a web application for contact data

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies](#technologies)
3. [Architecture](#architecture)
4. [Installation](#installation)


## Project Overview

This project is a web application to store contact data. Based on entered data application fetch rest of data from 3rd part APis.

## Technologies 

- **Python 3.12.1**
- **Django 5.0**
- **Bootstrap 5.3.5**
- **Django Crispy Forms 2.3**
- **Django Rest Framework 3.14.0**
- **Django Silk 5.3.2**
- **Crispy Bootstrap5 2025.4**

## Architecture

The app includes REST API configurations and follows the MVT (Model-View-Template) architectural pattern.

- **Model: Defines the data structure and stores it in the SQLite database.**
- **View: Defines the logic of the app, handling user interactions and updating the database.**
- **Template: The front-end of the app, which shows the HTML and CSS content to the user.**


## Installation

To run the project locally, follow these steps:

1. Clone the repository:

```
git clone https://github.com/bartekuznik/Django_MVT_with_3part_API.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Go to the project directory:

```
cd project
```

4. Run the server:

```
python manage.py runserver
```
