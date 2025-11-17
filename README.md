# CUFoodie
Check restaurants, dishes, reviews and food trails near Columbia University, New York. This is a full-stack project involving a React frontend, Flask service layer and PostgreSQL backend. The backend server, running in a Google Cloud VM, is pre-populated with realistic data.


## Demo:
https://www.loom.com/share/4ed548cb308f45f0bb03dfe17d8a17e8

We shall be switching off the backend server as we are almost out of credits unfortunately. The above link points to a recording of the project.

## Web Application URL (will not work since backend is off):
http://34.148.46.88:8111

## Part 1 features implemented
We implemented everything that we proposed in the part 1 of our project proposal as follows:


#### A. Query for a restaurant/browse all:

The user of the DB can search for a particular restaurant. They will find all the details
such as items, their prices, user of the DB reviews, location, etc.

*Returns the details about the restaurant.*

If the user of the DB does not filter by the restaurant ID, they will be able to see details
of the all the restaurants in the DB.

*Returns list of all restaurants.*

This is implemented in the Restaurants page. Users can see all restaurants when no filters are applied or search for a specific restaurant by name. Clicking on a restaurant’s “View Menu” link opens the Restaurant Detail page, where users can see the restaurant’s menu, location, cuisine, reviews, and average rating.

#### B. Query for restaurants in a locality:
User of the DB might want to search for restaurants nearby, check their reviews and
decide. In such a case, they will filter by the neighborhood of restaurants.

*Returns list of al food joints located in the given locality.*

Also in the Restaurants page, users can enter a neighborhood or location in the filter field. The app then shows only restaurants located in that area, allowing users to explore nearby dining options.


#### C. Find restaurants above a certain rating:
A user of the DB can choose to browse only restaurants above an average of let us say
4.0/5.0 rating.

*Returns list of restaurants above/below a rating.*

In the Restaurants page, there is a “Min Rating” filter. Users can type in a rating value, and only restaurants with an average rating above that value are shown.

#### D. Query for cuisine:
We can filter out restaurants based on the classified cuisine.

*Returns restaurants pertaining to the cuisine.*

The Restaurants page has a cuisine filter where users can enter a type of cuisine, such as Italian or Chinese. Only restaurants offering that cuisine are displayed.

#### E. Query a dish:
The user of the DB can filter out a certain dish and check which restaurant(s) prepare it.

*Returns list of restaurants offering the food item.*

The Dishes page lets users search for a specific dish by name. The app shows all restaurants serving that dish along with its price and dietary tags.

#### F. Find dishes below/above a price:
A user of the DB might want to check which dishes are available within the user of the
DB’s budget and details of restaurants offering those items.

*Returns list of dishes, mapped to list of restaurants offering them.*

This is implemented in both the Dishes page and the Budget Picks page. On the Dishes page, users can filter by “Max Price” to see dishes below a certain amount. The Budget Picks page specifically highlights dishes under a user-specified budget.

#### G. Query for late night trails:
A user of the DB might crave for a late-night snack. In such a case, they can browse
through the table of food trails depending on the type such as breakfast/dinner/late-
night snacks, etc.

*Returns list of recommended restaurants and dishes depending on the type selected.* 

The Trails page allows users to filter trails by type. For example, selecting “Late Night” shows curated trails for late-night snacks, listing restaurants and dishes included in those trails.

#### H. Check reviews of a user of the DB:
Given a username or ID, we can check all the reviews given by that person.

In the Profile page, users can view all reviews they have submitted. The page displays the number of reviews and details about each. Optionally, the Reviews page can be used to show recent reviews or filter them by the logged-in user.

#### I. Check all dishes with a dietary restriction:
If the user of the DB wants to check dishes that are vegan, let’s say.

The Dishes page allows users to enter a dietary tag, such as vegan or gluten-free. The app then lists all dishes matching that dietary restriction, along with the restaurants serving them.

## Interesting web pages of the application

### Restaurant browser page
This page contains filters and lets the user choose restaurants at their will, be it based on name, cuisine, locality or even an average rating.

The page will change dynamically as the user changes the filters. Initially, it will show all the restaurants, and then it gets smaller as the filters are applied. On the backend, it involves complicated joins with clauses to select only a handful of restaurants satisfying the predicate(s). The most interesting of these is the one with the average rating. This lets users decide on good restaurants. The join involves tables of restaurants, dishes and reviews. After applying the filters, it will give all the details, including the restaurant's name, locality, cuisine and average review.

### Food Trails Explorer
The page about food trails contains interesting details about different kinds of food trips, such as midnight snacks, etc. The output is a list containing the restaurant details, dish and its price. This operation also uses multiple joins on the server-side, combining details from the menu, dish, restaurant, and trail tables based on the trail name selected. The part about trails is a unique aspect of this project, as it gives users the ability to find curated lists based on the inputs of previous users.
