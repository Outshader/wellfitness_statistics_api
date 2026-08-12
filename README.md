Updated repo of https://github.com/Outshader/wellfitness_population_counter

This version uses the PerfectGym/Well Fitness API
  
## API usage overview
The API or the main hosting is provided by Perfect Gym. You may be able to infer something about the workings of specific endpoints from their official API documentation:
https://help.perfectgym.com/hc/en-001/sections/38985633521681-API

### Login
The Login endpoint:
https://wellfitness.perfectgym.pl/ClientPortal2/Auth/Login


#### Headers
By default works with these headers:
`"content-type": "application/json;charset=UTF-8", 
`"accept-language": "en-US,en;q=0.5",` 
`"accept": "application/json, text/plain, */*",` 
`"cp-lang": "en",` 
`"x-hash": "#/Login",` 
`"x-requested-with": "XMLHttpRequest"`
Although I believe it may also work with just the
`“content-type”: "application/json;charset=UTF-8"` 
header

#### Usage
The endpoint does not seem to provide a passwordless way to log in. Although it may be possible using the ClientID each user get.

Therefore to successfully log in, it requires a raw data body containing:
`"RememberMe": <“false” | “true”>, "Login": <email>, "Password": <password>`

It seems to be important (although technically might be dependent on the program making the request) that all the quotes contained in the password will be properly escaped, otherwise the API will return an Unhandled error message currently formatted as:
`{"Message":"Unhandled error occured, CorrelationId:UTC{2026-08-11_20-05}{rest of the ID}","CorrelationId:UTC{2026-08-11_20-05}{rest of the ID, as far as i know the same as previously

Entering a wrong password or login (email) will result in an error:
`{"Errors":[{"Message":"Login or password is incorrect.","Property":null,"Code":"","NestedBusinessErrors":[],"Data":null}]}`

You can adjust the “RememberMe” value to false or true formatted as a string not a bool. The former sets the     **"CpAuthToken"** to expire in around 8 hours, the latter in around 1 month and 1 hour.

The CpAuthToken will be required for every further action concerning the usage of the site’s or gym’s data.


### Classes
Endpoint:
https://wellfitness.perfectgym.com/ClientPortal2/Classes/ClassCalendar/WeeklyClasses
#### Headers
Only requires body. Only required argument is:
- “clubId”: {int}
Otherwise it returns null.

The other optional ones are:

**”daysInWeek”: {int}** - determines the range of the data pulled. The dates will be 
`current_date - value to current_date + value`

Meaning a passed value of 2 at the 10th will result in a range pulled from 8th and 12th. 

While it doesn’t seem to have a (unreasonable) upper limit, the bottom limit is 0 whence it returns an *Unhandled error occured*. If not given defaults to 7.

The maximum amount tested by me was 100,000, and it returned results from "1752-10-26" to the aforementioned "2300-05-26".

**“timeTableId”: {int}** - determines which class to pull. The specific values timeTableId are used to indentify specific classes and consistently appearing classes. The ID’s are determined globally, not locally per gym.

**“trainerId”: {int}** - determines which trainer’s classes to pull.


#### Usage


## Roadmap

* [x] JWT token stuff:
	- [x] refresh
	- [x] exit before trying with an outdated one/or just refresh during depends on how the refresh will work
	- [x] refresh failure handling
* [ ] statistics reliance improvement by accounting for classes via their site
* [x] dry runs
* [x] check if the user gave multiple same gyms
* [x] change password mail validation, if the response is bad THEN it prompts you or exits the program
* [x] change script.py to use classes
- [ ] QoL stuff:
	- [ ] Cleaner and consisten error handling
		- [ ] empty/bad responses
	- [ ] Cleaner code structure (more classes)
        - [x] club_requests.py cleaned
	- [ ] more dry run options