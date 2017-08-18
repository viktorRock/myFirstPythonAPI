git add --all
git commit -m "heroku test"
git push
heroku config:set DISABLE_COLLECTSTATIC=1
