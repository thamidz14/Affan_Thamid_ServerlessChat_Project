# To Add Files To a Repository:
```
git add serverless.yml
git commit -m "Added serverless.yml"
git push origin main
```
```
git add CLI-Commands.md
git commit -m "Added CLI-Commands.md"
git push origin main
```

Merge / Rebase
```
git pull --no-rebase
git pull --rebase
git pull --ff-only
aws s3 cp index.html s3://thamidaffan-bucket/index.html

git push -u origin main
git fetch origin

```
# To Set Up Development Environment

**Mac Users**
```
Download and install fnm: curl -o- https://fnm.vercel.app/install | bash
Download and install Node.js: fnm install 23
Verify the Node.js version: node -v # Should print "v23.6.0".
Verify npm version: npm -v # Should print "10.9.2".

```
**Windows Users**
```
Download and install fnm: winget install Schniz.fnm
Download and install Node.js: fnm install 22
Verify the Node.js version: node -v # Should print "v22.13.0".
Verify npm version: npm -v # Should print "10.9.2".
```
