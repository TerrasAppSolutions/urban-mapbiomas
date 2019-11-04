var worldpop = ee.ImageCollection('WorldPop/POP');
var nighttime_col = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG');
var infraprob = ee.ImageCollection('projects/mapbiomas-workspace/TRANSVERSAIS/INFRAURBANA4-PROB-V2');

var getNighttimeLayer = function () {

  var nighttime_2018 = nighttime_col.filterDate('2018-01-01', '2018-12-31').select(['avg_rad']).median();
  var nighttime_2017 = nighttime_col.filterDate('2017-01-01', '2017-12-31').select(['avg_rad']).median();
  var nighttime_2016 = nighttime_col.filterDate('2016-01-01', '2016-12-31').select(['avg_rad']).median();

  return ee.ImageCollection([nighttime_2017, nighttime_2018, nighttime_2016]).max().rename('nighttime');
};

var getInfraProbImage = function (year) {
  return infraprob.filterMetadata('year', 'equals', year).mosaic();
};

var getImageThreshold = function (image, worldpop, nighttime) {
  var low_nightlight = nighttime.gt(2);
  var medium_nightlight = nighttime.gt(10);
  var high_nightlight = nighttime.gt(40);
  var pop_high = worldpop.gt(50);

  var image_threshold1 = image.gt(95).multiply(low_nightlight);
  var image_threshold2 = image.gt(70).multiply(medium_nightlight);
  var image_threshold3 = image.gt(40).multiply(high_nightlight).multiply(pop_high);

  var result = ee.ImageCollection([image_threshold1, image_threshold2, image_threshold3]).max();

  return result;

};

var getWorlpopLayer = function () {
  return worldpop.filterMetadata('UNadj', 'equals', 'yes')
    .filterDate('2019-01-01', '2020-12-31').mosaic();
};

///////////////////////////////
exports.getNighttimeLayer = getNighttimeLayer;
exports.getInfraProbImage = getInfraProbImage;
exports.getImageThreshold = getImageThreshold;
exports.getWorlpopLayer = getWorlpopLayer;