First of all, I took some time to refresh on my Python knowledge and researched about Flask, even though the task makes this a free choice, I believe it very is benefitial for me to start getting familiar with it. For this I took a couple of hours of playing around with it.

For shortening the URLs I decided to simply get a hash of the url and use part of it (The first 8 hex chars should be fine). This makes it pretty simple to generate those short urls but means that I have to store the short_url -> url relation on a database. Thinking of ways to simply encode the long url into a shorter version in a way that can be decoded would reduce costs as it would remove the need for a database, but for the provided example the hash approach should be enough.

