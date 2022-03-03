from datetime import datetime
import json
import arrow
import sys


try:
    updatesFile = open("updates.json", 'r')
except OSError:
    print("Could not open/read file:", fname)
    sys.exit()

with updatesFile:
    updates = json.load(updatesFile)
with open("results.json", "r") as jsonFile:
    results = json.load(jsonFile)

# Iterate over updates
for update in updates:
    for url, data in update.items():
        # Match found
        if url in results:
            # Compare data between updates and results
            changes = {}
            for key, value in data.items():
                update_value = value
                result_value = results[url]['data'].get(key)
                if update_value != result_value:
                    changes[key] = {'old': result_value, 'new': update_value}
            if changes:
                results[url]['changelog'].append({
                    'timestamp': arrow.utcnow(),
                    'changes': changes
                })
                results[url]['data'] = data
        # No match found
        else:
            # Build changelog
            changes = {}
            for key, value in data.items():
                changes[key] = {'old': None, 'new': value}

            # Append new result
            results[url] = {
                'data': data,
                'changelog': [
                    {
                        'timestamp': arrow.utcnow(),
                        'changes': changes
                    }
                ]
            }


with open("results.json", "w") as jsonFile:
    json.dump(results, jsonFile, indent=4, sort_keys=True, default=str)