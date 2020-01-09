import mysql.connector
current_hotel = 1

def add_hotel(hotel_nombre, hotel_url, hotel_imagen, hotel_estrellas, hotel_estrellas_ta, listing_url):
	hotel_nombre 	= hotel_nombre.replace(',', '')
	hotel_nombre 	= hotel_nombre.replace("'", "")
	conn 			= mysql.connector.connect(host="localhost", user="local_db_user", passwd="local_db_pass", database="local_db_name", auth_plugin="mysql_native_password")
	try:
		mycursor 	= conn.cursor()
		query 		= "INSERT INTO hoteles (nombre, url, imagen, estrellas, estrellas_ta, url_listing) VALUES (%s, %s, %s, %s, %s, %s)"
		vals 		= (hotel_nombre, hotel_url, hotel_imagen, hotel_estrellas, hotel_estrellas_ta, listing_url)
		mycursor.execute(query, vals)
		conn.commit()
		print('Hotel %s added!'%hotel_nombre)
	except:
		print("ERROR in mysql syntax: %s"%mycursor.statement)
	conn.close()

def add_tag(hotel_id, tag):
	conn 	= mysql.connector.connect(host="localhost", user="local_db_user", passwd="local_db_pass", database="local_db_name", auth_plugin="mysql_native_password")
	try:
		cursor 	= conn.cursor()
		query 	= "INSERT INTO tags (id_hotel, tag) VALUES (%s, %s)"
		vals 	= (hotel_id, tag)
		cursor.execute(query, vals)
		conn.commit()
		print('Tag added to DB: %s'%tag)
	except:
		print('ERROR adding tag to DB: %s'%cursor.statement)
	conn.close()

def truncate_table(table_name):
	conn 	= mysql.connector.connect(host="localhost", user="local_db_user", passwd="local_db_pass", database="local_db_name", auth_plugin="mysql_native_password")
	cursor 	= conn.cursor()
	cursor.execute('TRUNCATE TABLE %s'%table_name)
	conn.commit()
	conn.close()	

def get_last_hotel_id():
	conn 	= mysql.connector.connect(host="localhost", user="local_db_user", passwd="local_db_pass", database="local_db_name", auth_plugin="mysql_native_password")
	cursor 	= conn.cursor()
	cursor.execute("SELECT id FROM hoteles ORDER BY id DESC LIMIT 1")
	result 	= cursor.fetchone()
	conn.close()
	return result[0]

def check_if_item_exists(hotel_url):
	print('Checking the database for hotel: %s'%hotel_url)
	conn 	= mysql.connector.connect(host="localhost", user="local_db_user", passwd="local_db_pass", database="local_db_name", auth_plugin="mysql_native_password")
	cursor 	= conn.cursor()
	cursor.execute('SELECT url FROM hoteles WHERE url = "%s"'%hotel_url)
	result 	= cursor.fetchone()
	conn.close()
	if not result:
		return False
	else:
		return True

def scrape(items, scrape_url, my_tags):
	import re
	global current_hotel
	i=0
	while i < len(items):
		print('Analizando item #%i'%current_hotel)
		#Scrape and add hotels to db
		try:
			hotel_nombre = items[i].find("h2").get_text().strip()
		except:
			hotel_nombre = "Unnamed hotel"
		
		try:
			hotel_url = items[i]['href']
			hotel_url = re.sub(r"\/\d{2}-\d{2}-\d{4}\/\d{2}-\d{2}-\d{4}\/",'/{{from}}/{{to}}/', hotel_url)
		except:
			hotel_url = ''

		try:
			hotel_imagen = items[i].find_all("img")[0]['src']
		except:
			hotel_imagen = ''

		try:
			hotel_estrellas = len(items[i].find("div", {"class": re.compile('star-rating___.*?')}).find_all("svg"))
		except:
			hotel_estrellas = '0'
		
		
		try:
			hotel_estrellas_ta = len(items[i].find_all("path", {"d":"M200.78,300A99.22,99.22,0,1,0,300,200.77,99,99,0,0,0,200.78,300"}))
		except:
			hotel_estrellas_ta = '0'
		
		#Check if hotel isn't already in DB
		exists = check_if_item_exists(hotel_url)
		if not exists:
			print('The hotel isn\'t in the database.')
			try:
				add_hotel(hotel_nombre, hotel_url, hotel_imagen, hotel_estrellas, hotel_estrellas_ta, scrape_url)
				
				#Get last hotel id
				print('Obtaining hotel id...')
				last_hotel_id = get_last_hotel_id()
				add_tag(last_hotel_id, geo)
				
				try:
					#Add custom tags
					for my_tag in my_tags:
						if my_tag != '':
							add_tag(last_hotel_id, my_tag)
				except:
					print("***Error: Custom tags not added.***")

				#Scrape and add tags to db
				print('Scraping tags...')
				try:
					tags = items[i].find("div", {"class":re.compile('amenities___.*?')})
					try:
						tags = tags.find_all("svg")
						print('%s tags found...'%len(tags))
						tgs = list()
						for t in tags:
							t = t.find_all("g")
							for g in t:
								tgs.append(g['id'])
						for t in tgs:
							add_tag(last_hotel_id, t)
						print("\n\n")
					except:
						print("")
				except:
					print("no ammenities found")
			except:
				print('***ERROR: Could not add hotel to database.***')
			

			
			

			'''
			#tags = items[i].find("div", {"class":"amenities___mxo1km amenities___ef96v amenities___di3b1 amenities___qzreky"})
			tags = items[i].find("div", {"class":re.compile('amenities___.*?')})
			tags = tags.find_all("svg")
			print('%s tags found.'%len(tags))
			tgs = list()
			for t in tags:
				t = t.find_all("g")
				for g in t:
					tgs.append(g['id'])
			tags = tgs
			print("***Tags***")
			for tag in tags:		
				add_tag(last_hotel_id, tag)
				print('Added tag to db: %s'%tag)
			'''
			
		else:
			print('Hotel %s was already in DB; skipping but adding custom tags'%hotel_nombre)

			try:
				#Add custom tags
				for my_tag in my_tags:
					if my_tag != '':
						add_tag(last_hotel_id, my_tag)
			except:
				print("No se pudieron agregar tags customizados para el hotel que ya estaba en la base.")
		i = i+2
		current_hotel +=1
		print("\n\n")