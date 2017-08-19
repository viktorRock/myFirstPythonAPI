git add --all
git commit -m "heroku test"
git push
echo heroku config:set DISABLE_COLLECTSTATIC=1
