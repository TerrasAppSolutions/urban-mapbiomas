var index_lib = require('users/dyedenm/urban:mapbiomas-c4/index_lib');


var getFeatureSpace = function (image, samples, bands) {

    image = image.select(bands);

    samples = image.sampleRegions({
        collection: samples,
        scale: 30,
        geometries: true

    }
    );

    return ee.FeatureCollection(samples);

};

var runRandomForest = function (ntree, image, samples, bands) {

    var classifier = ee.Classifier.randomForest({
        numberOfTrees: ntree,
        minLeafPopulation: 20
    })
        .train({
            'features': samples,
            'classProperty': 'value',
            'inputProperties': bands
        })
        .setOutputMode('PROBABILITY');

    var classified = image.classify(classifier);

    return classified;

};

var landsatAddIndex = function (landsat) {
    landsat = landsat.addBands(index_lib.getNDVI(landsat));
    landsat = landsat.addBands(index_lib.getMNDWI(landsat));
    landsat = landsat.addBands(index_lib.getEVI(landsat));
    landsat = landsat.addBands(index_lib.getNDBI(landsat));
    landsat = landsat.addBands(index_lib.getBU(landsat));
    landsat = landsat.addBands(index_lib.getUI(landsat));
    return landsat;

};


var classifyLandsat = function (landsat, samples, bands) {

    var classified = runRandomForest(500, landsat, samples, bands);

    return classified.multiply(100).byte();

};


////////////////////////////////////////////////////////////
exports.runRandomForest = runRandomForest;
exports.getFeatureSpace = getFeatureSpace;
exports.classifyLandsat = classifyLandsat;
exports.landsatAddIndex = landsatAddIndex;


