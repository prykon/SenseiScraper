echo "----------------------------------"
echo "Dumping local database..."
mysqldump --user=localhost_db_user --password=localhost_db_pass local_db_name > local_db.sql
echo "DONE."
echo ""
echo "Uploading database to server..."
echo ""

#replace 0.0.0.0 with server ip
mysql -h 0.0.0.0 --user=server_db_user --password=server_db_pass server_db_name < local_db.sql
echo "DONE."
echo "----------------------------------"