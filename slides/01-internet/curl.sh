# 1
curl http://httpi.dev

# 2
curl http://httpi.dev/anything

# 3
# Utiliser --request pour préciser la méthode (GET par défaut)
curl --request POST http://httpi.dev/anything

# 4
# --get impose la méthode GET et inclut dans l'url les données passées via --data
curl --get --data "value=pandas" http://httpi.dev/anything

# 5
# --ouput permet d'écrire le résultat dans un fichier plutôt que dans le terminal
curl http://www.google.com/robots.txt --output robots.txt

# 6
# --header pour passer des headers, ok
curl --header "User-Agent:Elephant" http://httpi.dev/anything

# 7
# --include fait afficher les headers de la *réponse*
curl --include http://httpi.dev/anything

# 8
# --request peut aussi s'écrire --request
curl --data '{"value": "panda"}' --request POST http://httpi.dev/anything

# 9
# En demandant un Content-Type, vous recevez une réponse différente
curl --header "Content-Type:application/json" --data '{"value": "panda"}' --request POST http://httpi.dev/anything

# 10
# Accept-Encoding signale qu'on veut bien recevoir une réponse compressée
curl --header "Accept-Encoding:gzip" https://www.google.com

# 11
curl http://httpi.dev/image --header "Accept:image/png"

# 12
curl --request PUT http://httpi.dev/anything

#13
curl http://httpi.dev/image/jpeg

#14
curl -v http://mastodon.social

# 301 "moved permanently" vers https://mastodon.social. Votre navigateur suit la redirection, mais
# curl par défaut non et il faut lui passer le flag --location:

curl --location http://mastodon.social

# Ou à la main

curl https://mastodon.social

#15
# -u permet de passer un nom d'utilisateurice et un mot de passe
curl http://httpi.dev/anything -u "morgan:pwd"

# 16
curl -H "accept-language:es"  https://duckduckgo.com