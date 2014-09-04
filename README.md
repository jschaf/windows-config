Install Mozilla Certs
=====================

A simple Powershell script to install all of Mozilla's root certs into
the Current User's Root Certificate store.

This project uses the PEM encoded certificates hosted by cURL at
http://curl.haxx.se/ca/cacert.pem.

**VERIFY the contents of the script to make sure it does what you think it does**

**Disclaimer**

This script will install certificates into to
`cert:\CurrentUser\Root`.  This means you will implicitly trust the
following three things.

* Mozilla - beacuse they created the list of certificate authorities (CA)

* cURL - because this script uses their PEM encoded version of Mozilla's list

* This script - because you're running it

To see Mozilla's certificate bundles, go to
http://mxr.mozilla.org/mozilla/source/security/nss/lib/ckfw/builtins/certdata.txt

For more infomation on how cURL creates the scripts, go to http://curl.haxx.se/ca/.

**Running the script**

Open a command prompt and paste the following.

```powershell
@powershell -NoProfile -ExecutionPolicy unrestricted -Command "iex ((new-object net.webclient).DownloadString('https://raw.github.com/jschaf/install-mozilla-certs/master/install-mozilla-cert.ps1'))"
```
