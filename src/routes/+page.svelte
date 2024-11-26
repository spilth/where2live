<script lang="ts">
  import 'ol/ol.css';
  import Map from 'ol/Map';
  import TileLayer from 'ol/layer/Tile';
  import View from 'ol/View';
  import OSM from 'ol/source/OSM';
  import VectorLayer from 'ol/layer/Vector';
  import VectorSource from 'ol/source/Vector';
  import { GeoJSON } from 'ol/format';
  import { Fill, Stroke, Style } from 'ol/style';
  import { Feature } from 'ol';

  let map: Map | null = null;

  let costOfLivingEnabled = $state(false);
  let educationEnabled = $state(false);
  let fiberEnabled = $state(false);
  let harrisVotesEnabled = $state(true);
  let homicidesEnabled = $state(false);
  let marijuanaEnabled = $state(false);

  const toggleLayer = (layerTitle: string, isVisible: boolean) => {
    if (map) {
      const layers = map.getLayers().getArray();
      layers.forEach((layer) => {
        if (layer.get('title') === layerTitle) {
          layer.setVisible(isVisible);
        }
      });
    }
  };

  let stateOutline = new Stroke({
    color: 'white',
    width: 0.5
  });

  const setupMap = (node: HTMLElement) => {
    const costOfLivingStyle = (feature: Feature): Style => {
      const index = feature.get('Cost of Living Index');
      const fillColor = `rgba(0,0,0, ${(index - 79) / 100})`;

      return new Style({
        fill: new Fill({
          color: fillColor
        }),
        stroke: stateOutline
      });
    };

    const marijuanaStyle = (feature: Feature): Style => {
      const legality = feature.get('Legal Status');

      let alpha = 1.0;
      switch (legality) {
        case 'Fully Legal':
          alpha = 0.0;
          break;
        case 'Mixed':
          alpha = 0.5;
          break;
        case 'Fully Illegal':
          alpha = 1.0;
          break;
        default:
          alpha = 0.0;
      }
      const fillColor = `rgba(0,0,0, ${alpha})`;

      return new Style({
        fill: new Fill({
          color: fillColor
        }),
        stroke: stateOutline
      });
    };

    const educationStyle = (feature: Feature): Style => {
      const rank = feature.get('Ranking');
      const fillColor = `rgba(0,0,0, ${(rank - 1) / (50 - 1)})`;

      return new Style({
        fill: new Fill({
          color: fillColor
        }),
        stroke: stateOutline
      });
    };

    const fiberStyle = (feature: Feature): Style => {
      const rank = feature.get('Rank');
      const fillColor = `rgba(0,0,0, ${(rank - 1) / (50 - 1)})`;

      return new Style({
        fill: new Fill({
          color: fillColor
        }),
        stroke: stateOutline
      });
    };

    const homicidesStyle = (feature: Feature): Style => {
      const per100k = feature.get('Homicides per 100k');
      const fillColor = `rgba(0,0,0, ${per100k / 24})`;

      return new Style({
        fill: new Fill({
          color: fillColor
        }),
        stroke: stateOutline
      });
    };

    const harrisVotesStyle = (feature: Feature): Style => {
      const harris = feature.get('Harris') * 100 - 26;
      const fillColor = `rgba(0,0,0, ${1 - harris / 38})`;

      return new Style({
        fill: new Fill({
          color: fillColor
        }),
        stroke: stateOutline
      });
    };

    map = new Map({
      target: node.id,
      layers: [
        new TileLayer({
          source: new OSM()
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_marijuana.geojson',
            format: new GeoJSON()
          }),
          style: marijuanaStyle,
          title: 'Marijuana',
          visible: false
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_homicides.geojson',
            format: new GeoJSON()
          }),
          style: homicidesStyle,
          title: 'Homicides',
          visible: false
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_fiber.geojson',
            format: new GeoJSON()
          }),
          style: fiberStyle,
          title: 'Fiber',
          visible: false
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_election.geojson',
            format: new GeoJSON()
          }),
          style: harrisVotesStyle,
          title: 'Harris Votes',
          visible: true
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_education.geojson',
            format: new GeoJSON()
          }),
          style: educationStyle,
          title: 'Education',
          visible: false
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_cost_of_living.geojson',
            format: new GeoJSON()
          }),
          style: costOfLivingStyle,
          title: 'Cost of Living',
          visible: false
        })
      ],
      view: new View({
        center: [0, 0],
        zoom: 2
      })
    });

    map
      .getView()
      .fit([-14288085.579078684, 2613236.080750007, -7307971.125095623, 6578328.874748718]);

    return {
      destroy() {
        if (map) {
          map.setTarget(undefined);
          map = null;
        }
      }
    };
  };
</script>

<div id="layout">
  <div id="about">
    <h1>Where To Live</h1>

    <p>An evolving collection of data to help folks choose which state to live in.</p>

    <p>The dark the state, the worse the ranking/assessment for a given factor.</p>

    <p>
      The <a
      href="https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html"
    >US States shapefile</a
    > comes from the United States Census Bureau.
    </p>

    <h2>Factors</h2>

    <table>
      <tbody>
      <tr>
        <td>
          <label><input
            type="checkbox"
            bind:checked={costOfLivingEnabled}
            onchange={() => {
                  toggleLayer('Cost of Living', costOfLivingEnabled);
                }}
          /> Cost of Living
          </label>
        </td
        >
        <td>
          <a
            href="https://worldpopulationreview.com/state-rankings/cost-of-living-index-by-state"
          >Source</a>
        </td>
      </tr>
      <tr>
        <td>
          <label><input
            type="checkbox"
            bind:checked={educationEnabled}
            onchange={() => {
                  toggleLayer('Education', educationEnabled);
                }}
          /> Public School Rankings</label>
        </td>
        <td><a
          href="https://worldpopulationreview.com/state-rankings/public-school-rankings-by-state"
        >Source</a></td>
      </tr>
      <tr>
        <td>
          <label><input
            type="checkbox"
            bind:checked={fiberEnabled}
            onchange={() => {
                  toggleLayer('Fiber', fiberEnabled);
                }}
          /> Fiber Internet Rank</label>
        </td>
        <td><a href="https://broadbandnow.com/report/fiber-optic-availability-map">Source</a></td>
      </tr>
      <tr>
        <td>
          <label><input
            type="checkbox"
            bind:checked={harrisVotesEnabled}
            onchange={() => {
                  toggleLayer('Harris Votes', harrisVotesEnabled);
                }}
          /> Harris Votes</label>
        </td>
        <td><a href="https://www.270towin.com">Source</a></td>
      </tr>
      <tr>
        <td>
          <label><input
            type="checkbox"
            bind:checked={homicidesEnabled}
            onchange={() => {
                  toggleLayer('Homicides', homicidesEnabled);
                }}
          /> Homicides per 100k</label></td>
        <td>
          <a href="https://worldpopulationreview.com/state-rankings/murder-rate-by-state"
          >Source</a>
        </td>
      </tr>
      <tr>
        <td>
          <label><input
            type="checkbox"
            bind:checked={marijuanaEnabled}
            onchange={() => {
                  toggleLayer('Marijuana', marijuanaEnabled);
                }}
          /> Marijuana Legality Status</label>
        </td>
        <td><a href="https://disa.com/marijuana-legality-by-state">Source</a></td>
      </tr>
      </tbody>
    </table>

    <h2>About</h2>

    <p>Feedback can be sent to <a href="mailto:brian@spilth.org">brian@spilth.org</a></p>
  </div>
  <div id="map" use:setupMap></div>
</div>

<style>
    :global(html, body) {
        margin: 0;
        padding: 0;
        font-family: sans-serif;
        width: 100%;
        height: 100%;
    }

    #layout {
        display: flex;
        width: 100%;
        height: 100%;
    }

    #about {
        width: 25%;
        padding: 8px;
    }

    #map {
        width: 100%;
        height: 100%;
    }

    :global(.layer-control) {
        position: absolute;
        bottom: 10px;
        left: 10px;
        background: white;
        padding: 10px;
        border: 1px solid #666;
        border-radius: 4px;
        font-size: 14px;
        z-index: 1000;
        box-shadow: 2px 2px 4px #333;
    }
</style>
