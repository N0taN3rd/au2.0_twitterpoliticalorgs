import json

tweetFile = open('retweets.json', 'r')
retweets = json.load(tweetFile)
tweetFile.close()

f = open('counting.json', 'r')
data = json.load(f)
f.close()

trumpRetweets = retweets["trump"]
trumpTweetChange = []
last = 1
for idx, entry in enumerate(trumpRetweets):
	for listing in trumpRetweets:
		date = listing["date"]
		count = listing["retweets"]
	change = ((count - last)/last) * 100
	trumpTweetChange.append({"Date": date, "name": "Trump Retweets", "% change": change})
	last = count

clintonRetweets = retweets["clinton"]
clintonTweetChange = []
last = 1
for idx, entry in enumerate(clintonRetweets):
	for listing in clintonRetweets:
		date = listing["date"]
		count = listing["retweets"]
	change = ((count - last)/last) * 100
	clintonTweetChange.append({"Date": date, "name": "Clinton Retweets", "% change": change})
	last = count

with open('trumpRetweetChange.json', 'w') as outfile:
    json.dump(clintonTweetChange, outfile)

with open('clintonRetweetChange.json', 'w') as outfile2:
    json.dump(trumpTweetChange, outfile2)

trump = data["trumpy"]

clinton = data["hilary"]

trumpDonorChange = []
last = 1
for k, v in trump.items():
	count = v
	date = k
	change = ((count - last)/last) * 100
	newDate = date[:4] + '-' + date[4:6] + '-' + date[6:]
	trumpDonorChange.append({"Date": newDate, "name": "Trump Donors", "% change": change})
	last = count

clintonDonorChange = []
last = 1
for k, v in clinton.items():
	count = v
	date = k
	change = ((count - last)/last) * 100
	newDate = date[:4] + '-' + date[4:6] + '-' + date[6:]
	clintonDonorChange.append({"Date": newDate, "name": "Trump Donors", "% change": change})
	last = count





with open('trumpDonorChange.json', 'w') as outfile3:
    json.dump(trumpDonorChange, outfile3)

with open('clintonDonorChange.json', 'w') as outfile4:
    json.dump(clintonDonorChange, outfile4)