import psycopg2
import urllib.parse as up

from flask import Flask,g,request
from flask import render_template,jsonify
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
	def loginpage():
		cursor = dbconn.cursor()		
		#phoneno= request.json['phoneno']
		#password= request.json['pwd']
	
		phoneno= '7338995417'
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
		
		phoneno= '7338995417'
		password= 'gops123'
		typess= 'rider'
		
		
		#password encryption:
		password=hashlib.sha256(password.encode('utf-8')).hexdigest() #hashvalue
		
		if typess=='rider':
			#names= request.json['name']
			#emails= request.json['email']
			
			names= 'joseph mani'
			emails= 'josephmani.uae@gmail.com'
		
			
			cursor.execute("INSERT INTO Signin_up (phoneno, pwd, type) VALUES(%s, %s, %s)",(phoneno, password, typess))
			dbconn.commit()
			
			cursor = dbconn.cursor()
			cursor.execute("INSERT INTO Rider (name, email, Rphoneno) VALUES(%s, %s, %s)",(names, emails, phoneno))
			dbconn.commit()
			
			cursor.execute("SELECT MAX(rid) from Rider")
			userid= cursor.fetchall()[0][0]
			dbconn.commit()
		
			return jsonify({"rid":userid,"name":names,"email":emails})
		
	
	
########################################  RIDER  ###############################################	
	
	@app.route("/book-ride")
	def fillnotes():
		cursor = dbconn.cursor()
		#phoneno= request.json['phoneno']
		#froma= request.json['from_add']
		#toa= request.json['to_add']
		#times= request.json['time']
		#shareds= request.json['shared']
		#vtypess= request.json['vehicletype']
		#amounts= request.json['amount']
		
		phoneno= '7338995417'
		froma= 'bangalore'
		toa= 'andhra'
		times='2021-11-25T02:56'
		shareds= 'T'
		vtypess= 'suv'
		amounts= 100
		
		#2018-06-07T00:00
		#share ride verification
	
		if shareds=='T':
			now = datetime.now()
			yr=times[2:4]
			month=times[5:7]
			day=times[8:10]
			hr=times[11:13]
			minute=times[14:]
			reqstr=day+'/'+month+'/'+yr+' '+hr+':'+minute+':00'

			date_time_obj = datetime.strptime(reqstr, '%d/%m/%y %H:%M:%S')

			diff=date_time_obj-now

			if abs(diff.total_seconds()) < 900:
				 shareds= 'F'
			else:
				 shareds='T'


		otps = random.randint(1000,9999)
				
		cursor.execute("INSERT INTO CurrentTrip (from_add, to_add, time, shared, vehicletype, amount, otp, Rphoneno) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(froma, toa, times, shareds, vtypess, amounts, otps, phoneno))
		dbconn.commit()
		
		cursor= dbconn.cursor()
		cursor.execute("SELECT MAX(tripid) from CurrentTrip where Rphoneno=%s",(phoneno,))
		tripids= cursor.fetchall()[0][0]
		dbconn.commit()
	
		return jsonify({"tripids":tripids,"phone":phoneno, "shareds": shareds})
	

#########################################################################################################################

	@app.route("/getallnotes", methods=["GET"])
	def getnotes():
		cursor = dbconn.cursor()
		userid= request.json['id']		
		
		cursor.execute("SELECT nid,title,dcp,dates,hids from notes where uid= %s",(userid,))
		temp= cursor.fetchall()
		
		result=[]
		for notesid,ntitle,description,dated,hashtag_ids in temp:
				dicts={"notesid":notesid, "title":ntitle, "description":description, "date":dated, "hashtags":hashtag_ids,"id":userid}
				result.append(dicts)
	
		return jsonify(result)

#########################################################################################################################
		
	@app.route("/update", methods=["PUT"])
	def updatenote():
		dated=str(date.today())
		cursor = dbconn.cursor()
		userid= request.json['id']
		notesid= request.json['notesid']
		ntitle= request.json['title']
		description= request.json['description']
		hashtag_ids= request.json['hashtags']
		hash_id=[v.strip() for v in hashtag_ids.split(',')]
		
		
		cursor = dbconn.cursor()
		cursor.execute("UPDATE notes SET title=%s, dcp=%s, dates=%s, hids=%s where nid=%s and uid=%s",(ntitle, description, dated, hashtag_ids, notesid, userid))
		cursor.execute("DELETE FROM hashtags where nid=%s and uid=%s",(notesid, userid))
		dbconn.commit()
		
		hashidlist=[]
		for hashes in hash_id:	
				cursor = dbconn.cursor()
				cursor.execute("INSERT INTO hashtags (label,nid,uid) SELECT %s, %s, %s where NOT exists( select 1 from hashtags where label=%s)",(hashes, notesid, userid, hashes))
				dbconn.commit()
				cursor = dbconn.cursor()
				cursor.execute("SELECT hid from hashtags where label=%s and uid=%s",(hashes,userid))
				hashids= cursor.fetchall()[0][0]
				hashidlist.append(hashids)
				dbconn.commit()
		
		cursor = dbconn.cursor()
		cursor.execute("SELECT title,dcp,dates,hids from notes where nid= %s and uid=%s",(notesid,userid))
		values= cursor.fetchall()
		dbconn.commit()
		return jsonify({"notesid":notesid, "title":ntitle, "description":description, "date":dated, "hashtags":hashtag_ids, "hashtagids": hashidlist ,"id":userid})	
		
#########################################################################################################################		
				
	@app.route("/delete", methods=["DELETE"])
	def deletenote():
		cursor = dbconn.cursor()
		userid= request.json['id']
		notesid= request.json['notesid']
		
		cursor.execute("SELECT title,dcp,dates,hids from notes where uid= %s and nid=%s",(userid,notesid))
		temp= cursor.fetchone()
		ntitle,description,dated,hashtag_ids=temp
		dbconn.commit()
		
		cursor = dbconn.cursor()
		cursor.execute("SELECT hids from notes where uid= %s and nid=%s",(userid,notesid))
		hashidlist= cursor.fetchone()
		dbconn.commit()
		
		
		cursor = dbconn.cursor()
		cursor.execute("DELETE FROM hashtags where nid=%s and uid=%s",(notesid, userid))
		cursor.execute("DELETE FROM notes where nid=%s and uid=%s",(notesid, userid))
		dbconn.commit()
		return jsonify({"notesid":notesid, "title":ntitle, "description":description, "date":dated, "hashtags":hashtag_ids, "hashtagids": hashidlist ,"id":userid})

#########################################################################################################################
	
	@app.route("/hashtags", methods=["GET"])
	def gethashtags():
		cursor = dbconn.cursor()
		userid= request.json['id']
		cursor.execute("SELECT hid,label from hashtags where uid= %s",(userid,))
		values= cursor.fetchall()
		dbconn.commit()
		result=[]
		for hashid,hashes in values:
			dicts={"hashtagid":hashid, "hashtag":hashes}
			result.append(dicts)
		
		return jsonify(result)		
	
	return app
	
