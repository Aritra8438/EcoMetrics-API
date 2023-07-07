# EcoMetrics-API
<p align="center">
  <a href=""><img src="https://img.shields.io/github/last-commit/Aritra8438/EcoMetrics-API?style=for-the-badge&logo=git" alt="MIT" /></a>
  <a href=""><img src="https://img.shields.io/github/issues/Aritra8438/EcoMetrics-API?style=for-the-badge&label=Issues" alt="MIT" /></a>
  <a href=""><img src="https://img.shields.io/github/issues-pr/Aritra8438/EcoMetrics-API?style=for-the-badge&logo=github" alt="MIT" /></a>
  <a href=""><img src="https://img.shields.io/github/issues-pr-closed/Aritra8438/EcoMetrics-API?style=for-the-badge&logo=github" alt="MIT" /></a>
</p>
<p align="center">
  <a href=""><img src="https://github.com/Aritra8438/EcoMetrics-API/actions/workflows/pytest.yml/badge.svg" alt="MIT" /></a> &nbsp;
  <a href=""><img src="https://github.com/Aritra8438/EcoMetrics-API/actions/workflows/pylint.yml/badge.svg" alt="MIT" /></a> &nbsp;
  <a href=""><img src="https://img.shields.io/codecov/c/github/Aritra8438/EcoMetrics-API" alt="MIT" /></a> &nbsp;
  <a href=""><img src="https://img.shields.io/github/commit-activity/w/Aritra8438/EcoMetrics-API" alt="MIT" /></a> &nbsp;
</p>

Hi, everyone. Welcome to this API.

**An API to query population, GDP per capita by years, countries, etc. that returns pretty tables and graphs.**

This API has four main endpoints:
- json ( `/json` -> Returns JSON response )
- table ( `/table` -> Returns table response )
- graph ( `/graph` -> Returns graph response )
- stats ( `/stats` -> Returns stats response )

It's a collaborative open-source project Raisa and I did (are doing) as a part of our code submission for the MLH fellowship. 
We have exposed all of our APIs in our own API documentation. Feel free to test APIs there (You will be able to test it on-screen).


# Website 
<a href="https://eco-metrics-api.vercel.app/"><strong>Our website is live!</strong></a>
<br>
- The application is hosted on **Vercel**.
<br>
<img width="944" alt="image" src="https://github.com/Aritra8438/EcoMetrics-API/assets/64671908/6c1114cd-803b-4a63-967f-5fa0274a3ebf">


# Local Development Setup:

**Note**: You don't currently have database access. We will be working on giving read-only access to all the contributors.
Nevertheless, you can always create your own database and populate it with dummy data. Schema is available in the `models.py`.

Open the terminal at the destination folder:

```console
# Cloning the repository
git clone https://github.com/Aritra8438/EcoMetrics-API.git

cd EcoMetrics-API

# Creating a virtual environment
pip install virtualenv

# linux users
virtualenv venv
source venv/bin/activate

# Windows users
python -m virtualenv venv
./venv\Scripts\activate

# Download packages
pip install -r requirements.txt 
```

Your virtual environment should be ready.

To bring up the server:
```console
flask --app api/index run --debug
```


