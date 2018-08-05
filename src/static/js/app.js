var map, featureList, fieldSearch = [];

$(window).resize(function() {
  sizeLayerControl();
});

$(document).on("click", ".feature-row", function(e) {
  $(document).off("mouseout", ".feature-row", clearHighlight);
  sidebarClick(parseInt($(this).attr("id"), 10));
});

if ( !("ontouchstart" in window) ) {
  $(document).on("mouseover", ".feature-row", function(e) {
    highlight.clearLayers().addLayer(L.circleMarker([$(this).attr("lat"), $(this).attr("lng")], highlightStyle));
  });
}

$(document).on("mouseout", ".feature-row", clearHighlight);

$("#about-btn").click(function() {
  $("#aboutModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$("#full-extent-btn").click(function() {
  map.fitBounds(boroughs.getBounds());
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$("#legend-btn").click(function() {
  $("#legendModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$("#login-btn").click(function() {
  $("#loginModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$("#signup-btn").click(function() {
  $("#sigupModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$('#login').validator().on('submit', function (e) {
  if (e.isDefaultPrevented()) {
    // handle the invalid form...
  } else {
	e.preventDefault();
	$.ajax({			
            url: '/v1/api/user/login',
            data: $('#login').serialize(),
            type: 'POST',
            success: function(response) {                
				console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
    });
	$("#loginModal").modal("hide");
  }
})
$('#signup').validator().on('submit', function (e) {
  if (e.isDefaultPrevented()) {
    // handle the invalid form...
  } else {
	e.preventDefault();
	$.ajax({
            url: '/v1/api/user/signup',
            data: $('#signup').serialize(),
            type: 'POST',
            success: function(response) {                
				console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
    });
	$("#sigupModal").modal("hide");
  }
})


$("#list-btn").click(function() {
  animateSidebar();
  return false;
});

$("#nav-btn").click(function() {
  $(".navbar-collapse").collapse("toggle");
  return false;
});

$("#sidebar-toggle-btn").click(function() {
  animateSidebar();
  return false;
});

$("#sidebar-hide-btn").click(function() {
  animateSidebar();
  return false;
});

function animateSidebar() {
  $("#sidebar").animate({
    width: "toggle"
  }, 350, function() {
    map.invalidateSize();
  });
}

function sizeLayerControl() {
  $(".leaflet-control-layers").css("max-height", $("#map").height() - 50);
}

function clearHighlight() {
  highlight.clearLayers();
}

function sidebarClick(id) {
  //console.log(plot_changed.getLayer(id));
  var layer = plot_changed.getLayer(id);  
  map.setView([layer.getBounds().getCenter().lat, layer.getBounds().getCenter().lng], 12);
  layer.fire("click");
  /* Hide sidebar and go to the map on small screens */
  if (document.body.clientWidth <= 767) {
    $("#sidebar").hide();
    map.invalidateSize();
  }
}

//var fieldsLayer = L.geoJson(null);	
var plot_changed = L.geoJson(null, {	
				style: function (feature) {
					if (feature.properties.changed_points >= 10) {
						return {
							color: "red",
							fill: true,
							weight: 1,
							fillOpacity:1,
							fillColor: '#ff0000',
							Opacity:1		
						};
					} else {
						return {
							color: "yellow",
							fill: true,
							weight: 1,
							fillOpacity:1,
							fillColor: '#fd9c06',
							Opacity:1		
						};
					}					
				  },
				onEachFeature: function (feature, layer) {													
					if (feature.properties) {
						//console.log(layer);
					  var content = "<table class='table table-striped table-bordered table-condensed'>" + "<tr><th>Lô - Khoảnh - Tiểu khu</th><td>" + feature.properties.lo + "-" + feature.properties.khoanh + "-" +  feature.properties.tk + "</td></tr>"+ "<tr><th>Địa chỉ</th><td>" + feature.properties.ddanh + "-"+ feature.properties.xa + "-"+ feature.properties.huyen + "-"+ feature.properties.tinh + "</td></tr>"+ "<tr><th>Ảnh 1</th><td>" + feature.properties.image1 + "</td></tr>"+ "<tr><th>Ảnh 2</th><td>" + feature.properties.image2 + "</td></tr>"+ "<tr><th>Hiện trạng</th><td>" + feature.properties.ldlr + "</td></tr>"+ "<tr><th>Diện tích lô (ha)</th><td>" + feature.properties.dtich + "</td></tr>"+ "<tr><th>Ngày phát hiện</th><td>" + feature.properties.processed_date + "</td></tr>" + "<tr><th>Tọa độ</th><td>" + layer.getBounds().getCenter().lat +":"+ layer.getBounds().getCenter().lng + "</td></tr>" + "</td></tr>" + "<tr><th>Diện tích bất thường</th><td><a class='url-break' href='#' target='_blank'>" + parseFloat(feature.properties.changed_square).toFixed(2) + "(" + feature.properties.image_type +")"+ "</a></td></tr>" + "<table>";
					  layer.on({
						click: function (e) {					  
						  $("#feature-title").html("Thông tin chi tiết");
						  $("#feature-info").html(content);
						  $("#featureModal").modal("show");
						  highlight.clearLayers().addLayer(L.marker([layer.getBounds().getCenter().lat, layer.getBounds().getCenter().lng], highlightStyle));	
						  //layer.setStyle(highlighted);
						}
					  });
					  $("#feature-list tbody").append('<tr class="feature-row" id="' + L.stamp(layer) + '" lat="' + layer.getBounds().getCenter().lat + '" lng="' + layer.getBounds().getCenter().lng+ '"><td style="vertical-align: middle;"><img width="16" height="18" src="../static/img/museum.png"></td><td class="feature-name">'+ feature.properties.lo + "-" + feature.properties.khoanh + "-" +  feature.properties.tk +'-'+ layer.feature.properties.ldlr + '('+ layer.feature.properties.changed_square +')</td><td style="vertical-align: middle;"><i class="fa fa-chevron-right pull-right"></i></td></tr>');		
					  fieldSearch.push({
							name: layer.feature.properties.lo,
							msdh: layer.feature.properties.ldlr,
							masothua: layer.feature.properties.changed_square,							
							source: "Fields",
							id: L.stamp(layer),
							lat: layer.getBounds().getCenter().lat,
							lng: layer.getBounds().getCenter().lng
						  });
						}				
				}
			});
function load_plot_changed(data) {    
    plot_changed.addData(data);	
    map.addLayer(plot_changed);	
};

var plot_maxzoom = 10; 
function get_plot_changed() {
  /* Empty sidebar features */
  //console.log(plot_maxzoom);
  if(map.getZoom() >= plot_maxzoom){
	$("#feature-list tbody").empty();
	var owsrootUrl = 'http://langbiang1.dbcr.info:8080/geoserver/wfs';
	var defaultParameters = {
		service : 'WFS',
		version : '2.0',
		request : 'GetFeature',	
		count:30,
		bbox: map.getBounds().getSouth()  +','+map.getBounds().getWest() +','+map.getBounds().getNorth() +','+map.getBounds().getEast(),
		typeName : 'fms:mp_lba_plot_changed',
		outputFormat : 'text/javascript',
		format_options : 'callback:getJson',	
		SrsName : 'EPSG:4326'
	};
	var parameters = L.Util.extend(defaultParameters);
	var URL = owsrootUrl + L.Util.getParamString(parameters);
	//console.log(URL);
	var fields = null;
	var ajax = $.ajax({
		url : URL,
		dataType : 'jsonp',
		jsonpCallback : 'getJson',	
		success : load_plot_changed
		});
		 
		/* Update list.js featureList */
		  featureList = new List("features", {
			valueNames: ["feature-name"]
		  });
		  featureList.sort("feature-name", {
			order: "asc"
		  });
		  $("#loading").hide();	
	}else{
    map.removeLayer(plot_changed);
	}
} 

/* Basemap Layers */

var ArcGiS = L.tileLayer("http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
  attribution: '&copy; <a href="http://www.esri.com/">Esri</a>'
});

var cartoLight = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
});

var mbAttr = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>',
		mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

var grayscale   = L.tileLayer(mbUrl, {id: 'mapbox.light', attribution: mbAttr}),
	streets  = L.tileLayer(mbUrl, {id: 'mapbox.streets',   attribution: mbAttr});
		
var BING_KEY = 'AuhiCJHlGzhg93IqUH_oCpl_-ZUrIE6SPftlyGYUvr9Amx5nzA-WqGcPquyFZl4L'
var bingLayer = L.tileLayer.bing(BING_KEY);

/* Overlay Layers */
var geoUrl = 'http://langbiang1.dbcr.info:8080/geoserver/wms?';	
var mp_lba_zone = L.tileLayer.wms(geoUrl,{layers: 'mp_lba_zone',format: 'image/png',transparent: true});
var hotspot = L.tileLayer.wms(geoUrl,{layers: 'cbdbcr:hotspot',format: 'image/png',transparent: true});
var mp_lba_boundary = L.tileLayer.wms(geoUrl,{layers: 'fms:mp_lba_boundary_merge',format: 'image/png',transparent: true});	
var mp_lba_mining = L.tileLayer.wms(geoUrl,{layers: 'fms:mp_lba_mining',format: 'image/png',transparent: true});
var mp_lba_boundary_region = L.tileLayer.wms(geoUrl,{layers: 'fms:mp_lba_boundary_region',format: 'image/png',transparent: true});	


var highlight = L.geoJson(null);
var highlightStyle = {
  stroke: false,
  fillColor: "#00FFFF",
  fillOpacity: 0.7,
  radius: 10
};

map = L.map("map", {
  zoom: 10,
  center: [12.0113, 108.4194],
  layers: [ArcGiS,plot_changed,mp_lba_boundary_region],
  zoomControl: false,  
  attributionControl: false
});



/* Filter sidebar feature list to only show features in current map bounds */
map.on("moveend", function (e) {
  //get_point_changed();
  get_plot_changed();
});


/* Clear feature highlight when map is clicked */
map.on("click", function(e) {
  highlight.clearLayers();
});

 // get_point_changed();
  get_plot_changed();
/* Attribution control */
function updateAttribution(e) {
  $.each(map._layers, function(index, layer) {
    if (layer.getAttribution) {
      $("#attribution").html((layer.getAttribution()));
    }
  });
}
map.on("layeradd", updateAttribution);
map.on("layerremove", updateAttribution);


var attributionControl = L.control({
  position: "bottomright"
});
attributionControl.onAdd = function (map) {
  var div = L.DomUtil.create("div", "leaflet-control-attribution");
  div.innerHTML = "<span class='hidden-xs'>Xây dựng bởi <a href='#'>KATA</a> | </span><a href='#' onclick='$(\"#attributionModal\").modal(\"show\"); return false;'>Thông tin</a>";
  return div;
};
map.addControl(attributionControl);

var zoomControl = L.control.zoom({
  position: "bottomright"
}).addTo(map);

/*Print map*/
L.easyPrint({
	title: 'In bản đồ',
	position: 'bottomright',
	sizeModes: ['A4Portrait', 'A4Landscape']
}).addTo(map);
var printer = L.easyPrint({
      		tileLayer: ArcGiS,
      		sizeModes: ['Current', 'A4Landscape', 'A4Portrait'],
      		filename: 'MapLangbiang',
			title: 'Tải bản đồ',
      		exportOnly: true,
			position: 'bottomright',
      		hideControlContainer: true
		}).addTo(map);

function manualPrint () {
	printer.printMap('CurrentSize', 'MyManualPrint')
}
/* GPS enabled geolocation control set to follow the user's location */
var locateControl = L.control.locate({
  position: "bottomright",
  drawCircle: true,
  follow: true,
  setView: true,
  keepCurrentZoomLevel: true,
  markerStyle: {
    weight: 1,
    opacity: 0.8,
    fillOpacity: 0.8
  },
  circleStyle: {
    weight: 1,
    clickable: false
  },
  icon: "fa fa-location-arrow",
  metric: false,
  strings: {
    title: "Vị trí của tôi",
    popup: "Bạn đang trong {distance} {unit} từ điểm này",
    outsideMapBoundsMsg: "Vị trí của bạn ngoài phạm vi"
  },
  locateOptions: {
    maxZoom: 18,
    watch: true,
    enableHighAccuracy: true,
    maximumAge: 10000,
    timeout: 10000
  }
}).addTo(map);



/* Larger screens get expanded layer control and visible sidebar */
if (document.body.clientWidth <= 767) {
  var isCollapsed = true;
} else {
  var isCollapsed = false;
}

var baseLayers = {
  "Ảnh vệ tinh": ArcGiS,    
};

var groupedOverlays = {
  "Dữ liệu nền": {		
	"Ranh giới ": mp_lba_boundary_region,
	"Hiện trạng rừng": mp_lba_zone,	
	"Điểm khai thác":mp_lba_mining
  },
  "Cảnh báo mất rừng": {    
	"Lô rừng cảnh báo": plot_changed,	
  },
  "Cảnh báo cháy rừng": {    		
	"Điểm cháy vệ tinh 24h": hotspot
  },
  
};

	
var layerControl = L.control.groupedLayers(baseLayers, groupedOverlays, {
  collapsed: isCollapsed
}).addTo(map);

/* Highlight search box text on click */
$("#searchbox").click(function () {
  $(this).select();
});

/* Prevent hitting enter from refreshing the page */
$("#searchbox").keypress(function (e) {
  if (e.which == 13) {
    e.preventDefault();
  }
});

$("#featureModal").on("hidden.bs.modal", function (e) {
  $(document).on("mouseout", ".feature-row", clearHighlight);
});


// Leaflet patch to make layer control scrollable on touch browsers
var container = $(".leaflet-control-layers")[0];
if (!L.Browser.touch) {
  L.DomEvent
  .disableClickPropagation(container)
  .disableScrollPropagation(container);
} else {
  L.DomEvent.disableClickPropagation(container);
}
