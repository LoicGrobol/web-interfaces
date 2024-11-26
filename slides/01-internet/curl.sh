# 1
curl http://httpbin.org

# 2
curl http://httpbin.org/anything

# 3
# Utiliser --request pour préciser la méthode (GET par défaut)
curl --request POST http://httpbin.org/anything

# 4
# --get impose la méthode GET et inclut dans l'url les données passées via --data
curl --get --data "value=pandas" http://httpbin.org/anything

# 5
# --ouput permet d'écrire le résultat dans un fichier plutôt que dans le terminal
curl http://www.google.com/robots.txt --output robots.txt

# 6
# --header pour passer des headers, ok
curl --header "User-Agent:Elephant" http://httpbin.org/anything

# 7
# --include fait afficher les headers de la *réponse*
curl --include http://httpbin.org/anything

# 8
# --request peut aussi s'écrire -X
curl --data '{"value": "panda"}' -X POST http://httpbin.org/anything

# 9
# En demandant un Content-Type, vous recevez une réponse différente
curl --header "Content-Type:application/json" --data '{"value": "panda"}' -X POST http://httpbin.org/anything

# 10
# Accept-Encoding signale qu'on veut bien recevoir une réponse compressée
curl --header "Accept-Encoding:gzip" https://www.google.com

# 11
curl http://httpbin.org/image --header "Accept:image/png"

# 12
curl -X PUT http://httpbin.org/anything

#13
curl http://httpbin.org/image/jpeg

#14
curl https://www.twitter.com

#15
# -u permet de passer un nom d'utilisateurice et un mot de passe
curl http://httpbin.org/anything -u "morgan:pwd"

# 16
curl -H "accept-language:es"  https://duckduckgo.com