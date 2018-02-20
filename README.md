# Sparbahn
Some python3 modules to query and filter the Deutsche Bahn Sparpreis search.

This uses an inofficial API endpoint for XHR-Requests. Please use with care.

## Why?
Just for fun.

## How To Use
Check spar.py on examples how to use.

## Known issues
StationID is only set for two train station. If you need other/more, please add them to
bahn.bahn.Sparbahn -> self.bhfId = {'N':'008000284', 'Dresden Hbf': '008010085'}.
