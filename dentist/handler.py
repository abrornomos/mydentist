from geopy.distance import distance


def sort_by_distance(dentists, location):
    if len(dentists) < 2:
        return dentists
    else:
        middle = dentists[0]
        less = [
            dentist for dentist in dentists[1:]
            if distance((dentist['latitude'], dentist['longitude']), location).kilometers <= distance((middle['latitude'], middle['longitude']), location).kilometers
        ]
        greater = [
            dentist for dentist in dentists[1:]
            if distance((dentist['latitude'], dentist['longitude']), location).kilometers <= distance((middle['latitude'], middle['longitude']), location).kilometers
        ]
        return sort_by_distance(less, location) + [middle] + sort_by_distance(greater, location)
