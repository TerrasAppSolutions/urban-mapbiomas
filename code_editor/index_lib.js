
var getNDVI = function(image){

    var out = image.expression(
    '(nir - red) / (nir + red )', {
      'nir': image.select('nir'), 
      'red': image.select('red')});
  
      
    return out.rename('ndvi');
    
  };
  
  var getNDWI = function(image){
  
    var out = image.expression(
    '(nir - green) / (nir + green )', {
      'nir': image.select('nir'), 
      'green': image.select('green')});
  
      
    return out.rename('ndwi');
    
  };
  
  
  var getEVI = function(image){
    
    var out = image.expression(
      '2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1))', {
        'nir': image.select('nir'), 
        'red': image.select('red'), 
        'blue': image.select('blue')
  });
  
    return out.rename('evi');
  };
  
  
  var getNDBI = function(image){
  
    var out = image.expression(
    '(swir1 - nir) / (swir1 + nir)', {
      'swir1': image.select('swir1'), 
      'nir': image.select('nir')});
  
      
    return out.rename('ndbi');
    
  };
  
  
  var getBU = function(image){
  
    var out = image.expression(
    'ndbi - ndvi', {
      'ndbi': image.select('ndbi'), 
      'ndvi': image.select('ndvi')});
  
      
    return out.rename('bu');
    
  };
  
  
  var getUI = function(image){
    var out = image.expression(
    '(swir2 - nir) / (swir2 + nir)', {
      'swir2': image.select('swir2'), 
      'nir': image.select('nir')});
    return out.rename('ui');
    
  };
  
  
  
  var getMNDWI = function(image){
  
    var out = image.expression(
    '(green - swir1) / (green + swir1)', {
      'swir1': image.select('swir1'), 
      'green': image.select('green')});
  
      
    return out.rename('mndwi');
    
  };
  
  
  var getNDVI_FocalMin = function(image, radius, iterations){
    /**/
    radius = (typeof radius !== 'undefined') ? radius : 2;
    iterations = (typeof iterations !== 'undefined') ? iterations : 1;
    /**/
    
    var out = getNDVI(image);
    
    return out.focal_min({'kernelType':'circle', 'radius':radius, 'iterations':iterations}).rename('ndvi');
    
  };
  
  var getNDVI_FocalMinThreshold = function(image, radius, iterations, threshold){
    /**/
    threshold = (typeof threshold !== 'undefined') ? threshold : 0.5;
    /**/
    
    var out = getNDVI_FocalMin(image, radius, iterations).gt(threshold);
    
    return out;
    
  };
  ////////////////////////////////////////////////////////////
  exports.getUI = getUI;
  exports.getBU = getBU;
  exports.getMNDWI = getMNDWI;
  exports.getNDBI = getNDBI;
  exports.getNDVI = getNDVI;
  exports.getNDWI = getNDWI;
  exports.getEVI = getEVI;
  exports.getNDVI_FocalMin = getNDVI_FocalMin;
  exports.getNDVI_FocalMinThreshold = getNDVI_FocalMinThreshold;