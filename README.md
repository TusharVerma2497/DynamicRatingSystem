# DynamicRatingSystem
Unlike the good old days when only a handful of movies were released and interested reviewers can view them all, nowadays, hundreds of movies are released in a week or so and due to this, reviewers rely heavily on the recommendation systems, which filter out movies that are not of their taste. This not only saves their time in today’s overburden lifestyle but also recommends them movies that they probably like. Unlike the current rating systems which are designed for one time review and not to update them later on, unless one is willing to do so, we have proposed a new rating system which will help users to update and interactively review their older ratings every time they have a new movie to rate and this will make their ratings much more scrupulous with their current predilection and by extension, ameliorate the overall performance of the existing recommendation systems.

#Install
This project is not yet competed entirely and surely will contain bugs however you can view the project running on django development server localy by following the the below commands

------------------>linux(arch based system)

1) Python should be pre installed in your machine.
	-> sudo pacman -S python3 python-pip
2) It would be better if you run it inside a virtual environment
	-> pip install virtualenv
3) Now go to root directory of the project and create the virtual environment
	-> virtualenv DynamicRS  //you can write any name here
	now activate it
	-> source DynamicRs/bin/activate
4) now install all the dependencies 
	-> pip install -r requirement.txt
5) Now install memcache in you system
	-> sudo pacman -S memcached
	-> systemctl start memcached
6) Make migrations for the sqlite3
	-> python manage.py migrate
7) Collect the static files 
	-> python manage.py collectstatic
8) Run the development server
	-> python manage.py runserver
	access it at localhost port 8000 
	

