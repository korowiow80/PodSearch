print "a"

# do a search
response = s.query('author:Me')
for hit in response.results:
    print "hit:", hit
   
print "b"