import psycopg2
import urllib.parse as up

from flask import Flask,request
from flask import jsonify
from flask_cors import CORS,cross_origin
from datetime import date
from datetime import datetime

import os
from os.path import join, dirname
from dotenv import load_dotenv

import random
import hashlib

dotenv_path = join(os.path.dirname(os.path.realpath(__file__)), '.env')
load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get("DATABASE_URL")

up.uses_netloc.append("postgres")
url = up.urlparse(DATABASE_URL)
dbconn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)



def create_app():
#create_app is a keyword.
	app= Flask(__name__)
	#CORS(app)
	app.config.from_mapping(
		DATABASE= "pimdb"
	)

#########################################################################################################################
		
	@app.route("/")
	#@cross_origin()
	def index():
		response = jsonify(message="The Server is running")
		return response
		
#########################################################################################################################		
		
	@app.route("/signin")
	#@cross_origin())
	def signinpage():
		cursor = dbconn.cursor()		
		#phoneno= request.json['phoneno']
		#password= request.json['pwd']
	
		phoneno= '7338995416'
		password= 'gops123'
		
		#password encryption:
		password=hashlib.sha256(password.encode('utf-8')).hexdigest() #hashvalue
		
		cursor.execute("SELECT phoneno,pwd from Signin_up where phoneno=%s",(phoneno,))
		temp= cursor.fetchone()
		if temp:
			phone,passcode=temp
			if passcode==password:
				return jsonify({"phoneno":phone,"pwd":passcode})
			else:
				return jsonify(message="Incorrect password")
		else:
			return jsonify(message="Complete the registration")

#########################################################################################################################

	@app.route("/signup")
	def registration():
		cursor = dbconn.cursor()
		#phoneno= request.json['phoneno']
		#password= request.json['pwd']
		#typess= request.json['type']
		
		phoneno= '7338995416'
		password= 'gops123'
		typess= 'rider'
		
		
		#password encryption:
		password=hashlib.sha256(password.encode('utf-8')).hexdigest() #hashvalue
		
		if typess=='rider':
			#names= request.json['name']
			#emails= request.json['email']
			
			names= 'gopu chad'
			emails= 'gopu.reddy@gmail.com'
		
			
			cursor.execute("INSERT INTO Signin_up (phoneno, pwd, type) VALUES(%s, %s, %s)",(phoneno, password, typess))
			dbconn.commit()
			
			cursor = dbconn.cursor()
			cursor.execute("INSERT INTO Rider (name, email, Rphoneno) VALUES(%s, %s, %s)",(names, emails, phoneno))
			dbconn.commit()
			
			cursor.execute("SELECT MAX(rid) from Rider")
			userid= cursor.fetchall()[0][0]
			dbconn.commit()
		
			return jsonify({"rid":userid,"name":names,"email":emails,"type":typess})
		
		elif typess=='driver':
			#names= request.json['name']
			#emails= request.json['email']
			#aadharids= request.json['aadharid']
			#lnos= request.json['licenseno']
			#vnos= request.json['vehicleno']
			#vtypess= request.json['vehicletype']
			
			names= 'joel'
			emails= 'joel.dubai@gmail.com'
			aadharids= '4444'
			lnos= '98777'
			vnos= 'D123456'
			vtypess= 'auto'
		
			
			cursor.execute("INSERT INTO Signin_up (phoneno, pwd, type) VALUES(%s, %s, %s)",(phoneno, password, typess))
			dbconn.commit()
			
			cursor = dbconn.cursor()
			cursor.execute("INSERT INTO Driver (name, aadharid, email, Dphoneno, licenseno, vehicleno, vehicletype) VALUES(%s, %s, %s, %s, %s, %s, %s)",(names, aadharids, emails, phoneno, lnos, vnos, vtypess))
			dbconn.commit()
			
			cursor.execute("SELECT MAX(did) from Driver")
			userid= cursor.fetchall()[0][0]
			dbconn.commit()
		
			return jsonify({"did":userid,"name":names,"aadharid":aadharids, "email":emails, "Dphoneno":phoneno, "licenseno":lnos, "vehicleno":vnos,"vehicletype":vtypess,"type":typess})
		
	
	
########################################  RIDER  ###############################################	
	
	@app.route("/book-ride")
	def ridebooking():
		cursor = dbconn.cursor()
		#phoneno= request.json['phoneno']
		#froma= request.json['from_add']
		#toa= request.json['to_add']
		#times= request.json['time']
		#shareds= request.json['shared']
		#vtypess= request.json['vehicletype']
		#amounts= request.json['amount']
		
		phoneno= '7338995417'
		froma= 'zzz'
		toa= 'ccc'
		times='2021-09-25T23:35'
		shareds= 'T'
		vtypess= 'auto'
		amounts= 400
		
		#2018-06-07T00:00
		#share ride verification
	
		
		now = datetime.now()
		yr=times[2:4]
		month=times[5:7]
		day=times[8:10]
		hr=times[11:13]
		minute=times[14:]
		reqstr=day+'/'+month+'/'+yr+' '+hr+':'+minute+':00'

		date_time_obj = datetime.strptime(reqstr, '%d/%m/%y %H:%M:%S')

		diff=date_time_obj-now

		if shareds=='T':
			if diff.total_seconds() < 1200: #20mins
				 shareds= 'F'
			else:
				 shareds='T'

		
		otps = random.randint(1000,9999)
				
		cursor.execute("INSERT INTO CurrentTrip (from_add, to_add, time, shared, vehicletype, amount, otp, Rphoneno) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(froma, toa, reqstr, shareds, vtypess, amounts, otps, phoneno))
		dbconn.commit()
		
		cursor= dbconn.cursor()
		cursor.execute("SELECT MAX(tripid) from CurrentTrip where Rphoneno=%s",(phoneno,))
		tripids= str(cursor.fetchall()[0][0])
		dbconn.commit()
		
		cursor= dbconn.cursor()
		cursor.execute("INSERT INTO TripHistory (tripid, from_add, to_add, time, shared, vehicletype, amount, Rphoneno) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(tripids, froma, toa, reqstr, shareds, vtypess, amounts, phoneno))
		dbconn.commit()
		
		
		return jsonify({"tripids":tripids, "from_add":froma, "to_add":toa, "time": reqstr, "shared":shareds, "vehicletype":vtypess, "amount":amounts, "otp":otps, "phone":phoneno})
	

#########################################################################################################################
	
	@app.route("/cancel-ride")
	def CancelRide():
		cursor = dbconn.cursor()
		#tripids=request.json['tripid']
		tripids='8' 
		cursor.execute("DELETE from CurrentTrip where tripid=%s",(tripids,))
		dbconn.commit()
		
		cursor= dbconn.cursor()
		cursor.execute("SELECT from_add,to_add,tripid from TripHistory where tripid=%s",(tripids,))
		dbconn.commit()

		temp= cursor.fetchone()
		froma,toa,tripids=temp
		
		cursor = dbconn.cursor()
		tripstatuss="Cancelled"
		cursor.execute("UPDATE TripHistory SET tripstatus=%s where tripid=%s",(tripstatuss,tripids))
		dbconn.commit()
		return jsonify({"tripid":tripids, "from_add":froma, "to_add":toa, "tripstatus": tripstatuss})

#########################################################################################################################
		
	@app.route("/get-history-customer")
	def customerhistory():
		cursor = dbconn.cursor()
		
		#phonenos=request.json['phoneno']
		phonenos='7338995416'
		cursor.execute("SELECT * from TripHistory where Rphoneno=%s ORDER BY tripid",(phonenos,))
		temp= cursor.fetchall()
		result=[]
		if temp:
			for tripids,froma,toa,times,shareds,vtypess,amounts,tripstatuss,Rphones,Dphones in temp:
				dicts={"tripid":tripids, "from_add":froma, "to_add":toa, "shared":shareds, "vehicletype":vtypess,"amount":amounts,"tripstatus":tripstatuss,"Rphoneno":Rphones,"Dphoneno":Dphones}
				result.append(dicts)
			
			return jsonify(result)
		else:
			return jsonify(message="You have no rides yet.")	

		
#########################################################################################################################		
				
	@app.route("/get-scheduled-rides")
	def schedulingrides():
		cursor = dbconn.cursor()
		
		#phonenos=request.json['phoneno']
		phonenos='7338995417'
		cursor.execute("SELECT tripid,from_add,to_add,time,shared,vehicletype,amount,otp,bookingstatus,Dphoneno from CurrentTrip where Rphoneno=%s",(phonenos,))
		temp= cursor.fetchall()
		result=[]
		if temp:
			for tripids,froma,toa,times,shareds,vtypess,amounts,otps,bookingstats,Dphones in temp:
				dicts={"tripid":tripids, "from_add":froma, "to_add":toa, "shared":shareds, "vehicletype":vtypess,"amount":amounts,"otp":otps,"bookingstatus":bookingstats,"Dphoneno":Dphones}
				result.append(dicts)
			
			return jsonify(result)
		else:
			return jsonify(message="You have no scheduled rides.")	
#########################################################################################################################
				
	@app.route("/get-profile-customer")
	def customerprofile():
		cursor = dbconn.cursor()
		
		#phonenos=request.json['phoneno']
		phonenos='7338995417'
		cursor.execute("SELECT name,email,Rphoneno from Rider where Rphoneno=%s",(phonenos,))
		temp= cursor.fetchone()
		names,emails,Rphones=temp
		return jsonify({"name":names,"email":emails, "Rphoneno":Rphones})
						
##################################################   DRIVER    #####################################################
	
	
	@app.route("/get-history-driver")
	def driverhistory():
		cursor = dbconn.cursor()
		
		#phonenos=request.json['phoneno']
		phonenos='7338995418'
		cursor.execute("SELECT * from TripHistory where Dphoneno=%s",(phonenos,))
		temp= cursor.fetchall()
		result=[]
		if temp:
			for tripids,froma,toa,times,shareds,vtypess,amounts,tripstatuss,Rphones,Dphones in temp:
				dicts={"tripid":tripids, "from_add":froma, "to_add":toa, "shared":shareds, "vehicletype":vtypess,"amount":amounts,"tripstatus":tripstatuss,"Rphoneno":Rphones,"Dphoneno":Dphones}
				result.append(dicts)
			
			return jsonify(result)
		else:
			return jsonify(message="You have no rides yet.")	

#########################################################################################################################
				
	@app.route("/get-profile-driver")
	def driverprofile():
		cursor = dbconn.cursor()
		
		#phonenos=request.json['phoneno']
		phonenos='7338995418'
	
		cursor.execute("SELECT name, aadharid, email, Dphoneno, licenseno, vehicleno, vehicletype from Driver where Dphoneno=%s",(phonenos,))
		dbconn.commit()
		
		temp= cursor.fetchone()
		names,aadharids,emails,Dphones,lnos,vnos,vtypess=temp
		return jsonify({"name":names,"aadharid": aadharids, "email":emails, "Dphoneno":Dphones,"licenseno":lnos,"vehicleno":vnos,"vehicletype":vtypess})

#########################################################################################################################

	@app.route("/get-available-rides")
	def schedulingdriverrides():
		cursor = dbconn.cursor()
		#vtypess=request.json['vehicletype']
		#phonenos=request.json['phoneno']
		phonenos='7338995419'
		vtypess='auto'
		
		cursor.execute("SELECT tripid,from_add,to_add,time,shared,vehicletype,amount,bookingstatus from CurrentTrip where bookingstatus=%s and vehicletype=%s ORDER BY tripid",('Pending',vtypess))
		temp= cursor.fetchall()
		result=[]
		if temp:
			for tripids,froma,toa,times,shareds,vtypess,amounts,bookstats in temp:
				dicts={"tripid":tripids, "from_add":froma, "to_add":toa,"time":times, "shared":shareds, "vehicletype":vtypess,"amount":amounts,"bookingstatus":bookstats}
				result.append(dicts)
			
			return jsonify(result)
		else:
			return jsonify(message="You have no rides available currently.")	
	

#########################################################################################################################
	

	@app.route("/accept-rides")
	def driveracceptrides():
		cursor = dbconn.cursor()
		#tripids=request.json['tripid']
		#Dphonenos=request.json['Dphoneno']

		tripids='13'
		Dphonenos='7338995419'

		tripstats='Ongoing'
		bookingstats='Accepted'
		cursor.execute("UPDATE CurrentTrip SET bookingstatus=%s, tripstatus=%s, Dphoneno=%s  where tripid=%s",(bookingstats,tripstats,Dphonenos,tripids))
		dbconn.commit()
		
		cursor = dbconn.cursor()
		cursor.execute("UPDATE TripHistory SET tripstatus=%s, Dphoneno=%s  where tripid=%s",(tripstats,Dphonenos,tripids))
		dbconn.commit()

		cursor = dbconn.cursor()
		cursor.execute("SELECT tripid,from_add,to_add,time,shared,vehicletype,amount,otp,bookingstatus,tripstatus,Rphoneno from CurrentTrip where tripid=%s",(tripids,))

		
		temp= cursor.fetchone()
		
		if temp:
			tripids,froma,toa,times,shareds,vtypess,amounts,otps,bookingstats,tripstats,Rphonenos=temp
			return jsonify({"tripid":tripids,"from_add": froma, "to_add":toa, "time":times,"shared":shareds,"vehicletype":vtypess,"amount":amounts, "otp":otps,"bookingstatus":bookingstats,"tripstatus":tripstats,"Rphoneno":Rphonenos})
		
		else:
			return jsonify(message="Ride not scheduled")

#########################################################################################################################

	@app.route("/trip-completed-driver")
	def drivercompleterides():
		cursor = dbconn.cursor()
		#tripids=request.json['tripid']

		tripids='11'
		tripstats='Completed'

		cursor.execute("DELETE from CurrentTrip where tripid=%s",(tripids,))
		dbconn.commit()


		cursor = dbconn.cursor()
		cursor.execute("UPDATE TripHistory SET tripstatus=%s where tripid=%s",(tripstats, tripids))
		dbconn.commit()

		cursor = dbconn.cursor()
		cursor.execute("SELECT tripid,from_add,to_add,time,shared,vehicletype,amount,tripstatus from TripHistory where tripid=%s",(tripids,))
		

		temp= cursor.fetchone()
		tripids,froma,toa,times,shareds,vtypess,amounts,tripstats=temp
		return jsonify({"tripid":tripids,"from_add": froma, "to_add":toa, "time":times,"shared":shareds,"vehicletype":vtypess,"amount":amounts, "tripstatus":tripstats})

#########################################################################################################################



	return app

	
