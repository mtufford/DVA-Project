function loadMonthDistrubtionChart() {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var monthFires = [0,0,0,0,0,0,0,0,0,0,0,0];
    for(var i=0; i<wildfires.length; i++) {
        monthFires[new Date(wildfires[i]["DISCOVERY_DATE"]).getMonth()] += 1;
    }

    var chartData = [];
    for(var i=0; i<monthNames.length; i++) {
        chartData.push({label: monthNames[i], y: monthFires[i], color: "#007bff"});
    }
    var chart = new CanvasJS.Chart("monthly-chart-container", {
    height: 300,
    width: 750,
    backgroundColor: "transparent",
	animationEnabled: true,
	title:{
		text:"Monthly Wildfire Distribution",
        fontSize: 15,
        fontWeight: "bold"
	},
	axisX:{
		title: "Month",
		interval: 1,
        labelFontSize: 12,
        titleFontSize: 14
    },
	axisY:{
	    title: "Number of wildfires",
        labelFontSize: 12,
        titleFontSize: 14
	},
	data: [{
		type: "column",
		dataPoints: chartData
	}]
    });
    chart.render();
}

function loadCausesChart() {
    var causes = {};
    for(var i=0; i<wildfires.length; i++) {
        if(wildfires[i]["STAT_CAUSE_DESCR"] in causes) {
            causes[wildfires[i]["STAT_CAUSE_DESCR"]] += 1;
        } else {
            causes[wildfires[i]["STAT_CAUSE_DESCR"]] = 0;
        }
    }
    var chartData = [];
    var causesKeys = Object.keys(causes);
    for(var i=0; i<causesKeys.length; i++) {
        chartData.push({label: causesKeys[i], y: causes[causesKeys[i]], color: window.colors[causesKeys[i]]});
    }
    chartData.sort((a,b) => (a.y > b.y) ? 1 : ((b.y > a.y) ? -1 : 0));

    var chart = new CanvasJS.Chart("causes-chart-container", {
    height: 300,
    width: 750,
    backgroundColor: "transparent",
	animationEnabled: true,
	title:{
		text:"Wildfire Cause Distribution",
        fontSize: 14,
        fontWeight: "bold"
	},
	axisX:{
		interval: 1,
        labelFontSize: 12,
        titleFontSize: 14
	},
	axisY2:{
		title: "Number of wildfires",
        labelFontSize: 12,
        titleFontSize: 14
	},
	data: [{
		type: "bar",
		axisYType: "secondary",
		dataPoints: chartData
	}]
    });
    chart.render();
}

function loadFireSizeClassChart() {
    var fireSizeClasses = {};
    var colors = {
        "A": "#0000CD",
        "B": "#3535FF",
        "C": "#577AE4",
        "D": "#4169E0",
        "E": "#4682B4",
        "F": "#B0C4DE",
        "G": "#B0E0E6"
    };
     var labels = {
        "A": "A<=0.25 acres  A",
        "B": "10>B>0.25 acres  B",
        "C": "100>C>=10 acres  C",
        "D": "300>D>=100 acres  D",
        "E": "1000>E>=300 acres  E",
        "F": "5000>F>=1000 acres  F",
        "G": "G>=5000 acres  G"
    };
    for(var i=0; i<wildfires.length; i++) {
        if(wildfires[i]["FIRE_SIZE_CLASS"] in fireSizeClasses) {
            fireSizeClasses[wildfires[i]["FIRE_SIZE_CLASS"]] += 1;
        } else {
            fireSizeClasses[wildfires[i]["FIRE_SIZE_CLASS"]] = 0;
        }
    }
    var chartData = [];
    var fireSizeClassesKeys = Object.keys(fireSizeClasses);
    for(var i=0; i<fireSizeClassesKeys.length; i++) {
        chartData.push({label: labels[fireSizeClassesKeys[i]],
            y: fireSizeClasses[fireSizeClassesKeys[i]],
            color: colors[fireSizeClassesKeys[i]]});
    }
    chartData.sort((a,b) => (a.label.slice(-1) > b.label.slice(-1)) ? -1 : ((b.label.slice(-1) > a.label.slice(-1)) ? 1 : 0));

    var chart = new CanvasJS.Chart("firesizeclass-chart-container", {
    height: 300,
    width: 750,
    backgroundColor: "transparent",
	animationEnabled: true,
	title:{
		text:"Wildfire Size Distribution",
        fontSize: 14,
        fontWeight: "bold"
	},
	axisX:{
        title: "Fire Size Class",
		interval: 1,
        labelFontSize: 12,
        titleFontSize: 14
	},
	axisY2:{
		title: "Number of wildfires",
        labelFontSize: 12,
        titleFontSize: 14
	},
	data: [{
		type: "bar",
		axisYType: "secondary",
		dataPoints: chartData
	}]
    });
    chart.render();
}

function loadCharts() {
    loadMonthDistrubtionChart();
    loadCausesChart();
    loadFireSizeClassChart();
}

function loadChart(evt, chartName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
	loadCharts();
  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(chartName).style.display = "block";
  if (evt.currentTarget !== undefined) {
      evt.currentTarget.className += " active";
  }
}