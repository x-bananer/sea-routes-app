# TODO: 5.3 Calculate the expected route rating based on current weather.
#
# The function will (suggested way of calculating suitability aka expected rating for current weather):
# 1. Get the current weather and ratings_across_conditions from get_route.py.
# 2. Take each group from ratings_across_conditions.
#    Each group contains average weather values, an average rating,
#    and the number of ratings.
# 3. Compare all six weather values of the group with the current weather.
#    Calculate the difference for each value.
# 4. Convert these differences into a similarity score from 0 to 1.
#    A score of 1 means the weather is identical.
#    A score of 0 means the weather is very different.
# 5. Calculate the weight of each group:
#    weight = similarity * total_ratings
# 6. Multiply each group's average_rating by its weight.
# 7. Add these results together and divide by the sum of all weights.
#    suitability = sum(average_rating * weight) / sum(weight)
# 8. Round suitability to one decimal place (1.0–5.0).
# 9. Return None if there are too few ratings or all weights are zero.
# 10. Return suitability to get_route.py.
#
# (We still need to define the allowed difference for each weather
# value and the minimum number of ratings.)