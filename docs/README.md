For the `doc` you can type 

```
make html
```

which generates the  `html` files and puts them into the `_build/html` directory.

To locally start the documentation environment navigate to `_build/html` and start an HTML server of your choice, 
e.g. by:

```
python -m http.server 9000
```

and then navigating to `0.0.0.0:9000`.