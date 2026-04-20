# forumerly

A web forum with all functionality based on NodeJS, Express, and MongoDB.

## Requirements

- Docker
- NodeJS

## How to launch

- Use `./launch.sh` to run the Authentication, Redis, and MongoDB services. The application needs these services running for it to correctly work.
  Note that the `launch.sh` script will use a clean database every time it starts. Thus, you should execute it in a separate terminal.
- Run `npm clean-install` to install application dependencies.
- Run `node app.js` to start the server.
- Open the browser in `localhost:3000` to see the website.

## How to shutdown

- Use <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop the server.
- Run `./stop.sh` to stop the third-party services.
- Run `./wipe.sh` to wipe the data of the third-party services.
