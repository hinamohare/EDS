Abstract

	Implement client-side sharding for the expense management application 

Requirements

    1. Use user generated id as object for hashing
    2. Three Docker the expense management applicaiton instances - each application instance uses its own MySQL instance.
	   The application instances are running at 
	   a. http://192.168.99.100:3001
	   b. http://192.168.99.100:3002
	   c. http://192.168.99.100:3003
    3. Three Docker MySQL DB instances mounted to three different local paths so that each one will have different data set.
	   The database instances are running at
	   a. 192.168.99.100:3306
	   b. 192.168.99.100:3307
	   c. 192.168.99.100:3308

The client.py program takes the user input and hashes the id of the input data to obtain the target node url to post the data.
However, it is found that the distribution of the data is uneven for small number of sample inputs. The distribution is more even 
for large size of the inputs.

Input:	The sample input is
 				{
   					 "id" : "1",
  					 "name" : "Foo 1",
    					 "email" : "foo1@bar.com",
    					 "category" : "office supplies",
    					 "description" : "iPad for office use",
    					 "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
   					 "estimated_costs" : "700",
   					 "submit_date" : "12-10-2016"
				}

Output:

The sample data obtained after posting the user input with id ranging between 1-15 is shown bellow


*******************************node_1 GET**************************************

http://192.168.99.100:3001/v1/expenses/170
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo170@bar.com", 
      "estimated_costs": "700", 
      "id": 170, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 170", 
      "submit_date": "12-10-2016"
    }
  ]
}


*******************************node_2 GET**************************************

http://192.168.99.100:3002/v1/expenses/6
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo6@bar.com", 
      "estimated_costs": "700", 
      "id": 6, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 6", 
      "submit_date": "12-10-2016"
    }
  ]
}

http://192.168.99.100:3002/v1/expenses/9
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo9@bar.com", 
      "estimated_costs": "700", 
      "id": 9, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 9", 
      "submit_date": "12-10-2016"
    }
  ]
}

http://192.168.99.100:3002/v1/expenses/11
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo11@bar.com", 
      "estimated_costs": "700", 
      "id": 11, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 11", 
      "submit_date": "12-10-2016"
    }
  ]
}

*******************************node_3 GET**************************************
http://192.168.99.100:3003/v1/expenses/1
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo1@bar.com", 
      "estimated_costs": "700", 
      "id": 1, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 1", 
      "submit_date": "12-10-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/2
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo2@bar.com", 
      "estimated_costs": "700", 
      "id": 2, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 2", 
      "submit_date": "12-10-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/3
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo3@bar.com", 
      "estimated_costs": "700", 
      "id": 3, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 3", 
      "submit_date": "12-10-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/4
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo4@bar.com", 
      "estimated_costs": "700", 
      "id": 4, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 4", 
      "submit_date": "12-10-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/5
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo5@bar.com", 
      "estimated_costs": "700", 
      "id": 5, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 5", 
      "submit_date": "12-10-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/7
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo7@bar.com", 
      "estimated_costs": "700", 
      "id": 7, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 7", 
      "submit_date": "12-10-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/8
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo8@bar.com", 
      "estimated_costs": "700", 
      "id": 8, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 8", 
      "submit_date": "12-10-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/10
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo10@bar.com", 
      "estimated_costs": "700", 
      "id": 10, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 10", 
      "submit_date": "12-10-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/12
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo12@bar.com", 
      "estimated_costs": "700", 
      "id": 12, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 12", 
      "submit_date": "12-10-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/13
{
  "result": [
    {
      "category": "office", 
      "description": "ipad for office", 
      "email": "foo13@gmail.com", 
      "estimated_costs": "1500", 
      "id": 13, 
      "link": "apple.com", 
      "name": "foo 13", 
      "submit_date": "12-12-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/14
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo14@bar.com", 
      "estimated_costs": "700", 
      "id": 14, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 14", 
      "submit_date": "12-10-2016"
    }
  ]
}
http://192.168.99.100:3003/v1/expenses/15
{
  "result": [
    {
      "category": "office supplies", 
      "description": "iPad for office use", 
      "email": "foo15@bar.com", 
      "estimated_costs": "700", 
      "id": 15, 
      "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", 
      "name": "Foo 15", 
      "submit_date": "12-10-2016"
    }
  ]
}
