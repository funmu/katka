/*  MavexUtils.js
 *
 */

 (function() {
	var MavexUtils = function() {
	}

 	function ParseURLParams( urlSearchString)
	{
		var urlParams;
	    var match,
	        pl     = /\+/g,  // Regex for replacing addition symbol with a space
	        search = /([^&=]+)=?([^&]*)/g,
	        decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
	        query  = urlSearchString.substring(1);

	    urlParams = {};
	    while (match = search.exec(query))
	       urlParams[decode(match[1])] = decode(match[2]);

	   return urlParams;
	}

	MavexUtils.prototype.ParseURLParams = function( urlSearchString) {
		return ParseURLParams(urlSearchString);
	}

	// create functtions for generating GUIDs
	// Credits to: http://stackoverflow.com/questions/105034/create-guid-uuid-in-javascript
	var GUID = GUID || (function () {

		var EMPTY = '00000000-0000-0000-0000-000000000000';

		var _padLeft = function (paddingString, width, replacementChar) {
		    return paddingString.length >= width ? paddingString : _padLeft(replacementChar + paddingString, width, replacementChar || ' ');
		};

		var _s4 = function (number) {
		    var hexadecimalResult = number.toString(16);
		    return _padLeft(hexadecimalResult, 4, '0');
		};

		var _cryptoGuid = function () {
		    var buffer = new window.Uint16Array(8);
		    window.crypto.getRandomValues(buffer);
		    return [_s4(buffer[0]) + _s4(buffer[1]), _s4(buffer[2]), _s4(buffer[3]), _s4(buffer[4]), _s4(buffer[5]) + _s4(buffer[6]) + _s4(buffer[7])].join('-');
		};

		var _guid = function () {
		    var currentDateMilliseconds = new Date().getTime();
		    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (currentChar) {
		        var randomChar = (currentDateMilliseconds + Math.random() * 16) % 16 | 0;
		        currentDateMilliseconds = Math.floor(currentDateMilliseconds / 16);
		        return (currentChar === 'x' ? randomChar : (randomChar & 0x7 | 0x8)).toString(16);
		    });
		};

		var create = function () {
			var guidFunc = _guid;	
			if ((typeof window) != 'undefined') {
				if ((typeof (window.crypto) != 'undefined') &&
					(typeof (window.crypto) != 'undefined')	) {
					guidFunc = _cryptoGuid;

				}
		    } 

		    return guidFunc;
		};

		return {
		    newGuid: create,
		    empty: EMPTY
		};
	})();	

	MavexUtils.prototype.newGuid = GUID.newGuid();
	MavexUtils.prototype.empty = GUID.empty;
// -------------------------------------------------------------------------
// export the constructor for local and remote usage

	if ((typeof module) === 'undefined') {
	    window.MavexUtils =  MavexUtils;
	} else {
	    module.exports =  MavexUtils;
	}

 })();
