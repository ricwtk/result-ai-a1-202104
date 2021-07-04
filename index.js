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
    reporttoshow: ""
  },
  computed: {
    loaded: function () {
      return this.groupswithmembersandplayers.length > 0
      && this.lecturereditedplayers.length > 0
      && this.marksummary.length > 0
      && Object.keys(this.marksdistribution).length > 0
      && this.resultsummary.length > 0
      && this.reportlist.length > 0;
    }
  },
  watch: {
    tab: function() { this.$nextTick().then(() => MathJax.typeset()).then(() => MathJax.typeset()); }
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
      return items;
      if (search !== "") {

      } else { return items; }
    },
    loadpdf: function (name) {
      let req = new Request(`reports/${name}.pdf`);
      fetch(req).then(res => res.blob())
      .then(res => {
        this.urlPdf = URL.createObjectURL(res);
      });
    }
  }
});
