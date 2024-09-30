# A Simplified OAuth2 Library
## No special configuration required 
No special configuration required, use the examples in the sample directory to run.   
The default configuration has the following limitations:   
Problem 1: Restarting the service will invalidate previous login information.
This is because fastoauth generates a random secret_key each time it starts, and tokens generated with the old secret_key will become invalid.   
Problem 2: Tokens cannot be shared between multiple OAuth processes.
Since different processes generate different random secret_keys, tokens cannot be parsed by different processes.   
Problem 3: Issued tokens cannot be revoked.
Since tokens are not stored by default and their validity is verified by decryption each time, issued tokens cannot be revoked within their validity period.

## Configuring the secret_key
It is generally recommended to set a secret_key or use Redis for better availability.   
This can solve problems 1 and 2 in the default configuration.

> Note: After configuring Redis, the secret_key setting is invalid. Please refer to the Redis section for details.
---
Generating the secret_key
```
openssl rand -hex 32
```

If you don't have the openssl command, you need to install it separately.

```
# Installation on Windows, refer to https://zhuanlan.zhihu.com/p/108833705 for choco installation
choco install openssl -y
```

## Configuring Redis
It is generally recommended to configure Redis for the highest security.   
After configuring Redis, all problems in the default configuration can be solved.   
At the same time, after configuring Redis, only shorter tokens need to be used during HTTP transmission, and richer content can be stored in Redis.

# A simplified server-side example
In the project directory ./sample/oauth_server.py