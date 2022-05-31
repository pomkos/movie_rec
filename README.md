# Background

A movie recommendation engine using the Steamlit library for webgui. Recommendations are based off of a score calcuated as:
1. `var1` = Users who liked (rated >= 4 stars) the `given movie` (the movie that was searched for)
2. `var1_recs` = The other movies in our database that these users also liked
3. `perc1_recs` = Percent of `var1` users that liked each of the recommendations, threshold of at least 10%
4. `var2` = Users who liked each of the `var1_recs`
5. `perc2_recs` = Percent of `var2` users that liked each of the recommendations, no threshold
6. `score` = `perc1_recs/perc2_recs`, or the share that `var1` users make up of all the users that liked each movie

## Example

<img src="https://github.com/pomkos/movie_rec/raw/main/images/example_screenshot.png" width="620">

Searching for `toy story` will give back `Wreck-It Ralph (2012)` as the top recommendation, with an average user rating of 3.7 stars and a score of 5.07. The score says that 5x as many users liked `Wreck-It Ralph` if they also liked `Toy Story 3`.

A higher score should be more likely to reflect the unique likes of users who also liked the `given movie`
