sudo docker run --name ytdl-sync -p 5000:5000 -it -v "$(pwd)/main:/ytdl-sync" -d ytdl-sync-image bash
sudo docker exec -d ytdl-sync python3 run.py db.sql