# Readme.md

## crl.py
### def get_contents(keyword, min_results=10)
> Get information from youtube search results, return more than the number specified in min_results.

### class Query(max_results=100)
> Manage the query results. The class method "expand" must be overriden.
> 
> Use subscript to get query result. Query result will calculate lazily

### class KeyWordQuery(keyword, kind=VIDEO, max_results=None)
> Class KeyWordQuery is derived class of the class Query.
> 
> The keyword parameter will be used as search keyword
> 
> If kind is set to VIDEO(or crl.VIDEO), KeyWordQuery results only contain video results. The same holds for CHANNEL or PLAYLIST
> 
> ex) KeyWordQuery("classic music", kind=VIDEO | CHANNEL)

### class ChannelVideoQuery(user=None, id=None, max_results=None)
> Class ChannelVideoQuery is derived class of the class ChannelQuery
> 
> If both parameter(user and id) is None, it will raise ValueError
> 
> ex) ChannelVideoQuery(user="YourRelaxMusic1")

> If not working, try to use your onw context data.

***
