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

  let costOfLivingEnabled = $state(true);
  let educationEnabled = $state(false);
  let fiberEnabled = $state(false);
  let harrisVotesEnabled = $state(false);
  let homicidesEnabled = $state(false);
  let marijuanaEnabled = $state(false);
  let abortionEnabled = $state(false);

  const toggleLayer = (layerTitle: string, isVisible: boolean) => {
    if (map) {
      map.getLayers().getArray().forEach((layer) => {
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

      return new Style({
        fill: new Fill({
          color: `rgba(0,0,0, ${(index - 79) / 100})`
        }),
        stroke: stateOutline
      });
    };

    const abortionStyle = (feature: Feature): Style => {
      const status = feature.get('Status of Abortion');

      const lookup = {
        'Abortion banned': 1.0,
        'Gestational limit between 6 and 12 weeks LMP': 0.75,
        'Gestational limit between 15 and 22 weeks LMP': 0.5,
        'Gestational limit at or near viability': 0.25,
        'No gestational limits': 0.0
      };

      const alpha = lookup[status];
      return new Style({
        fill: new Fill({
          color: `rgba(0,0,0, ${alpha})`
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

      return new Style({
        fill: new Fill({
          color: `rgba(0,0,0, ${alpha})`
        }),
        stroke: stateOutline
      });
    };

    const educationStyle = (feature: Feature): Style => {
      const rank = feature.get('Ranking');

      return new Style({
        fill: new Fill({
          color: `rgba(0,0,0, ${(rank - 1) / (50 - 1)})`
        }),
        stroke: stateOutline
      });
    };

    const fiberStyle = (feature: Feature): Style => {
      const rank = feature.get('Rank');

      return new Style({
        fill: new Fill({
          color: `rgba(0,0,0, ${(rank - 1) / (50 - 1)})`
        }),
        stroke: stateOutline
      });
    };

    const homicidesStyle = (feature: Feature): Style => {
      const per100k = feature.get('Homicides per 100k');

      return new Style({
        fill: new Fill({
          color: `rgba(0,0,0, ${per100k / 24})`
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
            url: 'states_data.geojson',
            format: new GeoJSON()
          }),
          style: abortionStyle,
          title: 'Abortion Bans Status',
          visible: false
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_data.geojson',
            format: new GeoJSON()
          }),
          style: marijuanaStyle,
          title: 'Marijuana',
          visible: false
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_data.geojson',
            format: new GeoJSON()
          }),
          style: homicidesStyle,
          title: 'Homicides',
          visible: false
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_data.geojson',
            format: new GeoJSON()
          }),
          style: fiberStyle,
          title: 'Fiber',
          visible: false
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_data.geojson',
            format: new GeoJSON()
          }),
          style: harrisVotesStyle,
          title: 'Harris Votes',
          visible: false
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_data.geojson',
            format: new GeoJSON()
          }),
          style: educationStyle,
          title: 'Education',
          visible: false
        }),
        new VectorLayer({
          source: new VectorSource({
            url: 'states_data.geojson',
            format: new GeoJSON()
          }),
          style: costOfLivingStyle,
          title: 'Cost of Living',
          visible: true
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

    <p>The darker the state, the worse the ranking/assessment for a given factor.</p>

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
            bind:checked={abortionEnabled}
            onchange={() => {
                  toggleLayer('Abortion Bans Status', abortionEnabled);
                }}
          /> Abortion Bans Status
          </label>
        </td
        >
        <td>
          <a
            href="https://www.kff.org/womens-health-policy/dashboard/abortion-in-the-u-s-dashboard/"
          >Source</a>
        </td>
      </tr>

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

    <h2>Resources</h2>

    <ul>
      <li><a href="https://github.com/spilth/where2live">Project Source Code</a></li>
      <li><a href="https://knowhere.live">Knowhere to Live</a></li>
      <li><a href="https://www.moveindigo.org">MoveIndigo</a></li>
      <li><a href="https://worldpopulationreview.com">World Population Review</a></li>
      <li><a href="https://www.census.gov">U.S. Census Bureau</a></li>
    </ul>

    <h2>Updates</h2>

    <dl>
      <dt>2024-11-26</dt>
      <dd>Added layer for Status of Abortion Bans</dd>
    </dl>

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
        overflow: hidden;
    }

    #about {
        min-width: 256px;
        width: 25%;
        padding: 12px;
        overflow: auto;
    }

    #map {
        width: 100%;
        height: 100%;
    }

    dt {
        font-weight: bold;
    }
</style>
