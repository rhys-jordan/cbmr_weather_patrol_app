from idlelib.colorizer import DEBUG

from CBMR_Weather import create_app

app = create_app()

if __name__ == '__main__':
    app.run()