from datetime import timedelta


# VK API Version
api_version = '5.71'

# Wall owner (user or group) address
domain = 'jumoreski'

# Database filename
db = 'db.sqlite'

# Table name
table = 'jumoreski'

# Time range of wall update (timedelta)
update_range = timedelta(days=30)

# Timeout between answers (seconds)
bot_timeout = 1

# Max dialogs count per request
dialogs_count = 200

# Max wall posts count per request
posts_count = 100
