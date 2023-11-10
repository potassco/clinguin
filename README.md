# Clinguin :penguin: 

Clinguin is a graphical-user-interface for Clingo, where one can specify the user-interface entirely in a logic-program. One might wonder how one can do this by him-/herself - for this see the descriptions below and have fun :-)

Visit the [documentation page](https://clinguin.readthedocs.io/en/latest/clinguin/installation.html).

## Web-Frontend Build and Deploy

1. (Optional) Manually build: `make all`
2. For e.g. the housing example you can type: 
```
clinguin client-server --domain-files examples/clingo/housing/instance.lp examples/clingo/housing/encoding.lp --ui-files examples/clingo/housing/ui.lp  --server-port 8000 --frontend AngularFrontend --client-port 8087
```
3. Then navigate in the browser of your choice to `127.0.0.1:8087` and enjoy :-)


### Details

Use the lines of code from the `Makefile`, i.e.:

```
pushd angular_frontend/; ng build; popd
mv angular_frontend/dist/clinguin_angular_frontend clinguin/client/presentation/frontends/angular_frontend
```

First `ng build` is executed, which builds the application in the `/angular_frontend/dist/clinguin_angular_frontend` folder.
This folder is then moved to `/clinguin/client/presentation/frontends/angular_frontend`. 
The corresponding clinguin frontend, `angular_frontend.py`, starts a web-server which serves our angular frontend.

To facilitate the options of different ports, the `--server-port` option specifies the port of the backend, when either using `client-server` or `server`.

When using the `--frontend AngularFrontend` frontend (`client-server` or `client`), one can always set the `--client-port` to specify the port of the webserver, which one accesses through the browser.
For `client` the additional `--server-url` and `--server-port` options let one specify the location of the server, when the server is e.g. on another machine than the client.

## Web-Frontend Development Enviroment

- Needed:
    - NPM/Node (default web-development setup):  [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm), [NODE](https://nodejs.org/en/download)
    - Angular: ([installation page](https://angular.io/guide/setup-local))

Then navigate to the folder `/angular_frontend`. There type `ng serve` and then go to the URL `127.0.0.1:4200` in your web-browser.
It is assumed that the backend is already started (just the `clinguin server`).





### Development mode

Show changes made on the `angular_fronted` folder in real time:

- Replace  `clinguin client-server` by `python start.py server` and remove argument `--frontend=AngularFrontend`
- Make sure angular is running in another terminal 

```
cd angular_fronted; ng serve
```