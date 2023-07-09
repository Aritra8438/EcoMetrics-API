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

This API has four primary endpoints:
- json ( `/json` -> Returns JSON response )
- table ( `/table` -> Returns table response )
- graph ( `/graph` -> Returns graph response )
- stats ( `/stats` -> Returns stats response )

It's a collaborative open-source project Raisa and I did (are doing) as a part of our code submission to Mercor Hackathon. 
We have exposed all of our APIs in our [API documentation](https://eco-metrics-api.vercel.app/api-documentation). Feel free to test APIs there (You will be able to try them on-screen).

This API might be (extremely!) slow, as both the backend server (deployed on Vercel) and database (hosted on Railway) are deployed using the free plan.
Nevertheless, we tried to optimize the database queries to compensate for that (Apologies!).

# Index 
To quickly jump to a subsection, 

* [Website](https://github.com/Aritra8438/EcoMetrics-API/tree/main#website)                          
                
* [Local Development Setup](https://github.com/Aritra8438/EcoMetrics-API/tree/main#local-development-setup)

* [Github workflows](https://github.com/Aritra8438/EcoMetrics-API/tree/main#workflows)                   

* [Contribution Workflow](https://github.com/Aritra8438/EcoMetrics-API/tree/main#contribution-workflow)
  
* [API documentation](https://github.com/Aritra8438/EcoMetrics-API/tree/main#api-documentation)

* [Current works](https://github.com/Aritra8438/EcoMetrics-API/tree/main#current-works)

* [Future plans](https://github.com/Aritra8438/EcoMetrics-API/tree/main#future-plans)


# Website 
<a href="https://eco-metrics-api.vercel.app/"><strong>Our website is live!</strong></a>
<br>
- The application is hosted on **Vercel**.
<br>
<img width="944" alt="image" src="https://github.com/Aritra8438/EcoMetrics-API/assets/64671908/6c1114cd-803b-4a63-967f-5fa0274a3ebf">


# Local Development Setup:

**Note**: You don't currently have database access. We will be working on giving read-only access to all the contributors.
Nevertheless, you can always create your database and populate it with dummy data. Schema is available in the `models.py`.

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

## Workflows:

The essential APIs are unit-tested using ```pytest``` and linted using ```pylint```. If you are contributing to this repo, it's recommended that you run ```pytest``` and ```pylint``` before your pull request.

- Open the project folder and run:
```console
# run pytest
pytest
pytest -s (to get the output of the tests if you've used print statement inside)
pytest -k test_abc (to run a particular test)

# run pylint
pip install pylint (Required to run once)
pylint $(git ls-files '*.py')
```
Alternatively, you can search [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) at the extension marketplace (in VSCode) and install the linter. The lint errors will be highlighted if Pylint is installed.

Currently, All the tests are linked to `client` @pytest.fixture, which is in `conftest.py`. If you have made changes to the backend, we recommend adding a pytest for it.

We have enabled `codecov` and `dependabot` for this repo. To learn about the workflows, please visit the corresponding `.yml` files.

## Contribution Workflow:

Hello contributors, here is the contribution guideline you should follow:

- **First, create a fork of this repo. (Available at the top right corner of the repo)** 

- Go to the forked repository and **Clone the fork of your repo to the destination folder**.
```console
$ git clone https://github.com/YOUR_USERNAME/YOUR_FORK.git

```
- Navigate to the Project repository
```console
$ cd EcoMetrics-API
```
- Add Upstream to your clone

```console
$ git remote -v
> origin  https://github.com/YOUR_USERNAME/YOUR_FORK.git (fetch)
> origin  https://github.com/YOUR_USERNAME/YOUR_FORK.git (push)
```
```console
$ git remote add upstream https://github.com/Aritra8438/EcoMetrics-API.git
```

```console
$ git remote -v
> origin    https://github.com/YOUR_USERNAME/YOUR_FORK.git (fetch)
> origin    https://github.com/YOUR_USERNAME/YOUR_FORK.git (push)
> upstream  https://github.com/Aritra8438/EcoMetrics-API.git (fetch)
> upstream  https://github.com/Aritra8438/EcoMetrics-API.git (push)
```
- Before making any changes, sync your origin with upstream 

```console
$ git pull upstream main --rebase
``` 


- Make some changes to the project. After that, open a new branch and commit the changes.

```console
$ git checkout -b <new_branch>
$ git add .
$ git commit -m "Commit message"
$ git push origin <new branch>
``` 

- There will be a visible change in your repo, click on that and create a new pull request.

Thank you for your contribution.

## API Documentation:

All of our APIs are available at [this](https://eco-metrics-api.vercel.app/api-documentation) documentation. The documentation has a minimum design (Apologies!) but we intend to keep it as it is because **It enables on-screen testing with HTML response**.

Here is a screenshot of the same.

<img width="960" alt="image" src="https://github.com/Aritra8438/EcoMetrics-API/assets/64671908/17d13fe3-ce00-45fe-a286-a675d52f2a8d">
Currently, Mathesar supports two aggregation functions (`Distinct list` & `Count`) as transformation steps while summarizing columns. 

## Current works:

- [x] Support for `population` database.
- [x] Support for effective querying.
- [x] Support for `GDP per capita` database.
- [x] Support for comparing data from different databases.
- [ ] Support for `Annual average temperature` database.
- [ ] Support for the `Forest Land percentage` database.

## Future plans:
- [ ] Support for predicting data when input has future years  as input.
- [ ] Support for extremely user-friendly and customizable graphs.

