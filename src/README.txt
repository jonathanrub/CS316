To generate the production dataset download the following csv files from 
https://drive.google.com/open?id=0B9SFK-ccdI2La1FLSnJ0bzFyOXc

create a user name and password in psql and update the config.py accordingly


Then inside of PSQL run:
Copy HasAllergen from ‘/file/location/example/Hasallergen.csv’ delimiter ‘,’ HEADER; then for each of the CSV files transform them into the production dataset.


dukedining=# Copy Food FROM '/home/vagrant/shared/cs316/src/Food.csv' with CSV Header delimiter as ',';
COPY 317
dukedining=# Copy Allergens FROM '/home/vagrant/shared/cs316/src/Allergens.csv' with CSV Header delimiter as ',';
COPY 9
dukedining=# Copy HasAllergen FROM '/home/vagrant/shared/cs316/src/Has_allergen.csv' with CSV Header delimiter as ',';
COPY 345
dukedining=# Copy Restaurant FROM '/home/vagrant/shared/cs316/src/Restaurant.csv' with CSV Header delimiter as ',';
COPY 35
dukedining=# Copy IsOpen FROM '/home/vagrant/shared/cs316/src/IsOpen.csv' with CSV Header delimiter as ',';
COPY 218
dukedining=# Copy Serves FROM '/home/vagrant/shared/cs316/src/Serves.csv' with CSV Header delimiter as ',';
COPY 317

then run app.py
