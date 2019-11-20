from application.app import create_app

app = create_app()

# --- main entry point
if __name__ == '__main__':
    from application.jobs.jobs import Jobs
    Jobs.start(app)
    app.run(debug=True, port=5000, host='0.0.0.0')
