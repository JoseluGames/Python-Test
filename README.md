First of all, I took some time to refresh on my Python knowledge and researched about Flask, even though the task makes this a free choice, I believe it very is benefitial for me to start getting familiar with it. For this I took a couple of hours of playing around with it.

### Shortening and storage

For shortening the URLs I decided to simply get a hash of the URL and use part of it (The first 8 hex chars should be fine). This makes it pretty simple to generate those short URLs but means that I have to store the short_url -> url relation on a database. Thinking of ways to simply encode the long URL into a shorter version in a way that can be decoded would reduce costs as it would remove the need for a database, but for the provided example the hash approach should be enough.

For the database I decided to go with SQLite for the sake of simplicity.

I decided to run the input URLs through a validation step to make sure they are valid URLs. This simplifies the redirection step.

### Authentication

For authentication, I decided to follow the suggested route in the task description and make a token based auth, simply make a post requets to /register to generate a token and use it to shorten a URL. This token is saved on a users table and checked before shortening any URLs.


### Analytics

For analytics I had to research about threading in Python, after that I decided to simply store the user actions on the database (Register, Shorten and Redirect) for simplicity.