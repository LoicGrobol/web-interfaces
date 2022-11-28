curl http://httpbin.org
curl http://httpbin.org/anything
curl -X POST http://httpbin.org/anything
curl -G -d "value=pandas" http://httpbin.org/anything
curl http://www.google.com/robots.txt -o robots.txt
curl -H "User-Agent:Elephant" http://httpbin.org/anything
curl -i http://httpbin.org/anything
curl --data '{"value": "panda"}' -X POST http://httpbin.org/anything
curl -H "Content-Type:application/json" --data '{"value": "panda"}' -X POST http://httpbin.org/anything
curl -H "Accept-Encoding:gzip" https://www.google.com
curl http://httpbin.org/image -H "Accept:image/png"
curl -X PUT http://httpbin.org/anything
curl http://httpbin.org/image/jpeg
curl https://www.twitter.com
curl http://httpbin.org/anything -u "loic:machin"
curl -H "accept-language:es"  https://twitter.com 