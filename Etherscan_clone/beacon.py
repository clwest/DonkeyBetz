from web3.beacon import Beacon
beacon = Beacon("http://localhost:5051")


test = beacon.get_genesis()
print(test)