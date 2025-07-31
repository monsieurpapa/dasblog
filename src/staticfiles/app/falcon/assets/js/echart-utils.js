var docReadyLoadFunction = function docReadyLoadFunction(fn) {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fn);
  } else {
    setTimeout(fn, 1);
  }
};

var getPosition = function getPosition(pos, params, dom, rect, size) {
  return {
    top: pos[1] - size.contentSize[1] - 10,
    left: pos[0] - size.contentSize[0] / 2
  };
};

var getData = function getData(el, data) {
  try {
    return JSON.parse(el.dataset[camelize(data)]);
  } catch (e) {
    return el.dataset[camelize(data)];
  }
};

var rgbaColor = function rgbaColor() {
  var color = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '#fff';
  var alpha = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0.5;
  return "rgba(".concat(hexToRgb(color), ", ").concat(alpha, ")");
};

var getColor = function getColor(name) {
  var dom = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : document.documentElement;
  return getComputedStyle(dom).getPropertyValue("--falcon-".concat(name)).trim();
};

var getColors = function getColors(dom) {
  return {
    primary: getColor('primary', dom),
    secondary: getColor('secondary', dom),
    success: getColor('success', dom),
    info: getColor('info', dom),
    warning: getColor('warning', dom),
    danger: getColor('danger', dom),
    light: getColor('light', dom),
    dark: getColor('dark', dom)
  };
};

var getSoftColors = function getSoftColors(dom) {
  return {
    primary: getColor('soft-primary', dom),
    secondary: getColor('soft-secondary', dom),
    success: getColor('soft-success', dom),
    info: getColor('soft-info', dom),
    warning: getColor('soft-warning', dom),
    danger: getColor('soft-danger', dom),
    light: getColor('soft-light', dom),
    dark: getColor('soft-dark', dom)
  };
};

var getGrays = function getGrays(dom) {
  return {
    white: getColor('white', dom),
    100: getColor('100', dom),
    200: getColor('200', dom),
    300: getColor('300', dom),
    400: getColor('400', dom),
    500: getColor('500', dom),
    600: getColor('600', dom),
    700: getColor('700', dom),
    800: getColor('800', dom),
    900: getColor('900', dom),
    1000: getColor('1000', dom),
    1100: getColor('1100', dom),
    black: getColor('black', dom)
  };
};

var getDates = function getDates(startDate, endDate) {
  var interval = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 1000 * 60 * 60 * 24;
  var duration = endDate - startDate;
  var steps = duration / interval;
  return Array.from({
    length: steps + 1
  }, function (v, i) {
    return new Date(startDate.valueOf() + interval * i);
  });
};

var getMinutes = function getMinutes(startDate, endDate) {
  var interval = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 1000 * 60;
  var duration = endDate - startDate;
  var steps = duration / interval;
  return Array.from({
    length: steps + 1
  }, function (v, i) {
    return new Date(startDate.valueOf() + interval * i);
  });
};

var getPastDates = function getPastDates(duration) {
  var days;

  switch (duration) {
    case 'week':
      days = 7;
      break;

    case 'month':
      days = 30;
      break;

    case 'year':
      days = 365;
      break;

    default:
      days = duration;
  }

  var date = new Date();
  var endDate = date;
  var startDate = new Date(new Date().setDate(date.getDate() - (days - 1)));
  return getDates(startDate, endDate);
};

var getPastHourInMinutes = function getPastHourInMinutes(duration) {
  var minutes;

  switch (duration) {
    case 'hour':
      minutes = 60;
      break;

    case 'day':
      minutes = 1440;
      break;

    case 'half-hour':
      minutes = 30;
      break;

    default:
      minutes = 30;
  }

  var date = new Date().getTime();
  var startDate = new Date(date-minutes*60000);
  var endDate=new Date()

  return getMinutes(startDate, endDate);
};

var convertEpochToDateTime = function convertEpochToDateTime(epochDates) {
  var dateTimeArray = [];
  epochDates.forEach(function (epoch) {
    var dateTime = new Date(0); 
    dateTime.setUTCSeconds(epoch);
    dateTimeArray.push(dateTime);
  });  
  return dateTimeArray;
};

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

function formatBitsPerSecond(bits, decimals = 2) {
    bits=8*bits
    if (bits === 0) return '0 bps';

    const k = 1000;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['bps', 'Kbps', 'Mbps', 'Gbps', 'Tbps', 'Pbps', 'Ebps', 'Zbps', 'Ybps'];

    const i = Math.floor(Math.log(bits) / Math.log(k));

    return parseFloat((bits / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

function getChartColor(index) {
  var color;
  switch (index) {
    case 1:
      color = "text-primary";
      break;

    case 2:
      color = "text-danger";
      break;

    case 3:
      color = "text-success";
      break;

    case 4:
      color = "text-info";
      break;

    case 5:
      color = "text-warning";
      break;                                

    default:
      color = "text-primary";
  }
  return color;
};


var getRandomNumber = function getRandomNumber(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
};

var get_units_of_measure = function get_units_of_measure(value, tab_key) {
    var measurement;
    console.log('switch_tab_uom:', tab_key)
    switch (tab_key) {
      case 'jitter':
        measurement = value+' ms';
        break;

      case 'loss':
        measurement = value+' %';
        break;

      case 'latency':
        measurement = value+' ms';
        break;

      case 'bandwidth':
        measurement = formatBitsPerSecond(value);
        break;  
        
      case 'availability':
        measurement = value+' %';
        break;

      default:
        measurement = formatBitsPerSecond(value);
      }
    return measurement;
  };

  var tooltipFormatter = function tooltipFormatter(params) {
    /* var percentage = (params[0].value - params[1].value) / params[1].value * 100; */
    /* var perTemp = "\n      <div class=\"d-flex align-items-center ms-2\">\n        <span class=\"fas fa-caret-".concat(percentage < 0 ? 'down' : 'up', " text-").concat(percentage < 0 ? 'danger' : 'success', "\"></span>\n        <h6 class=\"fs--2 mb-0 ms-1 fw-semi-bold\">").concat(Math.abs(percentage).toFixed(2), " %</h6>\n      </div>\n    "); */
    var currentDate = new Date(params[0].axisValue);    
    var date = new Date().getTime();
    var minutes=1;
    var prevDate = new Date(date-minutes*60000);
    var uom = get_units_of_measure(params[0].data, tab_key);  
    var measurement;
    if (tab_key) {
        measurement=tab_key;
     } else {
      measurement='bandwidth';
    }
    /* return "<div>\n          <p class='mb-0 fs--2 text-600'>".concat(window.dayjs(params[0].axisValue).format('MMM D, YYYY h:mm A'), " vs ").concat(window.dayjs(prevDate).format('MMM D, YYYY h:mm A'), "</p>\n          <div class=\"d-flex align-items-center\">\n            <p class='mb-0 text-600 fs--1'>\n              Data: <span class='text-800 fw-semi-bold fs--1'>").concat(params[0].data, "</span>\n            </p>\n            ").concat(perTemp, "\n          </div>\n        </div>"); */
    return "<div>\n          <p class='mb-0 fs--2 text-600'>".concat(window.dayjs(params[0].axisValue).format('MMM D, YYYY h:mm A'), "  ").concat(" ", "</p>\n          <div class=\"d-flex align-items-center\">\n            <p class='mb-0 text-600 fs--1'>\n              ", measurement,": <span class='text-800 fw-semi-bold fs--1'>").concat(uom, "</span>\n            </p>\n            ").concat(" ", "\n          </div>\n        </div>");
  };

var initChart = function initChart(el, options) {
    var userOptions = getData(el, 'options');
    var chart = window.echarts.init(el);     
    echartSetOption(chart, userOptions, options);
};