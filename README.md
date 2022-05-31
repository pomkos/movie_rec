# Background

A movie recommendation engine using the Steamlit library for webgui. Recommendations are based off of a score calcuated as:
1. var1 = Users who liked (rated >= 4 stars) the given movie also liked these movies
2. var2 = Users who did not like (rated < 4 stars) the given movie
