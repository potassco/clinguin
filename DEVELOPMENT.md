# Development

To improve code quality, we use [nox] to run linters, type checkers, unit
tests, documentation and more. We recommend installing nox using [pipx] to have
it available globally.

```bash
# install
python -m pip install pipx
python -m pipx install nox

# run all sessions
nox

# list all sessions
nox -l

# run individual session
nox -s session_name

# run individual session (reuse install)
nox -Rs session_name
```

Note that the nox sessions create [editable] installs. In case there are
issues, try recreating environments by dropping the `-R` option. If your
project is incompatible with editable installs, adjust the `noxfile.py` to
disable them.

We also provide a [pre-commit][pre] config to autoformat code upon commits. It
can be set up using the following commands:

```bash
python -m pipx install pre-commit
pre-commit install
```

## Frontend (SvelteKit)

The frontend lives in `src/clinguin/client/svelte/`. Node.js 18+ is required.

### Running in development

Start the backend server first, then in a separate terminal:

```bash
cd src/clinguin/client/svelte
npm install
npm run dev
```

The dev server runs on `http://localhost:5173` and connects to the backend at
`http://127.0.0.1:8000` by default.

### Building for production

The frontend is built automatically by `client.py` when `--build` is passed:

```bash
clinguin client --build
```

To build manually:

```bash
cd src/clinguin/client/svelte
npm install
npm run build
```

### Adding shadcn-svelte components

```bash
cd src/clinguin/client/svelte
npx shadcn-svelte@latest add <component>
```

Components are installed into `src/lib/components/ui/`. After installing,
import the component in the relevant Clinguin component in
`src/lib/components/` and register the new element type in
`src/lib/registry.ts` if needed.

[editable]: https://setuptools.pypa.io/en/latest/userguide/development_mode.html
[nox]: https://nox.thea.codes/en/stable/index.html
[pipx]: https://pypa.github.io/pipx/
[pre]: https://pre-commit.com/
