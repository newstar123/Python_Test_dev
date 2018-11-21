#!/usr/bin/python

import mod_html
import sys
import os

sys.stderr = sys.stdout

def htmlGet(name, age, sex, method):
	print'''\
<!DOCTYPE html>
<html>
	 <head>
		<title>Hello {3}</title>
	</head>
	<body>
		<h1>Hello {0}</h1>
		<h2>You are: {1} years old</h2>
		<h3>You are a: {2}</h3>
	</body>
</html>
'''.format(name, age, sex, method)

def htmlPost(city, state, country, continent, method):
        print'''\
<!DOCTYPE html>
<html>
         <head>
                <title>Hello {4}</title>
        </head>
        <body>
                <h1>Hello {0}</h1>
                <h2>You are in the state of: {1}</h2>
                <h3>Inside the country of: {2}</h3>
		<h4>On the continent of: {3}</h4>
        </body>
</html>
'''.format(city, state, country, continent, method)


def main():
	print"Content-type: text/html\n";
	value = ""
	parsed = mod_html.parse()
#	print parsed.keys(), parsed.values()
#	for key, val in parsed.items():
#		print (key, val)
	if 'submitGet' in parsed:
		if 'name' in parsed:
			name = parsed['name']
	
		if 'age' in parsed:
			age = parsed['age']

		if 'sex' in parsed:
        	        sex = parsed['sex']
		htmlGet(name, age, sex, 'GET')

	if 'submitPost' in parsed:
                if 'city' in parsed:
                        city = parsed['city']

                if 'state' in parsed:
                        state = parsed['state']

                if 'country' in parsed:
                        country = parsed['country']

		if 'continent' in parsed:
                        continent = parsed['continent']
                htmlPost(city, state, country, continent, 'POST')


main()

