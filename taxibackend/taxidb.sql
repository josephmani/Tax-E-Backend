drop table if exists TripHistory;
drop table if exists CurrentTrip;
drop table if exists Rider;
drop table if exists Driver;
drop table if exists Signin_up;


create table Signin_up(
	phoneno text primary key,
	pwd text NOT NULL,
	type text NOT NULL
);

create table Driver(
	did serial primary key,
	name text NOT NULL,
	aadharid text NOT NULL,
	email text NOT NULL,
	Dphoneno text REFERENCES Signin_up(phoneno),
	licenseno text NOT NULL,
	vehicleno text NOT NULL,
	vehicletype text NOT NULL
);
	
create table Rider(
	rid serial primary key,
	name text not null,
	email text not null,
	Rphoneno text REFERENCES Signin_up(phoneno)
);	

create table CurrentTrip(
	tripid serial primary key,
	from_add text not null,
	to_add text not null,
	time text not null,
	shared BOOLEAN not null,
	vehicletype text not null,
	amount text not null,
	otp text not null,
	bookingstatus text,
	tripstatus text,
	Dphoneno text REFERENCES Signin_up(phoneno) DEFAULT NULL,
	Rphoneno text REFERENCES Signin_up(phoneno)
);	

create table TripHistory(
	tripid text primary key,
	from_add text not null,
	to_add text not null,
	time text not null,
	shared BOOLEAN not null,
	vehicletype text not null,
	amount text not null,
	tripstatus text,
	Rphoneno text REFERENCES Signin_up(phoneno),
	Dphoneno text REFERENCES Signin_up(phoneno)
);

ALTER TABLE ONLY CurrentTrip ALTER COLUMN bookingstatus SET DEFAULT 'Pending';
ALTER TABLE ONLY CurrentTrip ALTER COLUMN tripstatus SET DEFAULT 'Pending';
ALTER TABLE ONLY TripHistory ALTER COLUMN tripstatus SET DEFAULT 'Pending';	
