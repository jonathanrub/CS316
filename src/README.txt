To generate the production dataset download the following csv files from 
https://drive.google.com/open?id=0B9SFK-ccdI2La1FLSnJ0bzFyOXc
Then inside of PSQL run:
Copy HasAllergen from ‘/file/location/example/Hasallergen.csv’ delimiter ‘,’ HEADER; then for each of the CSV files transform them into the production dataset.

Copy Food FROM '/home/vagrant/shared/cs316/src/Food.csv' with CSV Header delimiter as ',';

