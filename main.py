import numpy as np
from geopy import Point
from geopy import distance
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans



class Geocode:
    def __init__(self):
        self.NO_OF_BASKET = 30
        self.NO_OF_POINT = 600
        self.RAD = 0.01
        self.POINTS = []
        self.CENTER_POINT = "Maslak, Istanbul"
        self.geolocator = Nominatim(user_agent="my_application")
   
    def create_point(self):
        location = self.geolocator.geocode(self.CENTER_POINT)
        center = Point(latitude=location.latitude, longitude=location.longitude)
        for i in range(self.NO_OF_POINT):
            latitude = np.random.uniform(
                center.latitude - self.RAD, center.latitude + self.RAD)
            longitude = np.random.uniform(
                center.longitude - self.RAD, center.longitude + self.RAD)
            self.POINTS.append((latitude, longitude))
        print(f"{len(self.POINTS)} random points generated")
        self.point_clustering()

    def point_clustering(self):

        kmeans = KMeans(n_clusters=self.NO_OF_BASKET, init='random', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(self.POINTS)
        self.BASKETS = [[] for x in range(self.NO_OF_BASKET)]
        for i, point in enumerate(self.POINTS):
            idx = kmeans.predict([list(point)])[0]
            new_basket = self.BASKETS[idx]

            if new_basket:
                for p in new_basket:
                    if distance.distance(point, p).meters <= 1000:
                        new_basket.append(point)
                        break
                    else:
                        self.BASKETS.append([point])
            else:
                new_basket.append(point)

        self.create_file()
        
    def create_file(self):
        with open("results.txt", "w", encoding="utf-8") as file:
            for i, basket in enumerate(self.BASKETS):
                print(f"BASKET_NUM#{i+1}")
                file.write(f"BASKET_NUM#{i+1}")
                for j, location in enumerate(basket):
                    try:
                        address = self.geolocator.reverse(f"{location[0]}, {location[1]}")
                    except:
                        address = ""
                        print(f"Address could not find for this location {location[0]}, {location[1]}")
                    link = f"https://www.google.com/maps/search/?api=1&query={location[0]},{location[1]}"
                    file.write(f"\n item#{j+1} {location[0],location[1]}, {address}, {link} \n")
        print("File created successfully.")
        

if __name__ == "__main__":
    
    geocode_finder = Geocode()
    geocode_finder.create_point()