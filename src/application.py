''' The Europa project. '''

import sys
import europa

# Use a different configuration file, if specified.
config_file = None
if len(sys.argv) > 1:
    config_file = sys.argv[1]

# Load the configuration, if provided.
application = europa.initialize_all(config_file=config_file)


if __name__ == '__main__':
    with application.app_context():
        from europa.models import db
        db.create_all()

    # Let's go!
    application.run(debug=False)
