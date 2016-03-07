# wifi_mapper
An attempt in silliness to plot wifi ssids to an address, then create a pseudo gps out of it.

Currently - 
1. Scans wifi hotspots once a second on the train just using my laptop's antenna.
2. Organize data into workable format.
3. Tokenize and reduce all of Chicago's business names to shorter names.  For example, "An Awesome Business" would become, "AWESOMEBUSINESS" and "ANBUSINESS"
4. Run difflib comparison of ssids (with similar tokenization).  A decent example where this works: 
   STRONGBOX defaultdict(<type 'float'>, {'STRONGBOXSTORAGE': 0.72})

Todo: Use map information (street name, addr, etc) to help in identification of ssid location.
