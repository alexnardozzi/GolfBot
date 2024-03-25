# Golf Bot
A bot to automate tee time purchasing for Union County golf courses.

# How To Use
- Install python on your machine
- Download the files
- Modify config file (see How To Configure)
- From the project's root directory run:
  ```
  python app/golfbot.py
  ```

# How To Configure
- Copy the config template found in config/config.example.ini into new file config/config.ini
- The keys in the config file have the following uses:
  
    | Key  | Use |
    | ------------- | ------------- |
    | url  | URL for the tee time reservation landing page  |
    | max_retries  | Number of allowed attempts to initialize the search (should be a min of 2)  |
    | max_refreshes  | Number of times to refresh the tee time page. Refreshes occur every 2 seconds so 300 = 10 minutes  |
    | username  | Union county account username  |
    | password  | Union county account password  |
    | autobuy  | Determine if the bot should complete the entire transaction automatically (True), or hold at the final verification step (False)  |
    | date  | The date to search for tee times  |
    | start_time  | Earliest time to be selected  |
    | end_time  | Latest time to be selected  |
    | excluded_courses  | Courses to exclude from the search. GH = Galloping Hills, AB = Ash Brook, LC = Learning Center  |
    
