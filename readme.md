# MISTER PLOW

## Setup

1. Install mongodb.
2. Run mongodb locally.
3. Create a virtualenv for this project.
4. ```pip install -r requirements.txt```

## Cron

Run the cron every five minutes as the ubuntu user. Note: This user is not required, just an example.

```*/5 * * * * ubuntu workon mister-plow && /home/ubuntu/apps/mister-plow/repository/scraper.py```
