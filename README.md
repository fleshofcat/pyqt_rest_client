# PyQt Rest Client

This package was written to make work with the REST API server async and convenient for PyQt applications.

Authentication here is calculated based on password/secret and message body.

For stable work with qt event loop, this package uses under the hood native qt classes for networking: `QNetworkAccessManager`, `QNetworkRequest`, `QNetworkReply`.

To use [async/await](https://iximiuz.com/en/posts/from-callback-hell-to-async-await-heaven/) pattern the client wraps qt requests into python [Future](https://docs.python.org/3/library/asyncio-future.html) objects.
