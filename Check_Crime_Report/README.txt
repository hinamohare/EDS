RPC LAB ASSIGNMENT

Input (HttpRpc)

    lat - latitude of a location
    lon - longitude of a location
    radius - radius distance in miles.

curl "http://localhost:8000/checkcrime?lat=37.334164&lon=-121.884301&radius=0.02"

Expected Output Format

					
{
   "event_time_count":{
	  "3:01am-6am":1,
	  "12:01pm-3pm":2,
	  "6:01pm-9pm":0,
	  "3:01pm-6pm":4,
	  "9:01am-12noon":2,
	  "9:01pm-12midnight":41,
	  "6:01am-9am":0,
	  "12:01am-3am":0
   },
   "crime_type_count":{
	  "Vandalism":1,
	  "Arrest":6,
	  "Assault":2,
	  "Other":36,
	  "Theft":4,
	  "Burglary":1
   },
   "total_crime":50,
   "the_most_dangerous_streets":[
	  "E SANTA CLARA ST",
	  "E WILLIAM ST",
	  "S 1ST ST"
   ]
}




Dependency
CrimeReport API

# Example Crime Report near SJSU
curl -i "https://api.spotcrime.com/crimes.json?lat=37.334164&lon=-121.884301&radius=0.02&key=."