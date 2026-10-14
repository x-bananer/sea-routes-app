# TODO: 5.3 This file will contain a helper function for calculating
# how suitable the current weather is for the selected route.
#
# The function will:
# 1. Receive the current weather conditions and the route's
#    ratings_across_conditions from get_route.py.
# 2. Find weather groups that received high ratings from users.
# 3. Compare the current wind speed, wind direction, wave height,
#    water temperature, air temperature and cloud cover with these groups.
# 4. Calculate how closely the current weather matches the highly rated conditions.
# 5. Convert the similarity score into a suitability level:
#    Excellent, Good, Fair or Poor.
# 6. Return Not Enough Data if there are too few ratings for a reliable result.
# 7. Return the suitability level to get_route.py.
#
# (The exact weather comparison rules and minimum number of ratings
# still need to be defined.)

