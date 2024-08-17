CREATE DATABASE Red_Bus;

USE Red_Bus;
Drop table bus_routes;
CREATE TABLE bus_routes (
id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
route_name varchar(200) NOT NULL,
route_link varchar(500) NOT NULL,
busname varchar(200) NOT NULL,
bustype varchar(200) NOT NULL,
departing_time TIME NOT NULL,
duration varchar(20) NOT NULL,
reaching_time TIME NOT NULL,
star_rating FLOAT(5) NOT NULL,
price DECIMAL(10,2) NOT NULL,
seats_available INTEGER NOT NULL
);

INSERT INTO bus_routes (route_name,route_link,busname,bustype,departing_time,duration,reaching_time,
star_rating,price,seats_available)
VALUES 
('Bangalore to Kozhikode','/bus-tickets/bangalore-to-kozhikode','MMK Travels','VE A/C Seater / Sleeper (2+1)','22:30',
'09h 00m','07:30',4.4,999.00,23);

Select * From bus_routes where route_name = 'Kolkata to Digha' and BusName in ('Sagufta Travels(Maa Chandi)','Maa Chandi Travels'); 
Select * From bus_routes where route_name = 'Kolkata to Digha' and Price between 0 and 500; 
Select * From bus_routes where route_name = 'Kolkata to Digha' and star_rating >='4.0'; 
Select * From bus_routes where route_name = 'Kolkata to Digha' and seats_available >=4; 

select Distinct Departing_time from bus_routes;

select Busname 'Travels', Bustype 'Type', Departing_time 'Departure', Duration, Reaching_time 'Arrival',Star_Rating 'Rating', Price 'Fare', Seats_Available'Remaining Seats' from bus_routes where route_name='Kolkata to Mandarmani' and Price between 0 and 1500

Select Busname 'Travels', Bustype 'Type', Departing_time 'Departure', Duration, Reaching_time 'Arrival',
Star_Rating 'Rating', Price 'Fare', Seats_Available'Remaining Seats'  From bus_routes; 

Select distinct route_name From bus_routes;
Select distinct busname From bus_routes;
Select distinct bustype From bus_routes;
Select distinct star_rating From bus_routes;
Select CEIL(MIN(price)/100)*100 From bus_routes;
Select distinct price From bus_routes order by price;
Select Max(convert(price,unsigned)) as converted_price From bus_routes order by converted_price;
Select CEIL(MIN(convert(price,unsigned))/100)*100  as price From bus_routes;
Select CEIL(MAX(convert(price,unsigned))/100)*100  as price From bus_routes;