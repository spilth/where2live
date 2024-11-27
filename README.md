# Where To Live

## Getting Started

To check out the project and install required dependencies:

```bash
$ git clone git@github.com:spilth/where2live.git
$ cd where2live
$ pip install -r requirements.txt
$ npm install
```

### Processing Data

To combine the US States Shapefile with the CSV files:

```bash
$ invoke process
```

This will generates `static/states_data.geojson`

### Running the Web App Locally

To stand up the SvelteKit web app:

```bash
$ npm run dev -- --open
```

### Building the Web App Distribution

To create a production version of your app:

```bash
$ npm run build
```

### Deployment

To deploy using Netlify:

```bash
$ netlify deploy --dir=build --prod
```
