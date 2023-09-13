## Usage

Run `pip3 install -r requirements.txt` to install the required packages.

Run the app with `python3 main.py`, then post the `/register` endpoint to obtain an auth token in plain text.

To shorten a link make a post request to `/shorten/<token>` with `url=<your long url>` which will return a plain text response with the shortened url.

Then simply call `/<your short url>` to get redirected.

## Development

First of all, I took some time to refresh on my Python knowledge and researched about Flask, even though the task makes this a free choice, I believe it very is benefitial for me to start getting familiar with it. For this I took a couple of hours of playing around with it.

### Shortening and storage

For shortening the URLs I decided to simply get a hash of the URL and use part of it (The first 8 hex chars should be fine). This makes it pretty simple to generate those short URLs but means that I have to store the `short_url` -> `url` relation on a database, in a table called `urls`. Thinking of ways to simply encode the long URL into a shorter version in a way that can be decoded would reduce costs as it would remove the need for a database, but for the provided example the hash approach should be enough.

For the database I decided to go with SQLite for the sake of simplicity.

I decided to run the input URLs through a validation step to make sure they are valid URLs. This simplifies the redirection step.

### Authentication

For authentication, I decided to follow the suggested route in the task description and make a token based auth, simply make a post request to `/register` to generate a token and use it to shorten a URL. This token is saved on a `users` table and checked before shortening any URLs.

### Analytics

For analytics I had to research about threading in Python, after that I decided to simply store the user actions on the database (Register, Shorten and Redirect) for simplicity. The table is called `analytics` and store the `timestamp`, `ip`, `action`, `user_token` and `url`

### Scalability

For scalability testing I've used Locust and the current setup was able to scale the requests without issues. For further performance improvements I would suggest to maybe change the database to PostegreSQL to allow for concurrent transactions.

## Summary

In total, this task took me around 3-4 hours.

The main challenges were:
- Getting back to speed with Python in a different context from what I'm used to (As mentioned in our call, I've used it for analytics data ingestion mainly).
- Understanding Flask (I got the hang of it after just a bit of playing around).
- Profiling the performance of the service, as I hadn't done it before using Python so I had to learn how to use Locust and interpret it.

Overall, the task was pretty clear on it's requirements and relatively "simple"