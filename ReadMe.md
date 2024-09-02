# March Madness

Methods for selecting March Madness Winners!

The project offers an Evaluation and a Prediction Mode for creating a bracket.

* Evaluation Mode guides users through selecting a March Madness bracket, providing relevant information throughout the process
* Prediction Mode automatically selects a March Madness bracket through various prediction methods.

## Prerequisites

* Python (3.12 officially supported)
* Docker engine (ex. Docker Desktop)
* psql (16.3 used in development)

## Setup

### 1. Start and initialize database

Start the postgres database via Docker with `docker compose up -d`. Once running, initialize the database via `psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE march_madness;"`. The default DB password is `postgres`. The postgres container uses a volume mount, so data will persist if the container itself is stopped or deleted.

### 2. Check that rankings file exists

Check that a file called `tournament_rankings.r<current_year>` exists for the desired tournament year. If not, see [docs/adding_a_new_year.md](docs/adding_a_new_year.md).

### 3. Add data

Data is scraped from external sources and stored in the database. 

The database can be populated by running the following scripts:

```shell
cd mmsite
python manage.py migrate  # Runs DB migrations
cd ..
python generate_static_data.py
python generate_yearly_data.py  # Runs for current year by default
```

Alternatively, you can import the contents of `db/march_madness.sql` via `psql -h localhost -p 5432 -U postgres -d march_madness -a -f db/march_madness.sql`.

### 4. Create an .env file

Settings are configured via environment variables, which are loaded automatically when defined in `mmiste/.env`. For local development and use, the values from `mmsite/.env.sample` can be used as is.

## Usage - User Evaluation

### UI

Evaluation Mode can be run via the Django UI. Run `cd mmsite; python manage.py runserver` and then navigate to http://localhost:8000/marchmadness.

Click "Guided Selection" and go through the process of selecting teams. When complete, the selected winners for each round will be displayed.

### Shell

By default, the `run.py` script guides the user through manually picking teams for the current year. Run the following:

```shell
./run.py  # Go through selections
open NCAA_Tournament_Results.log  # Display selection results
```

Different years can be evaluated via the `-y` parameter, ex `./run.py -y 2023`

## Usage - Automated Prediction Methods

Automated methods that use an algorithm to decide matchups are defined as prediction methods. The desired prediction method should be provided to the `-p` parameter from one of the methods listed below:

* `random` - Pure random choice
* `lptr` - Weighted random choice. Teams with a higher ranking are more likely to be selected to win, where weighing is done by the difference in ranking on a linearly proportional scale. AP rankings are also considered in this choice.
* `sigmodal` - Weighted random choice. Teams with a higher ranking are more likely to be selected to win, where weighing is done by the difference in ranking on a sigmoidal scale. AP rankings are also considered in this choice. The parameter `k` is used to determine the shape of the sigmodal curve. By default, `k=.33`, which closely emulates the behavior of a sigmodal curve without a scaling factor. `k` can be adjusted via the command line parameter `-k`, where a higher value will make the sigmodal curve more closely emulate a step function, and a lower value will make it more closely emulate a horizontal line. Run `./visualize_weight_functions.py` to see the effect of altering `k`.
* `ranked` - Chooses the team with the higher tournament ranking. If rankings are the same, defer to the AP ranking. If neither team is ranked by the AP, choose a team randomly.
* `ap` - Chooses the team with the higher AP ranking. If neither team is ranked by the AP, choose the team with the higher tournament ranking. If tournament rankings are the same, choose a team randomly.
* `nickname` - Chooses the team whose nickname has a higher positive sentiment analysis value.

### Sample Usage

Currently, automated prediction can only be run via a shell, i.e. not via the Django app.

```shell
./run.py -p random           # Random Selection for the current year
./run.py -p lptr -y 2022     # Weighted LPTR selection for 2022
./run.py -p sigmodal -k 0.5  # Weighted Sigmodal selection with overriding value of k
```

## Results

Results are stored in `NCAA_Tournament_Results.log`. The file is always appended to, so should be removed between subsequent runs. There is no automated way to create a bracket on a site such as espn.com with these results, so they must be entered manually.

## Future Work

This project is being actively worked and improved. See the GitHub [Projects](https://github.com/AGnias47/march-madness/projects?query=is%3Aopen) tab for details.
