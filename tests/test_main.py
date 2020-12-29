import requests
import hashlib

test_no_args = requests.get('http://localhost:5000/mp3?v=https://www.youtube.com/watch?v=08kMdn8L7Yw&filename=If%20insects%20had%20to%20introduce%20themselves.mp3&title=&album=&artist=&album-art=', stream=True).content
test_all_args = requests.get('http://localhost:5000/mp3?v=https://www.youtube.com/watch?v=08kMdn8L7Yw&filename=If%20insects%20had%20to%20introduce%20themselves.mp3&title=test%20title%20for%20test%20video&album=album%20test%20setting!&artist=test%20artist&album-art=', stream=True).content
test_only_album = requests.get('http://localhost:5000/mp3?v=https://www.youtube.com/watch?v=08kMdn8L7Yw&filename=If%20insects%20had%20to%20introduce%20themselves.mp3&title=&album=album%20test%20setting!&artist=&album-art=', stream=True).content

hashed_test_no_args = hashlib.sha256(test_no_args)
hashed_test_all_args = hashlib.sha256(test_all_args)
hashed_only_album = hashlib.sha256(test_only_album)

print(hashed_test_no_args.hexdigest() == '7947c0f35877611cd7279c5ee51387044e2938f937e59267b38831637224e98c')
print(hashed_test_all_args.hexdigest() == '4b43bb8f246c9e71531a9b13b44674fe52f3c15d7f550bcd7be01cd9164f0044')
print(hashed_only_album.hexdigest() == '3fc4f00ee3190a374ded97cec9dda2051d9abfb548ea05c9782adea0b6300895')