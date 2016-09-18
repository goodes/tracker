## Install Horizon on system

```
npm install -g horizon@2.0.0
```


## Create the certificates

```
mkdir -p client/config/tls
cd client/config/tls && hz  create-cert
```

Add the following lines to `client/.hz/config.toml`

```
###############################################################################
# HTTPS Options
# 'secure' will disable HTTPS and use HTTP instead when set to 'false'
# 'key_file' and 'cert_file' are required for serving HTTPS
#------------------------------------------------------------------------------
secure = true
key_file = "config/tls/horizon-key.pem" 
cert_file = "config/tls/horizon-cert.pem"
```


## Basic ReactJS config

```
echo '{ "presets": ["react", "es2015", "stage-0"] }' > .babelrc
npm init -y
npm install --save-dev babel-core babel-loader
npm install --save-dev babel-preset-es2015 babel-preset-react babel-preset-stage-0 babel-polyfill
npm install --save-dev webpack
npm install --save react react-dom react-router
npm install --save @horizon/client@2.0.0

```

```
hz serve --dev --connect localhost:28015  --secure no client
```