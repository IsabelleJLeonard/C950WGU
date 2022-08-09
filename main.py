# Data Structure and Algorithm II C950 WGU
# Isabelle Matthews
# imatt12@wgu.edu

import csv
import datetime
from HashTable import HashTable


class Package:
    def __init__(self, idNumber, add, city, state, zipcode, dt, weight, special):
        self.idNumber = idNumber
        self.add = add
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.dt = dt
        self.weight = weight
        self.special = special
        self.status = None
        self.deliveryTime = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.idNumber, self.add, self.city, self.state, self.zipcode, self.dt, self.weight, self.special,
            self.status)

    def updateStatus(self, timeObject):
        if timeObject < self.departureTime:
            self.status = "at hub"

        elif timeObject < self.deliveryTime:
            self.status = "en route"

        else:
            self.status = "Delivered at %s" % self.deliveryTime


# Load the package data from CSV into hash table.
def loadPackageData(fileName):
    with open(fileName) as packageFile:
        packageData = csv.reader(packageFile, delimiter=',')
        for package in packageData:
            pID = int(package[0])
            pAdd = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDt = package[5]
            pWeight = package[6]
            if len(package) == 8:
                pSpecial = package[7]
            else:
                pSpecial = ""

            if pID == 9:
                if datetime.timedelta(hours=10, minutes=20, seconds=00):
                    pAdd = "410 S State St"
                    pCity = "Salt Lake City"
                    pZipcode = "84111"

            # movie object
            p = Package(pID, pAdd, pCity, pState, pZipcode, pDt, pWeight, pSpecial)
            # print(p)

            # insert it into the hash table
            myHash.insert(pID, p)


# Hash table instance
myHash = HashTable()

# Load movies to Hash Table
loadPackageData('Package File.csv')


# Get all Distance data from CSV file into hash table
def loadDistanceData(fileName):
    with open(fileName) as distanceFile:
        distances = csv.reader(distanceFile, delimiter=',')
        for distance in distances:
            distanceData.append(distance)


distanceData = []
# Loading distance file
loadDistanceData('DistanceData.csv')


# print(distanceData)


def loadAddressData(fileName):
    with open(fileName) as addressFile:
        addresses = csv.reader(addressFile, delimiter=',')
        for address in addresses:
            addressData.append(address[1][1:])


addressData = []
# Loading address file
loadAddressData('addressData')


# print(addressData)


# Get address from address data file.
def getAddress():
    return addressData


class Truck:
    def __init__(self, truckID, capacity, speed, startTime, packages):
        self.capacity = capacity
        self.speed = speed
        self.startTime = startTime
        self.packages = packages
        self.truckID = truckID

    # Get distance number from csv in both sides.
    def getDistance(dis1, dis2, total):
        distance = distanceData[dis1][dis2]
        if distance == '':
            distance = distanceData[dis2][dis1]
        return total + float(distance)

    def remove(self, packageID):
        if packageID in self.packages:
            self.packages.remove(packageID)
        else:
            print(packageID, "package not found in list")


# Get distance between address 1 to address 2, using nearest neighbor algorithm.
def distanceInBetween(address1, address2):
    if distanceData[addressData.index(address1)][addressData.index(address2)] == "":
        return float(distanceData[addressData.index(address2)][addressData.index(address1)])
    return float(distanceData[addressData.index(address1)][addressData.index(address2)])


address1 = addressData[6]
address2 = addressData[25]


# print(distanceInBetween(address1, address2))


# Use nearest neighbor Algorithm for min distance by picking up the nearest distance to go next with truck
def minDistanceFromAddress(addy, packageList):
    minn = 1000
    minPackage = None

    for idNumber in packageList:
        packages = myHash.search(idNumber)  # current package
        # currentDistance: float = distanceInBetween(add1, add2)
        currentDistance: float = distanceInBetween(addy,
                                                   packages.add)  # find distance between current package to address.

        if currentDistance < minn:
            minn = currentDistance
            minPackage = packages

    return minn, minPackage.idNumber


# print(minDistanceFromAddress(address, packageList))

def deliveringPackage(truck):
    addy = "4001 S 700 E"
    miles = 0
    p = 0
    truckTime = truck.startTime  # departure time

    while len(truck.packages) != 0:
        minn, packageID = minDistanceFromAddress(addy, truck.packages)
        miles += minn
        clock = (minn / 18) * 60 * 60
        truckTime += datetime.timedelta(seconds=clock)
        pack = myHash.search(packageID)
        pack.status = f"The package Delivered at: {truck.startTime}"
        truck.remove(packageID)
        addy = pack.add
        pack.departureTime = truck.startTime
        pack.deliveryTime = truckTime

        # print(truck.truckID, packageID)
    return miles, truckTime


truck1 = Truck(1, 16, 18, datetime.timedelta(hours=8, minutes=0, seconds=0),
               [1, 13, 14, 15, 16, 19, 20, 7, 29, 8, 30, 31, 34, 4, 40, 11])  # 16 FULL
truck2 = Truck(2, 16, 18, datetime.timedelta(hours=9, minutes=5, seconds=0),
               [3, 6, 18, 28, 32, 36, 37, 38, 2, 10, 12, 17, 21, 22, 23, 39])  # 16 FULL
truck3 = Truck(3, 16, 18, datetime.timedelta(hours=10, minutes=20, seconds=0),
               [5, 9, 27, 33, 25, 26, 35, 24])

truck1Miles, truck1FinishTime = deliveringPackage(truck1)

truck2Miles, truck2FinishTime = deliveringPackage(truck2)

truck3.startTime < truck1FinishTime
truck3Miles, truck3FinishTime = deliveringPackage(truck3)

totalMiles = truck1Miles + truck2Miles + truck3Miles


# print(truck1Miles, truck2Miles, truck3Miles, totalMiles)
# print(deliveringPackage(truck1))
# print("finished")


# user interface codes beginning
class Main:
    while True:
        print('WGUPS Package Information System')
        print("1. All Package Status")
        print("2. Total mileage")
        print("3. Status of all Package at a time")
        print("4. One package Status")
        print("5. Exit the Program")
        user = input('What option would you like to go with [1-5]? ')

        if user == "1":
            for i in range(len(myHash.table) + 1):
                print("Package: {}".format(myHash.search(i + 1)))

        elif user == "2":
            print(f'WGUPS routes have been completed within {totalMiles} miles')

        elif user == "3":
            checkTime = input("Please enter a time in the form HH:MM:SS")
            hour, minute, second = checkTime.split(":")
            timeObject = datetime.timedelta(hours=int(hour), minutes=int(minute), seconds=int(second))
            print("Package Status")
            for p in range(1, 41):
                pack = myHash.search(p)
                pack.updateStatus(timeObject)
                print(pack)

        elif user == "4":
            packageID = input("Enter Package ID:")
            pack = myHash.search(p)
            print(pack)

        elif user == "5":
            user = False
