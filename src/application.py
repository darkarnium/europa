''' The Europa project. '''
import europa

application = europa.initialize_all()

if __name__ == '__main__':
    with application.app_context():
        from europa.models import db
        db.create_all()

    # Run.
    application.run(debug=True)
