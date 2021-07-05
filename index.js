let vm = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  components: {
    "hideable-text": {
      data: function () {
        return { show: false }
      },
      template: "<span><template v-if='show'><slot></slot></template><v-btn @click='show = !show' icon><v-icon color='grey'>{{ show ? 'mdi-eye-off' : 'mdi-eye' }}</v-icon></v-btn></span>"
    }
  },
  data: {
    tab: 0,
    groupsearch: "",
    marksearch: "",
    resultsearch: "",
    groupswithmembersandplayers: [],
    lecturereditedplayers: [],
    marksummary: [],
    marksdistribution: {},
    resultsummary: [],
    reportlist: [],
    urlPdf: null,
    showresultselects: true,
    reporttoshow: "",
    modelist: ['base', 'dynamic', 'multidynamic'],
    resultselection: {
      player: "",
      mode: "",
      trial: 0
    },
    resultselectionerror: "",
    resulttoshow: {
      player: "",
      mode: "",
      trial: null
    },
    showingresult: {
      all: [],
      showingstep: 0
    },
    mazeSettings: {
      size: [10,10],
      unit: 25,
      gap: 1,
      snakedotr: 10,
      snakedotdirscale: 0.5,
    },
    allDirs: ["n", "s", "w", "e"],
    dirOperations: [ [0, -1], [0, +1], [-1, 0], [+1, 0] ],
  },
  computed: {
    loaded: function () {
      return this.groupswithmembersandplayers.length > 0
      && this.lecturereditedplayers.length > 0
      && this.marksummary.length > 0
      && Object.keys(this.marksdistribution).length > 0
      && this.resultsummary.length > 0
      && this.reportlist.length > 0;
    },
    playerlist: function () {
      return this.resultsummary.reduce((acc,pl) => acc.concat(Object.keys(pl).filter(k => !['group','name'].includes(k))), []);
    }
  },
  watch: {
    tab: function() { this.$nextTick().then(() => MathJax.typeset()).then(() => MathJax.typeset()); },
    "showingresult.showingstep": function (newval, oldval) { if (newval == undefined) { this.$set(this.showingresult, 'showingstep', oldval); } }
  },
  mounted: function () {
    let req = new Request("data/groupswithmembersandplayers.json");
    fetch(req)
    .then(resp => resp.json())
    .then(jsonresp => { this.groupswithmembersandplayers = jsonresp; });

    req = new Request("data/lecturereditedplayers.json");
    fetch(req)
    .then(resp => resp.json())
    .then(jsonresp => { this.lecturereditedplayers = jsonresp; });

    req = new Request("data/marksummary.json");
    fetch(req)
    .then(resp => resp.json())
    .then(jsonresp => { this.marksummary = jsonresp; });

    req = new Request("data/marksdistribution.json");
    fetch(req)
    .then(resp => resp.json())
    .then(jsonresp => { this.marksdistribution = jsonresp; });

    req = new Request("data/playerssummary.json");
    fetch(req)
    .then(resp => resp.json())
    .then(jsonresp => { this.resultsummary = jsonresp; });

    req = new Request("data/reportlist.json");
    fetch(req)
    .then(resp => resp.json())
    .then(jsonresp => { this.reportlist = jsonresp; });
  },
  methods: {
    filtergroup: function (items, search) {
      if (search !== "") {
        search = search.toLowerCase();
        return items.filter(item => {
          let checks = [item.name.toLowerCase().includes(search)];
          checks = checks.concat(item.members.map(it => {
            return it.name.toLowerCase().includes(search) || it.id.toLowerCase().includes(search);
          }));
          checks = checks.concat(item.players.map(it => {
            return it.name.toLowerCase().includes(search) || it.folder.toLowerCase().includes(search);
          }));
          return checks.some(it => it);
        })
      } else { return items; }
    },
    filtermarks: function (items, search) {
      if (search !== "") {
        search = search.toLowerCase();
        return items.filter(item => {
          return [
            item.group.toLowerCase().includes(search),
            item['group number'].toLowerCase().includes(search),
            `group ${item['group number']}`.includes(search)
          ].some(it => it);
        })
      } else { return items; }
    },
    filterresult: function (items, search) {
      if (search !== "") {
        search = search.toLowerCase();
        return items.filter(item => {
          return [
            item.name.toLowerCase().includes(search),
            item.group.toString().includes(search),
            `group ${item.group}`.includes(search)
          ].some(it => it);
        })
      } else { return items; }
    },
    loadpdf: function (name) {
      let req = new Request(`reports/${name}.pdf`);
      fetch(req).then(res => res.blob())
      .then(res => {
        this.urlPdf = URL.createObjectURL(res);
      });
    },
    loadresult: function () {
      this.resultselectionerror = "";
      if (this.resultselection.player == "" || this.resultselection.mode == "") {
        this.resultselectionerror = "Player and/or Mode are/is not selected.";
      } else {
        this.resulttoshow = Object.assign({}, this.resultselection);
        this.importresult();
      }
    },
    importresult: function () {
      let req = new Request(`data/logs/${this.resultselection.player}/${this.resultselection.mode}/${this.resultselection.trial}/output.json`);
      fetch(req)
      .then(resp => resp.json())
      .then(resp => { this.showingresult.all = resp; this.showingresult.showingstep = 0; });
    },
    getMazeViewBox: function (row, col) {
      return [
        0, 0,
        col * this.mazeSettings.unit + Math.max(col + 1, 0) * this.mazeSettings.gap,
        row * this.mazeSettings.unit + Math.max(row + 1, 0) * this.mazeSettings.gap
      ];
    },
    getMazePadLoc: function (row, col) {
      let locs = [];
      [...Array(col).keys()].forEach((cval,cidx,carr) => {
        [...Array(row).keys()].forEach((rval,ridx,rarr) => {
          locs.push([cval * this.mazeSettings.unit + Math.max(cval + 1, 0) * this.mazeSettings.gap, rval * this.mazeSettings.unit + Math.max(rval + 1, 0) * this.mazeSettings.gap]);
        });
      });
      return locs;
    },
    getCoord: function (idx) {
      return this.mazeSettings.unit/2 + idx * this.mazeSettings.unit + Math.max(idx+1,0) * this.mazeSettings.gap;
    },
    getSnakeColor: function (fullLength, index) {
      return Math.ceil((fullLength-index)/fullLength *10)*10;
    },
    getSnakeDotDirs: function (locations, firstDir) {
      return locations.map((val,idx,arr) => {
        if (idx == 0) {
          return firstDir;
        } else {
          let delta = JSON.stringify([arr[idx-1][0] - val[0], arr[idx-1][1] - val[1]]);
          return this.allDirs[ this.dirOperations.map(x => JSON.stringify(x)).indexOf(delta) ];
        }
      });
    },
    getNewLocByDir: function (oldLoc, dir) {
      let operation = this.dirOperations[this.allDirs.indexOf(dir)];
      return [oldLoc[0] + operation[0], oldLoc[1] + operation[1]];
    },
    getSolutionLine: function (snakehead, solution) {
      let solutionline = ((typeof solution.reduce == "undefined") ? [solution] : solution).reduce((acc,val) => acc.concat([this.getNewLocByDir(acc[acc.length-1], val)]), [snakehead]);
      solutionline = solutionline.map(point => point.map(pt => this.getCoord(pt)));
      return solutionline;
    }
  }
});
