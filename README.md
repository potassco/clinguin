# Clinguin :penguin: 

Clinguin is a framework for building User Interfaces (UI) using clingo. The UI is entirely specified in a logic-program.

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

This option show changes made on the `angular_fronted` folder in real time.


- Needed:
    - NPM/Node (default web-development setup):  [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm), [NODE](https://nodejs.org/en/download)
    - Angular: ([installation page](https://angular.io/guide/setup-local))

1. Start the server
    - Replace  `clinguin client-server` by `python start.py server` and remove argument `--frontend=AngularFrontend` from the command line of the desired example
2. Start the web client
    - Open a new tab
    - Navigate to the folder `/angular_frontend`. 
    - Type `ng serve`
    - Go to the URL `127.0.0.1:4200` in your web-browser.