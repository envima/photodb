# Configuration

All application settings are in the YAML file `config.yaml`.

Here, you configure your own PhotoDB instance. To configure your server settings refer to the following.

If you want to set up only a local PhotoDB instance you may skip directly to [PhotoDB cofiguration](config_photoDB.md).


# Application configuration

In the `config.yaml` you can specify *login*, *http_port*, *https_port*, *keystore_path*, and *keystore_password*. Your `config.yaml`may look like this:

`config.yaml` example:
```yaml
login: true
http_port: 0
https_port: 8000
keystore_path: 'certificate_with_certificate_chain.p12'
keystore_password: 'myPassword'
```

# Configuration YAML properties

**login**

Specifies if users need to login with indivdual credentials to get access to the PhotoDB instance.

No login needed, no access restrictions:
```yaml
login: false
```

Login needed:
```yaml
login: true
```
---

**http_port**

Specifies the application server listening on plain HTTP port.

Default port 8080:
```yaml
http_port: 8080
```

Disable HTTP, not listening on HTTP port:
```yaml
http_port: 0
```
---

**https_port**

Application server listening on encrypted secure HTTPS port. Needs keystore file at `keystore_path` and password at `keystore_password`.

Default port 8000:
```yaml
https_port: 8000
```

Disable HTTPS, not listening on HTTPS port:
```yaml
https_port: 0
```
---

**keystore_path**

*Needed for HTTPS connections only. Not needed for HTTP connections, so no keystore file. In the distribution package, no keystore file is included.*

Specifies filepath (relative to application root folder) to valid certificate for HTTPS encryption. Needs correct password at `keystore_password`.

Default `keystore.jks` filename at application root folder:
```yaml
keystore_path: 'keystore.jks'
```

Keystore should be in standardized [**PKCS #12**](https://en.wikipedia.org/wiki/PKCS_12) format, containing signed certificate, public key, encrypted private key and full certificate chain:
```yaml
keystore_path: 'certificate_with_certificate_chain.p12'
```
*For more information see [HTTPS certificates](https_certificates.md)*.

---

**keystore_password**

*Needed for HTTPS connections only. This password opens the keystore file. This password has no relation to user login accounts.*

Password for keystore. Needed by `keystore_path`.

Setting correct password needed to decrypt the keystore file at keystore_path:
```yaml
keystore_password: 'myPassword'
```
---