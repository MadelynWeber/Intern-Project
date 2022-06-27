# Intern-Project

## This repository holds our combined notes and code files for building a proof of concept for our project
* Our project's goal is to create a means of gathering reviews from various contractors across the internet, analyzing the language used within each reveiw, and re-calculating the given star rating to better match that from the language used within the review's text, to give the customer a more reliable and accurate star rating of a given contractor's service.
* This is done because most people select the services they wish to pay for based on an average star-to-number-of-reviews ratio (ie. the higher the star rating and the larger the number of reviewrs there are, the more likely a customer is to pay for that service based on the reviews they are seeing)
* The problem with this is that there are a number of fake reviews out there -- so a 3-star service may be advertised as a 5-star service based on these false reviews. There is also a problem with user error -- where someone may type out a 2-star review, but accidentally click on 3 or 4-stars instead. Finally, there is the aspect of differing oppinions -- what one person may see as a 3-star service may be seen as a 4-star service in the eyes of someone else.
* Through automation, we can adjust reviews to give an adjusted star rating which may be more accurate.
* This is done by employing web scraping for gathering data, and employing a sentiment analysis model to learn how different star ratings are described in text, and adjusting the star ratings given to new reviews base on the linguistic patterns learned by the model.
