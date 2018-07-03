#!/usr/bin/env python3
# WSGI: Web service gateway interface


from core import omnibus as app


if __name__ == "__main__":
	# Local
	app.run(host="127.0.0.1", port=5000)
	# Staging
	#app.run(host="0.0.0.0", port=5000)
	# Production
	#app.run(host="0.0.0.0", port=5000, debug=False)
