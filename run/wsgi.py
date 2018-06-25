#!/usr/bin/env python3


from core import omnibus


if __name__ == "__main__":
	# Local
	omnibus.run(host="127.0.0.1", port=5000, debug=True)
	# Staging
	#omnibus.run(host="0.0.0.0", port=5000, debug=True)
	# Production
	#omnibus.run(host="0.0.0.0", port=5000, debug=False)
