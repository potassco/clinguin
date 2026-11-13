## Pigeon Box Example

To run the server with the Pigeon Box example, use the following command:

```
clinguin server --domain-files examples/pigeon_box/encoding.lp --ui-files examples/pigeon_box/ui.lp
```

The client-side can be started with either of the following commands:

```
npm run dev
```

or

```
clinguin client --build
```

### Themes

**Green Theme:**

```
clinguin client --theme ../../../../examples/pigeon_box/green.css --build
```

**Orange Theme:**

```
clinguin client --theme ../../../../examples/pigeon_box/orange.css --build
```

**Blue Theme:**

```
clinguin client --theme ../../../../examples/pigeon_box/blue.css --build
```
