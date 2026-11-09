
/*! jQuery v3.5.1 | (c) JS Foundation and other contributors | jquery.org/license */
!function(e,t){"use strict";"object"==typeof module&&"object"==typeof module.exports?module.exports=e.document?t(e,!0):function(e){if(!e.document)throw new Error("jQuery requires a window with a document");return t(e)}:t(e)}("undefined"!=typeof window?window:this,function(C,e){"use strict";var t=[],r=Object.getPrototypeOf,s=t.slice,g=t.flat?function(e){return t.flat.call(e)}:function(e){return t.concat.apply([],e)},u=t.push,i=t.indexOf,n={},o=n.toString,v=n.hasOwnProperty,a=v.toString,l=a.call(Object),y={},m=function(e){return"function"==typeof e&&"number"!=typeof e.nodeType},x=function(e){return null!=e&&e===e.window},E=C.document,c={type:!0,src:!0,nonce:!0,noModule:!0};function b(e,t,n){var r,i,o=(n=n||E).createElement("script");if(o.text=e,t)for(r in c)(i=t[r]||t.getAttribute&&t.getAttribute(r))&&o.setAttribute(r,i);n.head.appendChild(o).parentNode.removeChild(o)}function w(e){return null==e?e+"":"object"==typeof e||"function"==typeof e?n[o.call(e)]||"object":typeof e}var f="3.5.1",S=function(e,t){return new S.fn.init(e,t)};function p(e){var t=!!e&&"length"in e&&e.length,n=w(e);return!m(e)&&!x(e)&&("array"===n||0===t||"number"==typeof t&&0<t&&t-1 in e)}S.fn=S.prototype={jquery:f,constructor:S,length:0,toArray:function(){return s.call(this)},get:function(e){return null==e?s.call(this):e<0?this[e+this.length]:this[e]},pushStack:function(e){var t=S.merge(this.constructor(),e);return t.prevObject=this,t},each:function(e){return S.each(this,e)},map:function(n){return this.pushStack(S.map(this,function(e,t){return n.call(e,t,e)}))},slice:function(){return this.pushStack(s.apply(this,arguments))},first:function(){return this.eq(0)},last:function(){return this.eq(-1)},even:function(){return this.pushStack(S.grep(this,function(e,t){return(t+1)%2}))},odd:function(){return this.pushStack(S.grep(this,function(e,t){return t%2}))},eq:function(e){var t=this.length,n=+e+(e<0?t:0);return this.pushStack(0<=n&&n<t?[this[n]]:[])},end:function(){return this.prevObject||this.constructor()},push:u,sort:t.sort,splice:t.splice},S.extend=S.fn.extend=function(){var e,t,n,r,i,o,a=arguments[0]||{},s=1,u=arguments.length,l=!1;for("boolean"==typeof a&&(l=a,a=arguments[s]||{},s++),"object"==typeof a||m(a)||(a={}),s===u&&(a=this,s--);s<u;s++)if(null!=(e=arguments[s]))for(t in e)r=e[t],"__proto__"!==t&&a!==r&&(l&&r&&(S.isPlainObject(r)||(i=Array.isArray(r)))?(n=a[t],o=i&&!Array.isArray(n)?[]:i||S.isPlainObject(n)?n:{},i=!1,a[t]=S.extend(l,o,r)):void 0!==r&&(a[t]=r));return a},S.extend({expando:"jQuery"+(f+Math.random()).replace(/\D/g,""),isReady:!0,error:function(e){throw new Error(e)},noop:function(){},isPlainObject:function(e){var t,n;return!(!e||"[object Object]"!==o.call(e))&&(!(t=r(e))||"function"==typeof(n=v.call(t,"constructor")&&t.constructor)&&a.call(n)===l)},isEmptyObject:function(e){var t;for(t in e)return!1;return!0},globalEval:function(e,t,n){b(e,{nonce:t&&t.nonce},n)},each:function(e,t){var n,r=0;if(p(e)){for(n=e.length;r<n;r++)if(!1===t.call(e[r],r,e[r]))break}else for(r in e)if(!1===t.call(e[r],r,e[r]))break;return e},makeArray:function(e,t){var n=t||[];return null!=e&&(p(Object(e))?S.merge(n,"string"==typeof e?[e]:e):u.call(n,e)),n},inArray:function(e,t,n){return null==t?-1:i.call(t,e,n)},merge:function(e,t){for(var n=+t.length,r=0,i=e.length;r<n;r++)e[i++]=t[r];return e.length=i,e},grep:function(e,t,n){for(var r=[],i=0,o=e.length,a=!n;i<o;i++)!t(e[i],i)!==a&&r.push(e[i]);return r},map:function(e,t,n){var r,i,o=0,a=[];if(p(e))for(r=e.length;o<r;o++)null!=(i=t(e[o],o,n))&&a.push(i);else for(o in e)null!=(i=t(e[o],o,n))&&a.push(i);return g(a)},guid:1,support:y}),"function"==typeof Symbol&&(S.fn[Symbol.iterator]=t[Symbol.iterator]),S.each("Boolean Number String Function Array Date RegExp Object Error Symbol".split(" "),function(e,t){n["[object "+t+"]"]=t.toLowerCase()});var d=function(n){var e,d,b,o,i,h,f,g,w,u,l,T,C,a,E,v,s,c,y,S="sizzle"+1*new Date,p=n.document,k=0,r=0,m=ue(),x=ue(),A=ue(),N=ue(),D=function(e,t){return e===t&&(l=!0),0},j={}.hasOwnProperty,t=[],q=t.pop,L=t.push,H=t.push,O=t.slice,P=function(e,t){for(var n=0,r=e.length;n<r;n++)if(e[n]===t)return n;return-1},R="checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped",M="[\\x20\\t\\r\\n\\f]",I="(?:\\\\[\\da-fA-F]{1,6}"+M+"?|\\\\[^\\r\\n\\f]|[\\w-]|[^\0-\\x7f])+",W="\\["+M+"*("+I+")(?:"+M+"*([*^$|!~]?=)"+M+"*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|("+I+"))|)"+M+"*\\]",F=":("+I+")(?:\\((('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|((?:\\\\.|[^\\\\()[\\]]|"+W+")*)|.*)\\)|)",B=new RegExp(M+"+","g"),$=new RegExp("^"+M+"+|((?:^|[^\\\\])(?:\\\\.)*)"+M+"+$","g"),_=new RegExp("^"+M+"*,"+M+"*"),z=new RegExp("^"+M+"*([>+~]|"+M+")"+M+"*"),U=new RegExp(M+"|>"),X=new RegExp(F),V=new RegExp("^"+I+"$"),G={ID:new RegExp("^#("+I+")"),CLASS:new RegExp("^\\.("+I+")"),TAG:new RegExp("^("+I+"|[*])"),ATTR:new RegExp("^"+W),PSEUDO:new RegExp("^"+F),CHILD:new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\("+M+"*(even|odd|(([+-]|)(\\d*)n|)"+M+"*(?:([+-]|)"+M+"*(\\d+)|))"+M+"*\\)|)","i"),bool:new RegExp("^(?:"+R+")$","i"),needsContext:new RegExp("^"+M+"*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\("+M+"*((?:-\\d)?\\d*)"+M+"*\\)|)(?=[^-]|$)","i")},Y=/HTML$/i,Q=/^(?:input|select|textarea|button)$/i,J=/^h\d$/i,K=/^[^{]+\{\s*\[native \w/,Z=/^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,ee=/[+~]/,te=new RegExp("\\\\[\\da-fA-F]{1,6}"+M+"?|\\\\([^\\r\\n\\f])","g"),ne=function(e,t){var n="0x"+e.slice(1)-65536;return t||(n<0?String.fromCharCode(n+65536):String.fromCharCode(n>>10|55296,1023&n|56320))},re=/([\0-\x1f\x7f]|^-?\d)|^-$|[^\0-\x1f\x7f-\uFFFF\w-]/g,ie=function(e,t){return t?"\0"===e?"\ufffd":e.slice(0,-1)+"\\"+e.charCodeAt(e.length-1).toString(16)+" ":"\\"+e},oe=function(){T()},ae=be(function(e){return!0===e.disabled&&"fieldset"===e.nodeName.toLowerCase()},{dir:"parentNode",next:"legend"});try{H.apply(t=O.call(p.childNodes),p.childNodes),t[p.childNodes.length].nodeType}catch(e){H={apply:t.length?function(e,t){L.apply(e,O.call(t))}:function(e,t){var n=e.length,r=0;while(e[n++]=t[r++]);e.length=n-1}}}function se(t,e,n,r){var i,o,a,s,u,l,c,f=e&&e.ownerDocument,p=e?e.nodeType:9;if(n=n||[],"string"!=typeof t||!t||1!==p&&9!==p&&11!==p)return n;if(!r&&(T(e),e=e||C,E)){if(11!==p&&(u=Z.exec(t)))if(i=u[1]){if(9===p){if(!(a=e.getElementById(i)))return n;if(a.id===i)return n.push(a),n}else if(f&&(a=f.getElementById(i))&&y(e,a)&&a.id===i)return n.push(a),n}else{if(u[2])return H.apply(n,e.getElementsByTagName(t)),n;if((i=u[3])&&d.getElementsByClassName&&e.getElementsByClassName)return H.apply(n,e.getElementsByClassName(i)),n}if(d.qsa&&!N[t+" "]&&(!v||!v.test(t))&&(1!==p||"object"!==e.nodeName.toLowerCase())){if(c=t,f=e,1===p&&(U.test(t)||z.test(t))){(f=ee.test(t)&&ye(e.parentNode)||e)===e&&d.scope||((s=e.getAttribute("id"))?s=s.replace(re,ie):e.setAttribute("id",s=S)),o=(l=h(t)).length;while(o--)l[o]=(s?"#"+s:":scope")+" "+xe(l[o]);c=l.join(",")}try{return H.apply(n,f.querySelectorAll(c)),n}catch(e){N(t,!0)}finally{s===S&&e.removeAttribute("id")}}}return g(t.replace($,"$1"),e,n,r)}function ue(){var r=[];return function e(t,n){return r.push(t+" ")>b.cacheLength&&delete e[r.shift()],e[t+" "]=n}}function le(e){return e[S]=!0,e}function ce(e){var t=C.createElement("fieldset");try{return!!e(t)}catch(e){return!1}finally{t.parentNode&&t.parentNode.removeChild(t),t=null}}function fe(e,t){var n=e.split("|"),r=n.length;while(r--)b.attrHandle[n[r]]=t}function pe(e,t){var n=t&&e,r=n&&1===e.nodeType&&1===t.nodeType&&e.sourceIndex-t.sourceIndex;if(r)return r;if(n)while(n=n.nextSibling)if(n===t)return-1;return e?1:-1}function de(t){return function(e){return"input"===e.nodeName.toLowerCase()&&e.type===t}}function he(n){return function(e){var t=e.nodeName.toLowerCase();return("input"===t||"button"===t)&&e.type===n}}function ge(t){return function(e){return"form"in e?e.parentNode&&!1===e.disabled?"label"in e?"label"in e.parentNode?e.parentNode.disabled===t:e.disabled===t:e.isDisabled===t||e.isDisabled!==!t&&ae(e)===t:e.disabled===t:"label"in e&&e.disabled===t}}function ve(a){return le(function(o){return o=+o,le(function(e,t){var n,r=a([],e.length,o),i=r.length;while(i--)e[n=r[i]]&&(e[n]=!(t[n]=e[n]))})})}function ye(e){return e&&"undefined"!=typeof e.getElementsByTagName&&e}for(e in d=se.support={},i=se.isXML=function(e){var t=e.namespaceURI,n=(e.ownerDocument||e).documentElement;return!Y.test(t||n&&n.nodeName||"HTML")},T=se.setDocument=function(e){var t,n,r=e?e.ownerDocument||e:p;return r!=C&&9===r.nodeType&&r.documentElement&&(a=(C=r).documentElement,E=!i(C),p!=C&&(n=C.defaultView)&&n.top!==n&&(n.addEventListener?n.addEventListener("unload",oe,!1):n.attachEvent&&n.attachEvent("onunload",oe)),d.scope=ce(function(e){return a.appendChild(e).appendChild(C.createElement("div")),"undefined"!=typeof e.querySelectorAll&&!e.querySelectorAll(":scope fieldset div").length}),d.attributes=ce(function(e){return e.className="i",!e.getAttribute("className")}),d.getElementsByTagName=ce(function(e){return e.appendChild(C.createComment("")),!e.getElementsByTagName("*").length}),d.getElementsByClassName=K.test(C.getElementsByClassName),d.getById=ce(function(e){return a.appendChild(e).id=S,!C.getElementsByName||!C.getElementsByName(S).length}),d.getById?(b.filter.ID=function(e){var t=e.replace(te,ne);return function(e){return e.getAttribute("id")===t}},b.find.ID=function(e,t){if("undefined"!=typeof t.getElementById&&E){var n=t.getElementById(e);return n?[n]:[]}}):(b.filter.ID=function(e){var n=e.replace(te,ne);return function(e){var t="undefined"!=typeof e.getAttributeNode&&e.getAttributeNode("id");return t&&t.value===n}},b.find.ID=function(e,t){if("undefined"!=typeof t.getElementById&&E){var n,r,i,o=t.getElementById(e);if(o){if((n=o.getAttributeNode("id"))&&n.value===e)return[o];i=t.getElementsByName(e),r=0;while(o=i[r++])if((n=o.getAttributeNode("id"))&&n.value===e)return[o]}return[]}}),b.find.TAG=d.getElementsByTagName?function(e,t){return"undefined"!=typeof t.getElementsByTagName?t.getElementsByTagName(e):d.qsa?t.querySelectorAll(e):void 0}:function(e,t){var n,r=[],i=0,o=t.getElementsByTagName(e);if("*"===e){while(n=o[i++])1===n.nodeType&&r.push(n);return r}return o},b.find.CLASS=d.getElementsByClassName&&function(e,t){if("undefined"!=typeof t.getElementsByClassName&&E)return t.getElementsByClassName(e)},s=[],v=[],(d.qsa=K.test(C.querySelectorAll))&&(ce(function(e){var t;a.appendChild(e).innerHTML="<a id='"+S+"'></a><select id='"+S+"-\r\\' msallowcapture=''><option selected=''></option></select>",e.querySelectorAll("[msallowcapture^='']").length&&v.push("[*^$]="+M+"*(?:''|\"\")"),e.querySelectorAll("[selected]").length||v.push("\\["+M+"*(?:value|"+R+")"),e.querySelectorAll("[id~="+S+"-]").length||v.push("~="),(t=C.createElement("input")).setAttribute("name",""),e.appendChild(t),e.querySelectorAll("[name='']").length||v.push("\\["+M+"*name"+M+"*="+M+"*(?:''|\"\")"),e.querySelectorAll(":checked").length||v.push(":checked"),e.querySelectorAll("a#"+S+"+*").length||v.push(".#.+[+~]"),e.querySelectorAll("\\\f"),v.push("[\\r\\n\\f]")}),ce(function(e){e.innerHTML="<a href='' disabled='disabled'></a><select disabled='disabled'><option/></select>";var t=C.createElement("input");t.setAttribute("type","hidden"),e.appendChild(t).setAttribute("name","D"),e.querySelectorAll("[name=d]").length&&v.push("name"+M+"*[*^$|!~]?="),2!==e.querySelectorAll(":enabled").length&&v.push(":enabled",":disabled"),a.appendChild(e).disabled=!0,2!==e.querySelectorAll(":disabled").length&&v.push(":enabled",":disabled"),e.querySelectorAll("*,:x"),v.push(",.*:")})),(d.matchesSelector=K.test(c=a.matches||a.webkitMatchesSelector||a.mozMatchesSelector||a.oMatchesSelector||a.msMatchesSelector))&&ce(function(e){d.disconnectedMatch=c.call(e,"*"),c.call(e,"[s!='']:x"),s.push("!=",F)}),v=v.length&&new RegExp(v.join("|")),s=s.length&&new RegExp(s.join("|")),t=K.test(a.compareDocumentPosition),y=t||K.test(a.contains)?function(e,t){var n=9===e.nodeType?e.documentElement:e,r=t&&t.parentNode;return e===r||!(!r||1!==r.nodeType||!(n.contains?n.contains(r):e.compareDocumentPosition&&16&e.compareDocumentPosition(r)))}:function(e,t){if(t)while(t=t.parentNode)if(t===e)return!0;return!1},D=t?function(e,t){if(e===t)return l=!0,0;var n=!e.compareDocumentPosition-!t.compareDocumentPosition;return n||(1&(n=(e.ownerDocument||e)==(t.ownerDocument||t)?e.compareDocumentPosition(t):1)||!d.sortDetached&&t.compareDocumentPosition(e)===n?e==C||e.ownerDocument==p&&y(p,e)?-1:t==C||t.ownerDocument==p&&y(p,t)?1:u?P(u,e)-P(u,t):0:4&n?-1:1)}:function(e,t){if(e===t)return l=!0,0;var n,r=0,i=e.parentNode,o=t.parentNode,a=[e],s=[t];if(!i||!o)return e==C?-1:t==C?1:i?-1:o?1:u?P(u,e)-P(u,t):0;if(i===o)return pe(e,t);n=e;while(n=n.parentNode)a.unshift(n);n=t;while(n=n.parentNode)s.unshift(n);while(a[r]===s[r])r++;return r?pe(a[r],s[r]):a[r]==p?-1:s[r]==p?1:0}),C},se.matches=function(e,t){return se(e,null,null,t)},se.matchesSelector=function(e,t){if(T(e),d.matchesSelector&&E&&!N[t+" "]&&(!s||!s.test(t))&&(!v||!v.test(t)))try{var n=c.call(e,t);if(n||d.disconnectedMatch||e.document&&11!==e.document.nodeType)return n}catch(e){N(t,!0)}return 0<se(t,C,null,[e]).length},se.contains=function(e,t){return(e.ownerDocument||e)!=C&&T(e),y(e,t)},se.attr=function(e,t){(e.ownerDocument||e)!=C&&T(e);var n=b.attrHandle[t.toLowerCase()],r=n&&j.call(b.attrHandle,t.toLowerCase())?n(e,t,!E):void 0;return void 0!==r?r:d.attributes||!E?e.getAttribute(t):(r=e.getAttributeNode(t))&&r.specified?r.value:null},se.escape=function(e){return(e+"").replace(re,ie)},se.error=function(e){throw new Error("Syntax error, unrecognized expression: "+e)},se.uniqueSort=function(e){var t,n=[],r=0,i=0;if(l=!d.detectDuplicates,u=!d.sortStable&&e.slice(0),e.sort(D),l){while(t=e[i++])t===e[i]&&(r=n.push(i));while(r--)e.splice(n[r],1)}return u=null,e},o=se.getText=function(e){var t,n="",r=0,i=e.nodeType;if(i){if(1===i||9===i||11===i){if("string"==typeof e.textContent)return e.textContent;for(e=e.firstChild;e;e=e.nextSibling)n+=o(e)}else if(3===i||4===i)return e.nodeValue}else while(t=e[r++])n+=o(t);return n},(b=se.selectors={cacheLength:50,createPseudo:le,match:G,attrHandle:{},find:{},relative:{">":{dir:"parentNode",first:!0}," ":{dir:"parentNode"},"+":{dir:"previousSibling",first:!0},"~":{dir:"previousSibling"}},preFilter:{ATTR:function(e){return e[1]=e[1].replace(te,ne),e[3]=(e[3]||e[4]||e[5]||"").replace(te,ne),"~="===e[2]&&(e[3]=" "+e[3]+" "),e.slice(0,4)},CHILD:function(e){return e[1]=e[1].toLowerCase(),"nth"===e[1].slice(0,3)?(e[3]||se.error(e[0]),e[4]=+(e[4]?e[5]+(e[6]||1):2*("even"===e[3]||"odd"===e[3])),e[5]=+(e[7]+e[8]||"odd"===e[3])):e[3]&&se.error(e[0]),e},PSEUDO:function(e){var t,n=!e[6]&&e[2];return G.CHILD.test(e[0])?null:(e[3]?e[2]=e[4]||e[5]||"":n&&X.test(n)&&(t=h(n,!0))&&(t=n.indexOf(")",n.length-t)-n.length)&&(e[0]=e[0].slice(0,t),e[2]=n.slice(0,t)),e.slice(0,3))}},filter:{TAG:function(e){var t=e.replace(te,ne).toLowerCase();return"*"===e?function(){return!0}:function(e){return e.nodeName&&e.nodeName.toLowerCase()===t}},CLASS:function(e){var t=m[e+" "];return t||(t=new RegExp("(^|"+M+")"+e+"("+M+"|$)"))&&m(e,function(e){return t.test("string"==typeof e.className&&e.className||"undefined"!=typeof e.getAttribute&&e.getAttribute("class")||"")})},ATTR:function(n,r,i){return function(e){var t=se.attr(e,n);return null==t?"!="===r:!r||(t+="","="===r?t===i:"!="===r?t!==i:"^="===r?i&&0===t.indexOf(i):"*="===r?i&&-1<t.indexOf(i):"$="===r?i&&t.slice(-i.length)===i:"~="===r?-1<(" "+t.replace(B," ")+" ").indexOf(i):"|="===r&&(t===i||t.slice(0,i.length+1)===i+"-"))}},CHILD:function(h,e,t,g,v){var y="nth"!==h.slice(0,3),m="last"!==h.slice(-4),x="of-type"===e;return 1===g&&0===v?function(e){return!!e.parentNode}:function(e,t,n){var r,i,o,a,s,u,l=y!==m?"nextSibling":"previousSibling",c=e.parentNode,f=x&&e.nodeName.toLowerCase(),p=!n&&!x,d=!1;if(c){if(y){while(l){a=e;while(a=a[l])if(x?a.nodeName.toLowerCase()===f:1===a.nodeType)return!1;u=l="only"===h&&!u&&"nextSibling"}return!0}if(u=[m?c.firstChild:c.lastChild],m&&p){d=(s=(r=(i=(o=(a=c)[S]||(a[S]={}))[a.uniqueID]||(o[a.uniqueID]={}))[h]||[])[0]===k&&r[1])&&r[2],a=s&&c.childNodes[s];while(a=++s&&a&&a[l]||(d=s=0)||u.pop())if(1===a.nodeType&&++d&&a===e){i[h]=[k,s,d];break}}else if(p&&(d=s=(r=(i=(o=(a=e)[S]||(a[S]={}))[a.uniqueID]||(o[a.uniqueID]={}))[h]||[])[0]===k&&r[1]),!1===d)while(a=++s&&a&&a[l]||(d=s=0)||u.pop())if((x?a.nodeName.toLowerCase()===f:1===a.nodeType)&&++d&&(p&&((i=(o=a[S]||(a[S]={}))[a.uniqueID]||(o[a.uniqueID]={}))[h]=[k,d]),a===e))break;return(d-=v)===g||d%g==0&&0<=d/g}}},PSEUDO:function(e,o){var t,a=b.pseudos[e]||b.setFilters[e.toLowerCase()]||se.error("unsupported pseudo: "+e);return a[S]?a(o):1<a.length?(t=[e,e,"",o],b.setFilters.hasOwnProperty(e.toLowerCase())?le(function(e,t){var n,r=a(e,o),i=r.length;while(i--)e[n=P(e,r[i])]=!(t[n]=r[i])}):function(e){return a(e,0,t)}):a}},pseudos:{not:le(function(e){var r=[],i=[],s=f(e.replace($,"$1"));return s[S]?le(function(e,t,n,r){var i,o=s(e,null,r,[]),a=e.length;while(a--)(i=o[a])&&(e[a]=!(t[a]=i))}):function(e,t,n){return r[0]=e,s(r,null,n,i),r[0]=null,!i.pop()}}),has:le(function(t){return function(e){return 0<se(t,e).length}}),contains:le(function(t){return t=t.replace(te,ne),function(e){return-1<(e.textContent||o(e)).indexOf(t)}}),lang:le(function(n){return V.test(n||"")||se.error("unsupported lang: "+n),n=n.replace(te,ne).toLowerCase(),function(e){var t;do{if(t=E?e.lang:e.getAttribute("xml:lang")||e.getAttribute("lang"))return(t=t.toLowerCase())===n||0===t.indexOf(n+"-")}while((e=e.parentNode)&&1===e.nodeType);return!1}}),target:function(e){var t=n.location&&n.location.hash;return t&&t.slice(1)===e.id},root:function(e){return e===a},focus:function(e){return e===C.activeElement&&(!C.hasFocus||C.hasFocus())&&!!(e.type||e.href||~e.tabIndex)},enabled:ge(!1),disabled:ge(!0),checked:function(e){var t=e.nodeName.toLowerCase();return"input"===t&&!!e.checked||"option"===t&&!!e.selected},selected:function(e){return e.parentNode&&e.parentNode.selectedIndex,!0===e.selected},empty:function(e){for(e=e.firstChild;e;e=e.nextSibling)if(e.nodeType<6)return!1;return!0},parent:function(e){return!b.pseudos.empty(e)},header:function(e){return J.test(e.nodeName)},input:function(e){return Q.test(e.nodeName)},button:function(e){var t=e.nodeName.toLowerCase();return"input"===t&&"button"===e.type||"button"===t},text:function(e){var t;return"input"===e.nodeName.toLowerCase()&&"text"===e.type&&(null==(t=e.getAttribute("type"))||"text"===t.toLowerCase())},first:ve(function(){return[0]}),last:ve(function(e,t){return[t-1]}),eq:ve(function(e,t,n){return[n<0?n+t:n]}),even:ve(function(e,t){for(var n=0;n<t;n+=2)e.push(n);return e}),odd:ve(function(e,t){for(var n=1;n<t;n+=2)e.push(n);return e}),lt:ve(function(e,t,n){for(var r=n<0?n+t:t<n?t:n;0<=--r;)e.push(r);return e}),gt:ve(function(e,t,n){for(var r=n<0?n+t:n;++r<t;)e.push(r);return e})}}).pseudos.nth=b.pseudos.eq,{radio:!0,checkbox:!0,file:!0,password:!0,image:!0})b.pseudos[e]=de(e);for(e in{submit:!0,reset:!0})b.pseudos[e]=he(e);function me(){}function xe(e){for(var t=0,n=e.length,r="";t<n;t++)r+=e[t].value;return r}function be(s,e,t){var u=e.dir,l=e.next,c=l||u,f=t&&"parentNode"===c,p=r++;return e.first?function(e,t,n){while(e=e[u])if(1===e.nodeType||f)return s(e,t,n);return!1}:function(e,t,n){var r,i,o,a=[k,p];if(n){while(e=e[u])if((1===e.nodeType||f)&&s(e,t,n))return!0}else while(e=e[u])if(1===e.nodeType||f)if(i=(o=e[S]||(e[S]={}))[e.uniqueID]||(o[e.uniqueID]={}),l&&l===e.nodeName.toLowerCase())e=e[u]||e;else{if((r=i[c])&&r[0]===k&&r[1]===p)return a[2]=r[2];if((i[c]=a)[2]=s(e,t,n))return!0}return!1}}function we(i){return 1<i.length?function(e,t,n){var r=i.length;while(r--)if(!i[r](e,t,n))return!1;return!0}:i[0]}function Te(e,t,n,r,i){for(var o,a=[],s=0,u=e.length,l=null!=t;s<u;s++)(o=e[s])&&(n&&!n(o,r,i)||(a.push(o),l&&t.push(s)));return a}function Ce(d,h,g,v,y,e){return v&&!v[S]&&(v=Ce(v)),y&&!y[S]&&(y=Ce(y,e)),le(function(e,t,n,r){var i,o,a,s=[],u=[],l=t.length,c=e||function(e,t,n){for(var r=0,i=t.length;r<i;r++)se(e,t[r],n);return n}(h||"*",n.nodeType?[n]:n,[]),f=!d||!e&&h?c:Te(c,s,d,n,r),p=g?y||(e?d:l||v)?[]:t:f;if(g&&g(f,p,n,r),v){i=Te(p,u),v(i,[],n,r),o=i.length;while(o--)(a=i[o])&&(p[u[o]]=!(f[u[o]]=a))}if(e){if(y||d){if(y){i=[],o=p.length;while(o--)(a=p[o])&&i.push(f[o]=a);y(null,p=[],i,r)}o=p.length;while(o--)(a=p[o])&&-1<(i=y?P(e,a):s[o])&&(e[i]=!(t[i]=a))}}else p=Te(p===t?p.splice(l,p.length):p),y?y(null,t,p,r):H.apply(t,p)})}function Ee(e){for(var i,t,n,r=e.length,o=b.relative[e[0].type],a=o||b.relative[" "],s=o?1:0,u=be(function(e){return e===i},a,!0),l=be(function(e){return-1<P(i,e)},a,!0),c=[function(e,t,n){var r=!o&&(n||t!==w)||((i=t).nodeType?u(e,t,n):l(e,t,n));return i=null,r}];s<r;s++)if(t=b.relative[e[s].type])c=[be(we(c),t)];else{if((t=b.filter[e[s].type].apply(null,e[s].matches))[S]){for(n=++s;n<r;n++)if(b.relative[e[n].type])break;return Ce(1<s&&we(c),1<s&&xe(e.slice(0,s-1).concat({value:" "===e[s-2].type?"*":""})).replace($,"$1"),t,s<n&&Ee(e.slice(s,n)),n<r&&Ee(e=e.slice(n)),n<r&&xe(e))}c.push(t)}return we(c)}return me.prototype=b.filters=b.pseudos,b.setFilters=new me,h=se.tokenize=function(e,t){var n,r,i,o,a,s,u,l=x[e+" "];if(l)return t?0:l.slice(0);a=e,s=[],u=b.preFilter;while(a){for(o in n&&!(r=_.exec(a))||(r&&(a=a.slice(r[0].length)||a),s.push(i=[])),n=!1,(r=z.exec(a))&&(n=r.shift(),i.push({value:n,type:r[0].replace($," ")}),a=a.slice(n.length)),b.filter)!(r=G[o].exec(a))||u[o]&&!(r=u[o](r))||(n=r.shift(),i.push({value:n,type:o,matches:r}),a=a.slice(n.length));if(!n)break}return t?a.length:a?se.error(e):x(e,s).slice(0)},f=se.compile=function(e,t){var n,v,y,m,x,r,i=[],o=[],a=A[e+" "];if(!a){t||(t=h(e)),n=t.length;while(n--)(a=Ee(t[n]))[S]?i.push(a):o.push(a);(a=A(e,(v=o,m=0<(y=i).length,x=0<v.length,r=function(e,t,n,r,i){var o,a,s,u=0,l="0",c=e&&[],f=[],p=w,d=e||x&&b.find.TAG("*",i),h=k+=null==p?1:Math.random()||.1,g=d.length;for(i&&(w=t==C||t||i);l!==g&&null!=(o=d[l]);l++){if(x&&o){a=0,t||o.ownerDocument==C||(T(o),n=!E);while(s=v[a++])if(s(o,t||C,n)){r.push(o);break}i&&(k=h)}m&&((o=!s&&o)&&u--,e&&c.push(o))}if(u+=l,m&&l!==u){a=0;while(s=y[a++])s(c,f,t,n);if(e){if(0<u)while(l--)c[l]||f[l]||(f[l]=q.call(r));f=Te(f)}H.apply(r,f),i&&!e&&0<f.length&&1<u+y.length&&se.uniqueSort(r)}return i&&(k=h,w=p),c},m?le(r):r))).selector=e}return a},g=se.select=function(e,t,n,r){var i,o,a,s,u,l="function"==typeof e&&e,c=!r&&h(e=l.selector||e);if(n=n||[],1===c.length){if(2<(o=c[0]=c[0].slice(0)).length&&"ID"===(a=o[0]).type&&9===t.nodeType&&E&&b.relative[o[1].type]){if(!(t=(b.find.ID(a.matches[0].replace(te,ne),t)||[])[0]))return n;l&&(t=t.parentNode),e=e.slice(o.shift().value.length)}i=G.needsContext.test(e)?0:o.length;while(i--){if(a=o[i],b.relative[s=a.type])break;if((u=b.find[s])&&(r=u(a.matches[0].replace(te,ne),ee.test(o[0].type)&&ye(t.parentNode)||t))){if(o.splice(i,1),!(e=r.length&&xe(o)))return H.apply(n,r),n;break}}}return(l||f(e,c))(r,t,!E,n,!t||ee.test(e)&&ye(t.parentNode)||t),n},d.sortStable=S.split("").sort(D).join("")===S,d.detectDuplicates=!!l,T(),d.sortDetached=ce(function(e){return 1&e.compareDocumentPosition(C.createElement("fieldset"))}),ce(function(e){return e.innerHTML="<a href='#'></a>","#"===e.firstChild.getAttribute("href")})||fe("type|href|height|width",function(e,t,n){if(!n)return e.getAttribute(t,"type"===t.toLowerCase()?1:2)}),d.attributes&&ce(function(e){return e.innerHTML="<input/>",e.firstChild.setAttribute("value",""),""===e.firstChild.getAttribute("value")})||fe("value",function(e,t,n){if(!n&&"input"===e.nodeName.toLowerCase())return e.defaultValue}),ce(function(e){return null==e.getAttribute("disabled")})||fe(R,function(e,t,n){var r;if(!n)return!0===e[t]?t.toLowerCase():(r=e.getAttributeNode(t))&&r.specified?r.value:null}),se}(C);S.find=d,S.expr=d.selectors,S.expr[":"]=S.expr.pseudos,S.uniqueSort=S.unique=d.uniqueSort,S.text=d.getText,S.isXMLDoc=d.isXML,S.contains=d.contains,S.escapeSelector=d.escape;var h=function(e,t,n){var r=[],i=void 0!==n;while((e=e[t])&&9!==e.nodeType)if(1===e.nodeType){if(i&&S(e).is(n))break;r.push(e)}return r},T=function(e,t){for(var n=[];e;e=e.nextSibling)1===e.nodeType&&e!==t&&n.push(e);return n},k=S.expr.match.needsContext;function A(e,t){return e.nodeName&&e.nodeName.toLowerCase()===t.toLowerCase()}var N=/^<([a-z][^\/\0>:\x20\t\r\n\f]*)[\x20\t\r\n\f]*\/?>(?:<\/\1>|)$/i;function D(e,n,r){return m(n)?S.grep(e,function(e,t){return!!n.call(e,t,e)!==r}):n.nodeType?S.grep(e,function(e){return e===n!==r}):"string"!=typeof n?S.grep(e,function(e){return-1<i.call(n,e)!==r}):S.filter(n,e,r)}S.filter=function(e,t,n){var r=t[0];return n&&(e=":not("+e+")"),1===t.length&&1===r.nodeType?S.find.matchesSelector(r,e)?[r]:[]:S.find.matches(e,S.grep(t,function(e){return 1===e.nodeType}))},S.fn.extend({find:function(e){var t,n,r=this.length,i=this;if("string"!=typeof e)return this.pushStack(S(e).filter(function(){for(t=0;t<r;t++)if(S.contains(i[t],this))return!0}));for(n=this.pushStack([]),t=0;t<r;t++)S.find(e,i[t],n);return 1<r?S.uniqueSort(n):n},filter:function(e){return this.pushStack(D(this,e||[],!1))},not:function(e){return this.pushStack(D(this,e||[],!0))},is:function(e){return!!D(this,"string"==typeof e&&k.test(e)?S(e):e||[],!1).length}});var j,q=/^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]+))$/;(S.fn.init=function(e,t,n){var r,i;if(!e)return this;if(n=n||j,"string"==typeof e){if(!(r="<"===e[0]&&">"===e[e.length-1]&&3<=e.length?[null,e,null]:q.exec(e))||!r[1]&&t)return!t||t.jquery?(t||n).find(e):this.constructor(t).find(e);if(r[1]){if(t=t instanceof S?t[0]:t,S.merge(this,S.parseHTML(r[1],t&&t.nodeType?t.ownerDocument||t:E,!0)),N.test(r[1])&&S.isPlainObject(t))for(r in t)m(this[r])?this[r](t[r]):this.attr(r,t[r]);return this}return(i=E.getElementById(r[2]))&&(this[0]=i,this.length=1),this}return e.nodeType?(this[0]=e,this.length=1,this):m(e)?void 0!==n.ready?n.ready(e):e(S):S.makeArray(e,this)}).prototype=S.fn,j=S(E);var L=/^(?:parents|prev(?:Until|All))/,H={children:!0,contents:!0,next:!0,prev:!0};function O(e,t){while((e=e[t])&&1!==e.nodeType);return e}S.fn.extend({has:function(e){var t=S(e,this),n=t.length;return this.filter(function(){for(var e=0;e<n;e++)if(S.contains(this,t[e]))return!0})},closest:function(e,t){var n,r=0,i=this.length,o=[],a="string"!=typeof e&&S(e);if(!k.test(e))for(;r<i;r++)for(n=this[r];n&&n!==t;n=n.parentNode)if(n.nodeType<11&&(a?-1<a.index(n):1===n.nodeType&&S.find.matchesSelector(n,e))){o.push(n);break}return this.pushStack(1<o.length?S.uniqueSort(o):o)},index:function(e){return e?"string"==typeof e?i.call(S(e),this[0]):i.call(this,e.jquery?e[0]:e):this[0]&&this[0].parentNode?this.first().prevAll().length:-1},add:function(e,t){return this.pushStack(S.uniqueSort(S.merge(this.get(),S(e,t))))},addBack:function(e){return this.add(null==e?this.prevObject:this.prevObject.filter(e))}}),S.each({parent:function(e){var t=e.parentNode;return t&&11!==t.nodeType?t:null},parents:function(e){return h(e,"parentNode")},parentsUntil:function(e,t,n){return h(e,"parentNode",n)},next:function(e){return O(e,"nextSibling")},prev:function(e){return O(e,"previousSibling")},nextAll:function(e){return h(e,"nextSibling")},prevAll:function(e){return h(e,"previousSibling")},nextUntil:function(e,t,n){return h(e,"nextSibling",n)},prevUntil:function(e,t,n){return h(e,"previousSibling",n)},siblings:function(e){return T((e.parentNode||{}).firstChild,e)},children:function(e){return T(e.firstChild)},contents:function(e){return null!=e.contentDocument&&r(e.contentDocument)?e.contentDocument:(A(e,"template")&&(e=e.content||e),S.merge([],e.childNodes))}},function(r,i){S.fn[r]=function(e,t){var n=S.map(this,i,e);return"Until"!==r.slice(-5)&&(t=e),t&&"string"==typeof t&&(n=S.filter(t,n)),1<this.length&&(H[r]||S.uniqueSort(n),L.test(r)&&n.reverse()),this.pushStack(n)}});var P=/[^\x20\t\r\n\f]+/g;function R(e){return e}function M(e){throw e}function I(e,t,n,r){var i;try{e&&m(i=e.promise)?i.call(e).done(t).fail(n):e&&m(i=e.then)?i.call(e,t,n):t.apply(void 0,[e].slice(r))}catch(e){n.apply(void 0,[e])}}S.Callbacks=function(r){var e,n;r="string"==typeof r?(e=r,n={},S.each(e.match(P)||[],function(e,t){n[t]=!0}),n):S.extend({},r);var i,t,o,a,s=[],u=[],l=-1,c=function(){for(a=a||r.once,o=i=!0;u.length;l=-1){t=u.shift();while(++l<s.length)!1===s[l].apply(t[0],t[1])&&r.stopOnFalse&&(l=s.length,t=!1)}r.memory||(t=!1),i=!1,a&&(s=t?[]:"")},f={add:function(){return s&&(t&&!i&&(l=s.length-1,u.push(t)),function n(e){S.each(e,function(e,t){m(t)?r.unique&&f.has(t)||s.push(t):t&&t.length&&"string"!==w(t)&&n(t)})}(arguments),t&&!i&&c()),this},remove:function(){return S.each(arguments,function(e,t){var n;while(-1<(n=S.inArray(t,s,n)))s.splice(n,1),n<=l&&l--}),this},has:function(e){return e?-1<S.inArray(e,s):0<s.length},empty:function(){return s&&(s=[]),this},disable:function(){return a=u=[],s=t="",this},disabled:function(){return!s},lock:function(){return a=u=[],t||i||(s=t=""),this},locked:function(){return!!a},fireWith:function(e,t){return a||(t=[e,(t=t||[]).slice?t.slice():t],u.push(t),i||c()),this},fire:function(){return f.fireWith(this,arguments),this},fired:function(){return!!o}};return f},S.extend({Deferred:function(e){var o=[["notify","progress",S.Callbacks("memory"),S.Callbacks("memory"),2],["resolve","done",S.Callbacks("once memory"),S.Callbacks("once memory"),0,"resolved"],["reject","fail",S.Callbacks("once memory"),S.Callbacks("once memory"),1,"rejected"]],i="pending",a={state:function(){return i},always:function(){return s.done(arguments).fail(arguments),this},"catch":function(e){return a.then(null,e)},pipe:function(){var i=arguments;return S.Deferred(function(r){S.each(o,function(e,t){var n=m(i[t[4]])&&i[t[4]];s[t[1]](function(){var e=n&&n.apply(this,arguments);e&&m(e.promise)?e.promise().progress(r.notify).done(r.resolve).fail(r.reject):r[t[0]+"With"](this,n?[e]:arguments)})}),i=null}).promise()},then:function(t,n,r){var u=0;function l(i,o,a,s){return function(){var n=this,r=arguments,e=function(){var e,t;if(!(i<u)){if((e=a.apply(n,r))===o.promise())throw new TypeError("Thenable self-resolution");t=e&&("object"==typeof e||"function"==typeof e)&&e.then,m(t)?s?t.call(e,l(u,o,R,s),l(u,o,M,s)):(u++,t.call(e,l(u,o,R,s),l(u,o,M,s),l(u,o,R,o.notifyWith))):(a!==R&&(n=void 0,r=[e]),(s||o.resolveWith)(n,r))}},t=s?e:function(){try{e()}catch(e){S.Deferred.exceptionHook&&S.Deferred.exceptionHook(e,t.stackTrace),u<=i+1&&(a!==M&&(n=void 0,r=[e]),o.rejectWith(n,r))}};i?t():(S.Deferred.getStackHook&&(t.stackTrace=S.Deferred.getStackHook()),C.setTimeout(t))}}return S.Deferred(function(e){o[0][3].add(l(0,e,m(r)?r:R,e.notifyWith)),o[1][3].add(l(0,e,m(t)?t:R)),o[2][3].add(l(0,e,m(n)?n:M))}).promise()},promise:function(e){return null!=e?S.extend(e,a):a}},s={};return S.each(o,function(e,t){var n=t[2],r=t[5];a[t[1]]=n.add,r&&n.add(function(){i=r},o[3-e][2].disable,o[3-e][3].disable,o[0][2].lock,o[0][3].lock),n.add(t[3].fire),s[t[0]]=function(){return s[t[0]+"With"](this===s?void 0:this,arguments),this},s[t[0]+"With"]=n.fireWith}),a.promise(s),e&&e.call(s,s),s},when:function(e){var n=arguments.length,t=n,r=Array(t),i=s.call(arguments),o=S.Deferred(),a=function(t){return function(e){r[t]=this,i[t]=1<arguments.length?s.call(arguments):e,--n||o.resolveWith(r,i)}};if(n<=1&&(I(e,o.done(a(t)).resolve,o.reject,!n),"pending"===o.state()||m(i[t]&&i[t].then)))return o.then();while(t--)I(i[t],a(t),o.reject);return o.promise()}});var W=/^(Eval|Internal|Range|Reference|Syntax|Type|URI)Error$/;S.Deferred.exceptionHook=function(e,t){C.console&&C.console.warn&&e&&W.test(e.name)&&C.console.warn("jQuery.Deferred exception: "+e.message,e.stack,t)},S.readyException=function(e){C.setTimeout(function(){throw e})};var F=S.Deferred();function B(){E.removeEventListener("DOMContentLoaded",B),C.removeEventListener("load",B),S.ready()}S.fn.ready=function(e){return F.then(e)["catch"](function(e){S.readyException(e)}),this},S.extend({isReady:!1,readyWait:1,ready:function(e){(!0===e?--S.readyWait:S.isReady)||(S.isReady=!0)!==e&&0<--S.readyWait||F.resolveWith(E,[S])}}),S.ready.then=F.then,"complete"===E.readyState||"loading"!==E.readyState&&!E.documentElement.doScroll?C.setTimeout(S.ready):(E.addEventListener("DOMContentLoaded",B),C.addEventListener("load",B));var $=function(e,t,n,r,i,o,a){var s=0,u=e.length,l=null==n;if("object"===w(n))for(s in i=!0,n)$(e,t,s,n[s],!0,o,a);else if(void 0!==r&&(i=!0,m(r)||(a=!0),l&&(a?(t.call(e,r),t=null):(l=t,t=function(e,t,n){return l.call(S(e),n)})),t))for(;s<u;s++)t(e[s],n,a?r:r.call(e[s],s,t(e[s],n)));return i?e:l?t.call(e):u?t(e[0],n):o},_=/^-ms-/,z=/-([a-z])/g;function U(e,t){return t.toUpperCase()}function X(e){return e.replace(_,"ms-").replace(z,U)}var V=function(e){return 1===e.nodeType||9===e.nodeType||!+e.nodeType};function G(){this.expando=S.expando+G.uid++}G.uid=1,G.prototype={cache:function(e){var t=e[this.expando];return t||(t={},V(e)&&(e.nodeType?e[this.expando]=t:Object.defineProperty(e,this.expando,{value:t,configurable:!0}))),t},set:function(e,t,n){var r,i=this.cache(e);if("string"==typeof t)i[X(t)]=n;else for(r in t)i[X(r)]=t[r];return i},get:function(e,t){return void 0===t?this.cache(e):e[this.expando]&&e[this.expando][X(t)]},access:function(e,t,n){return void 0===t||t&&"string"==typeof t&&void 0===n?this.get(e,t):(this.set(e,t,n),void 0!==n?n:t)},remove:function(e,t){var n,r=e[this.expando];if(void 0!==r){if(void 0!==t){n=(t=Array.isArray(t)?t.map(X):(t=X(t))in r?[t]:t.match(P)||[]).length;while(n--)delete r[t[n]]}(void 0===t||S.isEmptyObject(r))&&(e.nodeType?e[this.expando]=void 0:delete e[this.expando])}},hasData:function(e){var t=e[this.expando];return void 0!==t&&!S.isEmptyObject(t)}};var Y=new G,Q=new G,J=/^(?:\{[\w\W]*\}|\[[\w\W]*\])$/,K=/[A-Z]/g;function Z(e,t,n){var r,i;if(void 0===n&&1===e.nodeType)if(r="data-"+t.replace(K,"-$&").toLowerCase(),"string"==typeof(n=e.getAttribute(r))){try{n="true"===(i=n)||"false"!==i&&("null"===i?null:i===+i+""?+i:J.test(i)?JSON.parse(i):i)}catch(e){}Q.set(e,t,n)}else n=void 0;return n}S.extend({hasData:function(e){return Q.hasData(e)||Y.hasData(e)},data:function(e,t,n){return Q.access(e,t,n)},removeData:function(e,t){Q.remove(e,t)},_data:function(e,t,n){return Y.access(e,t,n)},_removeData:function(e,t){Y.remove(e,t)}}),S.fn.extend({data:function(n,e){var t,r,i,o=this[0],a=o&&o.attributes;if(void 0===n){if(this.length&&(i=Q.get(o),1===o.nodeType&&!Y.get(o,"hasDataAttrs"))){t=a.length;while(t--)a[t]&&0===(r=a[t].name).indexOf("data-")&&(r=X(r.slice(5)),Z(o,r,i[r]));Y.set(o,"hasDataAttrs",!0)}return i}return"object"==typeof n?this.each(function(){Q.set(this,n)}):$(this,function(e){var t;if(o&&void 0===e)return void 0!==(t=Q.get(o,n))?t:void 0!==(t=Z(o,n))?t:void 0;this.each(function(){Q.set(this,n,e)})},null,e,1<arguments.length,null,!0)},removeData:function(e){return this.each(function(){Q.remove(this,e)})}}),S.extend({queue:function(e,t,n){var r;if(e)return t=(t||"fx")+"queue",r=Y.get(e,t),n&&(!r||Array.isArray(n)?r=Y.access(e,t,S.makeArray(n)):r.push(n)),r||[]},dequeue:function(e,t){t=t||"fx";var n=S.queue(e,t),r=n.length,i=n.shift(),o=S._queueHooks(e,t);"inprogress"===i&&(i=n.shift(),r--),i&&("fx"===t&&n.unshift("inprogress"),delete o.stop,i.call(e,function(){S.dequeue(e,t)},o)),!r&&o&&o.empty.fire()},_queueHooks:function(e,t){var n=t+"queueHooks";return Y.get(e,n)||Y.access(e,n,{empty:S.Callbacks("once memory").add(function(){Y.remove(e,[t+"queue",n])})})}}),S.fn.extend({queue:function(t,n){var e=2;return"string"!=typeof t&&(n=t,t="fx",e--),arguments.length<e?S.queue(this[0],t):void 0===n?this:this.each(function(){var e=S.queue(this,t,n);S._queueHooks(this,t),"fx"===t&&"inprogress"!==e[0]&&S.dequeue(this,t)})},dequeue:function(e){return this.each(function(){S.dequeue(this,e)})},clearQueue:function(e){return this.queue(e||"fx",[])},promise:function(e,t){var n,r=1,i=S.Deferred(),o=this,a=this.length,s=function(){--r||i.resolveWith(o,[o])};"string"!=typeof e&&(t=e,e=void 0),e=e||"fx";while(a--)(n=Y.get(o[a],e+"queueHooks"))&&n.empty&&(r++,n.empty.add(s));return s(),i.promise(t)}});var ee=/[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source,te=new RegExp("^(?:([+-])=|)("+ee+")([a-z%]*)$","i"),ne=["Top","Right","Bottom","Left"],re=E.documentElement,ie=function(e){return S.contains(e.ownerDocument,e)},oe={composed:!0};re.getRootNode&&(ie=function(e){return S.contains(e.ownerDocument,e)||e.getRootNode(oe)===e.ownerDocument});var ae=function(e,t){return"none"===(e=t||e).style.display||""===e.style.display&&ie(e)&&"none"===S.css(e,"display")};function se(e,t,n,r){var i,o,a=20,s=r?function(){return r.cur()}:function(){return S.css(e,t,"")},u=s(),l=n&&n[3]||(S.cssNumber[t]?"":"px"),c=e.nodeType&&(S.cssNumber[t]||"px"!==l&&+u)&&te.exec(S.css(e,t));if(c&&c[3]!==l){u/=2,l=l||c[3],c=+u||1;while(a--)S.style(e,t,c+l),(1-o)*(1-(o=s()/u||.5))<=0&&(a=0),c/=o;c*=2,S.style(e,t,c+l),n=n||[]}return n&&(c=+c||+u||0,i=n[1]?c+(n[1]+1)*n[2]:+n[2],r&&(r.unit=l,r.start=c,r.end=i)),i}var ue={};function le(e,t){for(var n,r,i,o,a,s,u,l=[],c=0,f=e.length;c<f;c++)(r=e[c]).style&&(n=r.style.display,t?("none"===n&&(l[c]=Y.get(r,"display")||null,l[c]||(r.style.display="")),""===r.style.display&&ae(r)&&(l[c]=(u=a=o=void 0,a=(i=r).ownerDocument,s=i.nodeName,(u=ue[s])||(o=a.body.appendChild(a.createElement(s)),u=S.css(o,"display"),o.parentNode.removeChild(o),"none"===u&&(u="block"),ue[s]=u)))):"none"!==n&&(l[c]="none",Y.set(r,"display",n)));for(c=0;c<f;c++)null!=l[c]&&(e[c].style.display=l[c]);return e}S.fn.extend({show:function(){return le(this,!0)},hide:function(){return le(this)},toggle:function(e){return"boolean"==typeof e?e?this.show():this.hide():this.each(function(){ae(this)?S(this).show():S(this).hide()})}});var ce,fe,pe=/^(?:checkbox|radio)$/i,de=/<([a-z][^\/\0>\x20\t\r\n\f]*)/i,he=/^$|^module$|\/(?:java|ecma)script/i;ce=E.createDocumentFragment().appendChild(E.createElement("div")),(fe=E.createElement("input")).setAttribute("type","radio"),fe.setAttribute("checked","checked"),fe.setAttribute("name","t"),ce.appendChild(fe),y.checkClone=ce.cloneNode(!0).cloneNode(!0).lastChild.checked,ce.innerHTML="<textarea>x</textarea>",y.noCloneChecked=!!ce.cloneNode(!0).lastChild.defaultValue,ce.innerHTML="<option></option>",y.option=!!ce.lastChild;var ge={thead:[1,"<table>","</table>"],col:[2,"<table><colgroup>","</colgroup></table>"],tr:[2,"<table><tbody>","</tbody></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],_default:[0,"",""]};function ve(e,t){var n;return n="undefined"!=typeof e.getElementsByTagName?e.getElementsByTagName(t||"*"):"undefined"!=typeof e.querySelectorAll?e.querySelectorAll(t||"*"):[],void 0===t||t&&A(e,t)?S.merge([e],n):n}function ye(e,t){for(var n=0,r=e.length;n<r;n++)Y.set(e[n],"globalEval",!t||Y.get(t[n],"globalEval"))}ge.tbody=ge.tfoot=ge.colgroup=ge.caption=ge.thead,ge.th=ge.td,y.option||(ge.optgroup=ge.option=[1,"<select multiple='multiple'>","</select>"]);var me=/<|&#?\w+;/;function xe(e,t,n,r,i){for(var o,a,s,u,l,c,f=t.createDocumentFragment(),p=[],d=0,h=e.length;d<h;d++)if((o=e[d])||0===o)if("object"===w(o))S.merge(p,o.nodeType?[o]:o);else if(me.test(o)){a=a||f.appendChild(t.createElement("div")),s=(de.exec(o)||["",""])[1].toLowerCase(),u=ge[s]||ge._default,a.innerHTML=u[1]+S.htmlPrefilter(o)+u[2],c=u[0];while(c--)a=a.lastChild;S.merge(p,a.childNodes),(a=f.firstChild).textContent=""}else p.push(t.createTextNode(o));f.textContent="",d=0;while(o=p[d++])if(r&&-1<S.inArray(o,r))i&&i.push(o);else if(l=ie(o),a=ve(f.appendChild(o),"script"),l&&ye(a),n){c=0;while(o=a[c++])he.test(o.type||"")&&n.push(o)}return f}var be=/^key/,we=/^(?:mouse|pointer|contextmenu|drag|drop)|click/,Te=/^([^.]*)(?:\.(.+)|)/;function Ce(){return!0}function Ee(){return!1}function Se(e,t){return e===function(){try{return E.activeElement}catch(e){}}()==("focus"===t)}function ke(e,t,n,r,i,o){var a,s;if("object"==typeof t){for(s in"string"!=typeof n&&(r=r||n,n=void 0),t)ke(e,s,n,r,t[s],o);return e}if(null==r&&null==i?(i=n,r=n=void 0):null==i&&("string"==typeof n?(i=r,r=void 0):(i=r,r=n,n=void 0)),!1===i)i=Ee;else if(!i)return e;return 1===o&&(a=i,(i=function(e){return S().off(e),a.apply(this,arguments)}).guid=a.guid||(a.guid=S.guid++)),e.each(function(){S.event.add(this,t,i,r,n)})}function Ae(e,i,o){o?(Y.set(e,i,!1),S.event.add(e,i,{namespace:!1,handler:function(e){var t,n,r=Y.get(this,i);if(1&e.isTrigger&&this[i]){if(r.length)(S.event.special[i]||{}).delegateType&&e.stopPropagation();else if(r=s.call(arguments),Y.set(this,i,r),t=o(this,i),this[i](),r!==(n=Y.get(this,i))||t?Y.set(this,i,!1):n={},r!==n)return e.stopImmediatePropagation(),e.preventDefault(),n.value}else r.length&&(Y.set(this,i,{value:S.event.trigger(S.extend(r[0],S.Event.prototype),r.slice(1),this)}),e.stopImmediatePropagation())}})):void 0===Y.get(e,i)&&S.event.add(e,i,Ce)}S.event={global:{},add:function(t,e,n,r,i){var o,a,s,u,l,c,f,p,d,h,g,v=Y.get(t);if(V(t)){n.handler&&(n=(o=n).handler,i=o.selector),i&&S.find.matchesSelector(re,i),n.guid||(n.guid=S.guid++),(u=v.events)||(u=v.events=Object.create(null)),(a=v.handle)||(a=v.handle=function(e){return"undefined"!=typeof S&&S.event.triggered!==e.type?S.event.dispatch.apply(t,arguments):void 0}),l=(e=(e||"").match(P)||[""]).length;while(l--)d=g=(s=Te.exec(e[l])||[])[1],h=(s[2]||"").split(".").sort(),d&&(f=S.event.special[d]||{},d=(i?f.delegateType:f.bindType)||d,f=S.event.special[d]||{},c=S.extend({type:d,origType:g,data:r,handler:n,guid:n.guid,selector:i,needsContext:i&&S.expr.match.needsContext.test(i),namespace:h.join(".")},o),(p=u[d])||((p=u[d]=[]).delegateCount=0,f.setup&&!1!==f.setup.call(t,r,h,a)||t.addEventListener&&t.addEventListener(d,a)),f.add&&(f.add.call(t,c),c.handler.guid||(c.handler.guid=n.guid)),i?p.splice(p.delegateCount++,0,c):p.push(c),S.event.global[d]=!0)}},remove:function(e,t,n,r,i){var o,a,s,u,l,c,f,p,d,h,g,v=Y.hasData(e)&&Y.get(e);if(v&&(u=v.events)){l=(t=(t||"").match(P)||[""]).length;while(l--)if(d=g=(s=Te.exec(t[l])||[])[1],h=(s[2]||"").split(".").sort(),d){f=S.event.special[d]||{},p=u[d=(r?f.delegateType:f.bindType)||d]||[],s=s[2]&&new RegExp("(^|\\.)"+h.join("\\.(?:.*\\.|)")+"(\\.|$)"),a=o=p.length;while(o--)c=p[o],!i&&g!==c.origType||n&&n.guid!==c.guid||s&&!s.test(c.namespace)||r&&r!==c.selector&&("**"!==r||!c.selector)||(p.splice(o,1),c.selector&&p.delegateCount--,f.remove&&f.remove.call(e,c));a&&!p.length&&(f.teardown&&!1!==f.teardown.call(e,h,v.handle)||S.removeEvent(e,d,v.handle),delete u[d])}else for(d in u)S.event.remove(e,d+t[l],n,r,!0);S.isEmptyObject(u)&&Y.remove(e,"handle events")}},dispatch:function(e){var t,n,r,i,o,a,s=new Array(arguments.length),u=S.event.fix(e),l=(Y.get(this,"events")||Object.create(null))[u.type]||[],c=S.event.special[u.type]||{};for(s[0]=u,t=1;t<arguments.length;t++)s[t]=arguments[t];if(u.delegateTarget=this,!c.preDispatch||!1!==c.preDispatch.call(this,u)){a=S.event.handlers.call(this,u,l),t=0;while((i=a[t++])&&!u.isPropagationStopped()){u.currentTarget=i.elem,n=0;while((o=i.handlers[n++])&&!u.isImmediatePropagationStopped())u.rnamespace&&!1!==o.namespace&&!u.rnamespace.test(o.namespace)||(u.handleObj=o,u.data=o.data,void 0!==(r=((S.event.special[o.origType]||{}).handle||o.handler).apply(i.elem,s))&&!1===(u.result=r)&&(u.preventDefault(),u.stopPropagation()))}return c.postDispatch&&c.postDispatch.call(this,u),u.result}},handlers:function(e,t){var n,r,i,o,a,s=[],u=t.delegateCount,l=e.target;if(u&&l.nodeType&&!("click"===e.type&&1<=e.button))for(;l!==this;l=l.parentNode||this)if(1===l.nodeType&&("click"!==e.type||!0!==l.disabled)){for(o=[],a={},n=0;n<u;n++)void 0===a[i=(r=t[n]).selector+" "]&&(a[i]=r.needsContext?-1<S(i,this).index(l):S.find(i,this,null,[l]).length),a[i]&&o.push(r);o.length&&s.push({elem:l,handlers:o})}return l=this,u<t.length&&s.push({elem:l,handlers:t.slice(u)}),s},addProp:function(t,e){Object.defineProperty(S.Event.prototype,t,{enumerable:!0,configurable:!0,get:m(e)?function(){if(this.originalEvent)return e(this.originalEvent)}:function(){if(this.originalEvent)return this.originalEvent[t]},set:function(e){Object.defineProperty(this,t,{enumerable:!0,configurable:!0,writable:!0,value:e})}})},fix:function(e){return e[S.expando]?e:new S.Event(e)},special:{load:{noBubble:!0},click:{setup:function(e){var t=this||e;return pe.test(t.type)&&t.click&&A(t,"input")&&Ae(t,"click",Ce),!1},trigger:function(e){var t=this||e;return pe.test(t.type)&&t.click&&A(t,"input")&&Ae(t,"click"),!0},_default:function(e){var t=e.target;return pe.test(t.type)&&t.click&&A(t,"input")&&Y.get(t,"click")||A(t,"a")}},beforeunload:{postDispatch:function(e){void 0!==e.result&&e.originalEvent&&(e.originalEvent.returnValue=e.result)}}}},S.removeEvent=function(e,t,n){e.removeEventListener&&e.removeEventListener(t,n)},S.Event=function(e,t){if(!(this instanceof S.Event))return new S.Event(e,t);e&&e.type?(this.originalEvent=e,this.type=e.type,this.isDefaultPrevented=e.defaultPrevented||void 0===e.defaultPrevented&&!1===e.returnValue?Ce:Ee,this.target=e.target&&3===e.target.nodeType?e.target.parentNode:e.target,this.currentTarget=e.currentTarget,this.relatedTarget=e.relatedTarget):this.type=e,t&&S.extend(this,t),this.timeStamp=e&&e.timeStamp||Date.now(),this[S.expando]=!0},S.Event.prototype={constructor:S.Event,isDefaultPrevented:Ee,isPropagationStopped:Ee,isImmediatePropagationStopped:Ee,isSimulated:!1,preventDefault:function(){var e=this.originalEvent;this.isDefaultPrevented=Ce,e&&!this.isSimulated&&e.preventDefault()},stopPropagation:function(){var e=this.originalEvent;this.isPropagationStopped=Ce,e&&!this.isSimulated&&e.stopPropagation()},stopImmediatePropagation:function(){var e=this.originalEvent;this.isImmediatePropagationStopped=Ce,e&&!this.isSimulated&&e.stopImmediatePropagation(),this.stopPropagation()}},S.each({altKey:!0,bubbles:!0,cancelable:!0,changedTouches:!0,ctrlKey:!0,detail:!0,eventPhase:!0,metaKey:!0,pageX:!0,pageY:!0,shiftKey:!0,view:!0,"char":!0,code:!0,charCode:!0,key:!0,keyCode:!0,button:!0,buttons:!0,clientX:!0,clientY:!0,offsetX:!0,offsetY:!0,pointerId:!0,pointerType:!0,screenX:!0,screenY:!0,targetTouches:!0,toElement:!0,touches:!0,which:function(e){var t=e.button;return null==e.which&&be.test(e.type)?null!=e.charCode?e.charCode:e.keyCode:!e.which&&void 0!==t&&we.test(e.type)?1&t?1:2&t?3:4&t?2:0:e.which}},S.event.addProp),S.each({focus:"focusin",blur:"focusout"},function(e,t){S.event.special[e]={setup:function(){return Ae(this,e,Se),!1},trigger:function(){return Ae(this,e),!0},delegateType:t}}),S.each({mouseenter:"mouseover",mouseleave:"mouseout",pointerenter:"pointerover",pointerleave:"pointerout"},function(e,i){S.event.special[e]={delegateType:i,bindType:i,handle:function(e){var t,n=e.relatedTarget,r=e.handleObj;return n&&(n===this||S.contains(this,n))||(e.type=r.origType,t=r.handler.apply(this,arguments),e.type=i),t}}}),S.fn.extend({on:function(e,t,n,r){return ke(this,e,t,n,r)},one:function(e,t,n,r){return ke(this,e,t,n,r,1)},off:function(e,t,n){var r,i;if(e&&e.preventDefault&&e.handleObj)return r=e.handleObj,S(e.delegateTarget).off(r.namespace?r.origType+"."+r.namespace:r.origType,r.selector,r.handler),this;if("object"==typeof e){for(i in e)this.off(i,t,e[i]);return this}return!1!==t&&"function"!=typeof t||(n=t,t=void 0),!1===n&&(n=Ee),this.each(function(){S.event.remove(this,e,n,t)})}});var Ne=/<script|<style|<link/i,De=/checked\s*(?:[^=]|=\s*.checked.)/i,je=/^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g;function qe(e,t){return A(e,"table")&&A(11!==t.nodeType?t:t.firstChild,"tr")&&S(e).children("tbody")[0]||e}function Le(e){return e.type=(null!==e.getAttribute("type"))+"/"+e.type,e}function He(e){return"true/"===(e.type||"").slice(0,5)?e.type=e.type.slice(5):e.removeAttribute("type"),e}function Oe(e,t){var n,r,i,o,a,s;if(1===t.nodeType){if(Y.hasData(e)&&(s=Y.get(e).events))for(i in Y.remove(t,"handle events"),s)for(n=0,r=s[i].length;n<r;n++)S.event.add(t,i,s[i][n]);Q.hasData(e)&&(o=Q.access(e),a=S.extend({},o),Q.set(t,a))}}function Pe(n,r,i,o){r=g(r);var e,t,a,s,u,l,c=0,f=n.length,p=f-1,d=r[0],h=m(d);if(h||1<f&&"string"==typeof d&&!y.checkClone&&De.test(d))return n.each(function(e){var t=n.eq(e);h&&(r[0]=d.call(this,e,t.html())),Pe(t,r,i,o)});if(f&&(t=(e=xe(r,n[0].ownerDocument,!1,n,o)).firstChild,1===e.childNodes.length&&(e=t),t||o)){for(s=(a=S.map(ve(e,"script"),Le)).length;c<f;c++)u=e,c!==p&&(u=S.clone(u,!0,!0),s&&S.merge(a,ve(u,"script"))),i.call(n[c],u,c);if(s)for(l=a[a.length-1].ownerDocument,S.map(a,He),c=0;c<s;c++)u=a[c],he.test(u.type||"")&&!Y.access(u,"globalEval")&&S.contains(l,u)&&(u.src&&"module"!==(u.type||"").toLowerCase()?S._evalUrl&&!u.noModule&&S._evalUrl(u.src,{nonce:u.nonce||u.getAttribute("nonce")},l):b(u.textContent.replace(je,""),u,l))}return n}function Re(e,t,n){for(var r,i=t?S.filter(t,e):e,o=0;null!=(r=i[o]);o++)n||1!==r.nodeType||S.cleanData(ve(r)),r.parentNode&&(n&&ie(r)&&ye(ve(r,"script")),r.parentNode.removeChild(r));return e}S.extend({htmlPrefilter:function(e){return e},clone:function(e,t,n){var r,i,o,a,s,u,l,c=e.cloneNode(!0),f=ie(e);if(!(y.noCloneChecked||1!==e.nodeType&&11!==e.nodeType||S.isXMLDoc(e)))for(a=ve(c),r=0,i=(o=ve(e)).length;r<i;r++)s=o[r],u=a[r],void 0,"input"===(l=u.nodeName.toLowerCase())&&pe.test(s.type)?u.checked=s.checked:"input"!==l&&"textarea"!==l||(u.defaultValue=s.defaultValue);if(t)if(n)for(o=o||ve(e),a=a||ve(c),r=0,i=o.length;r<i;r++)Oe(o[r],a[r]);else Oe(e,c);return 0<(a=ve(c,"script")).length&&ye(a,!f&&ve(e,"script")),c},cleanData:function(e){for(var t,n,r,i=S.event.special,o=0;void 0!==(n=e[o]);o++)if(V(n)){if(t=n[Y.expando]){if(t.events)for(r in t.events)i[r]?S.event.remove(n,r):S.removeEvent(n,r,t.handle);n[Y.expando]=void 0}n[Q.expando]&&(n[Q.expando]=void 0)}}}),S.fn.extend({detach:function(e){return Re(this,e,!0)},remove:function(e){return Re(this,e)},text:function(e){return $(this,function(e){return void 0===e?S.text(this):this.empty().each(function(){1!==this.nodeType&&11!==this.nodeType&&9!==this.nodeType||(this.textContent=e)})},null,e,arguments.length)},append:function(){return Pe(this,arguments,function(e){1!==this.nodeType&&11!==this.nodeType&&9!==this.nodeType||qe(this,e).appendChild(e)})},prepend:function(){return Pe(this,arguments,function(e){if(1===this.nodeType||11===this.nodeType||9===this.nodeType){var t=qe(this,e);t.insertBefore(e,t.firstChild)}})},before:function(){return Pe(this,arguments,function(e){this.parentNode&&this.parentNode.insertBefore(e,this)})},after:function(){return Pe(this,arguments,function(e){this.parentNode&&this.parentNode.insertBefore(e,this.nextSibling)})},empty:function(){for(var e,t=0;null!=(e=this[t]);t++)1===e.nodeType&&(S.cleanData(ve(e,!1)),e.textContent="");return this},clone:function(e,t){return e=null!=e&&e,t=null==t?e:t,this.map(function(){return S.clone(this,e,t)})},html:function(e){return $(this,function(e){var t=this[0]||{},n=0,r=this.length;if(void 0===e&&1===t.nodeType)return t.innerHTML;if("string"==typeof e&&!Ne.test(e)&&!ge[(de.exec(e)||["",""])[1].toLowerCase()]){e=S.htmlPrefilter(e);try{for(;n<r;n++)1===(t=this[n]||{}).nodeType&&(S.cleanData(ve(t,!1)),t.innerHTML=e);t=0}catch(e){}}t&&this.empty().append(e)},null,e,arguments.length)},replaceWith:function(){var n=[];return Pe(this,arguments,function(e){var t=this.parentNode;S.inArray(this,n)<0&&(S.cleanData(ve(this)),t&&t.replaceChild(e,this))},n)}}),S.each({appendTo:"append",prependTo:"prepend",insertBefore:"before",insertAfter:"after",replaceAll:"replaceWith"},function(e,a){S.fn[e]=function(e){for(var t,n=[],r=S(e),i=r.length-1,o=0;o<=i;o++)t=o===i?this:this.clone(!0),S(r[o])[a](t),u.apply(n,t.get());return this.pushStack(n)}});var Me=new RegExp("^("+ee+")(?!px)[a-z%]+$","i"),Ie=function(e){var t=e.ownerDocument.defaultView;return t&&t.opener||(t=C),t.getComputedStyle(e)},We=function(e,t,n){var r,i,o={};for(i in t)o[i]=e.style[i],e.style[i]=t[i];for(i in r=n.call(e),t)e.style[i]=o[i];return r},Fe=new RegExp(ne.join("|"),"i");function Be(e,t,n){var r,i,o,a,s=e.style;return(n=n||Ie(e))&&(""!==(a=n.getPropertyValue(t)||n[t])||ie(e)||(a=S.style(e,t)),!y.pixelBoxStyles()&&Me.test(a)&&Fe.test(t)&&(r=s.width,i=s.minWidth,o=s.maxWidth,s.minWidth=s.maxWidth=s.width=a,a=n.width,s.width=r,s.minWidth=i,s.maxWidth=o)),void 0!==a?a+"":a}function $e(e,t){return{get:function(){if(!e())return(this.get=t).apply(this,arguments);delete this.get}}}!function(){function e(){if(l){u.style.cssText="position:absolute;left:-11111px;width:60px;margin-top:1px;padding:0;border:0",l.style.cssText="position:relative;display:block;box-sizing:border-box;overflow:scroll;margin:auto;border:1px;padding:1px;width:60%;top:1%",re.appendChild(u).appendChild(l);var e=C.getComputedStyle(l);n="1%"!==e.top,s=12===t(e.marginLeft),l.style.right="60%",o=36===t(e.right),r=36===t(e.width),l.style.position="absolute",i=12===t(l.offsetWidth/3),re.removeChild(u),l=null}}function t(e){return Math.round(parseFloat(e))}var n,r,i,o,a,s,u=E.createElement("div"),l=E.createElement("div");l.style&&(l.style.backgroundClip="content-box",l.cloneNode(!0).style.backgroundClip="",y.clearCloneStyle="content-box"===l.style.backgroundClip,S.extend(y,{boxSizingReliable:function(){return e(),r},pixelBoxStyles:function(){return e(),o},pixelPosition:function(){return e(),n},reliableMarginLeft:function(){return e(),s},scrollboxSize:function(){return e(),i},reliableTrDimensions:function(){var e,t,n,r;return null==a&&(e=E.createElement("table"),t=E.createElement("tr"),n=E.createElement("div"),e.style.cssText="position:absolute;left:-11111px",t.style.height="1px",n.style.height="9px",re.appendChild(e).appendChild(t).appendChild(n),r=C.getComputedStyle(t),a=3<parseInt(r.height),re.removeChild(e)),a}}))}();var _e=["Webkit","Moz","ms"],ze=E.createElement("div").style,Ue={};function Xe(e){var t=S.cssProps[e]||Ue[e];return t||(e in ze?e:Ue[e]=function(e){var t=e[0].toUpperCase()+e.slice(1),n=_e.length;while(n--)if((e=_e[n]+t)in ze)return e}(e)||e)}var Ve=/^(none|table(?!-c[ea]).+)/,Ge=/^--/,Ye={position:"absolute",visibility:"hidden",display:"block"},Qe={letterSpacing:"0",fontWeight:"400"};function Je(e,t,n){var r=te.exec(t);return r?Math.max(0,r[2]-(n||0))+(r[3]||"px"):t}function Ke(e,t,n,r,i,o){var a="width"===t?1:0,s=0,u=0;if(n===(r?"border":"content"))return 0;for(;a<4;a+=2)"margin"===n&&(u+=S.css(e,n+ne[a],!0,i)),r?("content"===n&&(u-=S.css(e,"padding"+ne[a],!0,i)),"margin"!==n&&(u-=S.css(e,"border"+ne[a]+"Width",!0,i))):(u+=S.css(e,"padding"+ne[a],!0,i),"padding"!==n?u+=S.css(e,"border"+ne[a]+"Width",!0,i):s+=S.css(e,"border"+ne[a]+"Width",!0,i));return!r&&0<=o&&(u+=Math.max(0,Math.ceil(e["offset"+t[0].toUpperCase()+t.slice(1)]-o-u-s-.5))||0),u}function Ze(e,t,n){var r=Ie(e),i=(!y.boxSizingReliable()||n)&&"border-box"===S.css(e,"boxSizing",!1,r),o=i,a=Be(e,t,r),s="offset"+t[0].toUpperCase()+t.slice(1);if(Me.test(a)){if(!n)return a;a="auto"}return(!y.boxSizingReliable()&&i||!y.reliableTrDimensions()&&A(e,"tr")||"auto"===a||!parseFloat(a)&&"inline"===S.css(e,"display",!1,r))&&e.getClientRects().length&&(i="border-box"===S.css(e,"boxSizing",!1,r),(o=s in e)&&(a=e[s])),(a=parseFloat(a)||0)+Ke(e,t,n||(i?"border":"content"),o,r,a)+"px"}function et(e,t,n,r,i){return new et.prototype.init(e,t,n,r,i)}S.extend({cssHooks:{opacity:{get:function(e,t){if(t){var n=Be(e,"opacity");return""===n?"1":n}}}},cssNumber:{animationIterationCount:!0,columnCount:!0,fillOpacity:!0,flexGrow:!0,flexShrink:!0,fontWeight:!0,gridArea:!0,gridColumn:!0,gridColumnEnd:!0,gridColumnStart:!0,gridRow:!0,gridRowEnd:!0,gridRowStart:!0,lineHeight:!0,opacity:!0,order:!0,orphans:!0,widows:!0,zIndex:!0,zoom:!0},cssProps:{},style:function(e,t,n,r){if(e&&3!==e.nodeType&&8!==e.nodeType&&e.style){var i,o,a,s=X(t),u=Ge.test(t),l=e.style;if(u||(t=Xe(s)),a=S.cssHooks[t]||S.cssHooks[s],void 0===n)return a&&"get"in a&&void 0!==(i=a.get(e,!1,r))?i:l[t];"string"===(o=typeof n)&&(i=te.exec(n))&&i[1]&&(n=se(e,t,i),o="number"),null!=n&&n==n&&("number"!==o||u||(n+=i&&i[3]||(S.cssNumber[s]?"":"px")),y.clearCloneStyle||""!==n||0!==t.indexOf("background")||(l[t]="inherit"),a&&"set"in a&&void 0===(n=a.set(e,n,r))||(u?l.setProperty(t,n):l[t]=n))}},css:function(e,t,n,r){var i,o,a,s=X(t);return Ge.test(t)||(t=Xe(s)),(a=S.cssHooks[t]||S.cssHooks[s])&&"get"in a&&(i=a.get(e,!0,n)),void 0===i&&(i=Be(e,t,r)),"normal"===i&&t in Qe&&(i=Qe[t]),""===n||n?(o=parseFloat(i),!0===n||isFinite(o)?o||0:i):i}}),S.each(["height","width"],function(e,u){S.cssHooks[u]={get:function(e,t,n){if(t)return!Ve.test(S.css(e,"display"))||e.getClientRects().length&&e.getBoundingClientRect().width?Ze(e,u,n):We(e,Ye,function(){return Ze(e,u,n)})},set:function(e,t,n){var r,i=Ie(e),o=!y.scrollboxSize()&&"absolute"===i.position,a=(o||n)&&"border-box"===S.css(e,"boxSizing",!1,i),s=n?Ke(e,u,n,a,i):0;return a&&o&&(s-=Math.ceil(e["offset"+u[0].toUpperCase()+u.slice(1)]-parseFloat(i[u])-Ke(e,u,"border",!1,i)-.5)),s&&(r=te.exec(t))&&"px"!==(r[3]||"px")&&(e.style[u]=t,t=S.css(e,u)),Je(0,t,s)}}}),S.cssHooks.marginLeft=$e(y.reliableMarginLeft,function(e,t){if(t)return(parseFloat(Be(e,"marginLeft"))||e.getBoundingClientRect().left-We(e,{marginLeft:0},function(){return e.getBoundingClientRect().left}))+"px"}),S.each({margin:"",padding:"",border:"Width"},function(i,o){S.cssHooks[i+o]={expand:function(e){for(var t=0,n={},r="string"==typeof e?e.split(" "):[e];t<4;t++)n[i+ne[t]+o]=r[t]||r[t-2]||r[0];return n}},"margin"!==i&&(S.cssHooks[i+o].set=Je)}),S.fn.extend({css:function(e,t){return $(this,function(e,t,n){var r,i,o={},a=0;if(Array.isArray(t)){for(r=Ie(e),i=t.length;a<i;a++)o[t[a]]=S.css(e,t[a],!1,r);return o}return void 0!==n?S.style(e,t,n):S.css(e,t)},e,t,1<arguments.length)}}),((S.Tween=et).prototype={constructor:et,init:function(e,t,n,r,i,o){this.elem=e,this.prop=n,this.easing=i||S.easing._default,this.options=t,this.start=this.now=this.cur(),this.end=r,this.unit=o||(S.cssNumber[n]?"":"px")},cur:function(){var e=et.propHooks[this.prop];return e&&e.get?e.get(this):et.propHooks._default.get(this)},run:function(e){var t,n=et.propHooks[this.prop];return this.options.duration?this.pos=t=S.easing[this.easing](e,this.options.duration*e,0,1,this.options.duration):this.pos=t=e,this.now=(this.end-this.start)*t+this.start,this.options.step&&this.options.step.call(this.elem,this.now,this),n&&n.set?n.set(this):et.propHooks._default.set(this),this}}).init.prototype=et.prototype,(et.propHooks={_default:{get:function(e){var t;return 1!==e.elem.nodeType||null!=e.elem[e.prop]&&null==e.elem.style[e.prop]?e.elem[e.prop]:(t=S.css(e.elem,e.prop,""))&&"auto"!==t?t:0},set:function(e){S.fx.step[e.prop]?S.fx.step[e.prop](e):1!==e.elem.nodeType||!S.cssHooks[e.prop]&&null==e.elem.style[Xe(e.prop)]?e.elem[e.prop]=e.now:S.style(e.elem,e.prop,e.now+e.unit)}}}).scrollTop=et.propHooks.scrollLeft={set:function(e){e.elem.nodeType&&e.elem.parentNode&&(e.elem[e.prop]=e.now)}},S.easing={linear:function(e){return e},swing:function(e){return.5-Math.cos(e*Math.PI)/2},_default:"swing"},S.fx=et.prototype.init,S.fx.step={};var tt,nt,rt,it,ot=/^(?:toggle|show|hide)$/,at=/queueHooks$/;function st(){nt&&(!1===E.hidden&&C.requestAnimationFrame?C.requestAnimationFrame(st):C.setTimeout(st,S.fx.interval),S.fx.tick())}function ut(){return C.setTimeout(function(){tt=void 0}),tt=Date.now()}function lt(e,t){var n,r=0,i={height:e};for(t=t?1:0;r<4;r+=2-t)i["margin"+(n=ne[r])]=i["padding"+n]=e;return t&&(i.opacity=i.width=e),i}function ct(e,t,n){for(var r,i=(ft.tweeners[t]||[]).concat(ft.tweeners["*"]),o=0,a=i.length;o<a;o++)if(r=i[o].call(n,t,e))return r}function ft(o,e,t){var n,a,r=0,i=ft.prefilters.length,s=S.Deferred().always(function(){delete u.elem}),u=function(){if(a)return!1;for(var e=tt||ut(),t=Math.max(0,l.startTime+l.duration-e),n=1-(t/l.duration||0),r=0,i=l.tweens.length;r<i;r++)l.tweens[r].run(n);return s.notifyWith(o,[l,n,t]),n<1&&i?t:(i||s.notifyWith(o,[l,1,0]),s.resolveWith(o,[l]),!1)},l=s.promise({elem:o,props:S.extend({},e),opts:S.extend(!0,{specialEasing:{},easing:S.easing._default},t),originalProperties:e,originalOptions:t,startTime:tt||ut(),duration:t.duration,tweens:[],createTween:function(e,t){var n=S.Tween(o,l.opts,e,t,l.opts.specialEasing[e]||l.opts.easing);return l.tweens.push(n),n},stop:function(e){var t=0,n=e?l.tweens.length:0;if(a)return this;for(a=!0;t<n;t++)l.tweens[t].run(1);return e?(s.notifyWith(o,[l,1,0]),s.resolveWith(o,[l,e])):s.rejectWith(o,[l,e]),this}}),c=l.props;for(!function(e,t){var n,r,i,o,a;for(n in e)if(i=t[r=X(n)],o=e[n],Array.isArray(o)&&(i=o[1],o=e[n]=o[0]),n!==r&&(e[r]=o,delete e[n]),(a=S.cssHooks[r])&&"expand"in a)for(n in o=a.expand(o),delete e[r],o)n in e||(e[n]=o[n],t[n]=i);else t[r]=i}(c,l.opts.specialEasing);r<i;r++)if(n=ft.prefilters[r].call(l,o,c,l.opts))return m(n.stop)&&(S._queueHooks(l.elem,l.opts.queue).stop=n.stop.bind(n)),n;return S.map(c,ct,l),m(l.opts.start)&&l.opts.start.call(o,l),l.progress(l.opts.progress).done(l.opts.done,l.opts.complete).fail(l.opts.fail).always(l.opts.always),S.fx.timer(S.extend(u,{elem:o,anim:l,queue:l.opts.queue})),l}S.Animation=S.extend(ft,{tweeners:{"*":[function(e,t){var n=this.createTween(e,t);return se(n.elem,e,te.exec(t),n),n}]},tweener:function(e,t){m(e)?(t=e,e=["*"]):e=e.match(P);for(var n,r=0,i=e.length;r<i;r++)n=e[r],ft.tweeners[n]=ft.tweeners[n]||[],ft.tweeners[n].unshift(t)},prefilters:[function(e,t,n){var r,i,o,a,s,u,l,c,f="width"in t||"height"in t,p=this,d={},h=e.style,g=e.nodeType&&ae(e),v=Y.get(e,"fxshow");for(r in n.queue||(null==(a=S._queueHooks(e,"fx")).unqueued&&(a.unqueued=0,s=a.empty.fire,a.empty.fire=function(){a.unqueued||s()}),a.unqueued++,p.always(function(){p.always(function(){a.unqueued--,S.queue(e,"fx").length||a.empty.fire()})})),t)if(i=t[r],ot.test(i)){if(delete t[r],o=o||"toggle"===i,i===(g?"hide":"show")){if("show"!==i||!v||void 0===v[r])continue;g=!0}d[r]=v&&v[r]||S.style(e,r)}if((u=!S.isEmptyObject(t))||!S.isEmptyObject(d))for(r in f&&1===e.nodeType&&(n.overflow=[h.overflow,h.overflowX,h.overflowY],null==(l=v&&v.display)&&(l=Y.get(e,"display")),"none"===(c=S.css(e,"display"))&&(l?c=l:(le([e],!0),l=e.style.display||l,c=S.css(e,"display"),le([e]))),("inline"===c||"inline-block"===c&&null!=l)&&"none"===S.css(e,"float")&&(u||(p.done(function(){h.display=l}),null==l&&(c=h.display,l="none"===c?"":c)),h.display="inline-block")),n.overflow&&(h.overflow="hidden",p.always(function(){h.overflow=n.overflow[0],h.overflowX=n.overflow[1],h.overflowY=n.overflow[2]})),u=!1,d)u||(v?"hidden"in v&&(g=v.hidden):v=Y.access(e,"fxshow",{display:l}),o&&(v.hidden=!g),g&&le([e],!0),p.done(function(){for(r in g||le([e]),Y.remove(e,"fxshow"),d)S.style(e,r,d[r])})),u=ct(g?v[r]:0,r,p),r in v||(v[r]=u.start,g&&(u.end=u.start,u.start=0))}],prefilter:function(e,t){t?ft.prefilters.unshift(e):ft.prefilters.push(e)}}),S.speed=function(e,t,n){var r=e&&"object"==typeof e?S.extend({},e):{complete:n||!n&&t||m(e)&&e,duration:e,easing:n&&t||t&&!m(t)&&t};return S.fx.off?r.duration=0:"number"!=typeof r.duration&&(r.duration in S.fx.speeds?r.duration=S.fx.speeds[r.duration]:r.duration=S.fx.speeds._default),null!=r.queue&&!0!==r.queue||(r.queue="fx"),r.old=r.complete,r.complete=function(){m(r.old)&&r.old.call(this),r.queue&&S.dequeue(this,r.queue)},r},S.fn.extend({fadeTo:function(e,t,n,r){return this.filter(ae).css("opacity",0).show().end().animate({opacity:t},e,n,r)},animate:function(t,e,n,r){var i=S.isEmptyObject(t),o=S.speed(e,n,r),a=function(){var e=ft(this,S.extend({},t),o);(i||Y.get(this,"finish"))&&e.stop(!0)};return a.finish=a,i||!1===o.queue?this.each(a):this.queue(o.queue,a)},stop:function(i,e,o){var a=function(e){var t=e.stop;delete e.stop,t(o)};return"string"!=typeof i&&(o=e,e=i,i=void 0),e&&this.queue(i||"fx",[]),this.each(function(){var e=!0,t=null!=i&&i+"queueHooks",n=S.timers,r=Y.get(this);if(t)r[t]&&r[t].stop&&a(r[t]);else for(t in r)r[t]&&r[t].stop&&at.test(t)&&a(r[t]);for(t=n.length;t--;)n[t].elem!==this||null!=i&&n[t].queue!==i||(n[t].anim.stop(o),e=!1,n.splice(t,1));!e&&o||S.dequeue(this,i)})},finish:function(a){return!1!==a&&(a=a||"fx"),this.each(function(){var e,t=Y.get(this),n=t[a+"queue"],r=t[a+"queueHooks"],i=S.timers,o=n?n.length:0;for(t.finish=!0,S.queue(this,a,[]),r&&r.stop&&r.stop.call(this,!0),e=i.length;e--;)i[e].elem===this&&i[e].queue===a&&(i[e].anim.stop(!0),i.splice(e,1));for(e=0;e<o;e++)n[e]&&n[e].finish&&n[e].finish.call(this);delete t.finish})}}),S.each(["toggle","show","hide"],function(e,r){var i=S.fn[r];S.fn[r]=function(e,t,n){return null==e||"boolean"==typeof e?i.apply(this,arguments):this.animate(lt(r,!0),e,t,n)}}),S.each({slideDown:lt("show"),slideUp:lt("hide"),slideToggle:lt("toggle"),fadeIn:{opacity:"show"},fadeOut:{opacity:"hide"},fadeToggle:{opacity:"toggle"}},function(e,r){S.fn[e]=function(e,t,n){return this.animate(r,e,t,n)}}),S.timers=[],S.fx.tick=function(){var e,t=0,n=S.timers;for(tt=Date.now();t<n.length;t++)(e=n[t])()||n[t]!==e||n.splice(t--,1);n.length||S.fx.stop(),tt=void 0},S.fx.timer=function(e){S.timers.push(e),S.fx.start()},S.fx.interval=13,S.fx.start=function(){nt||(nt=!0,st())},S.fx.stop=function(){nt=null},S.fx.speeds={slow:600,fast:200,_default:400},S.fn.delay=function(r,e){return r=S.fx&&S.fx.speeds[r]||r,e=e||"fx",this.queue(e,function(e,t){var n=C.setTimeout(e,r);t.stop=function(){C.clearTimeout(n)}})},rt=E.createElement("input"),it=E.createElement("select").appendChild(E.createElement("option")),rt.type="checkbox",y.checkOn=""!==rt.value,y.optSelected=it.selected,(rt=E.createElement("input")).value="t",rt.type="radio",y.radioValue="t"===rt.value;var pt,dt=S.expr.attrHandle;S.fn.extend({attr:function(e,t){return $(this,S.attr,e,t,1<arguments.length)},removeAttr:function(e){return this.each(function(){S.removeAttr(this,e)})}}),S.extend({attr:function(e,t,n){var r,i,o=e.nodeType;if(3!==o&&8!==o&&2!==o)return"undefined"==typeof e.getAttribute?S.prop(e,t,n):(1===o&&S.isXMLDoc(e)||(i=S.attrHooks[t.toLowerCase()]||(S.expr.match.bool.test(t)?pt:void 0)),void 0!==n?null===n?void S.removeAttr(e,t):i&&"set"in i&&void 0!==(r=i.set(e,n,t))?r:(e.setAttribute(t,n+""),n):i&&"get"in i&&null!==(r=i.get(e,t))?r:null==(r=S.find.attr(e,t))?void 0:r)},attrHooks:{type:{set:function(e,t){if(!y.radioValue&&"radio"===t&&A(e,"input")){var n=e.value;return e.setAttribute("type",t),n&&(e.value=n),t}}}},removeAttr:function(e,t){var n,r=0,i=t&&t.match(P);if(i&&1===e.nodeType)while(n=i[r++])e.removeAttribute(n)}}),pt={set:function(e,t,n){return!1===t?S.removeAttr(e,n):e.setAttribute(n,n),n}},S.each(S.expr.match.bool.source.match(/\w+/g),function(e,t){var a=dt[t]||S.find.attr;dt[t]=function(e,t,n){var r,i,o=t.toLowerCase();return n||(i=dt[o],dt[o]=r,r=null!=a(e,t,n)?o:null,dt[o]=i),r}});var ht=/^(?:input|select|textarea|button)$/i,gt=/^(?:a|area)$/i;function vt(e){return(e.match(P)||[]).join(" ")}function yt(e){return e.getAttribute&&e.getAttribute("class")||""}function mt(e){return Array.isArray(e)?e:"string"==typeof e&&e.match(P)||[]}S.fn.extend({prop:function(e,t){return $(this,S.prop,e,t,1<arguments.length)},removeProp:function(e){return this.each(function(){delete this[S.propFix[e]||e]})}}),S.extend({prop:function(e,t,n){var r,i,o=e.nodeType;if(3!==o&&8!==o&&2!==o)return 1===o&&S.isXMLDoc(e)||(t=S.propFix[t]||t,i=S.propHooks[t]),void 0!==n?i&&"set"in i&&void 0!==(r=i.set(e,n,t))?r:e[t]=n:i&&"get"in i&&null!==(r=i.get(e,t))?r:e[t]},propHooks:{tabIndex:{get:function(e){var t=S.find.attr(e,"tabindex");return t?parseInt(t,10):ht.test(e.nodeName)||gt.test(e.nodeName)&&e.href?0:-1}}},propFix:{"for":"htmlFor","class":"className"}}),y.optSelected||(S.propHooks.selected={get:function(e){var t=e.parentNode;return t&&t.parentNode&&t.parentNode.selectedIndex,null},set:function(e){var t=e.parentNode;t&&(t.selectedIndex,t.parentNode&&t.parentNode.selectedIndex)}}),S.each(["tabIndex","readOnly","maxLength","cellSpacing","cellPadding","rowSpan","colSpan","useMap","frameBorder","contentEditable"],function(){S.propFix[this.toLowerCase()]=this}),S.fn.extend({addClass:function(t){var e,n,r,i,o,a,s,u=0;if(m(t))return this.each(function(e){S(this).addClass(t.call(this,e,yt(this)))});if((e=mt(t)).length)while(n=this[u++])if(i=yt(n),r=1===n.nodeType&&" "+vt(i)+" "){a=0;while(o=e[a++])r.indexOf(" "+o+" ")<0&&(r+=o+" ");i!==(s=vt(r))&&n.setAttribute("class",s)}return this},removeClass:function(t){var e,n,r,i,o,a,s,u=0;if(m(t))return this.each(function(e){S(this).removeClass(t.call(this,e,yt(this)))});if(!arguments.length)return this.attr("class","");if((e=mt(t)).length)while(n=this[u++])if(i=yt(n),r=1===n.nodeType&&" "+vt(i)+" "){a=0;while(o=e[a++])while(-1<r.indexOf(" "+o+" "))r=r.replace(" "+o+" "," ");i!==(s=vt(r))&&n.setAttribute("class",s)}return this},toggleClass:function(i,t){var o=typeof i,a="string"===o||Array.isArray(i);return"boolean"==typeof t&&a?t?this.addClass(i):this.removeClass(i):m(i)?this.each(function(e){S(this).toggleClass(i.call(this,e,yt(this),t),t)}):this.each(function(){var e,t,n,r;if(a){t=0,n=S(this),r=mt(i);while(e=r[t++])n.hasClass(e)?n.removeClass(e):n.addClass(e)}else void 0!==i&&"boolean"!==o||((e=yt(this))&&Y.set(this,"__className__",e),this.setAttribute&&this.setAttribute("class",e||!1===i?"":Y.get(this,"__className__")||""))})},hasClass:function(e){var t,n,r=0;t=" "+e+" ";while(n=this[r++])if(1===n.nodeType&&-1<(" "+vt(yt(n))+" ").indexOf(t))return!0;return!1}});var xt=/\r/g;S.fn.extend({val:function(n){var r,e,i,t=this[0];return arguments.length?(i=m(n),this.each(function(e){var t;1===this.nodeType&&(null==(t=i?n.call(this,e,S(this).val()):n)?t="":"number"==typeof t?t+="":Array.isArray(t)&&(t=S.map(t,function(e){return null==e?"":e+""})),(r=S.valHooks[this.type]||S.valHooks[this.nodeName.toLowerCase()])&&"set"in r&&void 0!==r.set(this,t,"value")||(this.value=t))})):t?(r=S.valHooks[t.type]||S.valHooks[t.nodeName.toLowerCase()])&&"get"in r&&void 0!==(e=r.get(t,"value"))?e:"string"==typeof(e=t.value)?e.replace(xt,""):null==e?"":e:void 0}}),S.extend({valHooks:{option:{get:function(e){var t=S.find.attr(e,"value");return null!=t?t:vt(S.text(e))}},select:{get:function(e){var t,n,r,i=e.options,o=e.selectedIndex,a="select-one"===e.type,s=a?null:[],u=a?o+1:i.length;for(r=o<0?u:a?o:0;r<u;r++)if(((n=i[r]).selected||r===o)&&!n.disabled&&(!n.parentNode.disabled||!A(n.parentNode,"optgroup"))){if(t=S(n).val(),a)return t;s.push(t)}return s},set:function(e,t){var n,r,i=e.options,o=S.makeArray(t),a=i.length;while(a--)((r=i[a]).selected=-1<S.inArray(S.valHooks.option.get(r),o))&&(n=!0);return n||(e.selectedIndex=-1),o}}}}),S.each(["radio","checkbox"],function(){S.valHooks[this]={set:function(e,t){if(Array.isArray(t))return e.checked=-1<S.inArray(S(e).val(),t)}},y.checkOn||(S.valHooks[this].get=function(e){return null===e.getAttribute("value")?"on":e.value})}),y.focusin="onfocusin"in C;var bt=/^(?:focusinfocus|focusoutblur)$/,wt=function(e){e.stopPropagation()};S.extend(S.event,{trigger:function(e,t,n,r){var i,o,a,s,u,l,c,f,p=[n||E],d=v.call(e,"type")?e.type:e,h=v.call(e,"namespace")?e.namespace.split("."):[];if(o=f=a=n=n||E,3!==n.nodeType&&8!==n.nodeType&&!bt.test(d+S.event.triggered)&&(-1<d.indexOf(".")&&(d=(h=d.split(".")).shift(),h.sort()),u=d.indexOf(":")<0&&"on"+d,(e=e[S.expando]?e:new S.Event(d,"object"==typeof e&&e)).isTrigger=r?2:3,e.namespace=h.join("."),e.rnamespace=e.namespace?new RegExp("(^|\\.)"+h.join("\\.(?:.*\\.|)")+"(\\.|$)"):null,e.result=void 0,e.target||(e.target=n),t=null==t?[e]:S.makeArray(t,[e]),c=S.event.special[d]||{},r||!c.trigger||!1!==c.trigger.apply(n,t))){if(!r&&!c.noBubble&&!x(n)){for(s=c.delegateType||d,bt.test(s+d)||(o=o.parentNode);o;o=o.parentNode)p.push(o),a=o;a===(n.ownerDocument||E)&&p.push(a.defaultView||a.parentWindow||C)}i=0;while((o=p[i++])&&!e.isPropagationStopped())f=o,e.type=1<i?s:c.bindType||d,(l=(Y.get(o,"events")||Object.create(null))[e.type]&&Y.get(o,"handle"))&&l.apply(o,t),(l=u&&o[u])&&l.apply&&V(o)&&(e.result=l.apply(o,t),!1===e.result&&e.preventDefault());return e.type=d,r||e.isDefaultPrevented()||c._default&&!1!==c._default.apply(p.pop(),t)||!V(n)||u&&m(n[d])&&!x(n)&&((a=n[u])&&(n[u]=null),S.event.triggered=d,e.isPropagationStopped()&&f.addEventListener(d,wt),n[d](),e.isPropagationStopped()&&f.removeEventListener(d,wt),S.event.triggered=void 0,a&&(n[u]=a)),e.result}},simulate:function(e,t,n){var r=S.extend(new S.Event,n,{type:e,isSimulated:!0});S.event.trigger(r,null,t)}}),S.fn.extend({trigger:function(e,t){return this.each(function(){S.event.trigger(e,t,this)})},triggerHandler:function(e,t){var n=this[0];if(n)return S.event.trigger(e,t,n,!0)}}),y.focusin||S.each({focus:"focusin",blur:"focusout"},function(n,r){var i=function(e){S.event.simulate(r,e.target,S.event.fix(e))};S.event.special[r]={setup:function(){var e=this.ownerDocument||this.document||this,t=Y.access(e,r);t||e.addEventListener(n,i,!0),Y.access(e,r,(t||0)+1)},teardown:function(){var e=this.ownerDocument||this.document||this,t=Y.access(e,r)-1;t?Y.access(e,r,t):(e.removeEventListener(n,i,!0),Y.remove(e,r))}}});var Tt=C.location,Ct={guid:Date.now()},Et=/\?/;S.parseXML=function(e){var t;if(!e||"string"!=typeof e)return null;try{t=(new C.DOMParser).parseFromString(e,"text/xml")}catch(e){t=void 0}return t&&!t.getElementsByTagName("parsererror").length||S.error("Invalid XML: "+e),t};var St=/\[\]$/,kt=/\r?\n/g,At=/^(?:submit|button|image|reset|file)$/i,Nt=/^(?:input|select|textarea|keygen)/i;function Dt(n,e,r,i){var t;if(Array.isArray(e))S.each(e,function(e,t){r||St.test(n)?i(n,t):Dt(n+"["+("object"==typeof t&&null!=t?e:"")+"]",t,r,i)});else if(r||"object"!==w(e))i(n,e);else for(t in e)Dt(n+"["+t+"]",e[t],r,i)}S.param=function(e,t){var n,r=[],i=function(e,t){var n=m(t)?t():t;r[r.length]=encodeURIComponent(e)+"="+encodeURIComponent(null==n?"":n)};if(null==e)return"";if(Array.isArray(e)||e.jquery&&!S.isPlainObject(e))S.each(e,function(){i(this.name,this.value)});else for(n in e)Dt(n,e[n],t,i);return r.join("&")},S.fn.extend({serialize:function(){return S.param(this.serializeArray())},serializeArray:function(){return this.map(function(){var e=S.prop(this,"elements");return e?S.makeArray(e):this}).filter(function(){var e=this.type;return this.name&&!S(this).is(":disabled")&&Nt.test(this.nodeName)&&!At.test(e)&&(this.checked||!pe.test(e))}).map(function(e,t){var n=S(this).val();return null==n?null:Array.isArray(n)?S.map(n,function(e){return{name:t.name,value:e.replace(kt,"\r\n")}}):{name:t.name,value:n.replace(kt,"\r\n")}}).get()}});var jt=/%20/g,qt=/#.*$/,Lt=/([?&])_=[^&]*/,Ht=/^(.*?):[ \t]*([^\r\n]*)$/gm,Ot=/^(?:GET|HEAD)$/,Pt=/^\/\//,Rt={},Mt={},It="*/".concat("*"),Wt=E.createElement("a");function Ft(o){return function(e,t){"string"!=typeof e&&(t=e,e="*");var n,r=0,i=e.toLowerCase().match(P)||[];if(m(t))while(n=i[r++])"+"===n[0]?(n=n.slice(1)||"*",(o[n]=o[n]||[]).unshift(t)):(o[n]=o[n]||[]).push(t)}}function Bt(t,i,o,a){var s={},u=t===Mt;function l(e){var r;return s[e]=!0,S.each(t[e]||[],function(e,t){var n=t(i,o,a);return"string"!=typeof n||u||s[n]?u?!(r=n):void 0:(i.dataTypes.unshift(n),l(n),!1)}),r}return l(i.dataTypes[0])||!s["*"]&&l("*")}function $t(e,t){var n,r,i=S.ajaxSettings.flatOptions||{};for(n in t)void 0!==t[n]&&((i[n]?e:r||(r={}))[n]=t[n]);return r&&S.extend(!0,e,r),e}Wt.href=Tt.href,S.extend({active:0,lastModified:{},etag:{},ajaxSettings:{url:Tt.href,type:"GET",isLocal:/^(?:about|app|app-storage|.+-extension|file|res|widget):$/.test(Tt.protocol),global:!0,processData:!0,async:!0,contentType:"application/x-www-form-urlencoded; charset=UTF-8",accepts:{"*":It,text:"text/plain",html:"text/html",xml:"application/xml, text/xml",json:"application/json, text/javascript"},contents:{xml:/\bxml\b/,html:/\bhtml/,json:/\bjson\b/},responseFields:{xml:"responseXML",text:"responseText",json:"responseJSON"},converters:{"* text":String,"text html":!0,"text json":JSON.parse,"text xml":S.parseXML},flatOptions:{url:!0,context:!0}},ajaxSetup:function(e,t){return t?$t($t(e,S.ajaxSettings),t):$t(S.ajaxSettings,e)},ajaxPrefilter:Ft(Rt),ajaxTransport:Ft(Mt),ajax:function(e,t){"object"==typeof e&&(t=e,e=void 0),t=t||{};var c,f,p,n,d,r,h,g,i,o,v=S.ajaxSetup({},t),y=v.context||v,m=v.context&&(y.nodeType||y.jquery)?S(y):S.event,x=S.Deferred(),b=S.Callbacks("once memory"),w=v.statusCode||{},a={},s={},u="canceled",T={readyState:0,getResponseHeader:function(e){var t;if(h){if(!n){n={};while(t=Ht.exec(p))n[t[1].toLowerCase()+" "]=(n[t[1].toLowerCase()+" "]||[]).concat(t[2])}t=n[e.toLowerCase()+" "]}return null==t?null:t.join(", ")},getAllResponseHeaders:function(){return h?p:null},setRequestHeader:function(e,t){return null==h&&(e=s[e.toLowerCase()]=s[e.toLowerCase()]||e,a[e]=t),this},overrideMimeType:function(e){return null==h&&(v.mimeType=e),this},statusCode:function(e){var t;if(e)if(h)T.always(e[T.status]);else for(t in e)w[t]=[w[t],e[t]];return this},abort:function(e){var t=e||u;return c&&c.abort(t),l(0,t),this}};if(x.promise(T),v.url=((e||v.url||Tt.href)+"").replace(Pt,Tt.protocol+"//"),v.type=t.method||t.type||v.method||v.type,v.dataTypes=(v.dataType||"*").toLowerCase().match(P)||[""],null==v.crossDomain){r=E.createElement("a");try{r.href=v.url,r.href=r.href,v.crossDomain=Wt.protocol+"//"+Wt.host!=r.protocol+"//"+r.host}catch(e){v.crossDomain=!0}}if(v.data&&v.processData&&"string"!=typeof v.data&&(v.data=S.param(v.data,v.traditional)),Bt(Rt,v,t,T),h)return T;for(i in(g=S.event&&v.global)&&0==S.active++&&S.event.trigger("ajaxStart"),v.type=v.type.toUpperCase(),v.hasContent=!Ot.test(v.type),f=v.url.replace(qt,""),v.hasContent?v.data&&v.processData&&0===(v.contentType||"").indexOf("application/x-www-form-urlencoded")&&(v.data=v.data.replace(jt,"+")):(o=v.url.slice(f.length),v.data&&(v.processData||"string"==typeof v.data)&&(f+=(Et.test(f)?"&":"?")+v.data,delete v.data),!1===v.cache&&(f=f.replace(Lt,"$1"),o=(Et.test(f)?"&":"?")+"_="+Ct.guid+++o),v.url=f+o),v.ifModified&&(S.lastModified[f]&&T.setRequestHeader("If-Modified-Since",S.lastModified[f]),S.etag[f]&&T.setRequestHeader("If-None-Match",S.etag[f])),(v.data&&v.hasContent&&!1!==v.contentType||t.contentType)&&T.setRequestHeader("Content-Type",v.contentType),T.setRequestHeader("Accept",v.dataTypes[0]&&v.accepts[v.dataTypes[0]]?v.accepts[v.dataTypes[0]]+("*"!==v.dataTypes[0]?", "+It+"; q=0.01":""):v.accepts["*"]),v.headers)T.setRequestHeader(i,v.headers[i]);if(v.beforeSend&&(!1===v.beforeSend.call(y,T,v)||h))return T.abort();if(u="abort",b.add(v.complete),T.done(v.success),T.fail(v.error),c=Bt(Mt,v,t,T)){if(T.readyState=1,g&&m.trigger("ajaxSend",[T,v]),h)return T;v.async&&0<v.timeout&&(d=C.setTimeout(function(){T.abort("timeout")},v.timeout));try{h=!1,c.send(a,l)}catch(e){if(h)throw e;l(-1,e)}}else l(-1,"No Transport");function l(e,t,n,r){var i,o,a,s,u,l=t;h||(h=!0,d&&C.clearTimeout(d),c=void 0,p=r||"",T.readyState=0<e?4:0,i=200<=e&&e<300||304===e,n&&(s=function(e,t,n){var r,i,o,a,s=e.contents,u=e.dataTypes;while("*"===u[0])u.shift(),void 0===r&&(r=e.mimeType||t.getResponseHeader("Content-Type"));if(r)for(i in s)if(s[i]&&s[i].test(r)){u.unshift(i);break}if(u[0]in n)o=u[0];else{for(i in n){if(!u[0]||e.converters[i+" "+u[0]]){o=i;break}a||(a=i)}o=o||a}if(o)return o!==u[0]&&u.unshift(o),n[o]}(v,T,n)),!i&&-1<S.inArray("script",v.dataTypes)&&(v.converters["text script"]=function(){}),s=function(e,t,n,r){var i,o,a,s,u,l={},c=e.dataTypes.slice();if(c[1])for(a in e.converters)l[a.toLowerCase()]=e.converters[a];o=c.shift();while(o)if(e.responseFields[o]&&(n[e.responseFields[o]]=t),!u&&r&&e.dataFilter&&(t=e.dataFilter(t,e.dataType)),u=o,o=c.shift())if("*"===o)o=u;else if("*"!==u&&u!==o){if(!(a=l[u+" "+o]||l["* "+o]))for(i in l)if((s=i.split(" "))[1]===o&&(a=l[u+" "+s[0]]||l["* "+s[0]])){!0===a?a=l[i]:!0!==l[i]&&(o=s[0],c.unshift(s[1]));break}if(!0!==a)if(a&&e["throws"])t=a(t);else try{t=a(t)}catch(e){return{state:"parsererror",error:a?e:"No conversion from "+u+" to "+o}}}return{state:"success",data:t}}(v,s,T,i),i?(v.ifModified&&((u=T.getResponseHeader("Last-Modified"))&&(S.lastModified[f]=u),(u=T.getResponseHeader("etag"))&&(S.etag[f]=u)),204===e||"HEAD"===v.type?l="nocontent":304===e?l="notmodified":(l=s.state,o=s.data,i=!(a=s.error))):(a=l,!e&&l||(l="error",e<0&&(e=0))),T.status=e,T.statusText=(t||l)+"",i?x.resolveWith(y,[o,l,T]):x.rejectWith(y,[T,l,a]),T.statusCode(w),w=void 0,g&&m.trigger(i?"ajaxSuccess":"ajaxError",[T,v,i?o:a]),b.fireWith(y,[T,l]),g&&(m.trigger("ajaxComplete",[T,v]),--S.active||S.event.trigger("ajaxStop")))}return T},getJSON:function(e,t,n){return S.get(e,t,n,"json")},getScript:function(e,t){return S.get(e,void 0,t,"script")}}),S.each(["get","post"],function(e,i){S[i]=function(e,t,n,r){return m(t)&&(r=r||n,n=t,t=void 0),S.ajax(S.extend({url:e,type:i,dataType:r,data:t,success:n},S.isPlainObject(e)&&e))}}),S.ajaxPrefilter(function(e){var t;for(t in e.headers)"content-type"===t.toLowerCase()&&(e.contentType=e.headers[t]||"")}),S._evalUrl=function(e,t,n){return S.ajax({url:e,type:"GET",dataType:"script",cache:!0,async:!1,global:!1,converters:{"text script":function(){}},dataFilter:function(e){S.globalEval(e,t,n)}})},S.fn.extend({wrapAll:function(e){var t;return this[0]&&(m(e)&&(e=e.call(this[0])),t=S(e,this[0].ownerDocument).eq(0).clone(!0),this[0].parentNode&&t.insertBefore(this[0]),t.map(function(){var e=this;while(e.firstElementChild)e=e.firstElementChild;return e}).append(this)),this},wrapInner:function(n){return m(n)?this.each(function(e){S(this).wrapInner(n.call(this,e))}):this.each(function(){var e=S(this),t=e.contents();t.length?t.wrapAll(n):e.append(n)})},wrap:function(t){var n=m(t);return this.each(function(e){S(this).wrapAll(n?t.call(this,e):t)})},unwrap:function(e){return this.parent(e).not("body").each(function(){S(this).replaceWith(this.childNodes)}),this}}),S.expr.pseudos.hidden=function(e){return!S.expr.pseudos.visible(e)},S.expr.pseudos.visible=function(e){return!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length)},S.ajaxSettings.xhr=function(){try{return new C.XMLHttpRequest}catch(e){}};var _t={0:200,1223:204},zt=S.ajaxSettings.xhr();y.cors=!!zt&&"withCredentials"in zt,y.ajax=zt=!!zt,S.ajaxTransport(function(i){var o,a;if(y.cors||zt&&!i.crossDomain)return{send:function(e,t){var n,r=i.xhr();if(r.open(i.type,i.url,i.async,i.username,i.password),i.xhrFields)for(n in i.xhrFields)r[n]=i.xhrFields[n];for(n in i.mimeType&&r.overrideMimeType&&r.overrideMimeType(i.mimeType),i.crossDomain||e["X-Requested-With"]||(e["X-Requested-With"]="XMLHttpRequest"),e)r.setRequestHeader(n,e[n]);o=function(e){return function(){o&&(o=a=r.onload=r.onerror=r.onabort=r.ontimeout=r.onreadystatechange=null,"abort"===e?r.abort():"error"===e?"number"!=typeof r.status?t(0,"error"):t(r.status,r.statusText):t(_t[r.status]||r.status,r.statusText,"text"!==(r.responseType||"text")||"string"!=typeof r.responseText?{binary:r.response}:{text:r.responseText},r.getAllResponseHeaders()))}},r.onload=o(),a=r.onerror=r.ontimeout=o("error"),void 0!==r.onabort?r.onabort=a:r.onreadystatechange=function(){4===r.readyState&&C.setTimeout(function(){o&&a()})},o=o("abort");try{r.send(i.hasContent&&i.data||null)}catch(e){if(o)throw e}},abort:function(){o&&o()}}}),S.ajaxPrefilter(function(e){e.crossDomain&&(e.contents.script=!1)}),S.ajaxSetup({accepts:{script:"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},contents:{script:/\b(?:java|ecma)script\b/},converters:{"text script":function(e){return S.globalEval(e),e}}}),S.ajaxPrefilter("script",function(e){void 0===e.cache&&(e.cache=!1),e.crossDomain&&(e.type="GET")}),S.ajaxTransport("script",function(n){var r,i;if(n.crossDomain||n.scriptAttrs)return{send:function(e,t){r=S("<script>").attr(n.scriptAttrs||{}).prop({charset:n.scriptCharset,src:n.url}).on("load error",i=function(e){r.remove(),i=null,e&&t("error"===e.type?404:200,e.type)}),E.head.appendChild(r[0])},abort:function(){i&&i()}}});var Ut,Xt=[],Vt=/(=)\?(?=&|$)|\?\?/;S.ajaxSetup({jsonp:"callback",jsonpCallback:function(){var e=Xt.pop()||S.expando+"_"+Ct.guid++;return this[e]=!0,e}}),S.ajaxPrefilter("json jsonp",function(e,t,n){var r,i,o,a=!1!==e.jsonp&&(Vt.test(e.url)?"url":"string"==typeof e.data&&0===(e.contentType||"").indexOf("application/x-www-form-urlencoded")&&Vt.test(e.data)&&"data");if(a||"jsonp"===e.dataTypes[0])return r=e.jsonpCallback=m(e.jsonpCallback)?e.jsonpCallback():e.jsonpCallback,a?e[a]=e[a].replace(Vt,"$1"+r):!1!==e.jsonp&&(e.url+=(Et.test(e.url)?"&":"?")+e.jsonp+"="+r),e.converters["script json"]=function(){return o||S.error(r+" was not called"),o[0]},e.dataTypes[0]="json",i=C[r],C[r]=function(){o=arguments},n.always(function(){void 0===i?S(C).removeProp(r):C[r]=i,e[r]&&(e.jsonpCallback=t.jsonpCallback,Xt.push(r)),o&&m(i)&&i(o[0]),o=i=void 0}),"script"}),y.createHTMLDocument=((Ut=E.implementation.createHTMLDocument("").body).innerHTML="<form></form><form></form>",2===Ut.childNodes.length),S.parseHTML=function(e,t,n){return"string"!=typeof e?[]:("boolean"==typeof t&&(n=t,t=!1),t||(y.createHTMLDocument?((r=(t=E.implementation.createHTMLDocument("")).createElement("base")).href=E.location.href,t.head.appendChild(r)):t=E),o=!n&&[],(i=N.exec(e))?[t.createElement(i[1])]:(i=xe([e],t,o),o&&o.length&&S(o).remove(),S.merge([],i.childNodes)));var r,i,o},S.fn.load=function(e,t,n){var r,i,o,a=this,s=e.indexOf(" ");return-1<s&&(r=vt(e.slice(s)),e=e.slice(0,s)),m(t)?(n=t,t=void 0):t&&"object"==typeof t&&(i="POST"),0<a.length&&S.ajax({url:e,type:i||"GET",dataType:"html",data:t}).done(function(e){o=arguments,a.html(r?S("<div>").append(S.parseHTML(e)).find(r):e)}).always(n&&function(e,t){a.each(function(){n.apply(this,o||[e.responseText,t,e])})}),this},S.expr.pseudos.animated=function(t){return S.grep(S.timers,function(e){return t===e.elem}).length},S.offset={setOffset:function(e,t,n){var r,i,o,a,s,u,l=S.css(e,"position"),c=S(e),f={};"static"===l&&(e.style.position="relative"),s=c.offset(),o=S.css(e,"top"),u=S.css(e,"left"),("absolute"===l||"fixed"===l)&&-1<(o+u).indexOf("auto")?(a=(r=c.position()).top,i=r.left):(a=parseFloat(o)||0,i=parseFloat(u)||0),m(t)&&(t=t.call(e,n,S.extend({},s))),null!=t.top&&(f.top=t.top-s.top+a),null!=t.left&&(f.left=t.left-s.left+i),"using"in t?t.using.call(e,f):("number"==typeof f.top&&(f.top+="px"),"number"==typeof f.left&&(f.left+="px"),c.css(f))}},S.fn.extend({offset:function(t){if(arguments.length)return void 0===t?this:this.each(function(e){S.offset.setOffset(this,t,e)});var e,n,r=this[0];return r?r.getClientRects().length?(e=r.getBoundingClientRect(),n=r.ownerDocument.defaultView,{top:e.top+n.pageYOffset,left:e.left+n.pageXOffset}):{top:0,left:0}:void 0},position:function(){if(this[0]){var e,t,n,r=this[0],i={top:0,left:0};if("fixed"===S.css(r,"position"))t=r.getBoundingClientRect();else{t=this.offset(),n=r.ownerDocument,e=r.offsetParent||n.documentElement;while(e&&(e===n.body||e===n.documentElement)&&"static"===S.css(e,"position"))e=e.parentNode;e&&e!==r&&1===e.nodeType&&((i=S(e).offset()).top+=S.css(e,"borderTopWidth",!0),i.left+=S.css(e,"borderLeftWidth",!0))}return{top:t.top-i.top-S.css(r,"marginTop",!0),left:t.left-i.left-S.css(r,"marginLeft",!0)}}},offsetParent:function(){return this.map(function(){var e=this.offsetParent;while(e&&"static"===S.css(e,"position"))e=e.offsetParent;return e||re})}}),S.each({scrollLeft:"pageXOffset",scrollTop:"pageYOffset"},function(t,i){var o="pageYOffset"===i;S.fn[t]=function(e){return $(this,function(e,t,n){var r;if(x(e)?r=e:9===e.nodeType&&(r=e.defaultView),void 0===n)return r?r[i]:e[t];r?r.scrollTo(o?r.pageXOffset:n,o?n:r.pageYOffset):e[t]=n},t,e,arguments.length)}}),S.each(["top","left"],function(e,n){S.cssHooks[n]=$e(y.pixelPosition,function(e,t){if(t)return t=Be(e,n),Me.test(t)?S(e).position()[n]+"px":t})}),S.each({Height:"height",Width:"width"},function(a,s){S.each({padding:"inner"+a,content:s,"":"outer"+a},function(r,o){S.fn[o]=function(e,t){var n=arguments.length&&(r||"boolean"!=typeof e),i=r||(!0===e||!0===t?"margin":"border");return $(this,function(e,t,n){var r;return x(e)?0===o.indexOf("outer")?e["inner"+a]:e.document.documentElement["client"+a]:9===e.nodeType?(r=e.documentElement,Math.max(e.body["scroll"+a],r["scroll"+a],e.body["offset"+a],r["offset"+a],r["client"+a])):void 0===n?S.css(e,t,i):S.style(e,t,n,i)},s,n?e:void 0,n)}})}),S.each(["ajaxStart","ajaxStop","ajaxComplete","ajaxError","ajaxSuccess","ajaxSend"],function(e,t){S.fn[t]=function(e){return this.on(t,e)}}),S.fn.extend({bind:function(e,t,n){return this.on(e,null,t,n)},unbind:function(e,t){return this.off(e,null,t)},delegate:function(e,t,n,r){return this.on(t,e,n,r)},undelegate:function(e,t,n){return 1===arguments.length?this.off(e,"**"):this.off(t,e||"**",n)},hover:function(e,t){return this.mouseenter(e).mouseleave(t||e)}}),S.each("blur focus focusin focusout resize scroll click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup contextmenu".split(" "),function(e,n){S.fn[n]=function(e,t){return 0<arguments.length?this.on(n,null,e,t):this.trigger(n)}});var Gt=/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g;S.proxy=function(e,t){var n,r,i;if("string"==typeof t&&(n=e[t],t=e,e=n),m(e))return r=s.call(arguments,2),(i=function(){return e.apply(t||this,r.concat(s.call(arguments)))}).guid=e.guid=e.guid||S.guid++,i},S.holdReady=function(e){e?S.readyWait++:S.ready(!0)},S.isArray=Array.isArray,S.parseJSON=JSON.parse,S.nodeName=A,S.isFunction=m,S.isWindow=x,S.camelCase=X,S.type=w,S.now=Date.now,S.isNumeric=function(e){var t=S.type(e);return("number"===t||"string"===t)&&!isNaN(e-parseFloat(e))},S.trim=function(e){return null==e?"":(e+"").replace(Gt,"")},"function"==typeof define&&define.amd&&define("jquery",[],function(){return S});var Yt=C.jQuery,Qt=C.$;return S.noConflict=function(e){return C.$===S&&(C.$=Qt),e&&C.jQuery===S&&(C.jQuery=Yt),S},"undefined"==typeof e&&(C.jQuery=C.$=S),S});

!function(t,r){"object"==typeof exports?module.exports=exports=r():"function"==typeof define&&define.amd?define([],r):t.CryptoJS=r()}(this,function(){var t=t||function(t,r){var e=Object.create||function(){function t(){}return function(r){var e;return t.prototype=r,e=new t,t.prototype=null,e}}(),i={},n=i.lib={},o=n.Base=function(){return{extend:function(t){var r=e(this);return t&&r.mixIn(t),r.hasOwnProperty("init")&&this.init!==r.init||(r.init=function(){r.$super.init.apply(this,arguments)}),r.init.prototype=r,r.$super=this,r},create:function(){var t=this.extend();return t.init.apply(t,arguments),t},init:function(){},mixIn:function(t){for(var r in t)t.hasOwnProperty(r)&&(this[r]=t[r]);t.hasOwnProperty("toString")&&(this.toString=t.toString)},clone:function(){return this.init.prototype.extend(this)}}}(),s=n.WordArray=o.extend({init:function(t,e){t=this.words=t||[],e!=r?this.sigBytes=e:this.sigBytes=4*t.length},toString:function(t){return(t||c).stringify(this)},concat:function(t){var r=this.words,e=t.words,i=this.sigBytes,n=t.sigBytes;if(this.clamp(),i%4)for(var o=0;o<n;o++){var s=e[o>>>2]>>>24-o%4*8&255;r[i+o>>>2]|=s<<24-(i+o)%4*8}else for(var o=0;o<n;o+=4)r[i+o>>>2]=e[o>>>2];return this.sigBytes+=n,this},clamp:function(){var r=this.words,e=this.sigBytes;r[e>>>2]&=4294967295<<32-e%4*8,r.length=t.ceil(e/4)},clone:function(){var t=o.clone.call(this);return t.words=this.words.slice(0),t},random:function(r){for(var e,i=[],n=function(r){var r=r,e=987654321,i=4294967295;return function(){e=36969*(65535&e)+(e>>16)&i,r=18e3*(65535&r)+(r>>16)&i;var n=(e<<16)+r&i;return n/=4294967296,n+=.5,n*(t.random()>.5?1:-1)}},o=0;o<r;o+=4){var a=n(4294967296*(e||t.random()));e=987654071*a(),i.push(4294967296*a()|0)}return new s.init(i,r)}}),a=i.enc={},c=a.Hex={stringify:function(t){for(var r=t.words,e=t.sigBytes,i=[],n=0;n<e;n++){var o=r[n>>>2]>>>24-n%4*8&255;i.push((o>>>4).toString(16)),i.push((15&o).toString(16))}return i.join("")},parse:function(t){for(var r=t.length,e=[],i=0;i<r;i+=2)e[i>>>3]|=parseInt(t.substr(i,2),16)<<24-i%8*4;return new s.init(e,r/2)}},h=a.Latin1={stringify:function(t){for(var r=t.words,e=t.sigBytes,i=[],n=0;n<e;n++){var o=r[n>>>2]>>>24-n%4*8&255;i.push(String.fromCharCode(o))}return i.join("")},parse:function(t){for(var r=t.length,e=[],i=0;i<r;i++)e[i>>>2]|=(255&t.charCodeAt(i))<<24-i%4*8;return new s.init(e,r)}},l=a.Utf8={stringify:function(t){try{return decodeURIComponent(escape(h.stringify(t)))}catch(t){throw new Error("Malformed UTF-8 data")}},parse:function(t){return h.parse(unescape(encodeURIComponent(t)))}},f=n.BufferedBlockAlgorithm=o.extend({reset:function(){this._data=new s.init,this._nDataBytes=0},_append:function(t){"string"==typeof t&&(t=l.parse(t)),this._data.concat(t),this._nDataBytes+=t.sigBytes},_process:function(r){var e=this._data,i=e.words,n=e.sigBytes,o=this.blockSize,a=4*o,c=n/a;c=r?t.ceil(c):t.max((0|c)-this._minBufferSize,0);var h=c*o,l=t.min(4*h,n);if(h){for(var f=0;f<h;f+=o)this._doProcessBlock(i,f);var u=i.splice(0,h);e.sigBytes-=l}return new s.init(u,l)},clone:function(){var t=o.clone.call(this);return t._data=this._data.clone(),t},_minBufferSize:0}),u=(n.Hasher=f.extend({cfg:o.extend(),init:function(t){this.cfg=this.cfg.extend(t),this.reset()},reset:function(){f.reset.call(this),this._doReset()},update:function(t){return this._append(t),this._process(),this},finalize:function(t){t&&this._append(t);var r=this._doFinalize();return r},blockSize:16,_createHelper:function(t){return function(r,e){return new t.init(e).finalize(r)}},_createHmacHelper:function(t){return function(r,e){return new u.HMAC.init(t,e).finalize(r)}}}),i.algo={});return i}(Math);return function(){function r(t,r,e){for(var i=[],o=0,s=0;s<r;s++)if(s%4){var a=e[t.charCodeAt(s-1)]<<s%4*2,c=e[t.charCodeAt(s)]>>>6-s%4*2;i[o>>>2]|=(a|c)<<24-o%4*8,o++}return n.create(i,o)}var e=t,i=e.lib,n=i.WordArray,o=e.enc;o.Base64={stringify:function(t){var r=t.words,e=t.sigBytes,i=this._map;t.clamp();for(var n=[],o=0;o<e;o+=3)for(var s=r[o>>>2]>>>24-o%4*8&255,a=r[o+1>>>2]>>>24-(o+1)%4*8&255,c=r[o+2>>>2]>>>24-(o+2)%4*8&255,h=s<<16|a<<8|c,l=0;l<4&&o+.75*l<e;l++)n.push(i.charAt(h>>>6*(3-l)&63));var f=i.charAt(64);if(f)for(;n.length%4;)n.push(f);return n.join("")},parse:function(t){var e=t.length,i=this._map,n=this._reverseMap;if(!n){n=this._reverseMap=[];for(var o=0;o<i.length;o++)n[i.charCodeAt(o)]=o}var s=i.charAt(64);if(s){var a=t.indexOf(s);a!==-1&&(e=a)}return r(t,e,n)},_map:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="}}(),function(r){function e(t,r,e,i,n,o,s){var a=t+(r&e|~r&i)+n+s;return(a<<o|a>>>32-o)+r}function i(t,r,e,i,n,o,s){var a=t+(r&i|e&~i)+n+s;return(a<<o|a>>>32-o)+r}function n(t,r,e,i,n,o,s){var a=t+(r^e^i)+n+s;return(a<<o|a>>>32-o)+r}function o(t,r,e,i,n,o,s){var a=t+(e^(r|~i))+n+s;return(a<<o|a>>>32-o)+r}var s=t,a=s.lib,c=a.WordArray,h=a.Hasher,l=s.algo,f=[];!function(){for(var t=0;t<64;t++)f[t]=4294967296*r.abs(r.sin(t+1))|0}();var u=l.MD5=h.extend({_doReset:function(){this._hash=new c.init([1732584193,4023233417,2562383102,271733878])},_doProcessBlock:function(t,r){for(var s=0;s<16;s++){var a=r+s,c=t[a];t[a]=16711935&(c<<8|c>>>24)|4278255360&(c<<24|c>>>8)}var h=this._hash.words,l=t[r+0],u=t[r+1],d=t[r+2],v=t[r+3],p=t[r+4],_=t[r+5],y=t[r+6],g=t[r+7],B=t[r+8],w=t[r+9],k=t[r+10],S=t[r+11],m=t[r+12],x=t[r+13],b=t[r+14],H=t[r+15],z=h[0],A=h[1],C=h[2],D=h[3];z=e(z,A,C,D,l,7,f[0]),D=e(D,z,A,C,u,12,f[1]),C=e(C,D,z,A,d,17,f[2]),A=e(A,C,D,z,v,22,f[3]),z=e(z,A,C,D,p,7,f[4]),D=e(D,z,A,C,_,12,f[5]),C=e(C,D,z,A,y,17,f[6]),A=e(A,C,D,z,g,22,f[7]),z=e(z,A,C,D,B,7,f[8]),D=e(D,z,A,C,w,12,f[9]),C=e(C,D,z,A,k,17,f[10]),A=e(A,C,D,z,S,22,f[11]),z=e(z,A,C,D,m,7,f[12]),D=e(D,z,A,C,x,12,f[13]),C=e(C,D,z,A,b,17,f[14]),A=e(A,C,D,z,H,22,f[15]),z=i(z,A,C,D,u,5,f[16]),D=i(D,z,A,C,y,9,f[17]),C=i(C,D,z,A,S,14,f[18]),A=i(A,C,D,z,l,20,f[19]),z=i(z,A,C,D,_,5,f[20]),D=i(D,z,A,C,k,9,f[21]),C=i(C,D,z,A,H,14,f[22]),A=i(A,C,D,z,p,20,f[23]),z=i(z,A,C,D,w,5,f[24]),D=i(D,z,A,C,b,9,f[25]),C=i(C,D,z,A,v,14,f[26]),A=i(A,C,D,z,B,20,f[27]),z=i(z,A,C,D,x,5,f[28]),D=i(D,z,A,C,d,9,f[29]),C=i(C,D,z,A,g,14,f[30]),A=i(A,C,D,z,m,20,f[31]),z=n(z,A,C,D,_,4,f[32]),D=n(D,z,A,C,B,11,f[33]),C=n(C,D,z,A,S,16,f[34]),A=n(A,C,D,z,b,23,f[35]),z=n(z,A,C,D,u,4,f[36]),D=n(D,z,A,C,p,11,f[37]),C=n(C,D,z,A,g,16,f[38]),A=n(A,C,D,z,k,23,f[39]),z=n(z,A,C,D,x,4,f[40]),D=n(D,z,A,C,l,11,f[41]),C=n(C,D,z,A,v,16,f[42]),A=n(A,C,D,z,y,23,f[43]),z=n(z,A,C,D,w,4,f[44]),D=n(D,z,A,C,m,11,f[45]),C=n(C,D,z,A,H,16,f[46]),A=n(A,C,D,z,d,23,f[47]),z=o(z,A,C,D,l,6,f[48]),D=o(D,z,A,C,g,10,f[49]),C=o(C,D,z,A,b,15,f[50]),A=o(A,C,D,z,_,21,f[51]),z=o(z,A,C,D,m,6,f[52]),D=o(D,z,A,C,v,10,f[53]),C=o(C,D,z,A,k,15,f[54]),A=o(A,C,D,z,u,21,f[55]),z=o(z,A,C,D,B,6,f[56]),D=o(D,z,A,C,H,10,f[57]),C=o(C,D,z,A,y,15,f[58]),A=o(A,C,D,z,x,21,f[59]),z=o(z,A,C,D,p,6,f[60]),D=o(D,z,A,C,S,10,f[61]),C=o(C,D,z,A,d,15,f[62]),A=o(A,C,D,z,w,21,f[63]),h[0]=h[0]+z|0,h[1]=h[1]+A|0,h[2]=h[2]+C|0,h[3]=h[3]+D|0},_doFinalize:function(){var t=this._data,e=t.words,i=8*this._nDataBytes,n=8*t.sigBytes;e[n>>>5]|=128<<24-n%32;var o=r.floor(i/4294967296),s=i;e[(n+64>>>9<<4)+15]=16711935&(o<<8|o>>>24)|4278255360&(o<<24|o>>>8),e[(n+64>>>9<<4)+14]=16711935&(s<<8|s>>>24)|4278255360&(s<<24|s>>>8),t.sigBytes=4*(e.length+1),this._process();for(var a=this._hash,c=a.words,h=0;h<4;h++){var l=c[h];c[h]=16711935&(l<<8|l>>>24)|4278255360&(l<<24|l>>>8)}return a},clone:function(){var t=h.clone.call(this);return t._hash=this._hash.clone(),t}});s.MD5=h._createHelper(u),s.HmacMD5=h._createHmacHelper(u)}(Math),function(){var r=t,e=r.lib,i=e.WordArray,n=e.Hasher,o=r.algo,s=[],a=o.SHA1=n.extend({_doReset:function(){this._hash=new i.init([1732584193,4023233417,2562383102,271733878,3285377520])},_doProcessBlock:function(t,r){for(var e=this._hash.words,i=e[0],n=e[1],o=e[2],a=e[3],c=e[4],h=0;h<80;h++){if(h<16)s[h]=0|t[r+h];else{var l=s[h-3]^s[h-8]^s[h-14]^s[h-16];s[h]=l<<1|l>>>31}var f=(i<<5|i>>>27)+c+s[h];f+=h<20?(n&o|~n&a)+1518500249:h<40?(n^o^a)+1859775393:h<60?(n&o|n&a|o&a)-1894007588:(n^o^a)-899497514,c=a,a=o,o=n<<30|n>>>2,n=i,i=f}e[0]=e[0]+i|0,e[1]=e[1]+n|0,e[2]=e[2]+o|0,e[3]=e[3]+a|0,e[4]=e[4]+c|0},_doFinalize:function(){var t=this._data,r=t.words,e=8*this._nDataBytes,i=8*t.sigBytes;return r[i>>>5]|=128<<24-i%32,r[(i+64>>>9<<4)+14]=Math.floor(e/4294967296),r[(i+64>>>9<<4)+15]=e,t.sigBytes=4*r.length,this._process(),this._hash},clone:function(){var t=n.clone.call(this);return t._hash=this._hash.clone(),t}});r.SHA1=n._createHelper(a),r.HmacSHA1=n._createHmacHelper(a)}(),function(r){var e=t,i=e.lib,n=i.WordArray,o=i.Hasher,s=e.algo,a=[],c=[];!function(){function t(t){for(var e=r.sqrt(t),i=2;i<=e;i++)if(!(t%i))return!1;return!0}function e(t){return 4294967296*(t-(0|t))|0}for(var i=2,n=0;n<64;)t(i)&&(n<8&&(a[n]=e(r.pow(i,.5))),c[n]=e(r.pow(i,1/3)),n++),i++}();var h=[],l=s.SHA256=o.extend({_doReset:function(){this._hash=new n.init(a.slice(0))},_doProcessBlock:function(t,r){for(var e=this._hash.words,i=e[0],n=e[1],o=e[2],s=e[3],a=e[4],l=e[5],f=e[6],u=e[7],d=0;d<64;d++){if(d<16)h[d]=0|t[r+d];else{var v=h[d-15],p=(v<<25|v>>>7)^(v<<14|v>>>18)^v>>>3,_=h[d-2],y=(_<<15|_>>>17)^(_<<13|_>>>19)^_>>>10;h[d]=p+h[d-7]+y+h[d-16]}var g=a&l^~a&f,B=i&n^i&o^n&o,w=(i<<30|i>>>2)^(i<<19|i>>>13)^(i<<10|i>>>22),k=(a<<26|a>>>6)^(a<<21|a>>>11)^(a<<7|a>>>25),S=u+k+g+c[d]+h[d],m=w+B;u=f,f=l,l=a,a=s+S|0,s=o,o=n,n=i,i=S+m|0}e[0]=e[0]+i|0,e[1]=e[1]+n|0,e[2]=e[2]+o|0,e[3]=e[3]+s|0,e[4]=e[4]+a|0,e[5]=e[5]+l|0,e[6]=e[6]+f|0,e[7]=e[7]+u|0},_doFinalize:function(){var t=this._data,e=t.words,i=8*this._nDataBytes,n=8*t.sigBytes;return e[n>>>5]|=128<<24-n%32,e[(n+64>>>9<<4)+14]=r.floor(i/4294967296),e[(n+64>>>9<<4)+15]=i,t.sigBytes=4*e.length,this._process(),this._hash},clone:function(){var t=o.clone.call(this);return t._hash=this._hash.clone(),t}});e.SHA256=o._createHelper(l),e.HmacSHA256=o._createHmacHelper(l)}(Math),function(){function r(t){return t<<8&4278255360|t>>>8&16711935}var e=t,i=e.lib,n=i.WordArray,o=e.enc;o.Utf16=o.Utf16BE={stringify:function(t){for(var r=t.words,e=t.sigBytes,i=[],n=0;n<e;n+=2){var o=r[n>>>2]>>>16-n%4*8&65535;i.push(String.fromCharCode(o))}return i.join("")},parse:function(t){for(var r=t.length,e=[],i=0;i<r;i++)e[i>>>1]|=t.charCodeAt(i)<<16-i%2*16;return n.create(e,2*r)}};o.Utf16LE={stringify:function(t){for(var e=t.words,i=t.sigBytes,n=[],o=0;o<i;o+=2){var s=r(e[o>>>2]>>>16-o%4*8&65535);n.push(String.fromCharCode(s))}return n.join("")},parse:function(t){for(var e=t.length,i=[],o=0;o<e;o++)i[o>>>1]|=r(t.charCodeAt(o)<<16-o%2*16);return n.create(i,2*e)}}}(),function(){if("function"==typeof ArrayBuffer){var r=t,e=r.lib,i=e.WordArray,n=i.init,o=i.init=function(t){if(t instanceof ArrayBuffer&&(t=new Uint8Array(t)),(t instanceof Int8Array||"undefined"!=typeof Uint8ClampedArray&&t instanceof Uint8ClampedArray||t instanceof Int16Array||t instanceof Uint16Array||t instanceof Int32Array||t instanceof Uint32Array||t instanceof Float32Array||t instanceof Float64Array)&&(t=new Uint8Array(t.buffer,t.byteOffset,t.byteLength)),t instanceof Uint8Array){for(var r=t.byteLength,e=[],i=0;i<r;i++)e[i>>>2]|=t[i]<<24-i%4*8;n.call(this,e,r)}else n.apply(this,arguments)};o.prototype=i}}(),function(r){function e(t,r,e){return t^r^e}function i(t,r,e){return t&r|~t&e}function n(t,r,e){return(t|~r)^e}function o(t,r,e){return t&e|r&~e}function s(t,r,e){return t^(r|~e)}function a(t,r){return t<<r|t>>>32-r}var c=t,h=c.lib,l=h.WordArray,f=h.Hasher,u=c.algo,d=l.create([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8,3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12,1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2,4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13]),v=l.create([5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12,6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2,15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13,8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14,12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11]),p=l.create([11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8,7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12,11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5,11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12,9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6]),_=l.create([8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6,9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11,9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5,15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8,8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11]),y=l.create([0,1518500249,1859775393,2400959708,2840853838]),g=l.create([1352829926,1548603684,1836072691,2053994217,0]),B=u.RIPEMD160=f.extend({_doReset:function(){this._hash=l.create([1732584193,4023233417,2562383102,271733878,3285377520])},_doProcessBlock:function(t,r){for(var c=0;c<16;c++){var h=r+c,l=t[h];t[h]=16711935&(l<<8|l>>>24)|4278255360&(l<<24|l>>>8)}var f,u,B,w,k,S,m,x,b,H,z=this._hash.words,A=y.words,C=g.words,D=d.words,R=v.words,E=p.words,M=_.words;S=f=z[0],m=u=z[1],x=B=z[2],b=w=z[3],H=k=z[4];for(var F,c=0;c<80;c+=1)F=f+t[r+D[c]]|0,F+=c<16?e(u,B,w)+A[0]:c<32?i(u,B,w)+A[1]:c<48?n(u,B,w)+A[2]:c<64?o(u,B,w)+A[3]:s(u,B,w)+A[4],F|=0,F=a(F,E[c]),F=F+k|0,f=k,k=w,w=a(B,10),B=u,u=F,F=S+t[r+R[c]]|0,F+=c<16?s(m,x,b)+C[0]:c<32?o(m,x,b)+C[1]:c<48?n(m,x,b)+C[2]:c<64?i(m,x,b)+C[3]:e(m,x,b)+C[4],F|=0,F=a(F,M[c]),F=F+H|0,S=H,H=b,b=a(x,10),x=m,m=F;F=z[1]+B+b|0,z[1]=z[2]+w+H|0,z[2]=z[3]+k+S|0,z[3]=z[4]+f+m|0,z[4]=z[0]+u+x|0,z[0]=F},_doFinalize:function(){var t=this._data,r=t.words,e=8*this._nDataBytes,i=8*t.sigBytes;r[i>>>5]|=128<<24-i%32,r[(i+64>>>9<<4)+14]=16711935&(e<<8|e>>>24)|4278255360&(e<<24|e>>>8),t.sigBytes=4*(r.length+1),this._process();for(var n=this._hash,o=n.words,s=0;s<5;s++){var a=o[s];o[s]=16711935&(a<<8|a>>>24)|4278255360&(a<<24|a>>>8)}return n},clone:function(){var t=f.clone.call(this);return t._hash=this._hash.clone(),t}});c.RIPEMD160=f._createHelper(B),c.HmacRIPEMD160=f._createHmacHelper(B)}(Math),function(){var r=t,e=r.lib,i=e.Base,n=r.enc,o=n.Utf8,s=r.algo;s.HMAC=i.extend({init:function(t,r){t=this._hasher=new t.init,"string"==typeof r&&(r=o.parse(r));var e=t.blockSize,i=4*e;r.sigBytes>i&&(r=t.finalize(r)),r.clamp();for(var n=this._oKey=r.clone(),s=this._iKey=r.clone(),a=n.words,c=s.words,h=0;h<e;h++)a[h]^=1549556828,c[h]^=909522486;n.sigBytes=s.sigBytes=i,this.reset()},reset:function(){var t=this._hasher;t.reset(),t.update(this._iKey)},update:function(t){return this._hasher.update(t),this},finalize:function(t){var r=this._hasher,e=r.finalize(t);r.reset();var i=r.finalize(this._oKey.clone().concat(e));return i}})}(),function(){var r=t,e=r.lib,i=e.Base,n=e.WordArray,o=r.algo,s=o.SHA1,a=o.HMAC,c=o.PBKDF2=i.extend({cfg:i.extend({keySize:4,hasher:s,iterations:1}),init:function(t){this.cfg=this.cfg.extend(t)},compute:function(t,r){for(var e=this.cfg,i=a.create(e.hasher,t),o=n.create(),s=n.create([1]),c=o.words,h=s.words,l=e.keySize,f=e.iterations;c.length<l;){var u=i.update(r).finalize(s);i.reset();for(var d=u.words,v=d.length,p=u,_=1;_<f;_++){p=i.finalize(p),i.reset();for(var y=p.words,g=0;g<v;g++)d[g]^=y[g]}o.concat(u),h[0]++}return o.sigBytes=4*l,o}});r.PBKDF2=function(t,r,e){return c.create(e).compute(t,r)}}(),function(){var r=t,e=r.lib,i=e.Base,n=e.WordArray,o=r.algo,s=o.MD5,a=o.EvpKDF=i.extend({cfg:i.extend({keySize:4,hasher:s,iterations:1}),init:function(t){this.cfg=this.cfg.extend(t)},compute:function(t,r){for(var e=this.cfg,i=e.hasher.create(),o=n.create(),s=o.words,a=e.keySize,c=e.iterations;s.length<a;){h&&i.update(h);var h=i.update(t).finalize(r);i.reset();for(var l=1;l<c;l++)h=i.finalize(h),i.reset();o.concat(h)}return o.sigBytes=4*a,o}});r.EvpKDF=function(t,r,e){return a.create(e).compute(t,r)}}(),function(){var r=t,e=r.lib,i=e.WordArray,n=r.algo,o=n.SHA256,s=n.SHA224=o.extend({_doReset:function(){this._hash=new i.init([3238371032,914150663,812702999,4144912697,4290775857,1750603025,1694076839,3204075428])},_doFinalize:function(){var t=o._doFinalize.call(this);return t.sigBytes-=4,t}});r.SHA224=o._createHelper(s),r.HmacSHA224=o._createHmacHelper(s)}(),function(r){var e=t,i=e.lib,n=i.Base,o=i.WordArray,s=e.x64={};s.Word=n.extend({init:function(t,r){this.high=t,this.low=r}}),s.WordArray=n.extend({init:function(t,e){t=this.words=t||[],e!=r?this.sigBytes=e:this.sigBytes=8*t.length},toX32:function(){for(var t=this.words,r=t.length,e=[],i=0;i<r;i++){var n=t[i];e.push(n.high),e.push(n.low)}return o.create(e,this.sigBytes)},clone:function(){for(var t=n.clone.call(this),r=t.words=this.words.slice(0),e=r.length,i=0;i<e;i++)r[i]=r[i].clone();return t}})}(),function(r){var e=t,i=e.lib,n=i.WordArray,o=i.Hasher,s=e.x64,a=s.Word,c=e.algo,h=[],l=[],f=[];!function(){for(var t=1,r=0,e=0;e<24;e++){h[t+5*r]=(e+1)*(e+2)/2%64;var i=r%5,n=(2*t+3*r)%5;t=i,r=n}for(var t=0;t<5;t++)for(var r=0;r<5;r++)l[t+5*r]=r+(2*t+3*r)%5*5;for(var o=1,s=0;s<24;s++){for(var c=0,u=0,d=0;d<7;d++){if(1&o){var v=(1<<d)-1;v<32?u^=1<<v:c^=1<<v-32}128&o?o=o<<1^113:o<<=1}f[s]=a.create(c,u)}}();var u=[];!function(){for(var t=0;t<25;t++)u[t]=a.create()}();var d=c.SHA3=o.extend({cfg:o.cfg.extend({outputLength:512}),_doReset:function(){for(var t=this._state=[],r=0;r<25;r++)t[r]=new a.init;this.blockSize=(1600-2*this.cfg.outputLength)/32},_doProcessBlock:function(t,r){for(var e=this._state,i=this.blockSize/2,n=0;n<i;n++){var o=t[r+2*n],s=t[r+2*n+1];o=16711935&(o<<8|o>>>24)|4278255360&(o<<24|o>>>8),s=16711935&(s<<8|s>>>24)|4278255360&(s<<24|s>>>8);var a=e[n];a.high^=s,a.low^=o}for(var c=0;c<24;c++){for(var d=0;d<5;d++){for(var v=0,p=0,_=0;_<5;_++){var a=e[d+5*_];v^=a.high,p^=a.low}var y=u[d];y.high=v,y.low=p}for(var d=0;d<5;d++)for(var g=u[(d+4)%5],B=u[(d+1)%5],w=B.high,k=B.low,v=g.high^(w<<1|k>>>31),p=g.low^(k<<1|w>>>31),_=0;_<5;_++){var a=e[d+5*_];a.high^=v,a.low^=p}for(var S=1;S<25;S++){var a=e[S],m=a.high,x=a.low,b=h[S];if(b<32)var v=m<<b|x>>>32-b,p=x<<b|m>>>32-b;else var v=x<<b-32|m>>>64-b,p=m<<b-32|x>>>64-b;var H=u[l[S]];H.high=v,H.low=p}var z=u[0],A=e[0];z.high=A.high,z.low=A.low;for(var d=0;d<5;d++)for(var _=0;_<5;_++){var S=d+5*_,a=e[S],C=u[S],D=u[(d+1)%5+5*_],R=u[(d+2)%5+5*_];a.high=C.high^~D.high&R.high,a.low=C.low^~D.low&R.low}var a=e[0],E=f[c];a.high^=E.high,a.low^=E.low}},_doFinalize:function(){var t=this._data,e=t.words,i=(8*this._nDataBytes,8*t.sigBytes),o=32*this.blockSize;e[i>>>5]|=1<<24-i%32,e[(r.ceil((i+1)/o)*o>>>5)-1]|=128,t.sigBytes=4*e.length,this._process();for(var s=this._state,a=this.cfg.outputLength/8,c=a/8,h=[],l=0;l<c;l++){var f=s[l],u=f.high,d=f.low;u=16711935&(u<<8|u>>>24)|4278255360&(u<<24|u>>>8),d=16711935&(d<<8|d>>>24)|4278255360&(d<<24|d>>>8),h.push(d),h.push(u)}return new n.init(h,a)},clone:function(){for(var t=o.clone.call(this),r=t._state=this._state.slice(0),e=0;e<25;e++)r[e]=r[e].clone();return t}});e.SHA3=o._createHelper(d),e.HmacSHA3=o._createHmacHelper(d)}(Math),function(){function r(){return s.create.apply(s,arguments)}var e=t,i=e.lib,n=i.Hasher,o=e.x64,s=o.Word,a=o.WordArray,c=e.algo,h=[r(1116352408,3609767458),r(1899447441,602891725),r(3049323471,3964484399),r(3921009573,2173295548),r(961987163,4081628472),r(1508970993,3053834265),r(2453635748,2937671579),r(2870763221,3664609560),r(3624381080,2734883394),r(310598401,1164996542),r(607225278,1323610764),r(1426881987,3590304994),r(1925078388,4068182383),r(2162078206,991336113),r(2614888103,633803317),r(3248222580,3479774868),r(3835390401,2666613458),r(4022224774,944711139),r(264347078,2341262773),r(604807628,2007800933),r(770255983,1495990901),r(1249150122,1856431235),r(1555081692,3175218132),r(1996064986,2198950837),r(2554220882,3999719339),r(2821834349,766784016),r(2952996808,2566594879),r(3210313671,3203337956),r(3336571891,1034457026),r(3584528711,2466948901),r(113926993,3758326383),r(338241895,168717936),r(666307205,1188179964),r(773529912,1546045734),r(1294757372,1522805485),r(1396182291,2643833823),r(1695183700,2343527390),r(1986661051,1014477480),r(2177026350,1206759142),r(2456956037,344077627),r(2730485921,1290863460),r(2820302411,3158454273),r(3259730800,3505952657),r(3345764771,106217008),r(3516065817,3606008344),r(3600352804,1432725776),r(4094571909,1467031594),r(275423344,851169720),r(430227734,3100823752),r(506948616,1363258195),r(659060556,3750685593),r(883997877,3785050280),r(958139571,3318307427),r(1322822218,3812723403),r(1537002063,2003034995),r(1747873779,3602036899),r(1955562222,1575990012),r(2024104815,1125592928),r(2227730452,2716904306),r(2361852424,442776044),r(2428436474,593698344),r(2756734187,3733110249),r(3204031479,2999351573),r(3329325298,3815920427),r(3391569614,3928383900),r(3515267271,566280711),r(3940187606,3454069534),r(4118630271,4000239992),r(116418474,1914138554),r(174292421,2731055270),r(289380356,3203993006),r(460393269,320620315),r(685471733,587496836),r(852142971,1086792851),r(1017036298,365543100),r(1126000580,2618297676),r(1288033470,3409855158),r(1501505948,4234509866),r(1607167915,987167468),r(1816402316,1246189591)],l=[];!function(){for(var t=0;t<80;t++)l[t]=r()}();var f=c.SHA512=n.extend({_doReset:function(){this._hash=new a.init([new s.init(1779033703,4089235720),new s.init(3144134277,2227873595),new s.init(1013904242,4271175723),new s.init(2773480762,1595750129),new s.init(1359893119,2917565137),new s.init(2600822924,725511199),new s.init(528734635,4215389547),new s.init(1541459225,327033209)])},_doProcessBlock:function(t,r){for(var e=this._hash.words,i=e[0],n=e[1],o=e[2],s=e[3],a=e[4],c=e[5],f=e[6],u=e[7],d=i.high,v=i.low,p=n.high,_=n.low,y=o.high,g=o.low,B=s.high,w=s.low,k=a.high,S=a.low,m=c.high,x=c.low,b=f.high,H=f.low,z=u.high,A=u.low,C=d,D=v,R=p,E=_,M=y,F=g,P=B,W=w,O=k,U=S,I=m,K=x,X=b,L=H,j=z,N=A,T=0;T<80;T++){var Z=l[T];if(T<16)var q=Z.high=0|t[r+2*T],G=Z.low=0|t[r+2*T+1];else{var J=l[T-15],$=J.high,Q=J.low,V=($>>>1|Q<<31)^($>>>8|Q<<24)^$>>>7,Y=(Q>>>1|$<<31)^(Q>>>8|$<<24)^(Q>>>7|$<<25),tt=l[T-2],rt=tt.high,et=tt.low,it=(rt>>>19|et<<13)^(rt<<3|et>>>29)^rt>>>6,nt=(et>>>19|rt<<13)^(et<<3|rt>>>29)^(et>>>6|rt<<26),ot=l[T-7],st=ot.high,at=ot.low,ct=l[T-16],ht=ct.high,lt=ct.low,G=Y+at,q=V+st+(G>>>0<Y>>>0?1:0),G=G+nt,q=q+it+(G>>>0<nt>>>0?1:0),G=G+lt,q=q+ht+(G>>>0<lt>>>0?1:0);Z.high=q,Z.low=G}var ft=O&I^~O&X,ut=U&K^~U&L,dt=C&R^C&M^R&M,vt=D&E^D&F^E&F,pt=(C>>>28|D<<4)^(C<<30|D>>>2)^(C<<25|D>>>7),_t=(D>>>28|C<<4)^(D<<30|C>>>2)^(D<<25|C>>>7),yt=(O>>>14|U<<18)^(O>>>18|U<<14)^(O<<23|U>>>9),gt=(U>>>14|O<<18)^(U>>>18|O<<14)^(U<<23|O>>>9),Bt=h[T],wt=Bt.high,kt=Bt.low,St=N+gt,mt=j+yt+(St>>>0<N>>>0?1:0),St=St+ut,mt=mt+ft+(St>>>0<ut>>>0?1:0),St=St+kt,mt=mt+wt+(St>>>0<kt>>>0?1:0),St=St+G,mt=mt+q+(St>>>0<G>>>0?1:0),xt=_t+vt,bt=pt+dt+(xt>>>0<_t>>>0?1:0);j=X,N=L,X=I,L=K,I=O,K=U,U=W+St|0,O=P+mt+(U>>>0<W>>>0?1:0)|0,P=M,W=F,M=R,F=E,R=C,E=D,D=St+xt|0,C=mt+bt+(D>>>0<St>>>0?1:0)|0}v=i.low=v+D,i.high=d+C+(v>>>0<D>>>0?1:0),_=n.low=_+E,n.high=p+R+(_>>>0<E>>>0?1:0),g=o.low=g+F,o.high=y+M+(g>>>0<F>>>0?1:0),w=s.low=w+W,s.high=B+P+(w>>>0<W>>>0?1:0),S=a.low=S+U,a.high=k+O+(S>>>0<U>>>0?1:0),x=c.low=x+K,c.high=m+I+(x>>>0<K>>>0?1:0),H=f.low=H+L,f.high=b+X+(H>>>0<L>>>0?1:0),A=u.low=A+N,u.high=z+j+(A>>>0<N>>>0?1:0)},_doFinalize:function(){var t=this._data,r=t.words,e=8*this._nDataBytes,i=8*t.sigBytes;r[i>>>5]|=128<<24-i%32,r[(i+128>>>10<<5)+30]=Math.floor(e/4294967296),r[(i+128>>>10<<5)+31]=e,t.sigBytes=4*r.length,this._process();var n=this._hash.toX32();return n},clone:function(){var t=n.clone.call(this);return t._hash=this._hash.clone(),t},blockSize:32});e.SHA512=n._createHelper(f),e.HmacSHA512=n._createHmacHelper(f)}(),function(){var r=t,e=r.x64,i=e.Word,n=e.WordArray,o=r.algo,s=o.SHA512,a=o.SHA384=s.extend({_doReset:function(){this._hash=new n.init([new i.init(3418070365,3238371032),new i.init(1654270250,914150663),new i.init(2438529370,812702999),new i.init(355462360,4144912697),new i.init(1731405415,4290775857),new i.init(2394180231,1750603025),new i.init(3675008525,1694076839),new i.init(1203062813,3204075428)])},_doFinalize:function(){var t=s._doFinalize.call(this);return t.sigBytes-=16,t}});r.SHA384=s._createHelper(a),r.HmacSHA384=s._createHmacHelper(a)}(),t.lib.Cipher||function(r){var e=t,i=e.lib,n=i.Base,o=i.WordArray,s=i.BufferedBlockAlgorithm,a=e.enc,c=(a.Utf8,a.Base64),h=e.algo,l=h.EvpKDF,f=i.Cipher=s.extend({cfg:n.extend(),createEncryptor:function(t,r){return this.create(this._ENC_XFORM_MODE,t,r)},createDecryptor:function(t,r){return this.create(this._DEC_XFORM_MODE,t,r)},init:function(t,r,e){this.cfg=this.cfg.extend(e),this._xformMode=t,this._key=r,this.reset()},reset:function(){s.reset.call(this),this._doReset()},process:function(t){return this._append(t),this._process()},finalize:function(t){t&&this._append(t);var r=this._doFinalize();return r},keySize:4,ivSize:4,_ENC_XFORM_MODE:1,_DEC_XFORM_MODE:2,_createHelper:function(){function t(t){return"string"==typeof t?m:w}return function(r){return{encrypt:function(e,i,n){return t(i).encrypt(r,e,i,n)},decrypt:function(e,i,n){return t(i).decrypt(r,e,i,n)}}}}()}),u=(i.StreamCipher=f.extend({_doFinalize:function(){var t=this._process(!0);return t},blockSize:1}),e.mode={}),d=i.BlockCipherMode=n.extend({createEncryptor:function(t,r){return this.Encryptor.create(t,r)},createDecryptor:function(t,r){return this.Decryptor.create(t,r)},init:function(t,r){this._cipher=t,this._iv=r}}),v=u.CBC=function(){function t(t,e,i){var n=this._iv;if(n){var o=n;this._iv=r}else var o=this._prevBlock;for(var s=0;s<i;s++)t[e+s]^=o[s]}var e=d.extend();return e.Encryptor=e.extend({processBlock:function(r,e){var i=this._cipher,n=i.blockSize;t.call(this,r,e,n),i.encryptBlock(r,e),this._prevBlock=r.slice(e,e+n)}}),e.Decryptor=e.extend({processBlock:function(r,e){var i=this._cipher,n=i.blockSize,o=r.slice(e,e+n);i.decryptBlock(r,e),t.call(this,r,e,n),this._prevBlock=o}}),e}(),p=e.pad={},_=p.Pkcs7={pad:function(t,r){for(var e=4*r,i=e-t.sigBytes%e,n=i<<24|i<<16|i<<8|i,s=[],a=0;a<i;a+=4)s.push(n);var c=o.create(s,i);t.concat(c)},unpad:function(t){var r=255&t.words[t.sigBytes-1>>>2];t.sigBytes-=r}},y=(i.BlockCipher=f.extend({cfg:f.cfg.extend({mode:v,padding:_}),reset:function(){f.reset.call(this);var t=this.cfg,r=t.iv,e=t.mode;if(this._xformMode==this._ENC_XFORM_MODE)var i=e.createEncryptor;else{var i=e.createDecryptor;this._minBufferSize=1}this._mode&&this._mode.__creator==i?this._mode.init(this,r&&r.words):(this._mode=i.call(e,this,r&&r.words),this._mode.__creator=i)},_doProcessBlock:function(t,r){this._mode.processBlock(t,r)},_doFinalize:function(){var t=this.cfg.padding;if(this._xformMode==this._ENC_XFORM_MODE){t.pad(this._data,this.blockSize);var r=this._process(!0)}else{var r=this._process(!0);t.unpad(r)}return r},blockSize:4}),i.CipherParams=n.extend({init:function(t){this.mixIn(t)},toString:function(t){return(t||this.formatter).stringify(this)}})),g=e.format={},B=g.OpenSSL={stringify:function(t){var r=t.ciphertext,e=t.salt;if(e)var i=o.create([1398893684,1701076831]).concat(e).concat(r);else var i=r;return i.toString(c)},parse:function(t){var r=c.parse(t),e=r.words;if(1398893684==e[0]&&1701076831==e[1]){var i=o.create(e.slice(2,4));e.splice(0,4),r.sigBytes-=16}return y.create({ciphertext:r,salt:i})}},w=i.SerializableCipher=n.extend({cfg:n.extend({format:B}),encrypt:function(t,r,e,i){i=this.cfg.extend(i);var n=t.createEncryptor(e,i),o=n.finalize(r),s=n.cfg;return y.create({ciphertext:o,key:e,iv:s.iv,algorithm:t,mode:s.mode,padding:s.padding,blockSize:t.blockSize,formatter:i.format})},decrypt:function(t,r,e,i){i=this.cfg.extend(i),r=this._parse(r,i.format);var n=t.createDecryptor(e,i).finalize(r.ciphertext);return n},_parse:function(t,r){return"string"==typeof t?r.parse(t,this):t}}),k=e.kdf={},S=k.OpenSSL={execute:function(t,r,e,i){i||(i=o.random(8));var n=l.create({keySize:r+e}).compute(t,i),s=o.create(n.words.slice(r),4*e);return n.sigBytes=4*r,y.create({key:n,iv:s,salt:i})}},m=i.PasswordBasedCipher=w.extend({cfg:w.cfg.extend({kdf:S}),encrypt:function(t,r,e,i){i=this.cfg.extend(i);var n=i.kdf.execute(e,t.keySize,t.ivSize);i.iv=n.iv;var o=w.encrypt.call(this,t,r,n.key,i);return o.mixIn(n),o},decrypt:function(t,r,e,i){i=this.cfg.extend(i),r=this._parse(r,i.format);var n=i.kdf.execute(e,t.keySize,t.ivSize,r.salt);i.iv=n.iv;var o=w.decrypt.call(this,t,r,n.key,i);return o}})}(),t.mode.CFB=function(){function r(t,r,e,i){var n=this._iv;if(n){var o=n.slice(0);this._iv=void 0}else var o=this._prevBlock;i.encryptBlock(o,0);for(var s=0;s<e;s++)t[r+s]^=o[s]}var e=t.lib.BlockCipherMode.extend();return e.Encryptor=e.extend({processBlock:function(t,e){var i=this._cipher,n=i.blockSize;r.call(this,t,e,n,i),this._prevBlock=t.slice(e,e+n)}}),e.Decryptor=e.extend({processBlock:function(t,e){var i=this._cipher,n=i.blockSize,o=t.slice(e,e+n);r.call(this,t,e,n,i),this._prevBlock=o}}),e}(),t.mode.ECB=function(){var r=t.lib.BlockCipherMode.extend();return r.Encryptor=r.extend({processBlock:function(t,r){this._cipher.encryptBlock(t,r)}}),r.Decryptor=r.extend({processBlock:function(t,r){this._cipher.decryptBlock(t,r)}}),r}(),t.pad.AnsiX923={pad:function(t,r){var e=t.sigBytes,i=4*r,n=i-e%i,o=e+n-1;t.clamp(),t.words[o>>>2]|=n<<24-o%4*8,t.sigBytes+=n},unpad:function(t){var r=255&t.words[t.sigBytes-1>>>2];t.sigBytes-=r}},t.pad.Iso10126={pad:function(r,e){var i=4*e,n=i-r.sigBytes%i;r.concat(t.lib.WordArray.random(n-1)).concat(t.lib.WordArray.create([n<<24],1))},unpad:function(t){var r=255&t.words[t.sigBytes-1>>>2];t.sigBytes-=r}},t.pad.Iso97971={pad:function(r,e){r.concat(t.lib.WordArray.create([2147483648],1)),t.pad.ZeroPadding.pad(r,e)},unpad:function(r){t.pad.ZeroPadding.unpad(r),r.sigBytes--}},t.mode.OFB=function(){var r=t.lib.BlockCipherMode.extend(),e=r.Encryptor=r.extend({processBlock:function(t,r){var e=this._cipher,i=e.blockSize,n=this._iv,o=this._keystream;n&&(o=this._keystream=n.slice(0),this._iv=void 0),e.encryptBlock(o,0);for(var s=0;s<i;s++)t[r+s]^=o[s]}});return r.Decryptor=e,r}(),t.pad.NoPadding={pad:function(){},unpad:function(){}},function(r){var e=t,i=e.lib,n=i.CipherParams,o=e.enc,s=o.Hex,a=e.format;a.Hex={stringify:function(t){return t.ciphertext.toString(s)},parse:function(t){var r=s.parse(t);return n.create({ciphertext:r})}}}(),function(){var r=t,e=r.lib,i=e.BlockCipher,n=r.algo,o=[],s=[],a=[],c=[],h=[],l=[],f=[],u=[],d=[],v=[];!function(){for(var t=[],r=0;r<256;r++)r<128?t[r]=r<<1:t[r]=r<<1^283;for(var e=0,i=0,r=0;r<256;r++){var n=i^i<<1^i<<2^i<<3^i<<4;n=n>>>8^255&n^99,o[e]=n,s[n]=e;var p=t[e],_=t[p],y=t[_],g=257*t[n]^16843008*n;a[e]=g<<24|g>>>8,c[e]=g<<16|g>>>16,h[e]=g<<8|g>>>24,l[e]=g;var g=16843009*y^65537*_^257*p^16843008*e;f[n]=g<<24|g>>>8,u[n]=g<<16|g>>>16,d[n]=g<<8|g>>>24,v[n]=g,e?(e=p^t[t[t[y^p]]],i^=t[t[i]]):e=i=1}}();var p=[0,1,2,4,8,16,32,64,128,27,54],_=n.AES=i.extend({_doReset:function(){if(!this._nRounds||this._keyPriorReset!==this._key){for(var t=this._keyPriorReset=this._key,r=t.words,e=t.sigBytes/4,i=this._nRounds=e+6,n=4*(i+1),s=this._keySchedule=[],a=0;a<n;a++)if(a<e)s[a]=r[a];else{var c=s[a-1];a%e?e>6&&a%e==4&&(c=o[c>>>24]<<24|o[c>>>16&255]<<16|o[c>>>8&255]<<8|o[255&c]):(c=c<<8|c>>>24,c=o[c>>>24]<<24|o[c>>>16&255]<<16|o[c>>>8&255]<<8|o[255&c],c^=p[a/e|0]<<24),s[a]=s[a-e]^c}for(var h=this._invKeySchedule=[],l=0;l<n;l++){var a=n-l;if(l%4)var c=s[a];else var c=s[a-4];l<4||a<=4?h[l]=c:h[l]=f[o[c>>>24]]^u[o[c>>>16&255]]^d[o[c>>>8&255]]^v[o[255&c]]}}},encryptBlock:function(t,r){this._doCryptBlock(t,r,this._keySchedule,a,c,h,l,o)},decryptBlock:function(t,r){var e=t[r+1];t[r+1]=t[r+3],t[r+3]=e,this._doCryptBlock(t,r,this._invKeySchedule,f,u,d,v,s);var e=t[r+1];t[r+1]=t[r+3],t[r+3]=e},_doCryptBlock:function(t,r,e,i,n,o,s,a){for(var c=this._nRounds,h=t[r]^e[0],l=t[r+1]^e[1],f=t[r+2]^e[2],u=t[r+3]^e[3],d=4,v=1;v<c;v++){var p=i[h>>>24]^n[l>>>16&255]^o[f>>>8&255]^s[255&u]^e[d++],_=i[l>>>24]^n[f>>>16&255]^o[u>>>8&255]^s[255&h]^e[d++],y=i[f>>>24]^n[u>>>16&255]^o[h>>>8&255]^s[255&l]^e[d++],g=i[u>>>24]^n[h>>>16&255]^o[l>>>8&255]^s[255&f]^e[d++];h=p,l=_,f=y,u=g}var p=(a[h>>>24]<<24|a[l>>>16&255]<<16|a[f>>>8&255]<<8|a[255&u])^e[d++],_=(a[l>>>24]<<24|a[f>>>16&255]<<16|a[u>>>8&255]<<8|a[255&h])^e[d++],y=(a[f>>>24]<<24|a[u>>>16&255]<<16|a[h>>>8&255]<<8|a[255&l])^e[d++],g=(a[u>>>24]<<24|a[h>>>16&255]<<16|a[l>>>8&255]<<8|a[255&f])^e[d++];t[r]=p,t[r+1]=_,t[r+2]=y,t[r+3]=g},keySize:8});r.AES=i._createHelper(_)}(),function(){function r(t,r){var e=(this._lBlock>>>t^this._rBlock)&r;this._rBlock^=e,this._lBlock^=e<<t}function e(t,r){var e=(this._rBlock>>>t^this._lBlock)&r;this._lBlock^=e,this._rBlock^=e<<t;
}var i=t,n=i.lib,o=n.WordArray,s=n.BlockCipher,a=i.algo,c=[57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4],h=[14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32],l=[1,2,4,6,8,10,12,14,15,17,19,21,23,25,27,28],f=[{0:8421888,268435456:32768,536870912:8421378,805306368:2,1073741824:512,1342177280:8421890,1610612736:8389122,1879048192:8388608,2147483648:514,2415919104:8389120,2684354560:33280,2952790016:8421376,3221225472:32770,3489660928:8388610,3758096384:0,4026531840:33282,134217728:0,402653184:8421890,671088640:33282,939524096:32768,1207959552:8421888,1476395008:512,1744830464:8421378,2013265920:2,2281701376:8389120,2550136832:33280,2818572288:8421376,3087007744:8389122,3355443200:8388610,3623878656:32770,3892314112:514,4160749568:8388608,1:32768,268435457:2,536870913:8421888,805306369:8388608,1073741825:8421378,1342177281:33280,1610612737:512,1879048193:8389122,2147483649:8421890,2415919105:8421376,2684354561:8388610,2952790017:33282,3221225473:514,3489660929:8389120,3758096385:32770,4026531841:0,134217729:8421890,402653185:8421376,671088641:8388608,939524097:512,1207959553:32768,1476395009:8388610,1744830465:2,2013265921:33282,2281701377:32770,2550136833:8389122,2818572289:514,3087007745:8421888,3355443201:8389120,3623878657:0,3892314113:33280,4160749569:8421378},{0:1074282512,16777216:16384,33554432:524288,50331648:1074266128,67108864:1073741840,83886080:1074282496,100663296:1073758208,117440512:16,134217728:540672,150994944:1073758224,167772160:1073741824,184549376:540688,201326592:524304,218103808:0,234881024:16400,251658240:1074266112,8388608:1073758208,25165824:540688,41943040:16,58720256:1073758224,75497472:1074282512,92274688:1073741824,109051904:524288,125829120:1074266128,142606336:524304,159383552:0,176160768:16384,192937984:1074266112,209715200:1073741840,226492416:540672,243269632:1074282496,260046848:16400,268435456:0,285212672:1074266128,301989888:1073758224,318767104:1074282496,335544320:1074266112,352321536:16,369098752:540688,385875968:16384,402653184:16400,419430400:524288,436207616:524304,452984832:1073741840,469762048:540672,486539264:1073758208,503316480:1073741824,520093696:1074282512,276824064:540688,293601280:524288,310378496:1074266112,327155712:16384,343932928:1073758208,360710144:1074282512,377487360:16,394264576:1073741824,411041792:1074282496,427819008:1073741840,444596224:1073758224,461373440:524304,478150656:0,494927872:16400,511705088:1074266128,528482304:540672},{0:260,1048576:0,2097152:67109120,3145728:65796,4194304:65540,5242880:67108868,6291456:67174660,7340032:67174400,8388608:67108864,9437184:67174656,10485760:65792,11534336:67174404,12582912:67109124,13631488:65536,14680064:4,15728640:256,524288:67174656,1572864:67174404,2621440:0,3670016:67109120,4718592:67108868,5767168:65536,6815744:65540,7864320:260,8912896:4,9961472:256,11010048:67174400,12058624:65796,13107200:65792,14155776:67109124,15204352:67174660,16252928:67108864,16777216:67174656,17825792:65540,18874368:65536,19922944:67109120,20971520:256,22020096:67174660,23068672:67108868,24117248:0,25165824:67109124,26214400:67108864,27262976:4,28311552:65792,29360128:67174400,30408704:260,31457280:65796,32505856:67174404,17301504:67108864,18350080:260,19398656:67174656,20447232:0,21495808:65540,22544384:67109120,23592960:256,24641536:67174404,25690112:65536,26738688:67174660,27787264:65796,28835840:67108868,29884416:67109124,30932992:67174400,31981568:4,33030144:65792},{0:2151682048,65536:2147487808,131072:4198464,196608:2151677952,262144:0,327680:4198400,393216:2147483712,458752:4194368,524288:2147483648,589824:4194304,655360:64,720896:2147487744,786432:2151678016,851968:4160,917504:4096,983040:2151682112,32768:2147487808,98304:64,163840:2151678016,229376:2147487744,294912:4198400,360448:2151682112,425984:0,491520:2151677952,557056:4096,622592:2151682048,688128:4194304,753664:4160,819200:2147483648,884736:4194368,950272:4198464,1015808:2147483712,1048576:4194368,1114112:4198400,1179648:2147483712,1245184:0,1310720:4160,1376256:2151678016,1441792:2151682048,1507328:2147487808,1572864:2151682112,1638400:2147483648,1703936:2151677952,1769472:4198464,1835008:2147487744,1900544:4194304,1966080:64,2031616:4096,1081344:2151677952,1146880:2151682112,1212416:0,1277952:4198400,1343488:4194368,1409024:2147483648,1474560:2147487808,1540096:64,1605632:2147483712,1671168:4096,1736704:2147487744,1802240:2151678016,1867776:4160,1933312:2151682048,1998848:4194304,2064384:4198464},{0:128,4096:17039360,8192:262144,12288:536870912,16384:537133184,20480:16777344,24576:553648256,28672:262272,32768:16777216,36864:537133056,40960:536871040,45056:553910400,49152:553910272,53248:0,57344:17039488,61440:553648128,2048:17039488,6144:553648256,10240:128,14336:17039360,18432:262144,22528:537133184,26624:553910272,30720:536870912,34816:537133056,38912:0,43008:553910400,47104:16777344,51200:536871040,55296:553648128,59392:16777216,63488:262272,65536:262144,69632:128,73728:536870912,77824:553648256,81920:16777344,86016:553910272,90112:537133184,94208:16777216,98304:553910400,102400:553648128,106496:17039360,110592:537133056,114688:262272,118784:536871040,122880:0,126976:17039488,67584:553648256,71680:16777216,75776:17039360,79872:537133184,83968:536870912,88064:17039488,92160:128,96256:553910272,100352:262272,104448:553910400,108544:0,112640:553648128,116736:16777344,120832:262144,124928:537133056,129024:536871040},{0:268435464,256:8192,512:270532608,768:270540808,1024:268443648,1280:2097152,1536:2097160,1792:268435456,2048:0,2304:268443656,2560:2105344,2816:8,3072:270532616,3328:2105352,3584:8200,3840:270540800,128:270532608,384:270540808,640:8,896:2097152,1152:2105352,1408:268435464,1664:268443648,1920:8200,2176:2097160,2432:8192,2688:268443656,2944:270532616,3200:0,3456:270540800,3712:2105344,3968:268435456,4096:268443648,4352:270532616,4608:270540808,4864:8200,5120:2097152,5376:268435456,5632:268435464,5888:2105344,6144:2105352,6400:0,6656:8,6912:270532608,7168:8192,7424:268443656,7680:270540800,7936:2097160,4224:8,4480:2105344,4736:2097152,4992:268435464,5248:268443648,5504:8200,5760:270540808,6016:270532608,6272:270540800,6528:270532616,6784:8192,7040:2105352,7296:2097160,7552:0,7808:268435456,8064:268443656},{0:1048576,16:33555457,32:1024,48:1049601,64:34604033,80:0,96:1,112:34603009,128:33555456,144:1048577,160:33554433,176:34604032,192:34603008,208:1025,224:1049600,240:33554432,8:34603009,24:0,40:33555457,56:34604032,72:1048576,88:33554433,104:33554432,120:1025,136:1049601,152:33555456,168:34603008,184:1048577,200:1024,216:34604033,232:1,248:1049600,256:33554432,272:1048576,288:33555457,304:34603009,320:1048577,336:33555456,352:34604032,368:1049601,384:1025,400:34604033,416:1049600,432:1,448:0,464:34603008,480:33554433,496:1024,264:1049600,280:33555457,296:34603009,312:1,328:33554432,344:1048576,360:1025,376:34604032,392:33554433,408:34603008,424:0,440:34604033,456:1049601,472:1024,488:33555456,504:1048577},{0:134219808,1:131072,2:134217728,3:32,4:131104,5:134350880,6:134350848,7:2048,8:134348800,9:134219776,10:133120,11:134348832,12:2080,13:0,14:134217760,15:133152,2147483648:2048,2147483649:134350880,2147483650:134219808,2147483651:134217728,2147483652:134348800,2147483653:133120,2147483654:133152,2147483655:32,2147483656:134217760,2147483657:2080,2147483658:131104,2147483659:134350848,2147483660:0,2147483661:134348832,2147483662:134219776,2147483663:131072,16:133152,17:134350848,18:32,19:2048,20:134219776,21:134217760,22:134348832,23:131072,24:0,25:131104,26:134348800,27:134219808,28:134350880,29:133120,30:2080,31:134217728,2147483664:131072,2147483665:2048,2147483666:134348832,2147483667:133152,2147483668:32,2147483669:134348800,2147483670:134217728,2147483671:134219808,2147483672:134350880,2147483673:134217760,2147483674:134219776,2147483675:0,2147483676:133120,2147483677:2080,2147483678:131104,2147483679:134350848}],u=[4160749569,528482304,33030144,2064384,129024,8064,504,2147483679],d=a.DES=s.extend({_doReset:function(){for(var t=this._key,r=t.words,e=[],i=0;i<56;i++){var n=c[i]-1;e[i]=r[n>>>5]>>>31-n%32&1}for(var o=this._subKeys=[],s=0;s<16;s++){for(var a=o[s]=[],f=l[s],i=0;i<24;i++)a[i/6|0]|=e[(h[i]-1+f)%28]<<31-i%6,a[4+(i/6|0)]|=e[28+(h[i+24]-1+f)%28]<<31-i%6;a[0]=a[0]<<1|a[0]>>>31;for(var i=1;i<7;i++)a[i]=a[i]>>>4*(i-1)+3;a[7]=a[7]<<5|a[7]>>>27}for(var u=this._invSubKeys=[],i=0;i<16;i++)u[i]=o[15-i]},encryptBlock:function(t,r){this._doCryptBlock(t,r,this._subKeys)},decryptBlock:function(t,r){this._doCryptBlock(t,r,this._invSubKeys)},_doCryptBlock:function(t,i,n){this._lBlock=t[i],this._rBlock=t[i+1],r.call(this,4,252645135),r.call(this,16,65535),e.call(this,2,858993459),e.call(this,8,16711935),r.call(this,1,1431655765);for(var o=0;o<16;o++){for(var s=n[o],a=this._lBlock,c=this._rBlock,h=0,l=0;l<8;l++)h|=f[l][((c^s[l])&u[l])>>>0];this._lBlock=c,this._rBlock=a^h}var d=this._lBlock;this._lBlock=this._rBlock,this._rBlock=d,r.call(this,1,1431655765),e.call(this,8,16711935),e.call(this,2,858993459),r.call(this,16,65535),r.call(this,4,252645135),t[i]=this._lBlock,t[i+1]=this._rBlock},keySize:2,ivSize:2,blockSize:2});i.DES=s._createHelper(d);var v=a.TripleDES=s.extend({_doReset:function(){var t=this._key,r=t.words;this._des1=d.createEncryptor(o.create(r.slice(0,2))),this._des2=d.createEncryptor(o.create(r.slice(2,4))),this._des3=d.createEncryptor(o.create(r.slice(4,6)))},encryptBlock:function(t,r){this._des1.encryptBlock(t,r),this._des2.decryptBlock(t,r),this._des3.encryptBlock(t,r)},decryptBlock:function(t,r){this._des3.decryptBlock(t,r),this._des2.encryptBlock(t,r),this._des1.decryptBlock(t,r)},keySize:6,ivSize:2,blockSize:2});i.TripleDES=s._createHelper(v)}(),function(){function r(){for(var t=this._S,r=this._i,e=this._j,i=0,n=0;n<4;n++){r=(r+1)%256,e=(e+t[r])%256;var o=t[r];t[r]=t[e],t[e]=o,i|=t[(t[r]+t[e])%256]<<24-8*n}return this._i=r,this._j=e,i}var e=t,i=e.lib,n=i.StreamCipher,o=e.algo,s=o.RC4=n.extend({_doReset:function(){for(var t=this._key,r=t.words,e=t.sigBytes,i=this._S=[],n=0;n<256;n++)i[n]=n;for(var n=0,o=0;n<256;n++){var s=n%e,a=r[s>>>2]>>>24-s%4*8&255;o=(o+i[n]+a)%256;var c=i[n];i[n]=i[o],i[o]=c}this._i=this._j=0},_doProcessBlock:function(t,e){t[e]^=r.call(this)},keySize:8,ivSize:0});e.RC4=n._createHelper(s);var a=o.RC4Drop=s.extend({cfg:s.cfg.extend({drop:192}),_doReset:function(){s._doReset.call(this);for(var t=this.cfg.drop;t>0;t--)r.call(this)}});e.RC4Drop=n._createHelper(a)}(),t.mode.CTRGladman=function(){function r(t){if(255===(t>>24&255)){var r=t>>16&255,e=t>>8&255,i=255&t;255===r?(r=0,255===e?(e=0,255===i?i=0:++i):++e):++r,t=0,t+=r<<16,t+=e<<8,t+=i}else t+=1<<24;return t}function e(t){return 0===(t[0]=r(t[0]))&&(t[1]=r(t[1])),t}var i=t.lib.BlockCipherMode.extend(),n=i.Encryptor=i.extend({processBlock:function(t,r){var i=this._cipher,n=i.blockSize,o=this._iv,s=this._counter;o&&(s=this._counter=o.slice(0),this._iv=void 0),e(s);var a=s.slice(0);i.encryptBlock(a,0);for(var c=0;c<n;c++)t[r+c]^=a[c]}});return i.Decryptor=n,i}(),function(){function r(){for(var t=this._X,r=this._C,e=0;e<8;e++)a[e]=r[e];r[0]=r[0]+1295307597+this._b|0,r[1]=r[1]+3545052371+(r[0]>>>0<a[0]>>>0?1:0)|0,r[2]=r[2]+886263092+(r[1]>>>0<a[1]>>>0?1:0)|0,r[3]=r[3]+1295307597+(r[2]>>>0<a[2]>>>0?1:0)|0,r[4]=r[4]+3545052371+(r[3]>>>0<a[3]>>>0?1:0)|0,r[5]=r[5]+886263092+(r[4]>>>0<a[4]>>>0?1:0)|0,r[6]=r[6]+1295307597+(r[5]>>>0<a[5]>>>0?1:0)|0,r[7]=r[7]+3545052371+(r[6]>>>0<a[6]>>>0?1:0)|0,this._b=r[7]>>>0<a[7]>>>0?1:0;for(var e=0;e<8;e++){var i=t[e]+r[e],n=65535&i,o=i>>>16,s=((n*n>>>17)+n*o>>>15)+o*o,h=((4294901760&i)*i|0)+((65535&i)*i|0);c[e]=s^h}t[0]=c[0]+(c[7]<<16|c[7]>>>16)+(c[6]<<16|c[6]>>>16)|0,t[1]=c[1]+(c[0]<<8|c[0]>>>24)+c[7]|0,t[2]=c[2]+(c[1]<<16|c[1]>>>16)+(c[0]<<16|c[0]>>>16)|0,t[3]=c[3]+(c[2]<<8|c[2]>>>24)+c[1]|0,t[4]=c[4]+(c[3]<<16|c[3]>>>16)+(c[2]<<16|c[2]>>>16)|0,t[5]=c[5]+(c[4]<<8|c[4]>>>24)+c[3]|0,t[6]=c[6]+(c[5]<<16|c[5]>>>16)+(c[4]<<16|c[4]>>>16)|0,t[7]=c[7]+(c[6]<<8|c[6]>>>24)+c[5]|0}var e=t,i=e.lib,n=i.StreamCipher,o=e.algo,s=[],a=[],c=[],h=o.Rabbit=n.extend({_doReset:function(){for(var t=this._key.words,e=this.cfg.iv,i=0;i<4;i++)t[i]=16711935&(t[i]<<8|t[i]>>>24)|4278255360&(t[i]<<24|t[i]>>>8);var n=this._X=[t[0],t[3]<<16|t[2]>>>16,t[1],t[0]<<16|t[3]>>>16,t[2],t[1]<<16|t[0]>>>16,t[3],t[2]<<16|t[1]>>>16],o=this._C=[t[2]<<16|t[2]>>>16,4294901760&t[0]|65535&t[1],t[3]<<16|t[3]>>>16,4294901760&t[1]|65535&t[2],t[0]<<16|t[0]>>>16,4294901760&t[2]|65535&t[3],t[1]<<16|t[1]>>>16,4294901760&t[3]|65535&t[0]];this._b=0;for(var i=0;i<4;i++)r.call(this);for(var i=0;i<8;i++)o[i]^=n[i+4&7];if(e){var s=e.words,a=s[0],c=s[1],h=16711935&(a<<8|a>>>24)|4278255360&(a<<24|a>>>8),l=16711935&(c<<8|c>>>24)|4278255360&(c<<24|c>>>8),f=h>>>16|4294901760&l,u=l<<16|65535&h;o[0]^=h,o[1]^=f,o[2]^=l,o[3]^=u,o[4]^=h,o[5]^=f,o[6]^=l,o[7]^=u;for(var i=0;i<4;i++)r.call(this)}},_doProcessBlock:function(t,e){var i=this._X;r.call(this),s[0]=i[0]^i[5]>>>16^i[3]<<16,s[1]=i[2]^i[7]>>>16^i[5]<<16,s[2]=i[4]^i[1]>>>16^i[7]<<16,s[3]=i[6]^i[3]>>>16^i[1]<<16;for(var n=0;n<4;n++)s[n]=16711935&(s[n]<<8|s[n]>>>24)|4278255360&(s[n]<<24|s[n]>>>8),t[e+n]^=s[n]},blockSize:4,ivSize:2});e.Rabbit=n._createHelper(h)}(),t.mode.CTR=function(){var r=t.lib.BlockCipherMode.extend(),e=r.Encryptor=r.extend({processBlock:function(t,r){var e=this._cipher,i=e.blockSize,n=this._iv,o=this._counter;n&&(o=this._counter=n.slice(0),this._iv=void 0);var s=o.slice(0);e.encryptBlock(s,0),o[i-1]=o[i-1]+1|0;for(var a=0;a<i;a++)t[r+a]^=s[a]}});return r.Decryptor=e,r}(),function(){function r(){for(var t=this._X,r=this._C,e=0;e<8;e++)a[e]=r[e];r[0]=r[0]+1295307597+this._b|0,r[1]=r[1]+3545052371+(r[0]>>>0<a[0]>>>0?1:0)|0,r[2]=r[2]+886263092+(r[1]>>>0<a[1]>>>0?1:0)|0,r[3]=r[3]+1295307597+(r[2]>>>0<a[2]>>>0?1:0)|0,r[4]=r[4]+3545052371+(r[3]>>>0<a[3]>>>0?1:0)|0,r[5]=r[5]+886263092+(r[4]>>>0<a[4]>>>0?1:0)|0,r[6]=r[6]+1295307597+(r[5]>>>0<a[5]>>>0?1:0)|0,r[7]=r[7]+3545052371+(r[6]>>>0<a[6]>>>0?1:0)|0,this._b=r[7]>>>0<a[7]>>>0?1:0;for(var e=0;e<8;e++){var i=t[e]+r[e],n=65535&i,o=i>>>16,s=((n*n>>>17)+n*o>>>15)+o*o,h=((4294901760&i)*i|0)+((65535&i)*i|0);c[e]=s^h}t[0]=c[0]+(c[7]<<16|c[7]>>>16)+(c[6]<<16|c[6]>>>16)|0,t[1]=c[1]+(c[0]<<8|c[0]>>>24)+c[7]|0,t[2]=c[2]+(c[1]<<16|c[1]>>>16)+(c[0]<<16|c[0]>>>16)|0,t[3]=c[3]+(c[2]<<8|c[2]>>>24)+c[1]|0,t[4]=c[4]+(c[3]<<16|c[3]>>>16)+(c[2]<<16|c[2]>>>16)|0,t[5]=c[5]+(c[4]<<8|c[4]>>>24)+c[3]|0,t[6]=c[6]+(c[5]<<16|c[5]>>>16)+(c[4]<<16|c[4]>>>16)|0,t[7]=c[7]+(c[6]<<8|c[6]>>>24)+c[5]|0}var e=t,i=e.lib,n=i.StreamCipher,o=e.algo,s=[],a=[],c=[],h=o.RabbitLegacy=n.extend({_doReset:function(){var t=this._key.words,e=this.cfg.iv,i=this._X=[t[0],t[3]<<16|t[2]>>>16,t[1],t[0]<<16|t[3]>>>16,t[2],t[1]<<16|t[0]>>>16,t[3],t[2]<<16|t[1]>>>16],n=this._C=[t[2]<<16|t[2]>>>16,4294901760&t[0]|65535&t[1],t[3]<<16|t[3]>>>16,4294901760&t[1]|65535&t[2],t[0]<<16|t[0]>>>16,4294901760&t[2]|65535&t[3],t[1]<<16|t[1]>>>16,4294901760&t[3]|65535&t[0]];this._b=0;for(var o=0;o<4;o++)r.call(this);for(var o=0;o<8;o++)n[o]^=i[o+4&7];if(e){var s=e.words,a=s[0],c=s[1],h=16711935&(a<<8|a>>>24)|4278255360&(a<<24|a>>>8),l=16711935&(c<<8|c>>>24)|4278255360&(c<<24|c>>>8),f=h>>>16|4294901760&l,u=l<<16|65535&h;n[0]^=h,n[1]^=f,n[2]^=l,n[3]^=u,n[4]^=h,n[5]^=f,n[6]^=l,n[7]^=u;for(var o=0;o<4;o++)r.call(this)}},_doProcessBlock:function(t,e){var i=this._X;r.call(this),s[0]=i[0]^i[5]>>>16^i[3]<<16,s[1]=i[2]^i[7]>>>16^i[5]<<16,s[2]=i[4]^i[1]>>>16^i[7]<<16,s[3]=i[6]^i[3]>>>16^i[1]<<16;for(var n=0;n<4;n++)s[n]=16711935&(s[n]<<8|s[n]>>>24)|4278255360&(s[n]<<24|s[n]>>>8),t[e+n]^=s[n]},blockSize:4,ivSize:2});e.RabbitLegacy=n._createHelper(h)}(),t.pad.ZeroPadding={pad:function(t,r){var e=4*r;t.clamp(),t.sigBytes+=e-(t.sigBytes%e||e)},unpad:function(t){for(var r=t.words,e=t.sigBytes-1;!(r[e>>>2]>>>24-e%4*8&255);)e--;t.sigBytes=e+1}},t});
/*! JSEncrypt v2.3.0 | https://npmcdn.com/jsencrypt.2.3.0/LICENSE.txt */
var JSEncryptExports={};!function(t){function e(t,e,i){null!=t&&("number"==typeof t?this.fromNumber(t,e,i):null==e&&"string"!=typeof t?this.fromString(t,256):this.fromString(t,e))}function i(){return new e(null)}function r(t,e,i,r,s,n){for(;--n>=0;){var o=e*this[t++]+i[r]+s;s=Math.floor(o/67108864),i[r++]=67108863&o}return s}function s(t,e,i,r,s,n){for(var o=32767&e,h=e>>15;--n>=0;){var a=32767&this[t],u=this[t++]>>15,c=h*a+u*o;a=o*a+((32767&c)<<15)+i[r]+(1073741823&s),s=(a>>>30)+(c>>>15)+h*u+(s>>>30),i[r++]=1073741823&a}return s}function n(t,e,i,r,s,n){for(var o=16383&e,h=e>>14;--n>=0;){var a=16383&this[t],u=this[t++]>>14,c=h*a+u*o;a=o*a+((16383&c)<<14)+i[r]+s,s=(a>>28)+(c>>14)+h*u,i[r++]=268435455&a}return s}function o(t){return Be.charAt(t)}function h(t,e){var i=Ke[t.charCodeAt(e)];return null==i?-1:i}function a(t){for(var e=this.t-1;e>=0;--e)t[e]=this[e];t.t=this.t,t.s=this.s}function u(t){this.t=1,this.s=0>t?-1:0,t>0?this[0]=t:-1>t?this[0]=t+this.DV:this.t=0}function c(t){var e=i();return e.fromInt(t),e}function f(t,i){var r;if(16==i)r=4;else if(8==i)r=3;else if(256==i)r=8;else if(2==i)r=1;else if(32==i)r=5;else{if(4!=i)return void this.fromRadix(t,i);r=2}this.t=0,this.s=0;for(var s=t.length,n=!1,o=0;--s>=0;){var a=8==r?255&t[s]:h(t,s);0>a?"-"==t.charAt(s)&&(n=!0):(n=!1,0==o?this[this.t++]=a:o+r>this.DB?(this[this.t-1]|=(a&(1<<this.DB-o)-1)<<o,this[this.t++]=a>>this.DB-o):this[this.t-1]|=a<<o,o+=r,o>=this.DB&&(o-=this.DB))}8==r&&0!=(128&t[0])&&(this.s=-1,o>0&&(this[this.t-1]|=(1<<this.DB-o)-1<<o)),this.clamp(),n&&e.ZERO.subTo(this,this)}function p(){for(var t=this.s&this.DM;this.t>0&&this[this.t-1]==t;)--this.t}function l(t){if(this.s<0)return"-"+this.negate().toString(t);var e;if(16==t)e=4;else if(8==t)e=3;else if(2==t)e=1;else if(32==t)e=5;else{if(4!=t)return this.toRadix(t);e=2}var i,r=(1<<e)-1,s=!1,n="",h=this.t,a=this.DB-h*this.DB%e;if(h-- >0)for(a<this.DB&&(i=this[h]>>a)>0&&(s=!0,n=o(i));h>=0;)e>a?(i=(this[h]&(1<<a)-1)<<e-a,i|=this[--h]>>(a+=this.DB-e)):(i=this[h]>>(a-=e)&r,0>=a&&(a+=this.DB,--h)),i>0&&(s=!0),s&&(n+=o(i));return s?n:"0"}function d(){var t=i();return e.ZERO.subTo(this,t),t}function g(){return this.s<0?this.negate():this}function m(t){var e=this.s-t.s;if(0!=e)return e;var i=this.t;if(e=i-t.t,0!=e)return this.s<0?-e:e;for(;--i>=0;)if(0!=(e=this[i]-t[i]))return e;return 0}function y(t){var e,i=1;return 0!=(e=t>>>16)&&(t=e,i+=16),0!=(e=t>>8)&&(t=e,i+=8),0!=(e=t>>4)&&(t=e,i+=4),0!=(e=t>>2)&&(t=e,i+=2),0!=(e=t>>1)&&(t=e,i+=1),i}function b(){return this.t<=0?0:this.DB*(this.t-1)+y(this[this.t-1]^this.s&this.DM)}function T(t,e){var i;for(i=this.t-1;i>=0;--i)e[i+t]=this[i];for(i=t-1;i>=0;--i)e[i]=0;e.t=this.t+t,e.s=this.s}function S(t,e){for(var i=t;i<this.t;++i)e[i-t]=this[i];e.t=Math.max(this.t-t,0),e.s=this.s}function R(t,e){var i,r=t%this.DB,s=this.DB-r,n=(1<<s)-1,o=Math.floor(t/this.DB),h=this.s<<r&this.DM;for(i=this.t-1;i>=0;--i)e[i+o+1]=this[i]>>s|h,h=(this[i]&n)<<r;for(i=o-1;i>=0;--i)e[i]=0;e[o]=h,e.t=this.t+o+1,e.s=this.s,e.clamp()}function E(t,e){e.s=this.s;var i=Math.floor(t/this.DB);if(i>=this.t)return void(e.t=0);var r=t%this.DB,s=this.DB-r,n=(1<<r)-1;e[0]=this[i]>>r;for(var o=i+1;o<this.t;++o)e[o-i-1]|=(this[o]&n)<<s,e[o-i]=this[o]>>r;r>0&&(e[this.t-i-1]|=(this.s&n)<<s),e.t=this.t-i,e.clamp()}function D(t,e){for(var i=0,r=0,s=Math.min(t.t,this.t);s>i;)r+=this[i]-t[i],e[i++]=r&this.DM,r>>=this.DB;if(t.t<this.t){for(r-=t.s;i<this.t;)r+=this[i],e[i++]=r&this.DM,r>>=this.DB;r+=this.s}else{for(r+=this.s;i<t.t;)r-=t[i],e[i++]=r&this.DM,r>>=this.DB;r-=t.s}e.s=0>r?-1:0,-1>r?e[i++]=this.DV+r:r>0&&(e[i++]=r),e.t=i,e.clamp()}function w(t,i){var r=this.abs(),s=t.abs(),n=r.t;for(i.t=n+s.t;--n>=0;)i[n]=0;for(n=0;n<s.t;++n)i[n+r.t]=r.am(0,s[n],i,n,0,r.t);i.s=0,i.clamp(),this.s!=t.s&&e.ZERO.subTo(i,i)}function x(t){for(var e=this.abs(),i=t.t=2*e.t;--i>=0;)t[i]=0;for(i=0;i<e.t-1;++i){var r=e.am(i,e[i],t,2*i,0,1);(t[i+e.t]+=e.am(i+1,2*e[i],t,2*i+1,r,e.t-i-1))>=e.DV&&(t[i+e.t]-=e.DV,t[i+e.t+1]=1)}t.t>0&&(t[t.t-1]+=e.am(i,e[i],t,2*i,0,1)),t.s=0,t.clamp()}function B(t,r,s){var n=t.abs();if(!(n.t<=0)){var o=this.abs();if(o.t<n.t)return null!=r&&r.fromInt(0),void(null!=s&&this.copyTo(s));null==s&&(s=i());var h=i(),a=this.s,u=t.s,c=this.DB-y(n[n.t-1]);c>0?(n.lShiftTo(c,h),o.lShiftTo(c,s)):(n.copyTo(h),o.copyTo(s));var f=h.t,p=h[f-1];if(0!=p){var l=p*(1<<this.F1)+(f>1?h[f-2]>>this.F2:0),d=this.FV/l,g=(1<<this.F1)/l,m=1<<this.F2,v=s.t,b=v-f,T=null==r?i():r;for(h.dlShiftTo(b,T),s.compareTo(T)>=0&&(s[s.t++]=1,s.subTo(T,s)),e.ONE.dlShiftTo(f,T),T.subTo(h,h);h.t<f;)h[h.t++]=0;for(;--b>=0;){var S=s[--v]==p?this.DM:Math.floor(s[v]*d+(s[v-1]+m)*g);if((s[v]+=h.am(0,S,s,b,0,f))<S)for(h.dlShiftTo(b,T),s.subTo(T,s);s[v]<--S;)s.subTo(T,s)}null!=r&&(s.drShiftTo(f,r),a!=u&&e.ZERO.subTo(r,r)),s.t=f,s.clamp(),c>0&&s.rShiftTo(c,s),0>a&&e.ZERO.subTo(s,s)}}}function K(t){var r=i();return this.abs().divRemTo(t,null,r),this.s<0&&r.compareTo(e.ZERO)>0&&t.subTo(r,r),r}function A(t){this.m=t}function U(t){return t.s<0||t.compareTo(this.m)>=0?t.mod(this.m):t}function O(t){return t}function V(t){t.divRemTo(this.m,null,t)}function J(t,e,i){t.multiplyTo(e,i),this.reduce(i)}function N(t,e){t.squareTo(e),this.reduce(e)}function I(){if(this.t<1)return 0;var t=this[0];if(0==(1&t))return 0;var e=3&t;return e=e*(2-(15&t)*e)&15,e=e*(2-(255&t)*e)&255,e=e*(2-((65535&t)*e&65535))&65535,e=e*(2-t*e%this.DV)%this.DV,e>0?this.DV-e:-e}function P(t){this.m=t,this.mp=t.invDigit(),this.mpl=32767&this.mp,this.mph=this.mp>>15,this.um=(1<<t.DB-15)-1,this.mt2=2*t.t}function M(t){var r=i();return t.abs().dlShiftTo(this.m.t,r),r.divRemTo(this.m,null,r),t.s<0&&r.compareTo(e.ZERO)>0&&this.m.subTo(r,r),r}function L(t){var e=i();return t.copyTo(e),this.reduce(e),e}function q(t){for(;t.t<=this.mt2;)t[t.t++]=0;for(var e=0;e<this.m.t;++e){var i=32767&t[e],r=i*this.mpl+((i*this.mph+(t[e]>>15)*this.mpl&this.um)<<15)&t.DM;for(i=e+this.m.t,t[i]+=this.m.am(0,r,t,e,0,this.m.t);t[i]>=t.DV;)t[i]-=t.DV,t[++i]++}t.clamp(),t.drShiftTo(this.m.t,t),t.compareTo(this.m)>=0&&t.subTo(this.m,t)}function C(t,e){t.squareTo(e),this.reduce(e)}function H(t,e,i){t.multiplyTo(e,i),this.reduce(i)}function j(){return 0==(this.t>0?1&this[0]:this.s)}function k(t,r){if(t>4294967295||1>t)return e.ONE;var s=i(),n=i(),o=r.convert(this),h=y(t)-1;for(o.copyTo(s);--h>=0;)if(r.sqrTo(s,n),(t&1<<h)>0)r.mulTo(n,o,s);else{var a=s;s=n,n=a}return r.revert(s)}function F(t,e){var i;return i=256>t||e.isEven()?new A(e):new P(e),this.exp(t,i)}
// Copyright (c) 2005-2009  Tom Wu
// All Rights Reserved.
// See "LICENSE" for details.
function _(){var t=i();return this.copyTo(t),t}function z(){if(this.s<0){if(1==this.t)return this[0]-this.DV;if(0==this.t)return-1}else{if(1==this.t)return this[0];if(0==this.t)return 0}return(this[1]&(1<<32-this.DB)-1)<<this.DB|this[0]}function Z(){return 0==this.t?this.s:this[0]<<24>>24}function G(){return 0==this.t?this.s:this[0]<<16>>16}function $(t){return Math.floor(Math.LN2*this.DB/Math.log(t))}function Y(){return this.s<0?-1:this.t<=0||1==this.t&&this[0]<=0?0:1}function W(t){if(null==t&&(t=10),0==this.signum()||2>t||t>36)return"0";var e=this.chunkSize(t),r=Math.pow(t,e),s=c(r),n=i(),o=i(),h="";for(this.divRemTo(s,n,o);n.signum()>0;)h=(r+o.intValue()).toString(t).substr(1)+h,n.divRemTo(s,n,o);return o.intValue().toString(t)+h}function Q(t,i){this.fromInt(0),null==i&&(i=10);for(var r=this.chunkSize(i),s=Math.pow(i,r),n=!1,o=0,a=0,u=0;u<t.length;++u){var c=h(t,u);0>c?"-"==t.charAt(u)&&0==this.signum()&&(n=!0):(a=i*a+c,++o>=r&&(this.dMultiply(s),this.dAddOffset(a,0),o=0,a=0))}o>0&&(this.dMultiply(Math.pow(i,o)),this.dAddOffset(a,0)),n&&e.ZERO.subTo(this,this)}function X(t,i,r){if("number"==typeof i)if(2>t)this.fromInt(1);else for(this.fromNumber(t,r),this.testBit(t-1)||this.bitwiseTo(e.ONE.shiftLeft(t-1),ht,this),this.isEven()&&this.dAddOffset(1,0);!this.isProbablePrime(i);)this.dAddOffset(2,0),this.bitLength()>t&&this.subTo(e.ONE.shiftLeft(t-1),this);else{var s=new Array,n=7&t;s.length=(t>>3)+1,i.nextBytes(s),n>0?s[0]&=(1<<n)-1:s[0]=0,this.fromString(s,256)}}function tt(){var t=this.t,e=new Array;e[0]=this.s;var i,r=this.DB-t*this.DB%8,s=0;if(t-- >0)for(r<this.DB&&(i=this[t]>>r)!=(this.s&this.DM)>>r&&(e[s++]=i|this.s<<this.DB-r);t>=0;)8>r?(i=(this[t]&(1<<r)-1)<<8-r,i|=this[--t]>>(r+=this.DB-8)):(i=this[t]>>(r-=8)&255,0>=r&&(r+=this.DB,--t)),0!=(128&i)&&(i|=-256),0==s&&(128&this.s)!=(128&i)&&++s,(s>0||i!=this.s)&&(e[s++]=i);return e}function et(t){return 0==this.compareTo(t)}function it(t){return this.compareTo(t)<0?this:t}function rt(t){return this.compareTo(t)>0?this:t}function st(t,e,i){var r,s,n=Math.min(t.t,this.t);for(r=0;n>r;++r)i[r]=e(this[r],t[r]);if(t.t<this.t){for(s=t.s&this.DM,r=n;r<this.t;++r)i[r]=e(this[r],s);i.t=this.t}else{for(s=this.s&this.DM,r=n;r<t.t;++r)i[r]=e(s,t[r]);i.t=t.t}i.s=e(this.s,t.s),i.clamp()}function nt(t,e){return t&e}function ot(t){var e=i();return this.bitwiseTo(t,nt,e),e}function ht(t,e){return t|e}function at(t){var e=i();return this.bitwiseTo(t,ht,e),e}function ut(t,e){return t^e}function ct(t){var e=i();return this.bitwiseTo(t,ut,e),e}function ft(t,e){return t&~e}function pt(t){var e=i();return this.bitwiseTo(t,ft,e),e}function lt(){for(var t=i(),e=0;e<this.t;++e)t[e]=this.DM&~this[e];return t.t=this.t,t.s=~this.s,t}function dt(t){var e=i();return 0>t?this.rShiftTo(-t,e):this.lShiftTo(t,e),e}function gt(t){var e=i();return 0>t?this.lShiftTo(-t,e):this.rShiftTo(t,e),e}function mt(t){if(0==t)return-1;var e=0;return 0==(65535&t)&&(t>>=16,e+=16),0==(255&t)&&(t>>=8,e+=8),0==(15&t)&&(t>>=4,e+=4),0==(3&t)&&(t>>=2,e+=2),0==(1&t)&&++e,e}function yt(){for(var t=0;t<this.t;++t)if(0!=this[t])return t*this.DB+mt(this[t]);return this.s<0?this.t*this.DB:-1}function vt(t){for(var e=0;0!=t;)t&=t-1,++e;return e}function bt(){for(var t=0,e=this.s&this.DM,i=0;i<this.t;++i)t+=vt(this[i]^e);return t}function Tt(t){var e=Math.floor(t/this.DB);return e>=this.t?0!=this.s:0!=(this[e]&1<<t%this.DB)}function St(t,i){var r=e.ONE.shiftLeft(t);return this.bitwiseTo(r,i,r),r}function Rt(t){return this.changeBit(t,ht)}function Et(t){return this.changeBit(t,ft)}function Dt(t){return this.changeBit(t,ut)}function wt(t,e){for(var i=0,r=0,s=Math.min(t.t,this.t);s>i;)r+=this[i]+t[i],e[i++]=r&this.DM,r>>=this.DB;if(t.t<this.t){for(r+=t.s;i<this.t;)r+=this[i],e[i++]=r&this.DM,r>>=this.DB;r+=this.s}else{for(r+=this.s;i<t.t;)r+=t[i],e[i++]=r&this.DM,r>>=this.DB;r+=t.s}e.s=0>r?-1:0,r>0?e[i++]=r:-1>r&&(e[i++]=this.DV+r),e.t=i,e.clamp()}function xt(t){var e=i();return this.addTo(t,e),e}function Bt(t){var e=i();return this.subTo(t,e),e}function Kt(t){var e=i();return this.multiplyTo(t,e),e}function At(){var t=i();return this.squareTo(t),t}function Ut(t){var e=i();return this.divRemTo(t,e,null),e}function Ot(t){var e=i();return this.divRemTo(t,null,e),e}function Vt(t){var e=i(),r=i();return this.divRemTo(t,e,r),new Array(e,r)}function Jt(t){this[this.t]=this.am(0,t-1,this,0,0,this.t),++this.t,this.clamp()}function Nt(t,e){if(0!=t){for(;this.t<=e;)this[this.t++]=0;for(this[e]+=t;this[e]>=this.DV;)this[e]-=this.DV,++e>=this.t&&(this[this.t++]=0),++this[e]}}function It(){}function Pt(t){return t}function Mt(t,e,i){t.multiplyTo(e,i)}function Lt(t,e){t.squareTo(e)}function qt(t){return this.exp(t,new It)}function Ct(t,e,i){var r=Math.min(this.t+t.t,e);for(i.s=0,i.t=r;r>0;)i[--r]=0;var s;for(s=i.t-this.t;s>r;++r)i[r+this.t]=this.am(0,t[r],i,r,0,this.t);for(s=Math.min(t.t,e);s>r;++r)this.am(0,t[r],i,r,0,e-r);i.clamp()}function Ht(t,e,i){--e;var r=i.t=this.t+t.t-e;for(i.s=0;--r>=0;)i[r]=0;for(r=Math.max(e-this.t,0);r<t.t;++r)i[this.t+r-e]=this.am(e-r,t[r],i,0,0,this.t+r-e);i.clamp(),i.drShiftTo(1,i)}function jt(t){this.r2=i(),this.q3=i(),e.ONE.dlShiftTo(2*t.t,this.r2),this.mu=this.r2.divide(t),this.m=t}function kt(t){if(t.s<0||t.t>2*this.m.t)return t.mod(this.m);if(t.compareTo(this.m)<0)return t;var e=i();return t.copyTo(e),this.reduce(e),e}function Ft(t){return t}function _t(t){for(t.drShiftTo(this.m.t-1,this.r2),t.t>this.m.t+1&&(t.t=this.m.t+1,t.clamp()),this.mu.multiplyUpperTo(this.r2,this.m.t+1,this.q3),this.m.multiplyLowerTo(this.q3,this.m.t+1,this.r2);t.compareTo(this.r2)<0;)t.dAddOffset(1,this.m.t+1);for(t.subTo(this.r2,t);t.compareTo(this.m)>=0;)t.subTo(this.m,t)}function zt(t,e){t.squareTo(e),this.reduce(e)}function Zt(t,e,i){t.multiplyTo(e,i),this.reduce(i)}function Gt(t,e){var r,s,n=t.bitLength(),o=c(1);if(0>=n)return o;r=18>n?1:48>n?3:144>n?4:768>n?5:6,s=8>n?new A(e):e.isEven()?new jt(e):new P(e);var h=new Array,a=3,u=r-1,f=(1<<r)-1;if(h[1]=s.convert(this),r>1){var p=i();for(s.sqrTo(h[1],p);f>=a;)h[a]=i(),s.mulTo(p,h[a-2],h[a]),a+=2}var l,d,g=t.t-1,m=!0,v=i();for(n=y(t[g])-1;g>=0;){for(n>=u?l=t[g]>>n-u&f:(l=(t[g]&(1<<n+1)-1)<<u-n,g>0&&(l|=t[g-1]>>this.DB+n-u)),a=r;0==(1&l);)l>>=1,--a;if((n-=a)<0&&(n+=this.DB,--g),m)h[l].copyTo(o),m=!1;else{for(;a>1;)s.sqrTo(o,v),s.sqrTo(v,o),a-=2;a>0?s.sqrTo(o,v):(d=o,o=v,v=d),s.mulTo(v,h[l],o)}for(;g>=0&&0==(t[g]&1<<n);)s.sqrTo(o,v),d=o,o=v,v=d,--n<0&&(n=this.DB-1,--g)}return s.revert(o)}function $t(t){var e=this.s<0?this.negate():this.clone(),i=t.s<0?t.negate():t.clone();if(e.compareTo(i)<0){var r=e;e=i,i=r}var s=e.getLowestSetBit(),n=i.getLowestSetBit();if(0>n)return e;for(n>s&&(n=s),n>0&&(e.rShiftTo(n,e),i.rShiftTo(n,i));e.signum()>0;)(s=e.getLowestSetBit())>0&&e.rShiftTo(s,e),(s=i.getLowestSetBit())>0&&i.rShiftTo(s,i),e.compareTo(i)>=0?(e.subTo(i,e),e.rShiftTo(1,e)):(i.subTo(e,i),i.rShiftTo(1,i));return n>0&&i.lShiftTo(n,i),i}function Yt(t){if(0>=t)return 0;var e=this.DV%t,i=this.s<0?t-1:0;if(this.t>0)if(0==e)i=this[0]%t;else for(var r=this.t-1;r>=0;--r)i=(e*i+this[r])%t;return i}function Wt(t){var i=t.isEven();if(this.isEven()&&i||0==t.signum())return e.ZERO;for(var r=t.clone(),s=this.clone(),n=c(1),o=c(0),h=c(0),a=c(1);0!=r.signum();){for(;r.isEven();)r.rShiftTo(1,r),i?(n.isEven()&&o.isEven()||(n.addTo(this,n),o.subTo(t,o)),n.rShiftTo(1,n)):o.isEven()||o.subTo(t,o),o.rShiftTo(1,o);for(;s.isEven();)s.rShiftTo(1,s),i?(h.isEven()&&a.isEven()||(h.addTo(this,h),a.subTo(t,a)),h.rShiftTo(1,h)):a.isEven()||a.subTo(t,a),a.rShiftTo(1,a);r.compareTo(s)>=0?(r.subTo(s,r),i&&n.subTo(h,n),o.subTo(a,o)):(s.subTo(r,s),i&&h.subTo(n,h),a.subTo(o,a))}return 0!=s.compareTo(e.ONE)?e.ZERO:a.compareTo(t)>=0?a.subtract(t):a.signum()<0?(a.addTo(t,a),a.signum()<0?a.add(t):a):a}function Qt(t){var e,i=this.abs();if(1==i.t&&i[0]<=Ae[Ae.length-1]){for(e=0;e<Ae.length;++e)if(i[0]==Ae[e])return!0;return!1}if(i.isEven())return!1;for(e=1;e<Ae.length;){for(var r=Ae[e],s=e+1;s<Ae.length&&Ue>r;)r*=Ae[s++];for(r=i.modInt(r);s>e;)if(r%Ae[e++]==0)return!1}return i.millerRabin(t)}function Xt(t){var r=this.subtract(e.ONE),s=r.getLowestSetBit();if(0>=s)return!1;var n=r.shiftRight(s);t=t+1>>1,t>Ae.length&&(t=Ae.length);for(var o=i(),h=0;t>h;++h){o.fromInt(Ae[Math.floor(Math.random()*Ae.length)]);var a=o.modPow(n,this);if(0!=a.compareTo(e.ONE)&&0!=a.compareTo(r)){for(var u=1;u++<s&&0!=a.compareTo(r);)if(a=a.modPowInt(2,this),0==a.compareTo(e.ONE))return!1;if(0!=a.compareTo(r))return!1}}return!0}function te(){this.i=0,this.j=0,this.S=new Array}function ee(t){var e,i,r;for(e=0;256>e;++e)this.S[e]=e;for(i=0,e=0;256>e;++e)i=i+this.S[e]+t[e%t.length]&255,r=this.S[e],this.S[e]=this.S[i],this.S[i]=r;this.i=0,this.j=0}function ie(){var t;return this.i=this.i+1&255,this.j=this.j+this.S[this.i]&255,t=this.S[this.i],this.S[this.i]=this.S[this.j],this.S[this.j]=t,this.S[t+this.S[this.i]&255]}function re(){return new te}function se(){if(null==Oe){for(Oe=re();Ne>Je;){var t=Math.floor(65536*Math.random());Ve[Je++]=255&t}for(Oe.init(Ve),Je=0;Je<Ve.length;++Je)Ve[Je]=0;Je=0}return Oe.next()}function ne(t){var e;for(e=0;e<t.length;++e)t[e]=se()}function oe(){}function he(t,i){return new e(t,i)}function ae(t,i){if(i<t.length+11)return console.error("Message too long for RSA"),null;for(var r=new Array,s=t.length-1;s>=0&&i>0;){var n=t.charCodeAt(s--);128>n?r[--i]=n:n>127&&2048>n?(r[--i]=63&n|128,r[--i]=n>>6|192):(r[--i]=63&n|128,r[--i]=n>>6&63|128,r[--i]=n>>12|224)}r[--i]=0;for(var o=new oe,h=new Array;i>2;){for(h[0]=0;0==h[0];)o.nextBytes(h);r[--i]=h[0]}return r[--i]=2,r[--i]=0,new e(r)}function ue(){this.n=null,this.e=0,this.d=null,this.p=null,this.q=null,this.dmp1=null,this.dmq1=null,this.coeff=null}function ce(t,e){null!=t&&null!=e&&t.length>0&&e.length>0?(this.n=he(t,16),this.e=parseInt(e,16)):console.error("Invalid RSA public key")}function fe(t){return t.modPowInt(this.e,this.n)}function pe(t){var e=ae(t,this.n.bitLength()+7>>3);if(null==e)return null;var i=this.doPublic(e);if(null==i)return null;var r=i.toString(16);return 0==(1&r.length)?r:"0"+r}function le(t,e){for(var i=t.toByteArray(),r=0;r<i.length&&0==i[r];)++r;if(i.length-r!=e-1||2!=i[r])return null;for(++r;0!=i[r];)if(++r>=i.length)return null;for(var s="";++r<i.length;){var n=255&i[r];128>n?s+=String.fromCharCode(n):n>191&&224>n?(s+=String.fromCharCode((31&n)<<6|63&i[r+1]),++r):(s+=String.fromCharCode((15&n)<<12|(63&i[r+1])<<6|63&i[r+2]),r+=2)}return s}function de(t,e,i){null!=t&&null!=e&&t.length>0&&e.length>0?(this.n=he(t,16),this.e=parseInt(e,16),this.d=he(i,16)):console.error("Invalid RSA private key")}function ge(t,e,i,r,s,n,o,h){null!=t&&null!=e&&t.length>0&&e.length>0?(this.n=he(t,16),this.e=parseInt(e,16),this.d=he(i,16),this.p=he(r,16),this.q=he(s,16),this.dmp1=he(n,16),this.dmq1=he(o,16),this.coeff=he(h,16)):console.error("Invalid RSA private key")}function me(t,i){var r=new oe,s=t>>1;this.e=parseInt(i,16);for(var n=new e(i,16);;){for(;this.p=new e(t-s,1,r),0!=this.p.subtract(e.ONE).gcd(n).compareTo(e.ONE)||!this.p.isProbablePrime(10););for(;this.q=new e(s,1,r),0!=this.q.subtract(e.ONE).gcd(n).compareTo(e.ONE)||!this.q.isProbablePrime(10););if(this.p.compareTo(this.q)<=0){var o=this.p;this.p=this.q,this.q=o}var h=this.p.subtract(e.ONE),a=this.q.subtract(e.ONE),u=h.multiply(a);if(0==u.gcd(n).compareTo(e.ONE)){this.n=this.p.multiply(this.q),this.d=n.modInverse(u),this.dmp1=this.d.mod(h),this.dmq1=this.d.mod(a),this.coeff=this.q.modInverse(this.p);break}}}function ye(t){if(null==this.p||null==this.q)return t.modPow(this.d,this.n);for(var e=t.mod(this.p).modPow(this.dmp1,this.p),i=t.mod(this.q).modPow(this.dmq1,this.q);e.compareTo(i)<0;)e=e.add(this.p);return e.subtract(i).multiply(this.coeff).mod(this.p).multiply(this.q).add(i)}function ve(t){var e=he(t,16),i=this.doPrivate(e);return null==i?null:le(i,this.n.bitLength()+7>>3)}function be(t){var e,i,r="";for(e=0;e+3<=t.length;e+=3)i=parseInt(t.substring(e,e+3),16),r+=Le.charAt(i>>6)+Le.charAt(63&i);for(e+1==t.length?(i=parseInt(t.substring(e,e+1),16),r+=Le.charAt(i<<2)):e+2==t.length&&(i=parseInt(t.substring(e,e+2),16),r+=Le.charAt(i>>2)+Le.charAt((3&i)<<4));(3&r.length)>0;)r+=qe;return r}function Te(t){var e,i,r="",s=0;for(e=0;e<t.length&&t.charAt(e)!=qe;++e)v=Le.indexOf(t.charAt(e)),v<0||(0==s?(r+=o(v>>2),i=3&v,s=1):1==s?(r+=o(i<<2|v>>4),i=15&v,s=2):2==s?(r+=o(i),r+=o(v>>2),i=3&v,s=3):(r+=o(i<<2|v>>4),r+=o(15&v),s=0));return 1==s&&(r+=o(i<<2)),r}
// Copyright (c) 2005  Tom Wu
// All Rights Reserved.
// See "LICENSE" for details.
var Se,Re=0xdeadbeefcafe,Ee=15715070==(16777215&Re);Ee&&"Microsoft Internet Explorer"==navigator.appName?(e.prototype.am=s,Se=30):Ee&&"Netscape"!=navigator.appName?(e.prototype.am=r,Se=26):(e.prototype.am=n,Se=28),e.prototype.DB=Se,e.prototype.DM=(1<<Se)-1,e.prototype.DV=1<<Se;var De=52;e.prototype.FV=Math.pow(2,De),e.prototype.F1=De-Se,e.prototype.F2=2*Se-De;var we,xe,Be="0123456789abcdefghijklmnopqrstuvwxyz",Ke=new Array;for(we="0".charCodeAt(0),xe=0;9>=xe;++xe)Ke[we++]=xe;for(we="a".charCodeAt(0),xe=10;36>xe;++xe)Ke[we++]=xe;for(we="A".charCodeAt(0),xe=10;36>xe;++xe)Ke[we++]=xe;A.prototype.convert=U,A.prototype.revert=O,A.prototype.reduce=V,A.prototype.mulTo=J,A.prototype.sqrTo=N,P.prototype.convert=M,P.prototype.revert=L,P.prototype.reduce=q,P.prototype.mulTo=H,P.prototype.sqrTo=C,e.prototype.copyTo=a,e.prototype.fromInt=u,e.prototype.fromString=f,e.prototype.clamp=p,e.prototype.dlShiftTo=T,e.prototype.drShiftTo=S,e.prototype.lShiftTo=R,e.prototype.rShiftTo=E,e.prototype.subTo=D,e.prototype.multiplyTo=w,e.prototype.squareTo=x,e.prototype.divRemTo=B,e.prototype.invDigit=I,e.prototype.isEven=j,e.prototype.exp=k,e.prototype.toString=l,e.prototype.negate=d,e.prototype.abs=g,e.prototype.compareTo=m,e.prototype.bitLength=b,e.prototype.mod=K,e.prototype.modPowInt=F,e.ZERO=c(0),e.ONE=c(1),It.prototype.convert=Pt,It.prototype.revert=Pt,It.prototype.mulTo=Mt,It.prototype.sqrTo=Lt,jt.prototype.convert=kt,jt.prototype.revert=Ft,jt.prototype.reduce=_t,jt.prototype.mulTo=Zt,jt.prototype.sqrTo=zt;var Ae=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997],Ue=(1<<26)/Ae[Ae.length-1];e.prototype.chunkSize=$,e.prototype.toRadix=W,e.prototype.fromRadix=Q,e.prototype.fromNumber=X,e.prototype.bitwiseTo=st,e.prototype.changeBit=St,e.prototype.addTo=wt,e.prototype.dMultiply=Jt,e.prototype.dAddOffset=Nt,e.prototype.multiplyLowerTo=Ct,e.prototype.multiplyUpperTo=Ht,e.prototype.modInt=Yt,e.prototype.millerRabin=Xt,e.prototype.clone=_,e.prototype.intValue=z,e.prototype.byteValue=Z,e.prototype.shortValue=G,e.prototype.signum=Y,e.prototype.toByteArray=tt,e.prototype.equals=et,e.prototype.min=it,e.prototype.max=rt,e.prototype.and=ot,e.prototype.or=at,e.prototype.xor=ct,e.prototype.andNot=pt,e.prototype.not=lt,e.prototype.shiftLeft=dt,e.prototype.shiftRight=gt,e.prototype.getLowestSetBit=yt,e.prototype.bitCount=bt,e.prototype.testBit=Tt,e.prototype.setBit=Rt,e.prototype.clearBit=Et,e.prototype.flipBit=Dt,e.prototype.add=xt,e.prototype.subtract=Bt,e.prototype.multiply=Kt,e.prototype.divide=Ut,e.prototype.remainder=Ot,e.prototype.divideAndRemainder=Vt,e.prototype.modPow=Gt,e.prototype.modInverse=Wt,e.prototype.pow=qt,e.prototype.gcd=$t,e.prototype.isProbablePrime=Qt,e.prototype.square=At,te.prototype.init=ee,te.prototype.next=ie;var Oe,Ve,Je,Ne=256;if(null==Ve){Ve=new Array,Je=0;var Ie;if(window.crypto&&window.crypto.getRandomValues){var Pe=new Uint32Array(256);for(window.crypto.getRandomValues(Pe),Ie=0;Ie<Pe.length;++Ie)Ve[Je++]=255&Pe[Ie]}var Me=function(t){if(this.count=this.count||0,this.count>=256||Je>=Ne)return void(window.removeEventListener?window.removeEventListener("mousemove",Me,!1):window.detachEvent&&window.detachEvent("onmousemove",Me));try{var e=t.x+t.y;Ve[Je++]=255&e,this.count+=1}catch(i){}};window.addEventListener?window.addEventListener("mousemove",Me,!1):window.attachEvent&&window.attachEvent("onmousemove",Me)}oe.prototype.nextBytes=ne,ue.prototype.doPublic=fe,ue.prototype.setPublic=ce,ue.prototype.encrypt=pe,ue.prototype.doPrivate=ye,ue.prototype.setPrivate=de,ue.prototype.setPrivateEx=ge,ue.prototype.generate=me,ue.prototype.decrypt=ve,
// Copyright (c) 2011  Kevin M Burns Jr.
// All Rights Reserved.
// See "LICENSE" for details.
//
// Extension to jsbn which adds facilities for asynchronous RSA key generation
// Primarily created to avoid execution timeout on mobile devices
//
// http://www-cs-students.stanford.edu/~tjw/jsbn/
//
// ---
function(){var t=function(t,r,s){var n=new oe,o=t>>1;this.e=parseInt(r,16);var h=new e(r,16),a=this,u=function(){var r=function(){if(a.p.compareTo(a.q)<=0){var t=a.p;a.p=a.q,a.q=t}var i=a.p.subtract(e.ONE),r=a.q.subtract(e.ONE),n=i.multiply(r);0==n.gcd(h).compareTo(e.ONE)?(a.n=a.p.multiply(a.q),a.d=h.modInverse(n),a.dmp1=a.d.mod(i),a.dmq1=a.d.mod(r),a.coeff=a.q.modInverse(a.p),setTimeout(function(){s()},0)):setTimeout(u,0)},c=function(){a.q=i(),a.q.fromNumberAsync(o,1,n,function(){a.q.subtract(e.ONE).gcda(h,function(t){0==t.compareTo(e.ONE)&&a.q.isProbablePrime(10)?setTimeout(r,0):setTimeout(c,0)})})},f=function(){a.p=i(),a.p.fromNumberAsync(t-o,1,n,function(){a.p.subtract(e.ONE).gcda(h,function(t){0==t.compareTo(e.ONE)&&a.p.isProbablePrime(10)?setTimeout(c,0):setTimeout(f,0)})})};setTimeout(f,0)};setTimeout(u,0)};ue.prototype.generateAsync=t;var r=function(t,e){var i=this.s<0?this.negate():this.clone(),r=t.s<0?t.negate():t.clone();if(i.compareTo(r)<0){var s=i;i=r,r=s}var n=i.getLowestSetBit(),o=r.getLowestSetBit();if(0>o)return void e(i);o>n&&(o=n),o>0&&(i.rShiftTo(o,i),r.rShiftTo(o,r));var h=function(){(n=i.getLowestSetBit())>0&&i.rShiftTo(n,i),(n=r.getLowestSetBit())>0&&r.rShiftTo(n,r),i.compareTo(r)>=0?(i.subTo(r,i),i.rShiftTo(1,i)):(r.subTo(i,r),r.rShiftTo(1,r)),i.signum()>0?setTimeout(h,0):(o>0&&r.lShiftTo(o,r),setTimeout(function(){e(r)},0))};setTimeout(h,10)};e.prototype.gcda=r;var s=function(t,i,r,s){if("number"==typeof i)if(2>t)this.fromInt(1);else{this.fromNumber(t,r),this.testBit(t-1)||this.bitwiseTo(e.ONE.shiftLeft(t-1),ht,this),this.isEven()&&this.dAddOffset(1,0);var n=this,o=function(){n.dAddOffset(2,0),n.bitLength()>t&&n.subTo(e.ONE.shiftLeft(t-1),n),n.isProbablePrime(i)?setTimeout(function(){s()},0):setTimeout(o,0)};setTimeout(o,0)}else{var h=new Array,a=7&t;h.length=(t>>3)+1,i.nextBytes(h),a>0?h[0]&=(1<<a)-1:h[0]=0,this.fromString(h,256)}};e.prototype.fromNumberAsync=s}();var Le="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",qe="=",Ce=Ce||{};Ce.env=Ce.env||{};var He=Ce,je=Object.prototype,ke="[object Function]",Fe=["toString","valueOf"];Ce.env.parseUA=function(t){var e,i=function(t){var e=0;return parseFloat(t.replace(/\./g,function(){return 1==e++?"":"."}))},r=navigator,s={ie:0,opera:0,gecko:0,webkit:0,chrome:0,mobile:null,air:0,ipad:0,iphone:0,ipod:0,ios:null,android:0,webos:0,caja:r&&r.cajaVersion,secure:!1,os:null},n=t||navigator&&navigator.userAgent,o=window&&window.location,h=o&&o.href;return s.secure=h&&0===h.toLowerCase().indexOf("https"),n&&(/windows|win32/i.test(n)?s.os="windows":/macintosh/i.test(n)?s.os="macintosh":/rhino/i.test(n)&&(s.os="rhino"),/KHTML/.test(n)&&(s.webkit=1),e=n.match(/AppleWebKit\/([^\s]*)/),e&&e[1]&&(s.webkit=i(e[1]),/ Mobile\//.test(n)?(s.mobile="Apple",e=n.match(/OS ([^\s]*)/),e&&e[1]&&(e=i(e[1].replace("_","."))),s.ios=e,s.ipad=s.ipod=s.iphone=0,e=n.match(/iPad|iPod|iPhone/),e&&e[0]&&(s[e[0].toLowerCase()]=s.ios)):(e=n.match(/NokiaN[^\/]*|Android \d\.\d|webOS\/\d\.\d/),e&&(s.mobile=e[0]),/webOS/.test(n)&&(s.mobile="WebOS",e=n.match(/webOS\/([^\s]*);/),e&&e[1]&&(s.webos=i(e[1]))),/ Android/.test(n)&&(s.mobile="Android",e=n.match(/Android ([^\s]*);/),e&&e[1]&&(s.android=i(e[1])))),e=n.match(/Chrome\/([^\s]*)/),e&&e[1]?s.chrome=i(e[1]):(e=n.match(/AdobeAIR\/([^\s]*)/),e&&(s.air=e[0]))),s.webkit||(e=n.match(/Opera[\s\/]([^\s]*)/),e&&e[1]?(s.opera=i(e[1]),e=n.match(/Version\/([^\s]*)/),e&&e[1]&&(s.opera=i(e[1])),e=n.match(/Opera Mini[^;]*/),e&&(s.mobile=e[0])):(e=n.match(/MSIE\s([^;]*)/),e&&e[1]?s.ie=i(e[1]):(e=n.match(/Gecko\/([^\s]*)/),e&&(s.gecko=1,e=n.match(/rv:([^\s\)]*)/),e&&e[1]&&(s.gecko=i(e[1]))))))),s},Ce.env.ua=Ce.env.parseUA(),Ce.isFunction=function(t){return"function"==typeof t||je.toString.apply(t)===ke},Ce._IEEnumFix=Ce.env.ua.ie?function(t,e){var i,r,s;for(i=0;i<Fe.length;i+=1)r=Fe[i],s=e[r],He.isFunction(s)&&s!=je[r]&&(t[r]=s)}:function(){},Ce.extend=function(t,e,i){if(!e||!t)throw new Error("extend failed, please check that all dependencies are included.");var r,s=function(){};if(s.prototype=e.prototype,t.prototype=new s,t.prototype.constructor=t,t.superclass=e.prototype,e.prototype.constructor==je.constructor&&(e.prototype.constructor=e),i){for(r in i)He.hasOwnProperty(i,r)&&(t.prototype[r]=i[r]);He._IEEnumFix(t.prototype,i)}},/*
 * asn1.js - ASN.1 DER encoder classes
 *
 * Copyright (c) 2013 Kenji Urushima (kenji.urushima@gmail.com)
 *
 * This software is licensed under the terms of the MIT License.
 * http://kjur.github.com/jsrsasign/license
 *
 * The above copyright and license notice shall be 
 * included in all copies or substantial portions of the Software.
 */
/**
 * @fileOverview
 * @name asn1-1.0.js
 * @author Kenji Urushima kenji.urushima@gmail.com
 * @version 1.0.2 (2013-May-30)
 * @since 2.1
 * @license <a href="http://kjur.github.io/jsrsasign/license/">MIT License</a>
 */
"undefined"!=typeof KJUR&&KJUR||(KJUR={}),"undefined"!=typeof KJUR.asn1&&KJUR.asn1||(KJUR.asn1={}),KJUR.asn1.ASN1Util=new function(){this.integerToByteHex=function(t){var e=t.toString(16);return e.length%2==1&&(e="0"+e),e},this.bigIntToMinTwosComplementsHex=function(t){var i=t.toString(16);if("-"!=i.substr(0,1))i.length%2==1?i="0"+i:i.match(/^[0-7]/)||(i="00"+i);else{var r=i.substr(1),s=r.length;s%2==1?s+=1:i.match(/^[0-7]/)||(s+=2);for(var n="",o=0;s>o;o++)n+="f";var h=new e(n,16),a=h.xor(t).add(e.ONE);i=a.toString(16).replace(/^-/,"")}return i},this.getPEMStringFromHex=function(t,e){var i=CryptoJS.enc.Hex.parse(t),r=CryptoJS.enc.Base64.stringify(i),s=r.replace(/(.{64})/g,"$1\r\n");return s=s.replace(/\r\n$/,""),"-----BEGIN "+e+"-----\r\n"+s+"\r\n-----END "+e+"-----\r\n"}},KJUR.asn1.ASN1Object=function(){var t="";this.getLengthHexFromValue=function(){if("undefined"==typeof this.hV||null==this.hV)throw"this.hV is null or undefined.";if(this.hV.length%2==1)throw"value hex must be even length: n="+t.length+",v="+this.hV;var e=this.hV.length/2,i=e.toString(16);if(i.length%2==1&&(i="0"+i),128>e)return i;var r=i.length/2;if(r>15)throw"ASN.1 length too long to represent by 8x: n = "+e.toString(16);var s=128+r;return s.toString(16)+i},this.getEncodedHex=function(){return(null==this.hTLV||this.isModified)&&(this.hV=this.getFreshValueHex(),this.hL=this.getLengthHexFromValue(),this.hTLV=this.hT+this.hL+this.hV,this.isModified=!1),this.hTLV},this.getValueHex=function(){return this.getEncodedHex(),this.hV},this.getFreshValueHex=function(){return""}},KJUR.asn1.DERAbstractString=function(t){KJUR.asn1.DERAbstractString.superclass.constructor.call(this);this.getString=function(){return this.s},this.setString=function(t){this.hTLV=null,this.isModified=!0,this.s=t,this.hV=stohex(this.s)},this.setStringHex=function(t){this.hTLV=null,this.isModified=!0,this.s=null,this.hV=t},this.getFreshValueHex=function(){return this.hV},"undefined"!=typeof t&&("undefined"!=typeof t.str?this.setString(t.str):"undefined"!=typeof t.hex&&this.setStringHex(t.hex))},Ce.extend(KJUR.asn1.DERAbstractString,KJUR.asn1.ASN1Object),KJUR.asn1.DERAbstractTime=function(t){KJUR.asn1.DERAbstractTime.superclass.constructor.call(this);this.localDateToUTC=function(t){utc=t.getTime()+6e4*t.getTimezoneOffset();var e=new Date(utc);return e},this.formatDate=function(t,e){var i=this.zeroPadding,r=this.localDateToUTC(t),s=String(r.getFullYear());"utc"==e&&(s=s.substr(2,2));var n=i(String(r.getMonth()+1),2),o=i(String(r.getDate()),2),h=i(String(r.getHours()),2),a=i(String(r.getMinutes()),2),u=i(String(r.getSeconds()),2);return s+n+o+h+a+u+"Z"},this.zeroPadding=function(t,e){return t.length>=e?t:new Array(e-t.length+1).join("0")+t},this.getString=function(){return this.s},this.setString=function(t){this.hTLV=null,this.isModified=!0,this.s=t,this.hV=stohex(this.s)},this.setByDateValue=function(t,e,i,r,s,n){var o=new Date(Date.UTC(t,e-1,i,r,s,n,0));this.setByDate(o)},this.getFreshValueHex=function(){return this.hV}},Ce.extend(KJUR.asn1.DERAbstractTime,KJUR.asn1.ASN1Object),KJUR.asn1.DERAbstractStructured=function(t){KJUR.asn1.DERAbstractString.superclass.constructor.call(this);this.setByASN1ObjectArray=function(t){this.hTLV=null,this.isModified=!0,this.asn1Array=t},this.appendASN1Object=function(t){this.hTLV=null,this.isModified=!0,this.asn1Array.push(t)},this.asn1Array=new Array,"undefined"!=typeof t&&"undefined"!=typeof t.array&&(this.asn1Array=t.array)},Ce.extend(KJUR.asn1.DERAbstractStructured,KJUR.asn1.ASN1Object),KJUR.asn1.DERBoolean=function(){KJUR.asn1.DERBoolean.superclass.constructor.call(this),this.hT="01",this.hTLV="0101ff"},Ce.extend(KJUR.asn1.DERBoolean,KJUR.asn1.ASN1Object),KJUR.asn1.DERInteger=function(t){KJUR.asn1.DERInteger.superclass.constructor.call(this),this.hT="02",this.setByBigInteger=function(t){this.hTLV=null,this.isModified=!0,this.hV=KJUR.asn1.ASN1Util.bigIntToMinTwosComplementsHex(t)},this.setByInteger=function(t){var i=new e(String(t),10);this.setByBigInteger(i)},this.setValueHex=function(t){this.hV=t},this.getFreshValueHex=function(){return this.hV},"undefined"!=typeof t&&("undefined"!=typeof t.bigint?this.setByBigInteger(t.bigint):"undefined"!=typeof t["int"]?this.setByInteger(t["int"]):"undefined"!=typeof t.hex&&this.setValueHex(t.hex))},Ce.extend(KJUR.asn1.DERInteger,KJUR.asn1.ASN1Object),KJUR.asn1.DERBitString=function(t){KJUR.asn1.DERBitString.superclass.constructor.call(this),this.hT="03",this.setHexValueIncludingUnusedBits=function(t){this.hTLV=null,this.isModified=!0,this.hV=t},this.setUnusedBitsAndHexValue=function(t,e){if(0>t||t>7)throw"unused bits shall be from 0 to 7: u = "+t;var i="0"+t;this.hTLV=null,this.isModified=!0,this.hV=i+e},this.setByBinaryString=function(t){t=t.replace(/0+$/,"");var e=8-t.length%8;8==e&&(e=0);for(var i=0;e>=i;i++)t+="0";for(var r="",i=0;i<t.length-1;i+=8){var s=t.substr(i,8),n=parseInt(s,2).toString(16);1==n.length&&(n="0"+n),r+=n}this.hTLV=null,this.isModified=!0,this.hV="0"+e+r},this.setByBooleanArray=function(t){for(var e="",i=0;i<t.length;i++)e+=1==t[i]?"1":"0";this.setByBinaryString(e)},this.newFalseArray=function(t){for(var e=new Array(t),i=0;t>i;i++)e[i]=!1;return e},this.getFreshValueHex=function(){return this.hV},"undefined"!=typeof t&&("undefined"!=typeof t.hex?this.setHexValueIncludingUnusedBits(t.hex):"undefined"!=typeof t.bin?this.setByBinaryString(t.bin):"undefined"!=typeof t.array&&this.setByBooleanArray(t.array))},Ce.extend(KJUR.asn1.DERBitString,KJUR.asn1.ASN1Object),KJUR.asn1.DEROctetString=function(t){KJUR.asn1.DEROctetString.superclass.constructor.call(this,t),this.hT="04"},Ce.extend(KJUR.asn1.DEROctetString,KJUR.asn1.DERAbstractString),KJUR.asn1.DERNull=function(){KJUR.asn1.DERNull.superclass.constructor.call(this),this.hT="05",this.hTLV="0500"},Ce.extend(KJUR.asn1.DERNull,KJUR.asn1.ASN1Object),KJUR.asn1.DERObjectIdentifier=function(t){var i=function(t){var e=t.toString(16);return 1==e.length&&(e="0"+e),e},r=function(t){var r="",s=new e(t,10),n=s.toString(2),o=7-n.length%7;7==o&&(o=0);for(var h="",a=0;o>a;a++)h+="0";n=h+n;for(var a=0;a<n.length-1;a+=7){var u=n.substr(a,7);a!=n.length-7&&(u="1"+u),r+=i(parseInt(u,2))}return r};KJUR.asn1.DERObjectIdentifier.superclass.constructor.call(this),this.hT="06",this.setValueHex=function(t){this.hTLV=null,this.isModified=!0,this.s=null,this.hV=t},this.setValueOidString=function(t){if(!t.match(/^[0-9.]+$/))throw"malformed oid string: "+t;var e="",s=t.split("."),n=40*parseInt(s[0])+parseInt(s[1]);e+=i(n),s.splice(0,2);for(var o=0;o<s.length;o++)e+=r(s[o]);this.hTLV=null,this.isModified=!0,this.s=null,this.hV=e},this.setValueName=function(t){if("undefined"==typeof KJUR.asn1.x509.OID.name2oidList[t])throw"DERObjectIdentifier oidName undefined: "+t;var e=KJUR.asn1.x509.OID.name2oidList[t];this.setValueOidString(e)},this.getFreshValueHex=function(){return this.hV},"undefined"!=typeof t&&("undefined"!=typeof t.oid?this.setValueOidString(t.oid):"undefined"!=typeof t.hex?this.setValueHex(t.hex):"undefined"!=typeof t.name&&this.setValueName(t.name))},Ce.extend(KJUR.asn1.DERObjectIdentifier,KJUR.asn1.ASN1Object),KJUR.asn1.DERUTF8String=function(t){KJUR.asn1.DERUTF8String.superclass.constructor.call(this,t),this.hT="0c"},Ce.extend(KJUR.asn1.DERUTF8String,KJUR.asn1.DERAbstractString),KJUR.asn1.DERNumericString=function(t){KJUR.asn1.DERNumericString.superclass.constructor.call(this,t),this.hT="12"},Ce.extend(KJUR.asn1.DERNumericString,KJUR.asn1.DERAbstractString),KJUR.asn1.DERPrintableString=function(t){KJUR.asn1.DERPrintableString.superclass.constructor.call(this,t),this.hT="13"},Ce.extend(KJUR.asn1.DERPrintableString,KJUR.asn1.DERAbstractString),KJUR.asn1.DERTeletexString=function(t){KJUR.asn1.DERTeletexString.superclass.constructor.call(this,t),this.hT="14"},Ce.extend(KJUR.asn1.DERTeletexString,KJUR.asn1.DERAbstractString),KJUR.asn1.DERIA5String=function(t){KJUR.asn1.DERIA5String.superclass.constructor.call(this,t),this.hT="16"},Ce.extend(KJUR.asn1.DERIA5String,KJUR.asn1.DERAbstractString),KJUR.asn1.DERUTCTime=function(t){KJUR.asn1.DERUTCTime.superclass.constructor.call(this,t),this.hT="17",this.setByDate=function(t){this.hTLV=null,this.isModified=!0,this.date=t,this.s=this.formatDate(this.date,"utc"),this.hV=stohex(this.s)},"undefined"!=typeof t&&("undefined"!=typeof t.str?this.setString(t.str):"undefined"!=typeof t.hex?this.setStringHex(t.hex):"undefined"!=typeof t.date&&this.setByDate(t.date))},Ce.extend(KJUR.asn1.DERUTCTime,KJUR.asn1.DERAbstractTime),KJUR.asn1.DERGeneralizedTime=function(t){KJUR.asn1.DERGeneralizedTime.superclass.constructor.call(this,t),this.hT="18",this.setByDate=function(t){this.hTLV=null,this.isModified=!0,this.date=t,this.s=this.formatDate(this.date,"gen"),this.hV=stohex(this.s)},"undefined"!=typeof t&&("undefined"!=typeof t.str?this.setString(t.str):"undefined"!=typeof t.hex?this.setStringHex(t.hex):"undefined"!=typeof t.date&&this.setByDate(t.date))},Ce.extend(KJUR.asn1.DERGeneralizedTime,KJUR.asn1.DERAbstractTime),KJUR.asn1.DERSequence=function(t){KJUR.asn1.DERSequence.superclass.constructor.call(this,t),this.hT="30",this.getFreshValueHex=function(){for(var t="",e=0;e<this.asn1Array.length;e++){var i=this.asn1Array[e];t+=i.getEncodedHex()}return this.hV=t,this.hV}},Ce.extend(KJUR.asn1.DERSequence,KJUR.asn1.DERAbstractStructured),KJUR.asn1.DERSet=function(t){KJUR.asn1.DERSet.superclass.constructor.call(this,t),this.hT="31",this.getFreshValueHex=function(){for(var t=new Array,e=0;e<this.asn1Array.length;e++){var i=this.asn1Array[e];t.push(i.getEncodedHex())}return t.sort(),this.hV=t.join(""),this.hV}},Ce.extend(KJUR.asn1.DERSet,KJUR.asn1.DERAbstractStructured),KJUR.asn1.DERTaggedObject=function(t){KJUR.asn1.DERTaggedObject.superclass.constructor.call(this),this.hT="a0",this.hV="",this.isExplicit=!0,this.asn1Object=null,this.setASN1Object=function(t,e,i){this.hT=e,this.isExplicit=t,this.asn1Object=i,this.isExplicit?(this.hV=this.asn1Object.getEncodedHex(),this.hTLV=null,this.isModified=!0):(this.hV=null,this.hTLV=i.getEncodedHex(),this.hTLV=this.hTLV.replace(/^../,e),this.isModified=!1)},this.getFreshValueHex=function(){return this.hV},"undefined"!=typeof t&&("undefined"!=typeof t.tag&&(this.hT=t.tag),"undefined"!=typeof t.explicit&&(this.isExplicit=t.explicit),"undefined"!=typeof t.obj&&(this.asn1Object=t.obj,this.setASN1Object(this.isExplicit,this.hT,this.asn1Object)))},Ce.extend(KJUR.asn1.DERTaggedObject,KJUR.asn1.ASN1Object),
// Copyright (c) 2008-2013 Lapo Luchini <lapo@lapo.it>
// copyright notice and this permission notice appear in all copies.
// 
// THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
// WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
// ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
// WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
// ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
// OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
function(t){"use strict";var e,i={};i.decode=function(i){var r;if(e===t){var s="0123456789ABCDEF",n=" \f\n\r	 \u2028\u2029";for(e=[],r=0;16>r;++r)e[s.charAt(r)]=r;for(s=s.toLowerCase(),r=10;16>r;++r)e[s.charAt(r)]=r;for(r=0;r<n.length;++r)e[n.charAt(r)]=-1}var o=[],h=0,a=0;for(r=0;r<i.length;++r){var u=i.charAt(r);if("="==u)break;if(u=e[u],-1!=u){if(u===t)throw"Illegal character at offset "+r;h|=u,++a>=2?(o[o.length]=h,h=0,a=0):h<<=4}}if(a)throw"Hex encoding incomplete: 4 bits missing";return o},window.Hex=i}(),
// Copyright (c) 2008-2013 Lapo Luchini <lapo@lapo.it>
// copyright notice and this permission notice appear in all copies.
// 
// THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
// WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
// ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
// WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
// ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
// OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
function(t){"use strict";var e,i={};i.decode=function(i){var r;if(e===t){var s="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",n="= \f\n\r	 \u2028\u2029";for(e=[],r=0;64>r;++r)e[s.charAt(r)]=r;for(r=0;r<n.length;++r)e[n.charAt(r)]=-1}var o=[],h=0,a=0;for(r=0;r<i.length;++r){var u=i.charAt(r);if("="==u)break;if(u=e[u],-1!=u){if(u===t)throw"Illegal character at offset "+r;h|=u,++a>=4?(o[o.length]=h>>16,o[o.length]=h>>8&255,o[o.length]=255&h,h=0,a=0):h<<=6}}switch(a){case 1:throw"Base64 encoding incomplete: at least 2 bits missing";case 2:o[o.length]=h>>10;break;case 3:o[o.length]=h>>16,o[o.length]=h>>8&255}return o},i.re=/-----BEGIN [^-]+-----([A-Za-z0-9+\/=\s]+)-----END [^-]+-----|begin-base64[^\n]+\n([A-Za-z0-9+\/=\s]+)====/,i.unarmor=function(t){var e=i.re.exec(t);if(e)if(e[1])t=e[1];else{if(!e[2])throw"RegExp out of sync";t=e[2]}return i.decode(t)},window.Base64=i}(),
// Copyright (c) 2008-2013 Lapo Luchini <lapo@lapo.it>
// copyright notice and this permission notice appear in all copies.
// 
// THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
// WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
// ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
// WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
// ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
// OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
function(t){"use strict";function e(t,i){t instanceof e?(this.enc=t.enc,this.pos=t.pos):(this.enc=t,this.pos=i)}function i(t,e,i,r,s){this.stream=t,this.header=e,this.length=i,this.tag=r,this.sub=s}var r=100,s="…",n={tag:function(t,e){var i=document.createElement(t);return i.className=e,i},text:function(t){return document.createTextNode(t)}};e.prototype.get=function(e){if(e===t&&(e=this.pos++),e>=this.enc.length)throw"Requesting byte offset "+e+" on a stream of length "+this.enc.length;return this.enc[e]},e.prototype.hexDigits="0123456789ABCDEF",e.prototype.hexByte=function(t){return this.hexDigits.charAt(t>>4&15)+this.hexDigits.charAt(15&t)},e.prototype.hexDump=function(t,e,i){for(var r="",s=t;e>s;++s)if(r+=this.hexByte(this.get(s)),i!==!0)switch(15&s){case 7:r+="  ";break;case 15:r+="\n";break;default:r+=" "}return r},e.prototype.parseStringISO=function(t,e){for(var i="",r=t;e>r;++r)i+=String.fromCharCode(this.get(r));return i},e.prototype.parseStringUTF=function(t,e){for(var i="",r=t;e>r;){var s=this.get(r++);i+=128>s?String.fromCharCode(s):s>191&&224>s?String.fromCharCode((31&s)<<6|63&this.get(r++)):String.fromCharCode((15&s)<<12|(63&this.get(r++))<<6|63&this.get(r++))}return i},e.prototype.parseStringBMP=function(t,e){for(var i="",r=t;e>r;r+=2){var s=this.get(r),n=this.get(r+1);i+=String.fromCharCode((s<<8)+n)}return i},e.prototype.reTime=/^((?:1[89]|2\d)?\d\d)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])([01]\d|2[0-3])(?:([0-5]\d)(?:([0-5]\d)(?:[.,](\d{1,3}))?)?)?(Z|[-+](?:[0]\d|1[0-2])([0-5]\d)?)?$/,e.prototype.parseTime=function(t,e){var i=this.parseStringISO(t,e),r=this.reTime.exec(i);return r?(i=r[1]+"-"+r[2]+"-"+r[3]+" "+r[4],r[5]&&(i+=":"+r[5],r[6]&&(i+=":"+r[6],r[7]&&(i+="."+r[7]))),r[8]&&(i+=" UTC","Z"!=r[8]&&(i+=r[8],r[9]&&(i+=":"+r[9]))),i):"Unrecognized time: "+i},e.prototype.parseInteger=function(t,e){var i=e-t;if(i>4){i<<=3;var r=this.get(t);if(0===r)i-=8;else for(;128>r;)r<<=1,--i;return"("+i+" bit)"}for(var s=0,n=t;e>n;++n)s=s<<8|this.get(n);return s},e.prototype.parseBitString=function(t,e){var i=this.get(t),r=(e-t-1<<3)-i,s="("+r+" bit)";if(20>=r){var n=i;s+=" ";for(var o=e-1;o>t;--o){for(var h=this.get(o),a=n;8>a;++a)s+=h>>a&1?"1":"0";n=0}}return s},e.prototype.parseOctetString=function(t,e){var i=e-t,n="("+i+" byte) ";i>r&&(e=t+r);for(var o=t;e>o;++o)n+=this.hexByte(this.get(o));return i>r&&(n+=s),n},e.prototype.parseOID=function(t,e){for(var i="",r=0,s=0,n=t;e>n;++n){var o=this.get(n);if(r=r<<7|127&o,s+=7,!(128&o)){if(""===i){var h=80>r?40>r?0:1:2;i=h+"."+(r-40*h)}else i+="."+(s>=31?"bigint":r);r=s=0}}return i},i.prototype.typeName=function(){if(this.tag===t)return"unknown";var e=this.tag>>6,i=(this.tag>>5&1,31&this.tag);switch(e){case 0:switch(i){case 0:return"EOC";case 1:return"BOOLEAN";case 2:return"INTEGER";case 3:return"BIT_STRING";case 4:return"OCTET_STRING";case 5:return"NULL";case 6:return"OBJECT_IDENTIFIER";case 7:return"ObjectDescriptor";case 8:return"EXTERNAL";case 9:return"REAL";case 10:return"ENUMERATED";case 11:return"EMBEDDED_PDV";case 12:return"UTF8String";case 16:return"SEQUENCE";case 17:return"SET";case 18:return"NumericString";case 19:return"PrintableString";case 20:return"TeletexString";case 21:return"VideotexString";case 22:return"IA5String";case 23:return"UTCTime";case 24:return"GeneralizedTime";case 25:return"GraphicString";case 26:return"VisibleString";case 27:return"GeneralString";case 28:return"UniversalString";case 30:return"BMPString";default:return"Universal_"+i.toString(16)}case 1:return"Application_"+i.toString(16);case 2:return"["+i+"]";case 3:return"Private_"+i.toString(16)}},i.prototype.reSeemsASCII=/^[ -~]+$/,i.prototype.content=function(){if(this.tag===t)return null;var e=this.tag>>6,i=31&this.tag,n=this.posContent(),o=Math.abs(this.length);if(0!==e){if(null!==this.sub)return"("+this.sub.length+" elem)";var h=this.stream.parseStringISO(n,n+Math.min(o,r));return this.reSeemsASCII.test(h)?h.substring(0,2*r)+(h.length>2*r?s:""):this.stream.parseOctetString(n,n+o)}switch(i){case 1:return 0===this.stream.get(n)?"false":"true";case 2:return this.stream.parseInteger(n,n+o);case 3:return this.sub?"("+this.sub.length+" elem)":this.stream.parseBitString(n,n+o);case 4:return this.sub?"("+this.sub.length+" elem)":this.stream.parseOctetString(n,n+o);case 6:return this.stream.parseOID(n,n+o);case 16:case 17:return"("+this.sub.length+" elem)";case 12:return this.stream.parseStringUTF(n,n+o);case 18:case 19:case 20:case 21:case 22:case 26:return this.stream.parseStringISO(n,n+o);case 30:return this.stream.parseStringBMP(n,n+o);case 23:case 24:return this.stream.parseTime(n,n+o)}return null},i.prototype.toString=function(){return this.typeName()+"@"+this.stream.pos+"[header:"+this.header+",length:"+this.length+",sub:"+(null===this.sub?"null":this.sub.length)+"]"},i.prototype.print=function(e){if(e===t&&(e=""),document.writeln(e+this),null!==this.sub){e+="  ";for(var i=0,r=this.sub.length;r>i;++i)this.sub[i].print(e)}},i.prototype.toPrettyString=function(e){e===t&&(e="");var i=e+this.typeName()+" @"+this.stream.pos;if(this.length>=0&&(i+="+"),i+=this.length,32&this.tag?i+=" (constructed)":3!=this.tag&&4!=this.tag||null===this.sub||(i+=" (encapsulates)"),i+="\n",null!==this.sub){e+="  ";for(var r=0,s=this.sub.length;s>r;++r)i+=this.sub[r].toPrettyString(e)}return i},i.prototype.toDOM=function(){var t=n.tag("div","node");t.asn1=this;var e=n.tag("div","head"),i=this.typeName().replace(/_/g," ");e.innerHTML=i;var r=this.content();if(null!==r){r=String(r).replace(/</g,"&lt;");var s=n.tag("span","preview");s.appendChild(n.text(r)),e.appendChild(s)}t.appendChild(e),this.node=t,this.head=e;var o=n.tag("div","value");if(i="Offset: "+this.stream.pos+"<br/>",i+="Length: "+this.header+"+",i+=this.length>=0?this.length:-this.length+" (undefined)",32&this.tag?i+="<br/>(constructed)":3!=this.tag&&4!=this.tag||null===this.sub||(i+="<br/>(encapsulates)"),null!==r&&(i+="<br/>Value:<br/><b>"+r+"</b>","object"==typeof oids&&6==this.tag)){var h=oids[r];h&&(h.d&&(i+="<br/>"+h.d),h.c&&(i+="<br/>"+h.c),h.w&&(i+="<br/>(warning!)"))}o.innerHTML=i,t.appendChild(o);var a=n.tag("div","sub");if(null!==this.sub)for(var u=0,c=this.sub.length;c>u;++u)a.appendChild(this.sub[u].toDOM());return t.appendChild(a),e.onclick=function(){t.className="node collapsed"==t.className?"node":"node collapsed"},t},i.prototype.posStart=function(){return this.stream.pos},i.prototype.posContent=function(){return this.stream.pos+this.header},i.prototype.posEnd=function(){return this.stream.pos+this.header+Math.abs(this.length)},i.prototype.fakeHover=function(t){this.node.className+=" hover",t&&(this.head.className+=" hover")},i.prototype.fakeOut=function(t){var e=/ ?hover/;this.node.className=this.node.className.replace(e,""),t&&(this.head.className=this.head.className.replace(e,""))},i.prototype.toHexDOM_sub=function(t,e,i,r,s){if(!(r>=s)){var o=n.tag("span",e);o.appendChild(n.text(i.hexDump(r,s))),t.appendChild(o)}},i.prototype.toHexDOM=function(e){var i=n.tag("span","hex");if(e===t&&(e=i),this.head.hexNode=i,this.head.onmouseover=function(){this.hexNode.className="hexCurrent"},this.head.onmouseout=function(){this.hexNode.className="hex"},i.asn1=this,i.onmouseover=function(){var t=!e.selected;t&&(e.selected=this.asn1,this.className="hexCurrent"),this.asn1.fakeHover(t)},i.onmouseout=function(){var t=e.selected==this.asn1;this.asn1.fakeOut(t),t&&(e.selected=null,this.className="hex")},this.toHexDOM_sub(i,"tag",this.stream,this.posStart(),this.posStart()+1),this.toHexDOM_sub(i,this.length>=0?"dlen":"ulen",this.stream,this.posStart()+1,this.posContent()),null===this.sub)i.appendChild(n.text(this.stream.hexDump(this.posContent(),this.posEnd())));else if(this.sub.length>0){var r=this.sub[0],s=this.sub[this.sub.length-1];this.toHexDOM_sub(i,"intro",this.stream,this.posContent(),r.posStart());for(var o=0,h=this.sub.length;h>o;++o)i.appendChild(this.sub[o].toHexDOM(e));this.toHexDOM_sub(i,"outro",this.stream,s.posEnd(),this.posEnd())}return i},i.prototype.toHexString=function(t){return this.stream.hexDump(this.posStart(),this.posEnd(),!0)},i.decodeLength=function(t){var e=t.get(),i=127&e;if(i==e)return i;if(i>3)throw"Length over 24 bits not supported at position "+(t.pos-1);if(0===i)return-1;e=0;for(var r=0;i>r;++r)e=e<<8|t.get();return e},i.hasContent=function(t,r,s){if(32&t)return!0;if(3>t||t>4)return!1;var n=new e(s);3==t&&n.get();var o=n.get();if(o>>6&1)return!1;try{var h=i.decodeLength(n);return n.pos-s.pos+h==r}catch(a){return!1}},i.decode=function(t){t instanceof e||(t=new e(t,0));var r=new e(t),s=t.get(),n=i.decodeLength(t),o=t.pos-r.pos,h=null;if(i.hasContent(s,n,t)){var a=t.pos;if(3==s&&t.get(),h=[],n>=0){for(var u=a+n;t.pos<u;)h[h.length]=i.decode(t);if(t.pos!=u)throw"Content size is not correct for container starting at offset "+a}else try{for(;;){var c=i.decode(t);if(0===c.tag)break;h[h.length]=c}n=a-t.pos}catch(f){throw"Exception while decoding undefined length content: "+f}}else t.pos+=n;return new i(r,o,n,s,h)},i.test=function(){for(var t=[{value:[39],expected:39},{value:[129,201],expected:201},{value:[131,254,220,186],expected:16702650}],r=0,s=t.length;s>r;++r){var n=new e(t[r].value,0),o=i.decodeLength(n);o!=t[r].expected&&document.write("In test["+r+"] expected "+t[r].expected+" got "+o+"\n")}},window.ASN1=i}(),ASN1.prototype.getHexStringValue=function(){var t=this.toHexString(),e=2*this.header,i=2*this.length;return t.substr(e,i)},ue.prototype.parseKey=function(t){try{var e=0,i=0,r=/^\s*(?:[0-9A-Fa-f][0-9A-Fa-f]\s*)+$/,s=r.test(t)?Hex.decode(t):Base64.unarmor(t),n=ASN1.decode(s);if(3===n.sub.length&&(n=n.sub[2].sub[0]),9===n.sub.length){e=n.sub[1].getHexStringValue(),this.n=he(e,16),i=n.sub[2].getHexStringValue(),this.e=parseInt(i,16);var o=n.sub[3].getHexStringValue();this.d=he(o,16);var h=n.sub[4].getHexStringValue();this.p=he(h,16);var a=n.sub[5].getHexStringValue();this.q=he(a,16);var u=n.sub[6].getHexStringValue();this.dmp1=he(u,16);var c=n.sub[7].getHexStringValue();this.dmq1=he(c,16);var f=n.sub[8].getHexStringValue();this.coeff=he(f,16)}else{if(2!==n.sub.length)return!1;var p=n.sub[1],l=p.sub[0];e=l.sub[0].getHexStringValue(),this.n=he(e,16),i=l.sub[1].getHexStringValue(),this.e=parseInt(i,16)}return!0}catch(d){return!1}},ue.prototype.getPrivateBaseKey=function(){var t={array:[new KJUR.asn1.DERInteger({"int":0}),new KJUR.asn1.DERInteger({bigint:this.n}),new KJUR.asn1.DERInteger({"int":this.e}),new KJUR.asn1.DERInteger({bigint:this.d}),new KJUR.asn1.DERInteger({bigint:this.p}),new KJUR.asn1.DERInteger({bigint:this.q}),new KJUR.asn1.DERInteger({bigint:this.dmp1}),new KJUR.asn1.DERInteger({bigint:this.dmq1}),new KJUR.asn1.DERInteger({bigint:this.coeff})]},e=new KJUR.asn1.DERSequence(t);return e.getEncodedHex()},ue.prototype.getPrivateBaseKeyB64=function(){return be(this.getPrivateBaseKey())},ue.prototype.getPublicBaseKey=function(){var t={array:[new KJUR.asn1.DERObjectIdentifier({oid:"1.2.840.113549.1.1.1"}),new KJUR.asn1.DERNull]},e=new KJUR.asn1.DERSequence(t);t={array:[new KJUR.asn1.DERInteger({bigint:this.n}),new KJUR.asn1.DERInteger({"int":this.e})]};var i=new KJUR.asn1.DERSequence(t);t={hex:"00"+i.getEncodedHex()};var r=new KJUR.asn1.DERBitString(t);t={array:[e,r]};var s=new KJUR.asn1.DERSequence(t);return s.getEncodedHex()},ue.prototype.getPublicBaseKeyB64=function(){return be(this.getPublicBaseKey())},ue.prototype.wordwrap=function(t,e){if(e=e||64,!t)return t;var i="(.{1,"+e+"})( +|$\n?)|(.{1,"+e+"})";return t.match(RegExp(i,"g")).join("\n")},ue.prototype.getPrivateKey=function(){var t="-----BEGIN RSA PRIVATE KEY-----\n";return t+=this.wordwrap(this.getPrivateBaseKeyB64())+"\n",t+="-----END RSA PRIVATE KEY-----"},ue.prototype.getPublicKey=function(){var t="-----BEGIN PUBLIC KEY-----\n";return t+=this.wordwrap(this.getPublicBaseKeyB64())+"\n",t+="-----END PUBLIC KEY-----"},ue.prototype.hasPublicKeyProperty=function(t){return t=t||{},t.hasOwnProperty("n")&&t.hasOwnProperty("e")},ue.prototype.hasPrivateKeyProperty=function(t){return t=t||{},t.hasOwnProperty("n")&&t.hasOwnProperty("e")&&t.hasOwnProperty("d")&&t.hasOwnProperty("p")&&t.hasOwnProperty("q")&&t.hasOwnProperty("dmp1")&&t.hasOwnProperty("dmq1")&&t.hasOwnProperty("coeff")},ue.prototype.parsePropertiesFrom=function(t){this.n=t.n,this.e=t.e,t.hasOwnProperty("d")&&(this.d=t.d,this.p=t.p,this.q=t.q,this.dmp1=t.dmp1,this.dmq1=t.dmq1,this.coeff=t.coeff)};var _e=function(t){ue.call(this),t&&("string"==typeof t?this.parseKey(t):(this.hasPrivateKeyProperty(t)||this.hasPublicKeyProperty(t))&&this.parsePropertiesFrom(t))};_e.prototype=new ue,_e.prototype.constructor=_e;var ze=function(t){t=t||{},this.default_key_size=parseInt(t.default_key_size)||1024,this.default_public_exponent=t.default_public_exponent||"010001",this.log=t.log||!1,this.key=null};ze.prototype.setKey=function(t){this.log&&this.key&&console.warn("A key was already set, overriding existing."),this.key=new _e(t)},ze.prototype.setPrivateKey=function(t){this.setKey(t)},ze.prototype.setPublicKey=function(t){this.setKey(t)},ze.prototype.decrypt=function(t){try{return this.getKey().decrypt(Te(t))}catch(e){return!1}},ze.prototype.encrypt=function(t){try{return be(this.getKey().encrypt(t))}catch(e){return!1}},ze.prototype.getKey=function(t){if(!this.key){if(this.key=new _e,t&&"[object Function]"==={}.toString.call(t))return void this.key.generateAsync(this.default_key_size,this.default_public_exponent,t);this.key.generate(this.default_key_size,this.default_public_exponent)}return this.key},ze.prototype.getPrivateKey=function(){return this.getKey().getPrivateKey()},ze.prototype.getPrivateKeyB64=function(){return this.getKey().getPrivateBaseKeyB64()},ze.prototype.getPublicKey=function(){return this.getKey().getPublicKey()},ze.prototype.getPublicKeyB64=function(){return this.getKey().getPublicBaseKeyB64()},ze.version="2.3.0",t.JSEncrypt=ze}(JSEncryptExports),function(t,e){"object"==typeof exports&&"undefined"!=typeof module?module.exports=e:"function"==typeof define&&define.amd?define(e):t.JSEncrypt=e}(this,JSEncryptExports.JSEncrypt);
/*! jQuery Validation Plugin - v1.20.1 - 6/13/2024
 * https://jqueryvalidation.org/
 * Copyright (c) 2024 Jörn Zaefferer; Licensed MIT */
!function(a){"function"==typeof define&&define.amd?define(["jquery"],a):"object"==typeof module&&module.exports?module.exports=a(require("jquery")):a(jQuery)}(function(a){a.extend(a.fn,{validate:function(b){if(!this.length)return void(b&&b.debug&&window.console&&console.warn("Nothing selected, can't validate, returning nothing."));var c=a.data(this[0],"validator");return c?c:(this.attr("novalidate","novalidate"),c=new a.validator(b,this[0]),a.data(this[0],"validator",c),c.settings.onsubmit&&(this.on("click.validate",":submit",function(b){c.submitButton=b.currentTarget,a(this).hasClass("cancel")&&(c.cancelSubmit=!0),void 0!==a(this).attr("formnovalidate")&&(c.cancelSubmit=!0)}),this.on("submit.validate",function(b){function d(){var d,e;return c.submitButton&&(c.settings.submitHandler||c.formSubmitted)&&(d=a("<input type='hidden'/>").attr("name",c.submitButton.name).val(a(c.submitButton).val()).appendTo(c.currentForm)),!(c.settings.submitHandler&&!c.settings.debug)||(e=c.settings.submitHandler.call(c,c.currentForm,b),d&&d.remove(),void 0!==e&&e)}return c.settings.debug&&b.preventDefault(),c.cancelSubmit?(c.cancelSubmit=!1,d()):c.form()?c.pendingRequest?(c.formSubmitted=!0,!1):d():(c.focusInvalid(),!1)})),c)},valid:function(){var b,c,d;return a(this[0]).is("form")?b=this.validate().form():(d=[],b=!0,c=a(this[0].form).validate(),this.each(function(){b=c.element(this)&&b,b||(d=d.concat(c.errorList))}),c.errorList=d),b},rules:function(b,c){var d,e,f,g,h,i,j=this[0],k="undefined"!=typeof this.attr("contenteditable")&&"false"!==this.attr("contenteditable");if(null!=j&&(!j.form&&k&&(j.form=this.closest("form")[0],j.name=this.attr("name")),null!=j.form)){if(b)switch(d=a.data(j.form,"validator").settings,e=d.rules,f=a.validator.staticRules(j),b){case"add":a.extend(f,a.validator.normalizeRule(c)),delete f.messages,e[j.name]=f,c.messages&&(d.messages[j.name]=a.extend(d.messages[j.name],c.messages));break;case"remove":return c?(i={},a.each(c.split(/\s/),function(a,b){i[b]=f[b],delete f[b]}),i):(delete e[j.name],f)}return g=a.validator.normalizeRules(a.extend({},a.validator.classRules(j),a.validator.attributeRules(j),a.validator.dataRules(j),a.validator.staticRules(j)),j),g.required&&(h=g.required,delete g.required,g=a.extend({required:h},g)),g.remote&&(h=g.remote,delete g.remote,g=a.extend(g,{remote:h})),g}}});var b=function(a){return a.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,"")};a.extend(a.expr.pseudos||a.expr[":"],{blank:function(c){return!b(""+a(c).val())},filled:function(c){var d=a(c).val();return null!==d&&!!b(""+d)},unchecked:function(b){return!a(b).prop("checked")}}),a.validator=function(b,c){this.settings=a.extend(!0,{},a.validator.defaults,b),this.currentForm=c,this.init()},a.validator.format=function(b,c){return 1===arguments.length?function(){var c=a.makeArray(arguments);return c.unshift(b),a.validator.format.apply(this,c)}:void 0===c?b:(arguments.length>2&&c.constructor!==Array&&(c=a.makeArray(arguments).slice(1)),c.constructor!==Array&&(c=[c]),a.each(c,function(a,c){b=b.replace(new RegExp("\\{"+a+"\\}","g"),function(){return c})}),b)},a.extend(a.validator,{defaults:{messages:{},groups:{},rules:{},errorClass:"error",pendingClass:"pending",validClass:"valid",errorElement:"label",focusCleanup:!1,focusInvalid:!0,errorContainer:a([]),errorLabelContainer:a([]),onsubmit:!0,ignore:":hidden",ignoreTitle:!1,onfocusin:function(a){this.lastActive=a,this.settings.focusCleanup&&(this.settings.unhighlight&&this.settings.unhighlight.call(this,a,this.settings.errorClass,this.settings.validClass),this.hideThese(this.errorsFor(a)))},onfocusout:function(a){this.checkable(a)||!(a.name in this.submitted)&&this.optional(a)||this.element(a)},onkeyup:function(b,c){var d=[16,17,18,20,35,36,37,38,39,40,45,144,225];9===c.which&&""===this.elementValue(b)||a.inArray(c.keyCode,d)!==-1||(b.name in this.submitted||b.name in this.invalid)&&this.element(b)},onclick:function(a){a.name in this.submitted?this.element(a):a.parentNode.name in this.submitted&&this.element(a.parentNode)},highlight:function(b,c,d){"radio"===b.type?this.findByName(b.name).addClass(c).removeClass(d):a(b).addClass(c).removeClass(d)},unhighlight:function(b,c,d){"radio"===b.type?this.findByName(b.name).removeClass(c).addClass(d):a(b).removeClass(c).addClass(d)}},setDefaults:function(b){a.extend(a.validator.defaults,b)},messages:{required:"This field is required.",remote:"Please fix this field.",email:"Please enter a valid email address.",url:"Please enter a valid URL.",date:"Please enter a valid date.",dateISO:"Please enter a valid date (ISO).",number:"Please enter a valid number.",digits:"Please enter only digits.",equalTo:"Please enter the same value again.",maxlength:a.validator.format("Please enter no more than {0} characters."),minlength:a.validator.format("Please enter at least {0} characters."),rangelength:a.validator.format("Please enter a value between {0} and {1} characters long."),range:a.validator.format("Please enter a value between {0} and {1}."),max:a.validator.format("Please enter a value less than or equal to {0}."),min:a.validator.format("Please enter a value greater than or equal to {0}."),step:a.validator.format("Please enter a multiple of {0}.")},autoCreateRanges:!1,prototype:{init:function(){function b(b){var c="undefined"!=typeof a(this).attr("contenteditable")&&"false"!==a(this).attr("contenteditable");if(!this.form&&c&&(this.form=a(this).closest("form")[0],this.name=a(this).attr("name")),d===this.form){var e=a.data(this.form,"validator"),f="on"+b.type.replace(/^validate/,""),g=e.settings;g[f]&&!a(this).is(g.ignore)&&g[f].call(e,this,b)}}this.labelContainer=a(this.settings.errorLabelContainer),this.errorContext=this.labelContainer.length&&this.labelContainer||a(this.currentForm),this.containers=a(this.settings.errorContainer).add(this.settings.errorLabelContainer),this.submitted={},this.valueCache={},this.pendingRequest=0,this.pending={},this.invalid={},this.reset();var c,d=this.currentForm,e=this.groups={};a.each(this.settings.groups,function(b,c){"string"==typeof c&&(c=c.split(/\s/)),a.each(c,function(a,c){e[c]=b})}),c=this.settings.rules,a.each(c,function(b,d){c[b]=a.validator.normalizeRule(d)}),a(this.currentForm).on("focusin.validate focusout.validate keyup.validate",":text, [type='password'], [type='file'], select, textarea, [type='number'], [type='search'], [type='tel'], [type='url'], [type='email'], [type='datetime'], [type='date'], [type='month'], [type='week'], [type='time'], [type='datetime-local'], [type='range'], [type='color'], [type='radio'], [type='checkbox'], [contenteditable], [type='button']",b).on("click.validate","select, option, [type='radio'], [type='checkbox']",b),this.settings.invalidHandler&&a(this.currentForm).on("invalid-form.validate",this.settings.invalidHandler)},form:function(){return this.checkForm(),a.extend(this.submitted,this.errorMap),this.invalid=a.extend({},this.errorMap),this.valid()||a(this.currentForm).triggerHandler("invalid-form",[this]),this.showErrors(),this.valid()},checkForm:function(){this.prepareForm();for(var a=0,b=this.currentElements=this.elements();b[a];a++)this.check(b[a]);return this.valid()},element:function(b){var c,d,e=this.clean(b),f=this.validationTargetFor(e),g=this,h=!0;return void 0===f?delete this.invalid[e.name]:(this.prepareElement(f),this.currentElements=a(f),d=this.groups[f.name],d&&a.each(this.groups,function(a,b){b===d&&a!==f.name&&(e=g.validationTargetFor(g.clean(g.findByName(a))),e&&e.name in g.invalid&&(g.currentElements.push(e),h=g.check(e)&&h))}),c=this.check(f)!==!1,h=h&&c,c?this.invalid[f.name]=!1:this.invalid[f.name]=!0,this.numberOfInvalids()||(this.toHide=this.toHide.add(this.containers)),this.showErrors(),a(b).attr("aria-invalid",!c)),h},showErrors:function(b){if(b){var c=this;a.extend(this.errorMap,b),this.errorList=a.map(this.errorMap,function(a,b){return{message:a,element:c.findByName(b)[0]}}),this.successList=a.grep(this.successList,function(a){return!(a.name in b)})}this.settings.showErrors?this.settings.showErrors.call(this,this.errorMap,this.errorList):this.defaultShowErrors()},resetForm:function(){a.fn.resetForm&&a(this.currentForm).resetForm(),this.invalid={},this.submitted={},this.prepareForm(),this.hideErrors();var b=this.elements().removeData("previousValue").removeAttr("aria-invalid");this.resetElements(b)},resetElements:function(a){var b;if(this.settings.unhighlight)for(b=0;a[b];b++)this.settings.unhighlight.call(this,a[b],this.settings.errorClass,""),this.findByName(a[b].name).removeClass(this.settings.validClass);else a.removeClass(this.settings.errorClass).removeClass(this.settings.validClass)},numberOfInvalids:function(){return this.objectLength(this.invalid)},objectLength:function(a){var b,c=0;for(b in a)void 0!==a[b]&&null!==a[b]&&a[b]!==!1&&c++;return c},hideErrors:function(){this.hideThese(this.toHide)},hideThese:function(a){a.not(this.containers).text(""),this.addWrapper(a).hide()},valid:function(){return 0===this.size()},size:function(){return this.errorList.length},focusInvalid:function(){if(this.settings.focusInvalid)try{a(this.findLastActive()||this.errorList.length&&this.errorList[0].element||[]).filter(":visible").trigger("focus").trigger("focusin")}catch(b){}},findLastActive:function(){var b=this.lastActive;return b&&1===a.grep(this.errorList,function(a){return a.element.name===b.name}).length&&b},elements:function(){var b=this,c={};return a(this.currentForm).find("input, select, textarea, [contenteditable]").not(":submit, :reset, :image, :disabled").not(this.settings.ignore).filter(function(){var d=this.name||a(this).attr("name"),e="undefined"!=typeof a(this).attr("contenteditable")&&"false"!==a(this).attr("contenteditable");return!d&&b.settings.debug&&window.console&&console.error("%o has no name assigned",this),e&&(this.form=a(this).closest("form")[0],this.name=d),this.form===b.currentForm&&(!(d in c||!b.objectLength(a(this).rules()))&&(c[d]=!0,!0))})},clean:function(b){return a(b)[0]},errors:function(){var b=this.settings.errorClass.split(" ").join(".");return a(this.settings.errorElement+"."+b,this.errorContext)},resetInternals:function(){this.successList=[],this.errorList=[],this.errorMap={},this.toShow=a([]),this.toHide=a([])},reset:function(){this.resetInternals(),this.currentElements=a([])},prepareForm:function(){this.reset(),this.toHide=this.errors().add(this.containers)},prepareElement:function(a){this.reset(),this.toHide=this.errorsFor(a)},elementValue:function(b){var c,d,e=a(b),f=b.type,g="undefined"!=typeof e.attr("contenteditable")&&"false"!==e.attr("contenteditable");return"radio"===f||"checkbox"===f?this.findByName(b.name).filter(":checked").val():"number"===f&&"undefined"!=typeof b.validity?b.validity.badInput?"NaN":e.val():(c=g?e.text():e.val(),"file"===f?"C:\\fakepath\\"===c.substr(0,12)?c.substr(12):(d=c.lastIndexOf("/"),d>=0?c.substr(d+1):(d=c.lastIndexOf("\\"),d>=0?c.substr(d+1):c)):"string"==typeof c?c.replace(/\r/g,""):c)},check:function(b){b=this.validationTargetFor(this.clean(b));var c,d,e,f,g=a(b).rules(),h=a.map(g,function(a,b){return b}).length,i=!1,j=this.elementValue(b);this.abortRequest(b),"function"==typeof g.normalizer?f=g.normalizer:"function"==typeof this.settings.normalizer&&(f=this.settings.normalizer),f&&(j=f.call(b,j),delete g.normalizer);for(d in g){e={method:d,parameters:g[d]};try{if(c=a.validator.methods[d].call(this,j,b,e.parameters),"dependency-mismatch"===c&&1===h){i=!0;continue}if(i=!1,"pending"===c)return void(this.toHide=this.toHide.not(this.errorsFor(b)));if(!c)return this.formatAndAdd(b,e),!1}catch(k){throw this.settings.debug&&window.console&&console.log("Exception occurred when checking element "+b.id+", check the '"+e.method+"' method.",k),k instanceof TypeError&&(k.message+=".  Exception occurred when checking element "+b.id+", check the '"+e.method+"' method."),k}}if(!i)return this.objectLength(g)&&this.successList.push(b),!0},customDataMessage:function(b,c){return a(b).data("msg"+c.charAt(0).toUpperCase()+c.substring(1).toLowerCase())||a(b).data("msg")},customMessage:function(a,b){var c=this.settings.messages[a];return c&&(c.constructor===String?c:c[b])},findDefined:function(){for(var a=0;a<arguments.length;a++)if(void 0!==arguments[a])return arguments[a]},defaultMessage:function(b,c){"string"==typeof c&&(c={method:c});var d=this.findDefined(this.customMessage(b.name,c.method),this.customDataMessage(b,c.method),!this.settings.ignoreTitle&&b.title||void 0,a.validator.messages[c.method],"<strong>Warning: No message defined for "+b.name+"</strong>"),e=/\$?\{(\d+)\}/g;return"function"==typeof d?d=d.call(this,c.parameters,b):e.test(d)&&(d=a.validator.format(d.replace(e,"{$1}"),c.parameters)),d},formatAndAdd:function(a,b){var c=this.defaultMessage(a,b);this.errorList.push({message:c,element:a,method:b.method}),this.errorMap[a.name]=c,this.submitted[a.name]=c},addWrapper:function(a){return this.settings.wrapper&&(a=a.add(a.parent(this.settings.wrapper))),a},defaultShowErrors:function(){var a,b,c;for(a=0;this.errorList[a];a++)c=this.errorList[a],this.settings.highlight&&this.settings.highlight.call(this,c.element,this.settings.errorClass,this.settings.validClass),this.showLabel(c.element,c.message);if(this.errorList.length&&(this.toShow=this.toShow.add(this.containers)),this.settings.success)for(a=0;this.successList[a];a++)this.showLabel(this.successList[a]);if(this.settings.unhighlight)for(a=0,b=this.validElements();b[a];a++)this.settings.unhighlight.call(this,b[a],this.settings.errorClass,this.settings.validClass);this.toHide=this.toHide.not(this.toShow),this.hideErrors(),this.addWrapper(this.toShow).show()},validElements:function(){return this.currentElements.not(this.invalidElements())},invalidElements:function(){return a(this.errorList).map(function(){return this.element})},showLabel:function(b,c){var d,e,f,g,h=this.errorsFor(b),i=this.idOrName(b),j=a(b).attr("aria-describedby");h.length?(h.removeClass(this.settings.validClass).addClass(this.settings.errorClass),this.settings&&this.settings.escapeHtml?h.text(c||""):h.html(c||"")):(h=a("<"+this.settings.errorElement+">").attr("id",i+"-error").addClass(this.settings.errorClass),this.settings&&this.settings.escapeHtml?h.text(c||""):h.html(c||""),d=h,this.settings.wrapper&&(d=h.hide().show().wrap("<"+this.settings.wrapper+"/>").parent()),this.labelContainer.length?this.labelContainer.append(d):this.settings.errorPlacement?this.settings.errorPlacement.call(this,d,a(b)):d.insertAfter(b),h.is("label")?h.attr("for",i):0===h.parents("label[for='"+this.escapeCssMeta(i)+"']").length&&(f=h.attr("id"),j?j.match(new RegExp("\\b"+this.escapeCssMeta(f)+"\\b"))||(j+=" "+f):j=f,a(b).attr("aria-describedby",j),e=this.groups[b.name],e&&(g=this,a.each(g.groups,function(b,c){c===e&&a("[name='"+g.escapeCssMeta(b)+"']",g.currentForm).attr("aria-describedby",h.attr("id"))})))),!c&&this.settings.success&&(h.text(""),"string"==typeof this.settings.success?h.addClass(this.settings.success):this.settings.success(h,b)),this.toShow=this.toShow.add(h)},errorsFor:function(b){var c=this.escapeCssMeta(this.idOrName(b)),d=a(b).attr("aria-describedby"),e="label[for='"+c+"'], label[for='"+c+"'] *";return d&&(e=e+", #"+this.escapeCssMeta(d).replace(/\s+/g,", #")),this.errors().filter(e)},escapeCssMeta:function(a){return void 0===a?"":a.replace(/([\\!"#$%&'()*+,./:;<=>?@\[\]^`{|}~])/g,"\\$1")},idOrName:function(a){return this.groups[a.name]||(this.checkable(a)?a.name:a.id||a.name)},validationTargetFor:function(b){return this.checkable(b)&&(b=this.findByName(b.name)),a(b).not(this.settings.ignore)[0]},checkable:function(a){return/radio|checkbox/i.test(a.type)},findByName:function(b){return a(this.currentForm).find("[name='"+this.escapeCssMeta(b)+"']")},getLength:function(b,c){switch(c.nodeName.toLowerCase()){case"select":return a("option:selected",c).length;case"input":if(this.checkable(c))return this.findByName(c.name).filter(":checked").length}return b.length},depend:function(a,b){return!this.dependTypes[typeof a]||this.dependTypes[typeof a](a,b)},dependTypes:{"boolean":function(a){return a},string:function(b,c){return!!a(b,c.form).length},"function":function(a,b){return a(b)}},optional:function(b){var c=this.elementValue(b);return!a.validator.methods.required.call(this,c,b)&&"dependency-mismatch"},elementAjaxPort:function(a){return"validate"+a.name},startRequest:function(b){this.pending[b.name]||(this.pendingRequest++,a(b).addClass(this.settings.pendingClass),this.pending[b.name]=!0)},stopRequest:function(b,c){this.pendingRequest--,this.pendingRequest<0&&(this.pendingRequest=0),delete this.pending[b.name],a(b).removeClass(this.settings.pendingClass),c&&0===this.pendingRequest&&this.formSubmitted&&this.form()&&0===this.pendingRequest?(a(this.currentForm).trigger("submit"),this.submitButton&&a("input:hidden[name='"+this.submitButton.name+"']",this.currentForm).remove(),this.formSubmitted=!1):!c&&0===this.pendingRequest&&this.formSubmitted&&(a(this.currentForm).triggerHandler("invalid-form",[this]),this.formSubmitted=!1)},abortRequest:function(b){var c;this.pending[b.name]&&(c=this.elementAjaxPort(b),a.ajaxAbort(c),this.pendingRequest--,this.pendingRequest<0&&(this.pendingRequest=0),delete this.pending[b.name],a(b).removeClass(this.settings.pendingClass))},previousValue:function(b,c){return c="string"==typeof c&&c||"remote",a.data(b,"previousValue")||a.data(b,"previousValue",{old:null,valid:!0,message:this.defaultMessage(b,{method:c})})},destroy:function(){this.resetForm(),a(this.currentForm).off(".validate").removeData("validator").find(".validate-equalTo-blur").off(".validate-equalTo").removeClass("validate-equalTo-blur").find(".validate-lessThan-blur").off(".validate-lessThan").removeClass("validate-lessThan-blur").find(".validate-lessThanEqual-blur").off(".validate-lessThanEqual").removeClass("validate-lessThanEqual-blur").find(".validate-greaterThanEqual-blur").off(".validate-greaterThanEqual").removeClass("validate-greaterThanEqual-blur").find(".validate-greaterThan-blur").off(".validate-greaterThan").removeClass("validate-greaterThan-blur")}},classRuleSettings:{required:{required:!0},email:{email:!0},url:{url:!0},date:{date:!0},dateISO:{dateISO:!0},number:{number:!0},digits:{digits:!0},creditcard:{creditcard:!0}},addClassRules:function(b,c){b.constructor===String?this.classRuleSettings[b]=c:a.extend(this.classRuleSettings,b)},classRules:function(b){var c={},d=a(b).attr("class");return d&&a.each(d.split(" "),function(){this in a.validator.classRuleSettings&&a.extend(c,a.validator.classRuleSettings[this])}),c},normalizeAttributeRule:function(a,b,c,d){/min|max|step/.test(c)&&(null===b||/number|range|text/.test(b))&&(d=Number(d),isNaN(d)&&(d=void 0)),d||0===d?a[c]=d:b===c&&"range"!==b&&(a["date"===b?"dateISO":c]=!0)},attributeRules:function(b){var c,d,e={},f=a(b),g=b.getAttribute("type");for(c in a.validator.methods)"required"===c?(d=b.getAttribute(c),""===d&&(d=!0),d=!!d):d=f.attr(c),this.normalizeAttributeRule(e,g,c,d);return e.maxlength&&/-1|2147483647|524288/.test(e.maxlength)&&delete e.maxlength,e},dataRules:function(b){var c,d,e={},f=a(b),g=b.getAttribute("type");for(c in a.validator.methods)d=f.data("rule"+c.charAt(0).toUpperCase()+c.substring(1).toLowerCase()),""===d&&(d=!0),this.normalizeAttributeRule(e,g,c,d);return e},staticRules:function(b){var c={},d=a.data(b.form,"validator");return d.settings.rules&&(c=a.validator.normalizeRule(d.settings.rules[b.name])||{}),c},normalizeRules:function(b,c){return a.each(b,function(d,e){if(e===!1)return void delete b[d];if(e.param||e.depends){var f=!0;switch(typeof e.depends){case"string":f=!!a(e.depends,c.form).length;break;case"function":f=e.depends.call(c,c)}f?b[d]=void 0===e.param||e.param:(a.data(c.form,"validator").resetElements(a(c)),delete b[d])}}),a.each(b,function(a,d){b[a]="function"==typeof d&&"normalizer"!==a?d(c):d}),a.each(["minlength","maxlength"],function(){b[this]&&(b[this]=Number(b[this]))}),a.each(["rangelength","range"],function(){var a;b[this]&&(Array.isArray(b[this])?b[this]=[Number(b[this][0]),Number(b[this][1])]:"string"==typeof b[this]&&(a=b[this].replace(/[\[\]]/g,"").split(/[\s,]+/),b[this]=[Number(a[0]),Number(a[1])]))}),a.validator.autoCreateRanges&&(null!=b.min&&null!=b.max&&(b.range=[b.min,b.max],delete b.min,delete b.max),null!=b.minlength&&null!=b.maxlength&&(b.rangelength=[b.minlength,b.maxlength],delete b.minlength,delete b.maxlength)),b},normalizeRule:function(b){if("string"==typeof b){var c={};a.each(b.split(/\s/),function(){c[this]=!0}),b=c}return b},addMethod:function(b,c,d){a.validator.methods[b]=c,a.validator.messages[b]=void 0!==d?d:a.validator.messages[b],c.length<3&&a.validator.addClassRules(b,a.validator.normalizeRule(b))},methods:{required:function(b,c,d){if(!this.depend(d,c))return"dependency-mismatch";if("select"===c.nodeName.toLowerCase()){var e=a(c).val();return e&&e.length>0}return this.checkable(c)?this.getLength(b,c)>0:void 0!==b&&null!==b&&b.length>0},email:function(a,b){return this.optional(b)||/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/.test(a)},url:function(a,b){return this.optional(b)||/^(?:(?:(?:https?|ftp):)?\/\/)(?:(?:[^\]\[?\/<~#`!@$^&*()+=}|:";',>{ ]|%[0-9A-Fa-f]{2})+(?::(?:[^\]\[?\/<~#`!@$^&*()+=}|:";',>{ ]|%[0-9A-Fa-f]{2})*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$/i.test(a)},date:function(){var a=!1;return function(b,c){return a||(a=!0,this.settings.debug&&window.console&&console.warn("The `date` method is deprecated and will be removed in version '2.0.0'.\nPlease don't use it, since it relies on the Date constructor, which\nbehaves very differently across browsers and locales. Use `dateISO`\ninstead or one of the locale specific methods in `localizations/`\nand `additional-methods.js`.")),this.optional(c)||!/Invalid|NaN/.test(new Date(b).toString())}}(),dateISO:function(a,b){return this.optional(b)||/^\d{4}[\/\-](0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])$/.test(a)},number:function(a,b){return this.optional(b)||/^(?:-?\d+|-?\d{1,3}(?:,\d{3})+)?(?:\.\d+)?$/.test(a)},digits:function(a,b){return this.optional(b)||/^\d+$/.test(a)},minlength:function(a,b,c){var d=Array.isArray(a)?a.length:this.getLength(a,b);return this.optional(b)||d>=c},maxlength:function(a,b,c){var d=Array.isArray(a)?a.length:this.getLength(a,b);return this.optional(b)||d<=c},rangelength:function(a,b,c){var d=Array.isArray(a)?a.length:this.getLength(a,b);return this.optional(b)||d>=c[0]&&d<=c[1]},min:function(a,b,c){return this.optional(b)||a>=c},max:function(a,b,c){return this.optional(b)||a<=c},range:function(a,b,c){return this.optional(b)||a>=c[0]&&a<=c[1]},step:function(b,c,d){var e,f=a(c).attr("type"),g="Step attribute on input type "+f+" is not supported.",h=["text","number","range"],i=new RegExp("\\b"+f+"\\b"),j=f&&!i.test(h.join()),k=function(a){var b=(""+a).match(/(?:\.(\d+))?$/);return b&&b[1]?b[1].length:0},l=function(a){return Math.round(a*Math.pow(10,e))},m=!0;if(j)throw new Error(g);return e=k(d),(k(b)>e||l(b)%l(d)!==0)&&(m=!1),this.optional(c)||m},equalTo:function(b,c,d){var e=a(d);return this.settings.onfocusout&&e.not(".validate-equalTo-blur").length&&e.addClass("validate-equalTo-blur").on("blur.validate-equalTo",function(){a(c).valid()}),b===e.val()},remote:function(b,c,d,e){if(this.optional(c))return"dependency-mismatch";e="string"==typeof e&&e||"remote";var f,g,h,i=this.previousValue(c,e);return this.settings.messages[c.name]||(this.settings.messages[c.name]={}),i.originalMessage=i.originalMessage||this.settings.messages[c.name][e],this.settings.messages[c.name][e]=i.message,d="string"==typeof d&&{url:d}||d,h=a.param(a.extend({data:b},d.data)),null!==i.valid&&i.old===h?i.valid:(i.old=h,i.valid=null,f=this,this.startRequest(c),g={},g[c.name]=b,a.ajax(a.extend(!0,{mode:"abort",port:this.elementAjaxPort(c),dataType:"json",data:g,context:f.currentForm,success:function(a){var d,g,h,j=a===!0||"true"===a;f.settings.messages[c.name][e]=i.originalMessage,j?(h=f.formSubmitted,f.toHide=f.errorsFor(c),f.formSubmitted=h,f.successList.push(c),f.invalid[c.name]=!1,f.showErrors()):(d={},g=a||f.defaultMessage(c,{method:e,parameters:b}),d[c.name]=i.message=g,f.invalid[c.name]=!0,f.showErrors(d)),i.valid=j,f.stopRequest(c,j)}},d)),"pending")}}});var c,d={};return a.ajaxPrefilter?a.ajaxPrefilter(function(b,c,e){var f=b.port;"abort"===b.mode&&(a.ajaxAbort(f),d[f]=e)}):(c=a.ajax,a.ajax=function(b){var e=("mode"in b?b:a.ajaxSettings).mode,f=("port"in b?b:a.ajaxSettings).port;return"abort"===e?(a.ajaxAbort(f),d[f]=c.apply(this,arguments),d[f]):c.apply(this,arguments)}),a.ajaxAbort=function(a){d[a]&&(d[a].abort(),delete d[a])},a});;


(function($){var escapeable=/["\\\x00-\x1f\x7f-\x9f]/g,meta={'\b':'\\b','\t':'\\t','\n':'\\n','\f':'\\f','\r':'\\r','"':'\\"','\\':'\\\\'};$.toJSON=typeof JSON==='object'&&JSON.stringify?JSON.stringify:function(o){if(o===null){return'null';}
var type=typeof o;if(type==='undefined'){return undefined;}
if(type==='number'||type==='boolean'){return''+o;}
if(type==='string'){return $.quoteString(o);}
if(type==='object'){if(typeof o.toJSON==='function'){return $.toJSON(o.toJSON());}
if(o.constructor===Date){var month=o.getUTCMonth()+1,day=o.getUTCDate(),year=o.getUTCFullYear(),hours=o.getUTCHours(),minutes=o.getUTCMinutes(),seconds=o.getUTCSeconds(),milli=o.getUTCMilliseconds();if(month<10){month='0'+month;}
if(day<10){day='0'+day;}
if(hours<10){hours='0'+hours;}
if(minutes<10){minutes='0'+minutes;}
if(seconds<10){seconds='0'+seconds;}
if(milli<100){milli='0'+milli;}
if(milli<10){milli='0'+milli;}
return'"'+year+'-'+month+'-'+day+'T'+
hours+':'+minutes+':'+seconds+'.'+milli+'Z"';}
if(o.constructor===Array){var ret=[];for(var i=0;i<o.length;i++){ret.push($.toJSON(o[i])||'null');}
return'['+ret.join(',')+']';}
var name,val,pairs=[];for(var k in o){type=typeof k;if(type==='number'){name='"'+k+'"';}else if(type==='string'){name=$.quoteString(k);}else{continue;}
type=typeof o[k];if(type==='function'||type==='undefined'){continue;}
val=$.toJSON(o[k]);pairs.push(name+':'+val);}
return'{'+pairs.join(',')+'}';}};$.evalJSON=typeof JSON==='object'&&JSON.parse?JSON.parse:function(src){return eval('('+src+')');};$.secureEvalJSON=typeof JSON==='object'&&JSON.parse?JSON.parse:function(src){var filtered=src.replace(/\\["\\\/bfnrtu]/g,'@').replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,']').replace(/(?:^|:|,)(?:\s*\[)+/g,'');if(/^[\],:{}\s]*$/.test(filtered)){return eval('('+src+')');}else{throw new SyntaxError('Error parsing JSON, source is not valid.');}};$.quoteString=function(string){if(string.match(escapeable)){return'"'+string.replace(escapeable,function(a){var c=meta[a];if(typeof c==='string'){return c;}
c=a.charCodeAt();return'\\u00'+Math.floor(c/16).toString(16)+(c%16).toString(16);})+'"';}
return'"'+string+'"';};})(jQuery);;

/**
 * @version 0.5.0
 * @author Chen, Yi-Cyuan [emn178@gmail.com]
 * @copyright Chen, Yi-Cyuan 2014-2017
 * @license MIT
 */
!function(){"use strict";function t(t,h){h?(c[0]=c[16]=c[1]=c[2]=c[3]=c[4]=c[5]=c[6]=c[7]=c[8]=c[9]=c[10]=c[11]=c[12]=c[13]=c[14]=c[15]=0,this.blocks=c):this.blocks=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],t?(this.h0=3238371032,this.h1=914150663,this.h2=812702999,this.h3=4144912697,this.h4=4290775857,this.h5=1750603025,this.h6=1694076839,this.h7=3204075428):(this.h0=1779033703,this.h1=3144134277,this.h2=1013904242,this.h3=2773480762,this.h4=1359893119,this.h5=2600822924,this.h6=528734635,this.h7=1541459225),this.block=this.start=this.bytes=0,this.finalized=this.hashed=!1,this.first=!0,this.is224=t}var h="object"==typeof window?window:{},i=!h.JS_SHA256_NO_NODE_JS&&"object"==typeof process&&process.versions&&process.versions.node;i&&(h=global);var s=!h.JS_SHA256_NO_COMMON_JS&&"object"==typeof module&&module.exports,e="function"==typeof define&&define.amd,r="undefined"!=typeof ArrayBuffer,n="0123456789abcdef".split(""),o=[-2147483648,8388608,32768,128],a=[24,16,8,0],f=[1116352408,1899447441,3049323471,3921009573,961987163,1508970993,2453635748,2870763221,3624381080,310598401,607225278,1426881987,1925078388,2162078206,2614888103,3248222580,3835390401,4022224774,264347078,604807628,770255983,1249150122,1555081692,1996064986,2554220882,2821834349,2952996808,3210313671,3336571891,3584528711,113926993,338241895,666307205,773529912,1294757372,1396182291,1695183700,1986661051,2177026350,2456956037,2730485921,2820302411,3259730800,3345764771,3516065817,3600352804,4094571909,275423344,430227734,506948616,659060556,883997877,958139571,1322822218,1537002063,1747873779,1955562222,2024104815,2227730452,2361852424,2428436474,2756734187,3204031479,3329325298],u=["hex","array","digest","arrayBuffer"],c=[],p=function(h,i){return function(s){return new t(i,!0).update(s)[h]()}},d=function(h){var s=p("hex",h);i&&(s=y(s,h)),s.create=function(){return new t(h)},s.update=function(t){return s.create().update(t)};for(var e=0;e<u.length;++e){var r=u[e];s[r]=p(r,h)}return s},y=function(t,h){var i=require("crypto"),s=require("buffer").Buffer,e=h?"sha224":"sha256",n=function(h){if("string"==typeof h)return i.createHash(e).update(h,"utf8").digest("hex");if(r&&h instanceof ArrayBuffer)h=new Uint8Array(h);else if(void 0===h.length)return t(h);return i.createHash(e).update(new s(h)).digest("hex")};return n};t.prototype.update=function(t){if(!this.finalized){var i="string"!=typeof t;i&&r&&t instanceof h.ArrayBuffer&&(t=new Uint8Array(t));for(var s,e,n=0,o=t.length||0,f=this.blocks;o>n;){if(this.hashed&&(this.hashed=!1,f[0]=this.block,f[16]=f[1]=f[2]=f[3]=f[4]=f[5]=f[6]=f[7]=f[8]=f[9]=f[10]=f[11]=f[12]=f[13]=f[14]=f[15]=0),i)for(e=this.start;o>n&&64>e;++n)f[e>>2]|=t[n]<<a[3&e++];else for(e=this.start;o>n&&64>e;++n)s=t.charCodeAt(n),128>s?f[e>>2]|=s<<a[3&e++]:2048>s?(f[e>>2]|=(192|s>>6)<<a[3&e++],f[e>>2]|=(128|63&s)<<a[3&e++]):55296>s||s>=57344?(f[e>>2]|=(224|s>>12)<<a[3&e++],f[e>>2]|=(128|s>>6&63)<<a[3&e++],f[e>>2]|=(128|63&s)<<a[3&e++]):(s=65536+((1023&s)<<10|1023&t.charCodeAt(++n)),f[e>>2]|=(240|s>>18)<<a[3&e++],f[e>>2]|=(128|s>>12&63)<<a[3&e++],f[e>>2]|=(128|s>>6&63)<<a[3&e++],f[e>>2]|=(128|63&s)<<a[3&e++]);this.lastByteIndex=e,this.bytes+=e-this.start,e>=64?(this.block=f[16],this.start=e-64,this.hash(),this.hashed=!0):this.start=e}return this}},t.prototype.finalize=function(){if(!this.finalized){this.finalized=!0;var t=this.blocks,h=this.lastByteIndex;t[16]=this.block,t[h>>2]|=o[3&h],this.block=t[16],h>=56&&(this.hashed||this.hash(),t[0]=this.block,t[16]=t[1]=t[2]=t[3]=t[4]=t[5]=t[6]=t[7]=t[8]=t[9]=t[10]=t[11]=t[12]=t[13]=t[14]=t[15]=0),t[15]=this.bytes<<3,this.hash()}},t.prototype.hash=function(){var t,h,i,s,e,r,n,o,a,u,c,p=this.h0,d=this.h1,y=this.h2,l=this.h3,b=this.h4,v=this.h5,g=this.h6,w=this.h7,k=this.blocks;for(t=16;64>t;++t)e=k[t-15],h=(e>>>7|e<<25)^(e>>>18|e<<14)^e>>>3,e=k[t-2],i=(e>>>17|e<<15)^(e>>>19|e<<13)^e>>>10,k[t]=k[t-16]+h+k[t-7]+i<<0;for(c=d&y,t=0;64>t;t+=4)this.first?(this.is224?(o=300032,e=k[0]-1413257819,w=e-150054599<<0,l=e+24177077<<0):(o=704751109,e=k[0]-210244248,w=e-1521486534<<0,l=e+143694565<<0),this.first=!1):(h=(p>>>2|p<<30)^(p>>>13|p<<19)^(p>>>22|p<<10),i=(b>>>6|b<<26)^(b>>>11|b<<21)^(b>>>25|b<<7),o=p&d,s=o^p&y^c,n=b&v^~b&g,e=w+i+n+f[t]+k[t],r=h+s,w=l+e<<0,l=e+r<<0),h=(l>>>2|l<<30)^(l>>>13|l<<19)^(l>>>22|l<<10),i=(w>>>6|w<<26)^(w>>>11|w<<21)^(w>>>25|w<<7),a=l&p,s=a^l&d^o,n=w&b^~w&v,e=g+i+n+f[t+1]+k[t+1],r=h+s,g=y+e<<0,y=e+r<<0,h=(y>>>2|y<<30)^(y>>>13|y<<19)^(y>>>22|y<<10),i=(g>>>6|g<<26)^(g>>>11|g<<21)^(g>>>25|g<<7),u=y&l,s=u^y&p^a,n=g&w^~g&b,e=v+i+n+f[t+2]+k[t+2],r=h+s,v=d+e<<0,d=e+r<<0,h=(d>>>2|d<<30)^(d>>>13|d<<19)^(d>>>22|d<<10),i=(v>>>6|v<<26)^(v>>>11|v<<21)^(v>>>25|v<<7),c=d&y,s=c^d&l^u,n=v&g^~v&w,e=b+i+n+f[t+3]+k[t+3],r=h+s,b=p+e<<0,p=e+r<<0;this.h0=this.h0+p<<0,this.h1=this.h1+d<<0,this.h2=this.h2+y<<0,this.h3=this.h3+l<<0,this.h4=this.h4+b<<0,this.h5=this.h5+v<<0,this.h6=this.h6+g<<0,this.h7=this.h7+w<<0},t.prototype.hex=function(){this.finalize();var t=this.h0,h=this.h1,i=this.h2,s=this.h3,e=this.h4,r=this.h5,o=this.h6,a=this.h7,f=n[t>>28&15]+n[t>>24&15]+n[t>>20&15]+n[t>>16&15]+n[t>>12&15]+n[t>>8&15]+n[t>>4&15]+n[15&t]+n[h>>28&15]+n[h>>24&15]+n[h>>20&15]+n[h>>16&15]+n[h>>12&15]+n[h>>8&15]+n[h>>4&15]+n[15&h]+n[i>>28&15]+n[i>>24&15]+n[i>>20&15]+n[i>>16&15]+n[i>>12&15]+n[i>>8&15]+n[i>>4&15]+n[15&i]+n[s>>28&15]+n[s>>24&15]+n[s>>20&15]+n[s>>16&15]+n[s>>12&15]+n[s>>8&15]+n[s>>4&15]+n[15&s]+n[e>>28&15]+n[e>>24&15]+n[e>>20&15]+n[e>>16&15]+n[e>>12&15]+n[e>>8&15]+n[e>>4&15]+n[15&e]+n[r>>28&15]+n[r>>24&15]+n[r>>20&15]+n[r>>16&15]+n[r>>12&15]+n[r>>8&15]+n[r>>4&15]+n[15&r]+n[o>>28&15]+n[o>>24&15]+n[o>>20&15]+n[o>>16&15]+n[o>>12&15]+n[o>>8&15]+n[o>>4&15]+n[15&o];return this.is224||(f+=n[a>>28&15]+n[a>>24&15]+n[a>>20&15]+n[a>>16&15]+n[a>>12&15]+n[a>>8&15]+n[a>>4&15]+n[15&a]),f},t.prototype.toString=t.prototype.hex,t.prototype.digest=function(){this.finalize();var t=this.h0,h=this.h1,i=this.h2,s=this.h3,e=this.h4,r=this.h5,n=this.h6,o=this.h7,a=[t>>24&255,t>>16&255,t>>8&255,255&t,h>>24&255,h>>16&255,h>>8&255,255&h,i>>24&255,i>>16&255,i>>8&255,255&i,s>>24&255,s>>16&255,s>>8&255,255&s,e>>24&255,e>>16&255,e>>8&255,255&e,r>>24&255,r>>16&255,r>>8&255,255&r,n>>24&255,n>>16&255,n>>8&255,255&n];return this.is224||a.push(o>>24&255,o>>16&255,o>>8&255,255&o),a},t.prototype.array=t.prototype.digest,t.prototype.arrayBuffer=function(){this.finalize();var t=new ArrayBuffer(this.is224?28:32),h=new DataView(t);return h.setUint32(0,this.h0),h.setUint32(4,this.h1),h.setUint32(8,this.h2),h.setUint32(12,this.h3),h.setUint32(16,this.h4),h.setUint32(20,this.h5),h.setUint32(24,this.h6),this.is224||h.setUint32(28,this.h7),t};var l=d();l.sha256=l,l.sha224=d(!0),s?module.exports=l:(h.sha256=l.sha256,h.sha224=l.sha224,e&&define(function(){return l}))}();;

/**
 * AJAX File Upload
 * 
 * Copyright (c) 2010-2013 David Hancock 
 *
 * Thanks to Steven Barnett for his generous contributions
 *
 * Licensed under the MIT license 
 */

;(function($) {
	$.fn.AjaxFileUpload = function(options) {
		
		var defaults = {
			action:     "upload.php",
			onChange:   function(filename) {},
			onSubmit:   function(filename) {},
			onComplete: function(filename, response) {}
		},
		settings = $.extend({}, defaults, options),
		randomId = (function() {
			var id = 0;
			return function () {
				return "_AjaxFileUpload" + id++;
			};
		})();
		
		return this.each(function() {
			var $this = $(this);
			if ($this.is("input") && $this.attr("type") === "file") {
				$this.unbind("begin_uploading_file");
				$this.bind("begin_uploading_file", onChange);
			}
		});
		
		function onChange(e) {
			var $element = $(e.target),
				id       = $element.attr('id'),
				$clone   = $element.removeAttr('id').clone().attr('id', id).AjaxFileUpload(options),
				filename = $element.val().replace(/.*(\/|\\)/, ""),
				iframe   = createIframe(),
				form     = createForm(iframe);

			// We append a clone since the original input will be destroyed
			$clone.insertBefore($element);

			settings.onChange.call($clone[0], filename);

			iframe.bind("load", {element: $clone, form: form, filename: filename}, onComplete);
			
			form.append($element).bind("submit", {element: $clone, iframe: iframe, filename: filename}, onSubmit).submit();
		}
		
		function onSubmit(e) {
			var data = settings.onSubmit.call(e.data.element, e.data.filename);

			// If false cancel the submission
			if (data === false) {
				// Remove the temporary form and iframe
				$(e.target).remove();
				e.data.iframe.remove();
				return false;
			} else {
				// Else, append additional inputs
				for (var variable in data) {
					$("<input />")
						.attr("type", "hidden")
						.attr("name", variable)
						.val(data[variable])
						.appendTo(e.target);
				}
			}
		}
		
		function onComplete (e) {
			var $iframe  = $(e.target),
				doc      = ($iframe[0].contentWindow || $iframe[0].contentDocument).document,
				response = doc.body.innerHTML;

			if (response) {
				response = $.parseJSON(response);
			} else {
				response = {};
			}

			settings.onComplete.call(e.data.element, e.data.filename, response);
			
			// Remove the temporary form and iframe
			e.data.form.remove();
			$iframe.remove();
		}

		function createIframe() {
			var id = randomId();

			// The iframe must be appended as a string otherwise IE7 will pop up the response in a new window
			// http://stackoverflow.com/a/6222471/268669
			var iframStr = '<iframe src="javascript:false;" name="' + id + '" id="' + id + '" style="display: none;"></iframe>';
			// Chrome 83.x.x.x 浏览器需要特殊处理。
			if(browserCheck().chrome && browserCheck().chrome >= 83){
				iframStr = '<iframe src="about:blank;" name="' + id + '" id="' + id + '" style="display: none;"></iframe>';
			}
			$("body").append(iframStr);

			return $('#' + id);
			function browserCheck() {
				var ua = navigator.userAgent;
				var ret = {},
					webkit = ua.match(/WebKit\/([\d.]+)/),
					chrome = ua.match(/Chrome\/([\d.]+)/) || ua.match(/CriOS\/([\d.]+)/);

				webkit && (ret.webkit = parseFloat(webkit[1]));
				chrome && (ret.chrome = parseFloat(chrome[1]));
			return ret;
			}
		}
		
		function createForm(iframe) {
			return $("<form />")
				.attr({
					method: "post",
					action: settings.action,
					enctype: "multipart/form-data",
					target: iframe[0].name
				})
				.hide()
				.appendTo("body");
		}
	};
})(jQuery);
;

/*! svg.js v2.7.1 MIT*/;!function(t,e){"function"==typeof define&&define.amd?define(function(){return e(t,t.document)}):"object"==typeof exports?module.exports=t.document?e(t,t.document):function(t){return e(t,t.document)}:t.SVG=e(t,t.document)}("undefined"!=typeof window?window:this,function(t,e){function i(t,e,i,n){return i+n.replace(b.regex.dots," .")}function n(t){for(var e=t.slice(0),i=e.length;i--;)Array.isArray(e[i])&&(e[i]=n(e[i]));return e}function r(t,e){return t instanceof e}function s(t,e){return(t.matches||t.matchesSelector||t.msMatchesSelector||t.mozMatchesSelector||t.webkitMatchesSelector||t.oMatchesSelector).call(t,e)}function o(t){return t.toLowerCase().replace(/-(.)/g,function(t,e){return e.toUpperCase()})}function a(t){return t.charAt(0).toUpperCase()+t.slice(1)}function h(t){return 4==t.length?["#",t.substring(1,2),t.substring(1,2),t.substring(2,3),t.substring(2,3),t.substring(3,4),t.substring(3,4)].join(""):t}function u(t){var e=t.toString(16);return 1==e.length?"0"+e:e}function l(t,e,i){if(null==e||null==i){var n=t.bbox();null==e?e=n.width/n.height*i:null==i&&(i=n.height/n.width*e)}return{width:e,height:i}}function c(t,e,i){return{x:e*t.a+i*t.c+0,y:e*t.b+i*t.d+0}}function f(t){return{a:t[0],b:t[1],c:t[2],d:t[3],e:t[4],f:t[5]}}function d(t){return t instanceof b.Matrix||(t=new b.Matrix(t)),t}function p(t,e){t.cx=null==t.cx?e.bbox().cx:t.cx,t.cy=null==t.cy?e.bbox().cy:t.cy}function m(t){for(var e=0,i=t.length,n="";e<i;e++)n+=t[e][0],null!=t[e][1]&&(n+=t[e][1],null!=t[e][2]&&(n+=" ",n+=t[e][2],null!=t[e][3]&&(n+=" ",n+=t[e][3],n+=" ",n+=t[e][4],null!=t[e][5]&&(n+=" ",n+=t[e][5],n+=" ",n+=t[e][6],null!=t[e][7]&&(n+=" ",n+=t[e][7])))));return n+" "}function x(e){for(var i=e.childNodes.length-1;i>=0;i--)e.childNodes[i]instanceof t.SVGElement&&x(e.childNodes[i]);return b.adopt(e).id(b.eid(e.nodeName))}function y(t){return null==t.x&&(t.x=0,t.y=0,t.width=0,t.height=0),t.w=t.width,t.h=t.height,t.x2=t.x+t.width,t.y2=t.y+t.height,t.cx=t.x+t.width/2,t.cy=t.y+t.height/2,t}function v(t){var e=(t||"").toString().match(b.regex.reference);if(e)return e[1]}function g(t){return Math.abs(t)>1e-37?t:0}var w=void 0!==this?this:t,b=w.SVG=function(t){if(b.supported)return t=new b.Doc(t),b.parser.draw||b.prepare(),t};if(b.ns="http://www.w3.org/2000/svg",b.xmlns="http://www.w3.org/2000/xmlns/",b.xlink="http://www.w3.org/1999/xlink",b.svgjs="http://svgjs.com/svgjs",b.supported=function(){return!!e.createElementNS&&!!e.createElementNS(b.ns,"svg").createSVGRect}(),!b.supported)return!1;b.did=1e3,b.eid=function(t){return"Svgjs"+a(t)+b.did++},b.create=function(t){var i=e.createElementNS(this.ns,t);return i.setAttribute("id",this.eid(t)),i},b.extend=function(){var t,e,i,n;for(t=[].slice.call(arguments),e=t.pop(),n=t.length-1;n>=0;n--)if(t[n])for(i in e)t[n].prototype[i]=e[i];b.Set&&b.Set.inherit&&b.Set.inherit()},b.invent=function(t){var e="function"==typeof t.create?t.create:function(){this.constructor.call(this,b.create(t.create))};return t.inherit&&(e.prototype=new t.inherit),t.extend&&b.extend(e,t.extend),t.construct&&b.extend(t.parent||b.Container,t.construct),e},b.adopt=function(e){if(!e)return null;if(e.instance)return e.instance;var i;return i="svg"==e.nodeName?e.parentNode instanceof t.SVGElement?new b.Nested:new b.Doc:"linearGradient"==e.nodeName?new b.Gradient("linear"):"radialGradient"==e.nodeName?new b.Gradient("radial"):b[a(e.nodeName)]?new(b[a(e.nodeName)]):new b.Element(e),i.type=e.nodeName,i.node=e,e.instance=i,i instanceof b.Doc&&i.namespace().defs(),i.setData(JSON.parse(e.getAttribute("svgjs:data"))||{}),i},b.prepare=function(){var t=e.getElementsByTagName("body")[0],i=(t?new b.Doc(t):b.adopt(e.documentElement).nested()).size(2,0);b.parser={body:t||e.documentElement,draw:i.style("opacity:0;position:absolute;left:-100%;top:-100%;overflow:hidden").attr("focusable","false").node,poly:i.polyline().node,path:i.path().node,native:b.create("svg")}},b.parser={native:b.create("svg")},e.addEventListener("DOMContentLoaded",function(){b.parser.draw||b.prepare()},!1),b.regex={numberAndUnit:/^([+-]?(\d+(\.\d*)?|\.\d+)(e[+-]?\d+)?)([a-z%]*)$/i,hex:/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i,rgb:/rgb\((\d+),(\d+),(\d+)\)/,reference:/#([a-z0-9\-_]+)/i,transforms:/\)\s*,?\s*/,whitespace:/\s/g,isHex:/^#[a-f0-9]{3,6}$/i,isRgb:/^rgb\(/,isCss:/[^:]+:[^;]+;?/,isBlank:/^(\s+)?$/,isNumber:/^[+-]?(\d+(\.\d*)?|\.\d+)(e[+-]?\d+)?$/i,isPercent:/^-?[\d\.]+%$/,isImage:/\.(jpg|jpeg|png|gif|svg)(\?[^=]+.*)?/i,delimiter:/[\s,]+/,hyphen:/([^e])\-/gi,pathLetters:/[MLHVCSQTAZ]/gi,isPathLetter:/[MLHVCSQTAZ]/i,numbersWithDots:/((\d?\.\d+(?:e[+-]?\d+)?)((?:\.\d+(?:e[+-]?\d+)?)+))+/gi,dots:/\./g},b.utils={map:function(t,e){var i,n=t.length,r=[];for(i=0;i<n;i++)r.push(e(t[i]));return r},filter:function(t,e){var i,n=t.length,r=[];for(i=0;i<n;i++)e(t[i])&&r.push(t[i]);return r},radians:function(t){return t%360*Math.PI/180},degrees:function(t){return 180*t/Math.PI%360},filterSVGElements:function(e){return this.filter(e,function(e){return e instanceof t.SVGElement})}},b.defaults={attrs:{"fill-opacity":1,"stroke-opacity":1,"stroke-width":0,"stroke-linejoin":"miter","stroke-linecap":"butt",fill:"#000000",stroke:"#000000",opacity:1,x:0,y:0,cx:0,cy:0,width:0,height:0,r:0,rx:0,ry:0,offset:0,"stop-opacity":1,"stop-color":"#000000","font-size":16,"font-family":"Helvetica, Arial, sans-serif","text-anchor":"start"}},b.Color=function(t){var e;this.r=0,this.g=0,this.b=0,t&&("string"==typeof t?b.regex.isRgb.test(t)?(e=b.regex.rgb.exec(t.replace(b.regex.whitespace,"")),this.r=parseInt(e[1]),this.g=parseInt(e[2]),this.b=parseInt(e[3])):b.regex.isHex.test(t)&&(e=b.regex.hex.exec(h(t)),this.r=parseInt(e[1],16),this.g=parseInt(e[2],16),this.b=parseInt(e[3],16)):"object"==typeof t&&(this.r=t.r,this.g=t.g,this.b=t.b))},b.extend(b.Color,{toString:function(){return this.toHex()},toHex:function(){return"#"+u(this.r)+u(this.g)+u(this.b)},toRgb:function(){return"rgb("+[this.r,this.g,this.b].join()+")"},brightness:function(){return this.r/255*.3+this.g/255*.59+this.b/255*.11},morph:function(t){return this.destination=new b.Color(t),this},at:function(t){return this.destination?(t=t<0?0:t>1?1:t,new b.Color({r:~~(this.r+(this.destination.r-this.r)*t),g:~~(this.g+(this.destination.g-this.g)*t),b:~~(this.b+(this.destination.b-this.b)*t)})):this}}),b.Color.test=function(t){return t+="",b.regex.isHex.test(t)||b.regex.isRgb.test(t)},b.Color.isRgb=function(t){return t&&"number"==typeof t.r&&"number"==typeof t.g&&"number"==typeof t.b},b.Color.isColor=function(t){return b.Color.isRgb(t)||b.Color.test(t)},b.Array=function(t,e){t=(t||[]).valueOf(),0==t.length&&e&&(t=e.valueOf()),this.value=this.parse(t)},b.extend(b.Array,{morph:function(t){if(this.destination=this.parse(t),this.value.length!=this.destination.length){for(var e=this.value[this.value.length-1],i=this.destination[this.destination.length-1];this.value.length>this.destination.length;)this.destination.push(i);for(;this.value.length<this.destination.length;)this.value.push(e)}return this},settle:function(){for(var t=0,e=this.value.length,i=[];t<e;t++)-1==i.indexOf(this.value[t])&&i.push(this.value[t]);return this.value=i},at:function(t){if(!this.destination)return this;for(var e=0,i=this.value.length,n=[];e<i;e++)n.push(this.value[e]+(this.destination[e]-this.value[e])*t);return new b.Array(n)},toString:function(){return this.value.join(" ")},valueOf:function(){return this.value},parse:function(t){return t=t.valueOf(),Array.isArray(t)?t:this.split(t)},split:function(t){return t.trim().split(b.regex.delimiter).map(parseFloat)},reverse:function(){return this.value.reverse(),this},clone:function(){var t=new this.constructor;return t.value=n(this.value),t}}),b.PointArray=function(t,e){b.Array.call(this,t,e||[[0,0]])},b.PointArray.prototype=new b.Array,b.PointArray.prototype.constructor=b.PointArray,b.extend(b.PointArray,{toString:function(){for(var t=0,e=this.value.length,i=[];t<e;t++)i.push(this.value[t].join(","));return i.join(" ")},toLine:function(){return{x1:this.value[0][0],y1:this.value[0][1],x2:this.value[1][0],y2:this.value[1][1]}},at:function(t){if(!this.destination)return this;for(var e=0,i=this.value.length,n=[];e<i;e++)n.push([this.value[e][0]+(this.destination[e][0]-this.value[e][0])*t,this.value[e][1]+(this.destination[e][1]-this.value[e][1])*t]);return new b.PointArray(n)},parse:function(t){var e=[];if(t=t.valueOf(),Array.isArray(t)){if(Array.isArray(t[0]))return t.map(function(t){return t.slice()});if(null!=t[0].x)return t.map(function(t){return[t.x,t.y]})}else t=t.trim().split(b.regex.delimiter).map(parseFloat);t.length%2!=0&&t.pop();for(var i=0,n=t.length;i<n;i+=2)e.push([t[i],t[i+1]]);return e},move:function(t,e){var i=this.bbox();if(t-=i.x,e-=i.y,!isNaN(t)&&!isNaN(e))for(var n=this.value.length-1;n>=0;n--)this.value[n]=[this.value[n][0]+t,this.value[n][1]+e];return this},size:function(t,e){var i,n=this.bbox();for(i=this.value.length-1;i>=0;i--)n.width&&(this.value[i][0]=(this.value[i][0]-n.x)*t/n.width+n.x),n.height&&(this.value[i][1]=(this.value[i][1]-n.y)*e/n.height+n.y);return this},bbox:function(){return b.parser.poly.setAttribute("points",this.toString()),b.parser.poly.getBBox()}});for(var C={M:function(t,e,i){return e.x=i.x=t[0],e.y=i.y=t[1],["M",e.x,e.y]},L:function(t,e){return e.x=t[0],e.y=t[1],["L",t[0],t[1]]},H:function(t,e){return e.x=t[0],["H",t[0]]},V:function(t,e){return e.y=t[0],["V",t[0]]},C:function(t,e){return e.x=t[4],e.y=t[5],["C",t[0],t[1],t[2],t[3],t[4],t[5]]},S:function(t,e){return e.x=t[2],e.y=t[3],["S",t[0],t[1],t[2],t[3]]},Q:function(t,e){return e.x=t[2],e.y=t[3],["Q",t[0],t[1],t[2],t[3]]},T:function(t,e){return e.x=t[0],e.y=t[1],["T",t[0],t[1]]},Z:function(t,e,i){return e.x=i.x,e.y=i.y,["Z"]},A:function(t,e){return e.x=t[5],e.y=t[6],["A",t[0],t[1],t[2],t[3],t[4],t[5],t[6]]}},N="mlhvqtcsaz".split(""),A=0,P=N.length;A<P;++A)C[N[A]]=function(t){return function(e,i,n){if("H"==t)e[0]=e[0]+i.x;else if("V"==t)e[0]=e[0]+i.y;else if("A"==t)e[5]=e[5]+i.x,e[6]=e[6]+i.y;else for(var r=0,s=e.length;r<s;++r)e[r]=e[r]+(r%2?i.y:i.x);return C[t](e,i,n)}}(N[A].toUpperCase());b.PathArray=function(t,e){b.Array.call(this,t,e||[["M",0,0]])},b.PathArray.prototype=new b.Array,b.PathArray.prototype.constructor=b.PathArray,b.extend(b.PathArray,{toString:function(){return m(this.value)},move:function(t,e){var i=this.bbox();if(t-=i.x,e-=i.y,!isNaN(t)&&!isNaN(e))for(var n,r=this.value.length-1;r>=0;r--)n=this.value[r][0],"M"==n||"L"==n||"T"==n?(this.value[r][1]+=t,this.value[r][2]+=e):"H"==n?this.value[r][1]+=t:"V"==n?this.value[r][1]+=e:"C"==n||"S"==n||"Q"==n?(this.value[r][1]+=t,this.value[r][2]+=e,this.value[r][3]+=t,this.value[r][4]+=e,"C"==n&&(this.value[r][5]+=t,this.value[r][6]+=e)):"A"==n&&(this.value[r][6]+=t,this.value[r][7]+=e);return this},size:function(t,e){var i,n,r=this.bbox();for(i=this.value.length-1;i>=0;i--)n=this.value[i][0],"M"==n||"L"==n||"T"==n?(this.value[i][1]=(this.value[i][1]-r.x)*t/r.width+r.x,this.value[i][2]=(this.value[i][2]-r.y)*e/r.height+r.y):"H"==n?this.value[i][1]=(this.value[i][1]-r.x)*t/r.width+r.x:"V"==n?this.value[i][1]=(this.value[i][1]-r.y)*e/r.height+r.y:"C"==n||"S"==n||"Q"==n?(this.value[i][1]=(this.value[i][1]-r.x)*t/r.width+r.x,this.value[i][2]=(this.value[i][2]-r.y)*e/r.height+r.y,this.value[i][3]=(this.value[i][3]-r.x)*t/r.width+r.x,this.value[i][4]=(this.value[i][4]-r.y)*e/r.height+r.y,"C"==n&&(this.value[i][5]=(this.value[i][5]-r.x)*t/r.width+r.x,this.value[i][6]=(this.value[i][6]-r.y)*e/r.height+r.y)):"A"==n&&(this.value[i][1]=this.value[i][1]*t/r.width,this.value[i][2]=this.value[i][2]*e/r.height,this.value[i][6]=(this.value[i][6]-r.x)*t/r.width+r.x,this.value[i][7]=(this.value[i][7]-r.y)*e/r.height+r.y);return this},equalCommands:function(t){var e,i,n;for(t=new b.PathArray(t),n=this.value.length===t.value.length,e=0,i=this.value.length;n&&e<i;e++)n=this.value[e][0]===t.value[e][0];return n},morph:function(t){return t=new b.PathArray(t),this.equalCommands(t)?this.destination=t:this.destination=null,this},at:function(t){if(!this.destination)return this;var e,i,n,r,s=this.value,o=this.destination.value,a=[],h=new b.PathArray;for(e=0,i=s.length;e<i;e++){for(a[e]=[s[e][0]],n=1,r=s[e].length;n<r;n++)a[e][n]=s[e][n]+(o[e][n]-s[e][n])*t;"A"===a[e][0]&&(a[e][4]=+(0!=a[e][4]),a[e][5]=+(0!=a[e][5]))}return h.value=a,h},parse:function(t){if(t instanceof b.PathArray)return t.valueOf();var e,n,r={M:2,L:2,H:1,V:1,C:6,S:4,Q:4,T:2,A:7,Z:0};t="string"==typeof t?t.replace(b.regex.numbersWithDots,i).replace(b.regex.pathLetters," $& ").replace(b.regex.hyphen,"$1 -").trim().split(b.regex.delimiter):t.reduce(function(t,e){return[].concat.call(t,e)},[]);var n=[],s=new b.Point,o=new b.Point,a=0,h=t.length;do{b.regex.isPathLetter.test(t[a])?(e=t[a],++a):"M"==e?e="L":"m"==e&&(e="l"),n.push(C[e].call(null,t.slice(a,a+=r[e.toUpperCase()]).map(parseFloat),s,o))}while(h>a);return n},bbox:function(){return b.parser.path.setAttribute("d",this.toString()),b.parser.path.getBBox()}}),b.Number=b.invent({create:function(t,e){this.value=0,this.unit=e||"","number"==typeof t?this.value=isNaN(t)?0:isFinite(t)?t:t<0?-3.4e38:3.4e38:"string"==typeof t?(e=t.match(b.regex.numberAndUnit))&&(this.value=parseFloat(e[1]),"%"==e[5]?this.value/=100:"s"==e[5]&&(this.value*=1e3),this.unit=e[5]):t instanceof b.Number&&(this.value=t.valueOf(),this.unit=t.unit)},extend:{toString:function(){return("%"==this.unit?~~(1e8*this.value)/1e6:"s"==this.unit?this.value/1e3:this.value)+this.unit},toJSON:function(){return this.toString()},valueOf:function(){return this.value},plus:function(t){return t=new b.Number(t),new b.Number(this+t,this.unit||t.unit)},minus:function(t){return t=new b.Number(t),new b.Number(this-t,this.unit||t.unit)},times:function(t){return t=new b.Number(t),new b.Number(this*t,this.unit||t.unit)},divide:function(t){return t=new b.Number(t),new b.Number(this/t,this.unit||t.unit)},to:function(t){var e=new b.Number(this);return"string"==typeof t&&(e.unit=t),e},morph:function(t){return this.destination=new b.Number(t),t.relative&&(this.destination.value+=this.value),this},at:function(t){return this.destination?new b.Number(this.destination).minus(this).times(t).plus(this):this}}}),b.Element=b.invent({create:function(t){this._stroke=b.defaults.attrs.stroke,this._event=null,this._events={},this.dom={},(this.node=t)&&(this.type=t.nodeName,this.node.instance=this,this._events=t._events||{},this._stroke=t.getAttribute("stroke")||this._stroke)},extend:{x:function(t){return this.attr("x",t)},y:function(t){return this.attr("y",t)},cx:function(t){return null==t?this.x()+this.width()/2:this.x(t-this.width()/2)},cy:function(t){return null==t?this.y()+this.height()/2:this.y(t-this.height()/2)},move:function(t,e){return this.x(t).y(e)},center:function(t,e){return this.cx(t).cy(e)},width:function(t){return this.attr("width",t)},height:function(t){return this.attr("height",t)},size:function(t,e){var i=l(this,t,e);return this.width(new b.Number(i.width)).height(new b.Number(i.height))},clone:function(t){this.writeDataToDom();var e=x(this.node.cloneNode(!0));return t?t.add(e):this.after(e),e},remove:function(){return this.parent()&&this.parent().removeElement(this),this},replace:function(t){return this.after(t).remove(),t},addTo:function(t){return t.put(this)},putIn:function(t){return t.add(this)},id:function(t){return this.attr("id",t)},inside:function(t,e){var i=this.bbox();return t>i.x&&e>i.y&&t<i.x+i.width&&e<i.y+i.height},show:function(){return this.style("display","")},hide:function(){return this.style("display","none")},visible:function(){return"none"!=this.style("display")},toString:function(){return this.attr("id")},classes:function(){var t=this.attr("class");return null==t?[]:t.trim().split(b.regex.delimiter)},hasClass:function(t){return-1!=this.classes().indexOf(t)},addClass:function(t){if(!this.hasClass(t)){var e=this.classes();e.push(t),this.attr("class",e.join(" "))}return this},removeClass:function(t){return this.hasClass(t)&&this.attr("class",this.classes().filter(function(e){return e!=t}).join(" ")),this},toggleClass:function(t){return this.hasClass(t)?this.removeClass(t):this.addClass(t)},reference:function(t){return b.get(this.attr(t))},parent:function(e){var i=this;if(!i.node.parentNode)return null;if(i=b.adopt(i.node.parentNode),!e)return i;for(;i&&i.node instanceof t.SVGElement;){if("string"==typeof e?i.matches(e):i instanceof e)return i;if(!i.node.parentNode||"#document"==i.node.parentNode.nodeName||"#document-fragment"==i.node.parentNode.nodeName)return null;i=b.adopt(i.node.parentNode)}},doc:function(){return this instanceof b.Doc?this:this.parent(b.Doc)},parents:function(t){var e=[],i=this;do{if(!(i=i.parent(t))||!i.node)break;e.push(i)}while(i.parent);return e},matches:function(t){return s(this.node,t)},native:function(){return this.node},svg:function(t){var i=e.createElement("svg");if(!(t&&this instanceof b.Parent))return i.appendChild(t=e.createElement("svg")),this.writeDataToDom(),t.appendChild(this.node.cloneNode(!0)),i.innerHTML.replace(/^<svg>/,"").replace(/<\/svg>$/,"");i.innerHTML="<svg>"+t.replace(/\n/,"").replace(/<([\w:-]+)([^<]+?)\/>/g,"<$1$2></$1>")+"</svg>";for(var n=0,r=i.firstChild.childNodes.length;n<r;n++)this.node.appendChild(i.firstChild.firstChild);return this},writeDataToDom:function(){if(this.each||this.lines){(this.each?this:this.lines()).each(function(){this.writeDataToDom()})}return this.node.removeAttribute("svgjs:data"),Object.keys(this.dom).length&&this.node.setAttribute("svgjs:data",JSON.stringify(this.dom)),this},setData:function(t){return this.dom=t,this},is:function(t){return r(this,t)}}}),b.easing={"-":function(t){return t},"<>":function(t){return-Math.cos(t*Math.PI)/2+.5},">":function(t){return Math.sin(t*Math.PI/2)},"<":function(t){return 1-Math.cos(t*Math.PI/2)}},b.morph=function(t){return function(e,i){return new b.MorphObj(e,i).at(t)}},b.Situation=b.invent({create:function(t){this.init=!1,this.reversed=!1,this.reversing=!1,this.duration=new b.Number(t.duration).valueOf(),this.delay=new b.Number(t.delay).valueOf(),this.start=+new Date+this.delay,this.finish=this.start+this.duration,this.ease=t.ease,this.loop=0,this.loops=!1,this.animations={},this.attrs={},this.styles={},this.transforms=[],this.once={}}}),b.FX=b.invent({create:function(t){this._target=t,this.situations=[],this.active=!1,this.situation=null,this.paused=!1,this.lastPos=0,this.pos=0,this.absPos=0,this._speed=1},extend:{animate:function(t,e,i){"object"==typeof t&&(e=t.ease,i=t.delay,t=t.duration);var n=new b.Situation({duration:t||1e3,delay:i||0,ease:b.easing[e||"-"]||e});return this.queue(n),this},delay:function(t){var e=new b.Situation({duration:t,delay:0,ease:b.easing["-"]});return this.queue(e)},target:function(t){return t&&t instanceof b.Element?(this._target=t,this):this._target},timeToAbsPos:function(t){return(t-this.situation.start)/(this.situation.duration/this._speed)},absPosToTime:function(t){return this.situation.duration/this._speed*t+this.situation.start},startAnimFrame:function(){this.stopAnimFrame(),this.animationFrame=t.requestAnimationFrame(function(){this.step()}.bind(this))},stopAnimFrame:function(){t.cancelAnimationFrame(this.animationFrame)},start:function(){return!this.active&&this.situation&&(this.active=!0,this.startCurrent()),this},startCurrent:function(){return this.situation.start=+new Date+this.situation.delay/this._speed,this.situation.finish=this.situation.start+this.situation.duration/this._speed,this.initAnimations().step()},queue:function(t){return("function"==typeof t||t instanceof b.Situation)&&this.situations.push(t),this.situation||(this.situation=this.situations.shift()),this},dequeue:function(){return this.stop(),this.situation=this.situations.shift(),this.situation&&(this.situation instanceof b.Situation?this.start():this.situation.call(this)),this},initAnimations:function(){var t,e,i,n=this.situation;if(n.init)return this;for(t in n.animations)for(i=this.target()[t](),Array.isArray(i)||(i=[i]),Array.isArray(n.animations[t])||(n.animations[t]=[n.animations[t]]),e=i.length;e--;)n.animations[t][e]instanceof b.Number&&(i[e]=new b.Number(i[e])),n.animations[t][e]=i[e].morph(n.animations[t][e]);for(t in n.attrs)n.attrs[t]=new b.MorphObj(this.target().attr(t),n.attrs[t]);for(t in n.styles)n.styles[t]=new b.MorphObj(this.target().style(t),n.styles[t]);return n.initialTransformation=this.target().matrixify(),n.init=!0,this},clearQueue:function(){return this.situations=[],this},clearCurrent:function(){return this.situation=null,this},stop:function(t,e){var i=this.active;return this.active=!1,e&&this.clearQueue(),t&&this.situation&&(!i&&this.startCurrent(),this.atEnd()),this.stopAnimFrame(),this.clearCurrent()},reset:function(){if(this.situation){var t=this.situation;this.stop(),this.situation=t,this.atStart()}return this},finish:function(){for(this.stop(!0,!1);this.dequeue().situation&&this.stop(!0,!1););return this.clearQueue().clearCurrent(),this},atStart:function(){return this.at(0,!0)},atEnd:function(){return!0===this.situation.loops&&(this.situation.loops=this.situation.loop+1),"number"==typeof this.situation.loops?this.at(this.situation.loops,!0):this.at(1,!0)},at:function(t,e){var i=this.situation.duration/this._speed;return this.absPos=t,e||(this.situation.reversed&&(this.absPos=1-this.absPos),this.absPos+=this.situation.loop),this.situation.start=+new Date-this.absPos*i,this.situation.finish=this.situation.start+i,this.step(!0)},speed:function(t){return 0===t?this.pause():t?(this._speed=t,this.at(this.absPos,!0)):this._speed},loop:function(t,e){var i=this.last();return i.loops=null==t||t,i.loop=0,e&&(i.reversing=!0),this},pause:function(){return this.paused=!0,this.stopAnimFrame(),this},play:function(){return this.paused?(this.paused=!1,this.at(this.absPos,!0)):this},reverse:function(t){var e=this.last();return e.reversed=void 0===t?!e.reversed:t,this},progress:function(t){return t?this.situation.ease(this.pos):this.pos},after:function(t){var e=this.last(),i=function i(n){n.detail.situation==e&&(t.call(this,e),this.off("finished.fx",i))};return this.target().on("finished.fx",i),this._callStart()},during:function(t){var e=this.last(),i=function(i){i.detail.situation==e&&t.call(this,i.detail.pos,b.morph(i.detail.pos),i.detail.eased,e)};return this.target().off("during.fx",i).on("during.fx",i),this.after(function(){this.off("during.fx",i)}),this._callStart()},afterAll:function(t){var e=function e(i){t.call(this),this.off("allfinished.fx",e)};return this.target().off("allfinished.fx",e).on("allfinished.fx",e),this._callStart()},duringAll:function(t){var e=function(e){t.call(this,e.detail.pos,b.morph(e.detail.pos),e.detail.eased,e.detail.situation)};return this.target().off("during.fx",e).on("during.fx",e),this.afterAll(function(){this.off("during.fx",e)}),this._callStart()},last:function(){return this.situations.length?this.situations[this.situations.length-1]:this.situation},add:function(t,e,i){return this.last()[i||"animations"][t]=e,this._callStart()},step:function(t){if(t||(this.absPos=this.timeToAbsPos(+new Date)),!1!==this.situation.loops){var e,i,n;e=Math.max(this.absPos,0),i=Math.floor(e),!0===this.situation.loops||i<this.situation.loops?(this.pos=e-i,n=this.situation.loop,this.situation.loop=i):(this.absPos=this.situation.loops,this.pos=1,n=this.situation.loop-1,this.situation.loop=this.situation.loops),this.situation.reversing&&(this.situation.reversed=this.situation.reversed!=Boolean((this.situation.loop-n)%2))}else this.absPos=Math.min(this.absPos,1),this.pos=this.absPos;this.pos<0&&(this.pos=0),this.situation.reversed&&(this.pos=1-this.pos);var r=this.situation.ease(this.pos);for(var s in this.situation.once)s>this.lastPos&&s<=r&&(this.situation.once[s].call(this.target(),this.pos,r),delete this.situation.once[s]);return this.active&&this.target().fire("during",{pos:this.pos,eased:r,fx:this,situation:this.situation}),this.situation?(this.eachAt(),1==this.pos&&!this.situation.reversed||this.situation.reversed&&0==this.pos?(this.stopAnimFrame(),this.target().fire("finished",{fx:this,situation:this.situation}),this.situations.length||(this.target().fire("allfinished"),this.situations.length||(this.target().off(".fx"),this.active=!1)),this.active?this.dequeue():this.clearCurrent()):!this.paused&&this.active&&this.startAnimFrame(),this.lastPos=r,this):this},eachAt:function(){var t,e,i,n=this,r=this.target(),s=this.situation;for(t in s.animations)i=[].concat(s.animations[t]).map(function(t){return"string"!=typeof t&&t.at?t.at(s.ease(n.pos),n.pos):t}),r[t].apply(r,i);for(t in s.attrs)i=[t].concat(s.attrs[t]).map(function(t){return"string"!=typeof t&&t.at?t.at(s.ease(n.pos),n.pos):t}),r.attr.apply(r,i);for(t in s.styles)i=[t].concat(s.styles[t]).map(function(t){return"string"!=typeof t&&t.at?t.at(s.ease(n.pos),n.pos):t}),r.style.apply(r,i);if(s.transforms.length){for(i=s.initialTransformation,t=0,e=s.transforms.length;t<e;t++){var o=s.transforms[t];o instanceof b.Matrix?i=o.relative?i.multiply((new b.Matrix).morph(o).at(s.ease(this.pos))):i.morph(o).at(s.ease(this.pos)):(o.relative||o.undo(i.extract()),i=i.multiply(o.at(s.ease(this.pos))))}r.matrix(i)}return this},once:function(t,e,i){var n=this.last();return i||(t=n.ease(t)),n.once[t]=e,this},_callStart:function(){return setTimeout(function(){this.start()}.bind(this),0),this}},parent:b.Element,construct:{animate:function(t,e,i){return(this.fx||(this.fx=new b.FX(this))).animate(t,e,i)},delay:function(t){return(this.fx||(this.fx=new b.FX(this))).delay(t)},stop:function(t,e){return this.fx&&this.fx.stop(t,e),this},finish:function(){return this.fx&&this.fx.finish(),this},pause:function(){return this.fx&&this.fx.pause(),this},play:function(){return this.fx&&this.fx.play(),this},speed:function(t){if(this.fx){if(null==t)return this.fx.speed();this.fx.speed(t)}return this}}}),b.MorphObj=b.invent({create:function(t,e){return b.Color.isColor(e)?new b.Color(t).morph(e):b.regex.delimiter.test(t)?b.regex.pathLetters.test(t)?new b.PathArray(t).morph(e):new b.Array(t).morph(e):b.regex.numberAndUnit.test(e)?new b.Number(t).morph(e):(this.value=t,void(this.destination=e))},extend:{at:function(t,e){return e<1?this.value:this.destination},valueOf:function(){return this.value}}}),b.extend(b.FX,{attr:function(t,e,i){if("object"==typeof t)for(var n in t)this.attr(n,t[n]);else this.add(t,e,"attrs");return this},style:function(t,e){if("object"==typeof t)for(var i in t)this.style(i,t[i]);else this.add(t,e,"styles");return this},x:function(t,e){if(this.target()instanceof b.G)return this.transform({x:t},e),this;var i=new b.Number(t);return i.relative=e,this.add("x",i)},y:function(t,e){if(this.target()instanceof b.G)return this.transform({y:t},e),this;var i=new b.Number(t);return i.relative=e,this.add("y",i)},cx:function(t){return this.add("cx",new b.Number(t))},cy:function(t){return this.add("cy",new b.Number(t))},move:function(t,e){return this.x(t).y(e)},center:function(t,e){return this.cx(t).cy(e)},size:function(t,e){if(this.target()instanceof b.Text)this.attr("font-size",t);else{var i;t&&e||(i=this.target().bbox()),t||(t=i.width/i.height*e),e||(e=i.height/i.width*t),this.add("width",new b.Number(t)).add("height",new b.Number(e))}return this},width:function(t){return this.add("width",new b.Number(t))},height:function(t){return this.add("height",new b.Number(t))},plot:function(t,e,i,n){return 4==arguments.length?this.plot([t,e,i,n]):this.add("plot",new(this.target().morphArray)(t))},leading:function(t){return this.target().leading?this.add("leading",new b.Number(t)):this},viewbox:function(t,e,i,n){return this.target()instanceof b.Container&&this.add("viewbox",new b.ViewBox(t,e,i,n)),this},update:function(t){if(this.target()instanceof b.Stop){if("number"==typeof t||t instanceof b.Number)return this.update({offset:arguments[0],color:arguments[1],opacity:arguments[2]});null!=t.opacity&&this.attr("stop-opacity",t.opacity),null!=t.color&&this.attr("stop-color",t.color),null!=t.offset&&this.attr("offset",t.offset)}return this}}),b.Box=b.invent({create:function(t,e,i,n){if(!("object"!=typeof t||t instanceof b.Element))return b.Box.call(this,null!=t.left?t.left:t.x,null!=t.top?t.top:t.y,t.width,t.height);4==arguments.length&&(this.x=t,this.y=e,this.width=i,this.height=n),y(this)},extend:{merge:function(t){var e=new this.constructor;return e.x=Math.min(this.x,t.x),e.y=Math.min(this.y,t.y),e.width=Math.max(this.x+this.width,t.x+t.width)-e.x,e.height=Math.max(this.y+this.height,t.y+t.height)-e.y,y(e)},transform:function(t){var e,i=1/0,n=-1/0,r=1/0,s=-1/0;return[new b.Point(this.x,this.y),new b.Point(this.x2,this.y),new b.Point(this.x,this.y2),new b.Point(this.x2,this.y2)].forEach(function(e){e=e.transform(t),i=Math.min(i,e.x),n=Math.max(n,e.x),r=Math.min(r,e.y),s=Math.max(s,e.y)}),e=new this.constructor,e.x=i,e.width=n-i,e.y=r,e.height=s-r,y(e),e}}}),b.BBox=b.invent({create:function(t){if(b.Box.apply(this,[].slice.call(arguments)),t instanceof b.Element){var i;try{if(e.documentElement.contains){if(!e.documentElement.contains(t.node))throw new Exception("Element not in the dom")}else{for(var n=t.node;n.parentNode;)n=n.parentNode;if(n!=e)throw new Exception("Element not in the dom")}i=t.node.getBBox()}catch(e){if(t instanceof b.Shape){var r=t.clone(b.parser.draw.instance).show();i=r.node.getBBox(),r.remove()}else i={x:t.node.clientLeft,y:t.node.clientTop,width:t.node.clientWidth,height:t.node.clientHeight}}b.Box.call(this,i)}},inherit:b.Box,parent:b.Element,construct:{bbox:function(){return new b.BBox(this)}}}),b.BBox.prototype.constructor=b.BBox,b.extend(b.Element,{tbox:function(){return console.warn("Use of TBox is deprecated and mapped to RBox. Use .rbox() instead."),this.rbox(this.doc())}}),b.RBox=b.invent({create:function(t){b.Box.apply(this,[].slice.call(arguments)),t instanceof b.Element&&b.Box.call(this,t.node.getBoundingClientRect())},inherit:b.Box,parent:b.Element,extend:{addOffset:function(){return this.x+=t.pageXOffset,this.y+=t.pageYOffset,this}},construct:{rbox:function(t){return t?new b.RBox(this).transform(t.screenCTM().inverse()):new b.RBox(this).addOffset()}}}),b.RBox.prototype.constructor=b.RBox,b.Matrix=b.invent({create:function(t){var e,i=f([1,0,0,1,0,0]);for(t=t instanceof b.Element?t.matrixify():"string"==typeof t?f(t.split(b.regex.delimiter).map(parseFloat)):6==arguments.length?f([].slice.call(arguments)):Array.isArray(t)?f(t):"object"==typeof t?t:i,e=k.length-1;e>=0;--e)this[k[e]]=null!=t[k[e]]?t[k[e]]:i[k[e]]},extend:{extract:function(){var t=c(this,0,1),e=c(this,1,0),i=180/Math.PI*Math.atan2(t.y,t.x)-90;return{x:this.e,y:this.f,transformedX:(this.e*Math.cos(i*Math.PI/180)+this.f*Math.sin(i*Math.PI/180))/Math.sqrt(this.a*this.a+this.b*this.b),transformedY:(this.f*Math.cos(i*Math.PI/180)+this.e*Math.sin(-i*Math.PI/180))/Math.sqrt(this.c*this.c+this.d*this.d),skewX:-i,skewY:180/Math.PI*Math.atan2(e.y,e.x),scaleX:Math.sqrt(this.a*this.a+this.b*this.b),scaleY:Math.sqrt(this.c*this.c+this.d*this.d),rotation:i,a:this.a,b:this.b,c:this.c,d:this.d,e:this.e,f:this.f,matrix:new b.Matrix(this)}},clone:function(){return new b.Matrix(this)},morph:function(t){return this.destination=new b.Matrix(t),this},at:function(t){return this.destination?new b.Matrix({a:this.a+(this.destination.a-this.a)*t,b:this.b+(this.destination.b-this.b)*t,c:this.c+(this.destination.c-this.c)*t,d:this.d+(this.destination.d-this.d)*t,e:this.e+(this.destination.e-this.e)*t,f:this.f+(this.destination.f-this.f)*t}):this},multiply:function(t){return new b.Matrix(this.native().multiply(d(t).native()))},inverse:function(){return new b.Matrix(this.native().inverse())},translate:function(t,e){return new b.Matrix(this.native().translate(t||0,e||0))},scale:function(t,e,i,n){return 1==arguments.length?e=t:3==arguments.length&&(n=i,i=e,e=t),this.around(i,n,new b.Matrix(t,0,0,e,0,0))},rotate:function(t,e,i){return t=b.utils.radians(t),this.around(e,i,new b.Matrix(Math.cos(t),Math.sin(t),-Math.sin(t),Math.cos(t),0,0))},flip:function(t,e){return"x"==t?this.scale(-1,1,e,0):"y"==t?this.scale(1,-1,0,e):this.scale(-1,-1,t,null!=e?e:t)},skew:function(t,e,i,n){
return 1==arguments.length?e=t:3==arguments.length&&(n=i,i=e,e=t),t=b.utils.radians(t),e=b.utils.radians(e),this.around(i,n,new b.Matrix(1,Math.tan(e),Math.tan(t),1,0,0))},skewX:function(t,e,i){return this.skew(t,0,e,i)},skewY:function(t,e,i){return this.skew(0,t,e,i)},around:function(t,e,i){return this.multiply(new b.Matrix(1,0,0,1,t||0,e||0)).multiply(i).multiply(new b.Matrix(1,0,0,1,-t||0,-e||0))},native:function(){for(var t=b.parser.native.createSVGMatrix(),e=k.length-1;e>=0;e--)t[k[e]]=this[k[e]];return t},toString:function(){return"matrix("+g(this.a)+","+g(this.b)+","+g(this.c)+","+g(this.d)+","+g(this.e)+","+g(this.f)+")"}},parent:b.Element,construct:{ctm:function(){return new b.Matrix(this.node.getCTM())},screenCTM:function(){if(this instanceof b.Nested){var t=this.rect(1,1),e=t.node.getScreenCTM();return t.remove(),new b.Matrix(e)}return new b.Matrix(this.node.getScreenCTM())}}}),b.Point=b.invent({create:function(t,e){var i,n={x:0,y:0};i=Array.isArray(t)?{x:t[0],y:t[1]}:"object"==typeof t?{x:t.x,y:t.y}:null!=t?{x:t,y:null!=e?e:t}:n,this.x=i.x,this.y=i.y},extend:{clone:function(){return new b.Point(this)},morph:function(t,e){return this.destination=new b.Point(t,e),this},at:function(t){return this.destination?new b.Point({x:this.x+(this.destination.x-this.x)*t,y:this.y+(this.destination.y-this.y)*t}):this},native:function(){var t=b.parser.native.createSVGPoint();return t.x=this.x,t.y=this.y,t},transform:function(t){return new b.Point(this.native().matrixTransform(t.native()))}}}),b.extend(b.Element,{point:function(t,e){return new b.Point(t,e).transform(this.screenCTM().inverse())}}),b.extend(b.Element,{attr:function(t,e,i){if(null==t){for(t={},e=this.node.attributes,i=e.length-1;i>=0;i--)t[e[i].nodeName]=b.regex.isNumber.test(e[i].nodeValue)?parseFloat(e[i].nodeValue):e[i].nodeValue;return t}if("object"==typeof t)for(e in t)this.attr(e,t[e]);else if(null===e)this.node.removeAttribute(t);else{if(null==e)return e=this.node.getAttribute(t),null==e?b.defaults.attrs[t]:b.regex.isNumber.test(e)?parseFloat(e):e;"stroke-width"==t?this.attr("stroke",parseFloat(e)>0?this._stroke:null):"stroke"==t&&(this._stroke=e),"fill"!=t&&"stroke"!=t||(b.regex.isImage.test(e)&&(e=this.doc().defs().image(e,0,0)),e instanceof b.Image&&(e=this.doc().defs().pattern(0,0,function(){this.add(e)}))),"number"==typeof e?e=new b.Number(e):b.Color.isColor(e)?e=new b.Color(e):Array.isArray(e)&&(e=new b.Array(e)),"leading"==t?this.leading&&this.leading(e):"string"==typeof i?this.node.setAttributeNS(i,t,e.toString()):this.node.setAttribute(t,e.toString()),!this.rebuild||"font-size"!=t&&"x"!=t||this.rebuild(t,e)}return this}}),b.extend(b.Element,{transform:function(t,e){var i,n,r=this;if("object"!=typeof t)return i=new b.Matrix(r).extract(),"string"==typeof t?i[t]:i;if(i=new b.Matrix(r),e=!!e||!!t.relative,null!=t.a)i=e?i.multiply(new b.Matrix(t)):new b.Matrix(t);else if(null!=t.rotation)p(t,r),i=e?i.rotate(t.rotation,t.cx,t.cy):i.rotate(t.rotation-i.extract().rotation,t.cx,t.cy);else if(null!=t.scale||null!=t.scaleX||null!=t.scaleY){if(p(t,r),t.scaleX=null!=t.scale?t.scale:null!=t.scaleX?t.scaleX:1,t.scaleY=null!=t.scale?t.scale:null!=t.scaleY?t.scaleY:1,!e){var s=i.extract();t.scaleX=1*t.scaleX/s.scaleX,t.scaleY=1*t.scaleY/s.scaleY}i=i.scale(t.scaleX,t.scaleY,t.cx,t.cy)}else if(null!=t.skew||null!=t.skewX||null!=t.skewY){if(p(t,r),t.skewX=null!=t.skew?t.skew:null!=t.skewX?t.skewX:0,t.skewY=null!=t.skew?t.skew:null!=t.skewY?t.skewY:0,!e){var s=i.extract();i=i.multiply((new b.Matrix).skew(s.skewX,s.skewY,t.cx,t.cy).inverse())}i=i.skew(t.skewX,t.skewY,t.cx,t.cy)}else t.flip?("x"==t.flip||"y"==t.flip?t.offset=null==t.offset?r.bbox()["c"+t.flip]:t.offset:null==t.offset?(n=r.bbox(),t.flip=n.cx,t.offset=n.cy):t.flip=t.offset,i=(new b.Matrix).flip(t.flip,t.offset)):null==t.x&&null==t.y||(e?i=i.translate(t.x,t.y):(null!=t.x&&(i.e=t.x),null!=t.y&&(i.f=t.y)));return this.attr("transform",i)}}),b.extend(b.FX,{transform:function(t,e){var i,n,r=this.target();return"object"!=typeof t?(i=new b.Matrix(r).extract(),"string"==typeof t?i[t]:i):(e=!!e||!!t.relative,null!=t.a?i=new b.Matrix(t):null!=t.rotation?(p(t,r),i=new b.Rotate(t.rotation,t.cx,t.cy)):null!=t.scale||null!=t.scaleX||null!=t.scaleY?(p(t,r),t.scaleX=null!=t.scale?t.scale:null!=t.scaleX?t.scaleX:1,t.scaleY=null!=t.scale?t.scale:null!=t.scaleY?t.scaleY:1,i=new b.Scale(t.scaleX,t.scaleY,t.cx,t.cy)):null!=t.skewX||null!=t.skewY?(p(t,r),t.skewX=null!=t.skewX?t.skewX:0,t.skewY=null!=t.skewY?t.skewY:0,i=new b.Skew(t.skewX,t.skewY,t.cx,t.cy)):t.flip?("x"==t.flip||"y"==t.flip?t.offset=null==t.offset?r.bbox()["c"+t.flip]:t.offset:null==t.offset?(n=r.bbox(),t.flip=n.cx,t.offset=n.cy):t.flip=t.offset,i=(new b.Matrix).flip(t.flip,t.offset)):null==t.x&&null==t.y||(i=new b.Translate(t.x,t.y)),i?(i.relative=e,this.last().transforms.push(i),this._callStart()):this)}}),b.extend(b.Element,{untransform:function(){return this.attr("transform",null)},matrixify:function(){return(this.attr("transform")||"").split(b.regex.transforms).slice(0,-1).map(function(t){var e=t.trim().split("(");return[e[0],e[1].split(b.regex.delimiter).map(function(t){return parseFloat(t)})]}).reduce(function(t,e){return"matrix"==e[0]?t.multiply(f(e[1])):t[e[0]].apply(t,e[1])},new b.Matrix)},toParent:function(t){if(this==t)return this;var e=this.screenCTM(),i=t.screenCTM().inverse();return this.addTo(t).untransform().transform(i.multiply(e)),this},toDoc:function(){return this.toParent(this.doc())}}),b.Transformation=b.invent({create:function(t,e){if(arguments.length>1&&"boolean"!=typeof e)return this.constructor.call(this,[].slice.call(arguments));if(Array.isArray(t))for(var i=0,n=this.arguments.length;i<n;++i)this[this.arguments[i]]=t[i];else if("object"==typeof t)for(var i=0,n=this.arguments.length;i<n;++i)this[this.arguments[i]]=t[this.arguments[i]];this.inversed=!1,!0===e&&(this.inversed=!0)},extend:{arguments:[],method:"",at:function(t){for(var e=[],i=0,n=this.arguments.length;i<n;++i)e.push(this[this.arguments[i]]);var r=this._undo||new b.Matrix;return r=(new b.Matrix).morph(b.Matrix.prototype[this.method].apply(r,e)).at(t),this.inversed?r.inverse():r},undo:function(t){for(var e=0,i=this.arguments.length;e<i;++e)t[this.arguments[e]]=void 0===this[this.arguments[e]]?0:t[this.arguments[e]];return t.cx=this.cx,t.cy=this.cy,this._undo=new(b[a(this.method)])(t,!0).at(1),this}}}),b.Translate=b.invent({parent:b.Matrix,inherit:b.Transformation,create:function(t,e){this.constructor.apply(this,[].slice.call(arguments))},extend:{arguments:["transformedX","transformedY"],method:"translate"}}),b.Rotate=b.invent({parent:b.Matrix,inherit:b.Transformation,create:function(t,e){this.constructor.apply(this,[].slice.call(arguments))},extend:{arguments:["rotation","cx","cy"],method:"rotate",at:function(t){var e=(new b.Matrix).rotate((new b.Number).morph(this.rotation-(this._undo?this._undo.rotation:0)).at(t),this.cx,this.cy);return this.inversed?e.inverse():e},undo:function(t){return this._undo=t,this}}}),b.Scale=b.invent({parent:b.Matrix,inherit:b.Transformation,create:function(t,e){this.constructor.apply(this,[].slice.call(arguments))},extend:{arguments:["scaleX","scaleY","cx","cy"],method:"scale"}}),b.Skew=b.invent({parent:b.Matrix,inherit:b.Transformation,create:function(t,e){this.constructor.apply(this,[].slice.call(arguments))},extend:{arguments:["skewX","skewY","cx","cy"],method:"skew"}}),b.extend(b.Element,{style:function(t,e){if(0==arguments.length)return this.node.style.cssText||"";if(arguments.length<2)if("object"==typeof t)for(e in t)this.style(e,t[e]);else{if(!b.regex.isCss.test(t))return this.node.style[o(t)];for(t=t.split(/\s*;\s*/).filter(function(t){return!!t}).map(function(t){return t.split(/\s*:\s*/)});e=t.pop();)this.style(e[0],e[1])}else this.node.style[o(t)]=null===e||b.regex.isBlank.test(e)?"":e;return this}}),b.Parent=b.invent({create:function(t){this.constructor.call(this,t)},inherit:b.Element,extend:{children:function(){return b.utils.map(b.utils.filterSVGElements(this.node.childNodes),function(t){return b.adopt(t)})},add:function(t,e){return null==e?this.node.appendChild(t.node):t.node!=this.node.childNodes[e]&&this.node.insertBefore(t.node,this.node.childNodes[e]),this},put:function(t,e){return this.add(t,e),t},has:function(t){return this.index(t)>=0},index:function(t){return[].slice.call(this.node.childNodes).indexOf(t.node)},get:function(t){return b.adopt(this.node.childNodes[t])},first:function(){return this.get(0)},last:function(){return this.get(this.node.childNodes.length-1)},each:function(t,e){var i,n,r=this.children();for(i=0,n=r.length;i<n;i++)r[i]instanceof b.Element&&t.apply(r[i],[i,r]),e&&r[i]instanceof b.Container&&r[i].each(t,e);return this},removeElement:function(t){return this.node.removeChild(t.node),this},clear:function(){for(;this.node.hasChildNodes();)this.node.removeChild(this.node.lastChild);return delete this._defs,this},defs:function(){return this.doc().defs()}}}),b.extend(b.Parent,{ungroup:function(t,e){return 0===e||this instanceof b.Defs||this.node==b.parser.draw?this:(t=t||(this instanceof b.Doc?this:this.parent(b.Parent)),e=e||1/0,this.each(function(){return this instanceof b.Defs?this:this instanceof b.Parent?this.ungroup(t,e-1):this.toParent(t)}),this.node.firstChild||this.remove(),this)},flatten:function(t,e){return this.ungroup(t,e)}}),b.Container=b.invent({create:function(t){this.constructor.call(this,t)},inherit:b.Parent}),b.ViewBox=b.invent({create:function(t){var e,i,n,r,s,o,a,h=[0,0,0,0],u=1,l=1,c=/[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?/gi;if(t instanceof b.Element){for(o=t,a=t,s=(t.attr("viewBox")||"").match(c),t.bbox,n=new b.Number(t.width()),r=new b.Number(t.height());"%"==n.unit;)u*=n.value,n=new b.Number(o instanceof b.Doc?o.parent().offsetWidth:o.parent().width()),o=o.parent();for(;"%"==r.unit;)l*=r.value,r=new b.Number(a instanceof b.Doc?a.parent().offsetHeight:a.parent().height()),a=a.parent();this.x=0,this.y=0,this.width=n*u,this.height=r*l,this.zoom=1,s&&(e=parseFloat(s[0]),i=parseFloat(s[1]),n=parseFloat(s[2]),r=parseFloat(s[3]),this.zoom=this.width/this.height>n/r?this.height/r:this.width/n,this.x=e,this.y=i,this.width=n,this.height=r)}else t="string"==typeof t?t.match(c).map(function(t){return parseFloat(t)}):Array.isArray(t)?t:"object"==typeof t?[t.x,t.y,t.width,t.height]:4==arguments.length?[].slice.call(arguments):h,this.x=t[0],this.y=t[1],this.width=t[2],this.height=t[3]},extend:{toString:function(){return this.x+" "+this.y+" "+this.width+" "+this.height},morph:function(t,e,i,n){return this.destination=new b.ViewBox(t,e,i,n),this},at:function(t){return this.destination?new b.ViewBox([this.x+(this.destination.x-this.x)*t,this.y+(this.destination.y-this.y)*t,this.width+(this.destination.width-this.width)*t,this.height+(this.destination.height-this.height)*t]):this}},parent:b.Container,construct:{viewbox:function(t,e,i,n){return 0==arguments.length?new b.ViewBox(this):this.attr("viewBox",new b.ViewBox(t,e,i,n))}}}),["click","dblclick","mousedown","mouseup","mouseover","mouseout","mousemove","mouseenter","mouseleave","touchstart","touchmove","touchleave","touchend","touchcancel"].forEach(function(t){b.Element.prototype[t]=function(e){return null==e?b.off(this,t):b.on(this,t,e),this}}),b.listenerId=0,b.on=function(t,e,i,n,r){var s=i.bind(n||t),o=t instanceof b.Element?t.node:t;o.instance=o.instance||{_events:{}};var a=o.instance._events;i._svgjsListenerId||(i._svgjsListenerId=++b.listenerId),e.split(b.regex.delimiter).forEach(function(t){var e=t.split(".")[0],n=t.split(".")[1]||"*";a[e]=a[e]||{},a[e][n]=a[e][n]||{},a[e][n][i._svgjsListenerId]=s,o.addEventListener(e,s,r||!1)})},b.off=function(t,e,i,n){var r=t instanceof b.Element?t.node:t;if(r.instance&&("function"!=typeof i||(i=i._svgjsListenerId))){var s=r.instance._events;(e||"").split(b.regex.delimiter).forEach(function(t){var e,o,a=t&&t.split(".")[0],h=t&&t.split(".")[1];if(i)s[a]&&s[a][h||"*"]&&(r.removeEventListener(a,s[a][h||"*"][i],n||!1),delete s[a][h||"*"][i]);else if(a&&h){if(s[a]&&s[a][h]){for(o in s[a][h])b.off(r,[a,h].join("."),o);delete s[a][h]}}else if(h)for(t in s)for(e in s[t])h===e&&b.off(r,[t,h].join("."));else if(a){if(s[a]){for(e in s[a])b.off(r,[a,e].join("."));delete s[a]}}else{for(t in s)b.off(r,t);r.instance._events={}}})}},b.extend(b.Element,{on:function(t,e,i,n){return b.on(this,t,e,i,n),this},off:function(t,e){return b.off(this.node,t,e),this},fire:function(e,i){return e instanceof t.Event?this.node.dispatchEvent(e):this.node.dispatchEvent(e=new b.CustomEvent(e,{detail:i,cancelable:!0})),this._event=e,this},event:function(){return this._event}}),b.Defs=b.invent({create:"defs",inherit:b.Container}),b.G=b.invent({create:"g",inherit:b.Container,extend:{x:function(t){return null==t?this.transform("x"):this.transform({x:t-this.x()},!0)},y:function(t){return null==t?this.transform("y"):this.transform({y:t-this.y()},!0)},cx:function(t){return null==t?this.gbox().cx:this.x(t-this.gbox().width/2)},cy:function(t){return null==t?this.gbox().cy:this.y(t-this.gbox().height/2)},gbox:function(){var t=this.bbox(),e=this.transform();return t.x+=e.x,t.x2+=e.x,t.cx+=e.x,t.y+=e.y,t.y2+=e.y,t.cy+=e.y,t}},construct:{group:function(){return this.put(new b.G)}}}),b.Doc=b.invent({create:function(t){t&&(t="string"==typeof t?e.getElementById(t):t,"svg"==t.nodeName?this.constructor.call(this,t):(this.constructor.call(this,b.create("svg")),t.appendChild(this.node),this.size("100%","100%")),this.namespace().defs())},inherit:b.Container,extend:{namespace:function(){return this.attr({xmlns:b.ns,version:"1.1"}).attr("xmlns:xlink",b.xlink,b.xmlns).attr("xmlns:svgjs",b.svgjs,b.xmlns)},defs:function(){if(!this._defs){var t;(t=this.node.getElementsByTagName("defs")[0])?this._defs=b.adopt(t):this._defs=new b.Defs,this.node.appendChild(this._defs.node)}return this._defs},parent:function(){return this.node.parentNode&&"#document"!=this.node.parentNode.nodeName&&"#document-fragment"!=this.node.parentNode.nodeName?this.node.parentNode:null},spof:function(){var t=this.node.getScreenCTM();return t&&this.style("left",-t.e%1+"px").style("top",-t.f%1+"px"),this},remove:function(){return this.parent()&&this.parent().removeChild(this.node),this},clear:function(){for(;this.node.hasChildNodes();)this.node.removeChild(this.node.lastChild);return delete this._defs,b.parser.draw.parentNode||this.node.appendChild(b.parser.draw),this},clone:function(t){this.writeDataToDom();var e=this.node,i=x(e.cloneNode(!0));return t?(t.node||t).appendChild(i.node):e.parentNode.insertBefore(i.node,e.nextSibling),i}}}),b.extend(b.Element,{siblings:function(){return this.parent().children()},position:function(){return this.parent().index(this)},next:function(){return this.siblings()[this.position()+1]},previous:function(){return this.siblings()[this.position()-1]},forward:function(){var t=this.position()+1,e=this.parent();return e.removeElement(this).add(this,t),e instanceof b.Doc&&e.node.appendChild(e.defs().node),this},backward:function(){var t=this.position();return t>0&&this.parent().removeElement(this).add(this,t-1),this},front:function(){var t=this.parent();return t.node.appendChild(this.node),t instanceof b.Doc&&t.node.appendChild(t.defs().node),this},back:function(){return this.position()>0&&this.parent().removeElement(this).add(this,0),this},before:function(t){t.remove();var e=this.position();return this.parent().add(t,e),this},after:function(t){t.remove();var e=this.position();return this.parent().add(t,e+1),this}}),b.Mask=b.invent({create:function(){this.constructor.call(this,b.create("mask")),this.targets=[]},inherit:b.Container,extend:{remove:function(){for(var t=this.targets.length-1;t>=0;t--)this.targets[t]&&this.targets[t].unmask();return this.targets=[],b.Element.prototype.remove.call(this),this}},construct:{mask:function(){return this.defs().put(new b.Mask)}}}),b.extend(b.Element,{maskWith:function(t){return this.masker=t instanceof b.Mask?t:this.parent().mask().add(t),this.masker.targets.push(this),this.attr("mask",'url("#'+this.masker.attr("id")+'")')},unmask:function(){return delete this.masker,this.attr("mask",null)}}),b.ClipPath=b.invent({create:function(){this.constructor.call(this,b.create("clipPath")),this.targets=[]},inherit:b.Container,extend:{remove:function(){for(var t=this.targets.length-1;t>=0;t--)this.targets[t]&&this.targets[t].unclip();return this.targets=[],this.parent().removeElement(this),this}},construct:{clip:function(){return this.defs().put(new b.ClipPath)}}}),b.extend(b.Element,{clipWith:function(t){return this.clipper=t instanceof b.ClipPath?t:this.parent().clip().add(t),this.clipper.targets.push(this),this.attr("clip-path",'url("#'+this.clipper.attr("id")+'")')},unclip:function(){return delete this.clipper,this.attr("clip-path",null)}}),b.Gradient=b.invent({create:function(t){this.constructor.call(this,b.create(t+"Gradient")),this.type=t},inherit:b.Container,extend:{at:function(t,e,i){return this.put(new b.Stop).update(t,e,i)},update:function(t){return this.clear(),"function"==typeof t&&t.call(this,this),this},fill:function(){return"url(#"+this.id()+")"},toString:function(){return this.fill()},attr:function(t,e,i){return"transform"==t&&(t="gradientTransform"),b.Container.prototype.attr.call(this,t,e,i)}},construct:{gradient:function(t,e){return this.defs().gradient(t,e)}}}),b.extend(b.Gradient,b.FX,{from:function(t,e){return"radial"==(this._target||this).type?this.attr({fx:new b.Number(t),fy:new b.Number(e)}):this.attr({x1:new b.Number(t),y1:new b.Number(e)})},to:function(t,e){return"radial"==(this._target||this).type?this.attr({cx:new b.Number(t),cy:new b.Number(e)}):this.attr({x2:new b.Number(t),y2:new b.Number(e)})}}),b.extend(b.Defs,{gradient:function(t,e){return this.put(new b.Gradient(t)).update(e)}}),b.Stop=b.invent({create:"stop",inherit:b.Element,extend:{update:function(t){return("number"==typeof t||t instanceof b.Number)&&(t={offset:arguments[0],color:arguments[1],opacity:arguments[2]}),null!=t.opacity&&this.attr("stop-opacity",t.opacity),null!=t.color&&this.attr("stop-color",t.color),null!=t.offset&&this.attr("offset",new b.Number(t.offset)),this}}}),b.Pattern=b.invent({create:"pattern",inherit:b.Container,extend:{fill:function(){return"url(#"+this.id()+")"},update:function(t){return this.clear(),"function"==typeof t&&t.call(this,this),this},toString:function(){return this.fill()},attr:function(t,e,i){return"transform"==t&&(t="patternTransform"),b.Container.prototype.attr.call(this,t,e,i)}},construct:{pattern:function(t,e,i){return this.defs().pattern(t,e,i)}}}),b.extend(b.Defs,{pattern:function(t,e,i){return this.put(new b.Pattern).update(i).attr({x:0,y:0,width:t,height:e,patternUnits:"userSpaceOnUse"})}}),b.Shape=b.invent({create:function(t){this.constructor.call(this,t)},inherit:b.Element}),b.Bare=b.invent({create:function(t,e){if(this.constructor.call(this,b.create(t)),e)for(var i in e.prototype)"function"==typeof e.prototype[i]&&(this[i]=e.prototype[i])},inherit:b.Element,extend:{words:function(t){for(;this.node.hasChildNodes();)this.node.removeChild(this.node.lastChild);return this.node.appendChild(e.createTextNode(t)),this}}}),b.extend(b.Parent,{element:function(t,e){return this.put(new b.Bare(t,e))}}),b.Symbol=b.invent({create:"symbol",inherit:b.Container,construct:{symbol:function(){return this.put(new b.Symbol)}}}),b.Use=b.invent({create:"use",inherit:b.Shape,extend:{element:function(t,e){return this.attr("href",(e||"")+"#"+t,b.xlink)}},construct:{use:function(t,e){return this.put(new b.Use).element(t,e)}}}),b.Rect=b.invent({create:"rect",inherit:b.Shape,construct:{rect:function(t,e){return this.put(new b.Rect).size(t,e)}}}),b.Circle=b.invent({create:"circle",inherit:b.Shape,construct:{circle:function(t){return this.put(new b.Circle).rx(new b.Number(t).divide(2)).move(0,0)}}}),b.extend(b.Circle,b.FX,{rx:function(t){return this.attr("r",t)},ry:function(t){return this.rx(t)}}),b.Ellipse=b.invent({create:"ellipse",inherit:b.Shape,construct:{ellipse:function(t,e){return this.put(new b.Ellipse).size(t,e).move(0,0)}}}),b.extend(b.Ellipse,b.Rect,b.FX,{rx:function(t){return this.attr("rx",t)},ry:function(t){return this.attr("ry",t)}}),b.extend(b.Circle,b.Ellipse,{x:function(t){return null==t?this.cx()-this.rx():this.cx(t+this.rx())},y:function(t){return null==t?this.cy()-this.ry():this.cy(t+this.ry())},cx:function(t){return null==t?this.attr("cx"):this.attr("cx",t)},cy:function(t){return null==t?this.attr("cy"):this.attr("cy",t)},width:function(t){return null==t?2*this.rx():this.rx(new b.Number(t).divide(2))},height:function(t){return null==t?2*this.ry():this.ry(new b.Number(t).divide(2))},size:function(t,e){var i=l(this,t,e);return this.rx(new b.Number(i.width).divide(2)).ry(new b.Number(i.height).divide(2))}}),b.Line=b.invent({create:"line",inherit:b.Shape,extend:{array:function(){return new b.PointArray([[this.attr("x1"),this.attr("y1")],[this.attr("x2"),this.attr("y2")]])},plot:function(t,e,i,n){return null==t?this.array():(t=void 0!==e?{x1:t,y1:e,x2:i,y2:n}:new b.PointArray(t).toLine(),this.attr(t))},move:function(t,e){return this.attr(this.array().move(t,e).toLine())},size:function(t,e){var i=l(this,t,e);return this.attr(this.array().size(i.width,i.height).toLine())}},construct:{line:function(t,e,i,n){return b.Line.prototype.plot.apply(this.put(new b.Line),null!=t?[t,e,i,n]:[0,0,0,0])}}}),b.Polyline=b.invent({create:"polyline",inherit:b.Shape,construct:{polyline:function(t){return this.put(new b.Polyline).plot(t||new b.PointArray)}}}),b.Polygon=b.invent({create:"polygon",inherit:b.Shape,construct:{polygon:function(t){return this.put(new b.Polygon).plot(t||new b.PointArray)}}}),b.extend(b.Polyline,b.Polygon,{array:function(){return this._array||(this._array=new b.PointArray(this.attr("points")))},plot:function(t){return null==t?this.array():this.clear().attr("points","string"==typeof t?t:this._array=new b.PointArray(t))},clear:function(){return delete this._array,this},move:function(t,e){return this.attr("points",this.array().move(t,e))},size:function(t,e){var i=l(this,t,e);return this.attr("points",this.array().size(i.width,i.height))}}),b.extend(b.Line,b.Polyline,b.Polygon,{morphArray:b.PointArray,x:function(t){return null==t?this.bbox().x:this.move(t,this.bbox().y)},y:function(t){return null==t?this.bbox().y:this.move(this.bbox().x,t)},width:function(t){var e=this.bbox();return null==t?e.width:this.size(t,e.height)},height:function(t){var e=this.bbox();return null==t?e.height:this.size(e.width,t)}}),b.Path=b.invent({create:"path",inherit:b.Shape,extend:{morphArray:b.PathArray,array:function(){return this._array||(this._array=new b.PathArray(this.attr("d")))},plot:function(t){return null==t?this.array():this.clear().attr("d","string"==typeof t?t:this._array=new b.PathArray(t))},clear:function(){return delete this._array,this},move:function(t,e){return this.attr("d",this.array().move(t,e))},x:function(t){return null==t?this.bbox().x:this.move(t,this.bbox().y)},y:function(t){return null==t?this.bbox().y:this.move(this.bbox().x,t)},size:function(t,e){var i=l(this,t,e);return this.attr("d",this.array().size(i.width,i.height))},width:function(t){return null==t?this.bbox().width:this.size(t,this.bbox().height)},height:function(t){return null==t?this.bbox().height:this.size(this.bbox().width,t)}},construct:{path:function(t){return this.put(new b.Path).plot(t||new b.PathArray)}}}),b.Image=b.invent({create:"image",inherit:b.Shape,extend:{load:function(e){if(!e)return this;var i=this,n=new t.Image;return b.on(n,"load",function(){b.off(n);var t=i.parent(b.Pattern);null!==t&&(0==i.width()&&0==i.height()&&i.size(n.width,n.height),t&&0==t.width()&&0==t.height()&&t.size(i.width(),i.height()),"function"==typeof i._loaded&&i._loaded.call(i,{width:n.width,height:n.height,ratio:n.width/n.height,url:e}))}),b.on(n,"error",function(t){b.off(n),"function"==typeof i._error&&i._error.call(i,t)}),this.attr("href",n.src=this.src=e,b.xlink)},loaded:function(t){return this._loaded=t,this},error:function(t){return this._error=t,this}},construct:{image:function(t,e,i){return this.put(new b.Image).load(t).size(e||0,i||e||0)}}}),b.Text=b.invent({create:function(){this.constructor.call(this,b.create("text")),this.dom.leading=new b.Number(1.3),this._rebuild=!0,this._build=!1,this.attr("font-family",b.defaults.attrs["font-family"])},inherit:b.Shape,extend:{x:function(t){return null==t?this.attr("x"):this.attr("x",t)},y:function(t){var e=this.attr("y"),i="number"==typeof e?e-this.bbox().y:0;return null==t?"number"==typeof e?e-i:e:this.attr("y","number"==typeof t.valueOf()?t+i:t)},cx:function(t){return null==t?this.bbox().cx:this.x(t-this.bbox().width/2)},cy:function(t){return null==t?this.bbox().cy:this.y(t-this.bbox().height/2)},text:function(t){if(void 0===t){for(var t="",e=this.node.childNodes,i=0,n=e.length;i<n;++i)0!=i&&3!=e[i].nodeType&&1==b.adopt(e[i]).dom.newLined&&(t+="\n"),t+=e[i].textContent;return t}if(this.clear().build(!0),"function"==typeof t)t.call(this,this);else{t=t.split("\n");for(var i=0,r=t.length;i<r;i++)this.tspan(t[i]).newLine()}return this.build(!1).rebuild()},size:function(t){return this.attr("font-size",t).rebuild()},leading:function(t){return null==t?this.dom.leading:(this.dom.leading=new b.Number(t),this.rebuild())},lines:function(){var t=(this.textPath&&this.textPath()||this).node,e=b.utils.map(b.utils.filterSVGElements(t.childNodes),function(t){return b.adopt(t)});return new b.Set(e)},rebuild:function(t){if("boolean"==typeof t&&(this._rebuild=t),this._rebuild){var e=this,i=0,n=this.dom.leading*new b.Number(this.attr("font-size"));this.lines().each(function(){this.dom.newLined&&(e.textPath()||this.attr("x",e.attr("x")),"\n"==this.text()?i+=n:(this.attr("dy",n+i),i=0))}),this.fire("rebuild")}return this},build:function(t){return this._build=!!t,this},setData:function(t){return this.dom=t,this.dom.leading=new b.Number(t.leading||1.3),this}},construct:{text:function(t){return this.put(new b.Text).text(t)},plain:function(t){return this.put(new b.Text).plain(t)}}}),b.Tspan=b.invent({create:"tspan",inherit:b.Shape,extend:{text:function(t){return null==t?this.node.textContent+(this.dom.newLined?"\n":""):("function"==typeof t?t.call(this,this):this.plain(t),this)},dx:function(t){return this.attr("dx",t)},dy:function(t){return this.attr("dy",t)},newLine:function(){var t=this.parent(b.Text);return this.dom.newLined=!0,this.dy(t.dom.leading*t.attr("font-size")).attr("x",t.x())}}}),b.extend(b.Text,b.Tspan,{plain:function(t){return!1===this._build&&this.clear(),this.node.appendChild(e.createTextNode(t)),this},tspan:function(t){var e=(this.textPath&&this.textPath()||this).node,i=new b.Tspan;return!1===this._build&&this.clear(),e.appendChild(i.node),i.text(t)},clear:function(){for(var t=(this.textPath&&this.textPath()||this).node;t.hasChildNodes();)t.removeChild(t.lastChild);return this},length:function(){return this.node.getComputedTextLength()}}),b.TextPath=b.invent({create:"textPath",inherit:b.Parent,parent:b.Text,construct:{morphArray:b.PathArray,path:function(t){for(var e=new b.TextPath,i=this.doc().defs().path(t);this.node.hasChildNodes();)e.node.appendChild(this.node.firstChild);return this.node.appendChild(e.node),e.attr("href","#"+i,b.xlink),this},array:function(){var t=this.track();return t?t.array():null},plot:function(t){var e=this.track(),i=null;return e&&(i=e.plot(t)),null==t?i:this},track:function(){var t=this.textPath();if(t)return t.reference("href")},textPath:function(){if(this.node.firstChild&&"textPath"==this.node.firstChild.nodeName)return b.adopt(this.node.firstChild)}}}),b.Nested=b.invent({create:function(){this.constructor.call(this,b.create("svg")),this.style("overflow","visible")},inherit:b.Container,construct:{nested:function(){return this.put(new b.Nested)}}}),b.A=b.invent({create:"a",inherit:b.Container,extend:{to:function(t){return this.attr("href",t,b.xlink)},show:function(t){return this.attr("show",t,b.xlink)},target:function(t){return this.attr("target",t)}},construct:{link:function(t){return this.put(new b.A).to(t)}}}),b.extend(b.Element,{linkTo:function(t){var e=new b.A;return"function"==typeof t?t.call(e,e):e.to(t),this.parent().put(e).put(this)}}),b.Marker=b.invent({create:"marker",inherit:b.Container,extend:{width:function(t){return this.attr("markerWidth",t)},height:function(t){return this.attr("markerHeight",t)},ref:function(t,e){return this.attr("refX",t).attr("refY",e)},update:function(t){return this.clear(),"function"==typeof t&&t.call(this,this),this},toString:function(){return"url(#"+this.id()+")"}},construct:{marker:function(t,e,i){return this.defs().marker(t,e,i)}}}),b.extend(b.Defs,{marker:function(t,e,i){return this.put(new b.Marker).size(t,e).ref(t/2,e/2).viewbox(0,0,t,e).attr("orient","auto").update(i)}}),b.extend(b.Line,b.Polyline,b.Polygon,b.Path,{marker:function(t,e,i,n){var r=["marker"];return"all"!=t&&r.push(t),r=r.join("-"),t=arguments[1]instanceof b.Marker?arguments[1]:this.doc().marker(e,i,n),this.attr(r,t)}});var M={stroke:["color","width","opacity","linecap","linejoin","miterlimit","dasharray","dashoffset"],fill:["color","opacity","rule"],prefix:function(t,e){return"color"==e?t:t+"-"+e}};["fill","stroke"].forEach(function(t){var e,i={};i[t]=function(i){if(void 0===i)return this;if("string"==typeof i||b.Color.isRgb(i)||i&&"function"==typeof i.fill)this.attr(t,i);else for(e=M[t].length-1;e>=0;e--)null!=i[M[t][e]]&&this.attr(M.prefix(t,M[t][e]),i[M[t][e]]);return this},b.extend(b.Element,b.FX,i)}),b.extend(b.Element,b.FX,{rotate:function(t,e,i){return this.transform({rotation:t,cx:e,cy:i})},skew:function(t,e,i,n){return 1==arguments.length||3==arguments.length?this.transform({skew:t,cx:e,cy:i}):this.transform({skewX:t,skewY:e,cx:i,cy:n})},scale:function(t,e,i,n){return 1==arguments.length||3==arguments.length?this.transform({scale:t,cx:e,cy:i}):this.transform({scaleX:t,scaleY:e,cx:i,cy:n})},translate:function(t,e){return this.transform({x:t,y:e})},flip:function(t,e){return e="number"==typeof t?t:e,this.transform({flip:t||"both",offset:e})},matrix:function(t){return this.attr("transform",new b.Matrix(6==arguments.length?[].slice.call(arguments):t))},opacity:function(t){return this.attr("opacity",t)},dx:function(t){return this.x(new b.Number(t).plus(this instanceof b.FX?0:this.x()),!0)},dy:function(t){return this.y(new b.Number(t).plus(this instanceof b.FX?0:this.y()),!0)},dmove:function(t,e){return this.dx(t).dy(e)}}),b.extend(b.Rect,b.Ellipse,b.Circle,b.Gradient,b.FX,{radius:function(t,e){var i=(this._target||this).type;return"radial"==i||"circle"==i?this.attr("r",new b.Number(t)):this.rx(t).ry(null==e?t:e)}}),b.extend(b.Path,{length:function(){return this.node.getTotalLength()},pointAt:function(t){return this.node.getPointAtLength(t)}}),b.extend(b.Parent,b.Text,b.Tspan,b.FX,{font:function(t,e){if("object"==typeof t)for(e in t)this.font(e,t[e]);return"leading"==t?this.leading(e):"anchor"==t?this.attr("text-anchor",e):"size"==t||"family"==t||"weight"==t||"stretch"==t||"variant"==t||"style"==t?this.attr("font-"+t,e):this.attr(t,e)}}),b.Set=b.invent({create:function(t){t instanceof b.Set?this.members=t.members.slice():Array.isArray(t)?this.members=t:this.clear()},extend:{add:function(){var t,e,i=[].slice.call(arguments);for(t=0,e=i.length;t<e;t++)this.members.push(i[t]);return this},remove:function(t){var e=this.index(t);return e>-1&&this.members.splice(e,1),this},each:function(t){for(var e=0,i=this.members.length;e<i;e++)t.apply(this.members[e],[e,this.members]);return this},clear:function(){return this.members=[],this},length:function(){return this.members.length},has:function(t){return this.index(t)>=0},index:function(t){return this.members.indexOf(t)},get:function(t){return this.members[t]},first:function(){return this.get(0)},last:function(){return this.get(this.members.length-1)},valueOf:function(){return this.members},bbox:function(){if(0==this.members.length)return new b.RBox;var t=this.members[0].rbox(this.members[0].doc());return this.each(function(){t=t.merge(this.rbox(this.doc()))}),t}},construct:{set:function(t){
return new b.Set(t)}}}),b.FX.Set=b.invent({create:function(t){this.set=t}}),b.Set.inherit=function(){var t,e=[];for(var t in b.Shape.prototype)"function"==typeof b.Shape.prototype[t]&&"function"!=typeof b.Set.prototype[t]&&e.push(t);e.forEach(function(t){b.Set.prototype[t]=function(){for(var e=0,i=this.members.length;e<i;e++)this.members[e]&&"function"==typeof this.members[e][t]&&this.members[e][t].apply(this.members[e],arguments);return"animate"==t?this.fx||(this.fx=new b.FX.Set(this)):this}}),e=[];for(var t in b.FX.prototype)"function"==typeof b.FX.prototype[t]&&"function"!=typeof b.FX.Set.prototype[t]&&e.push(t);e.forEach(function(t){b.FX.Set.prototype[t]=function(){for(var e=0,i=this.set.members.length;e<i;e++)this.set.members[e].fx[t].apply(this.set.members[e].fx,arguments);return this}})},b.extend(b.Element,{data:function(t,e,i){if("object"==typeof t)for(e in t)this.data(e,t[e]);else if(arguments.length<2)try{return JSON.parse(this.attr("data-"+t))}catch(e){return this.attr("data-"+t)}else this.attr("data-"+t,null===e?null:!0===i||"string"==typeof e||"number"==typeof e?e:JSON.stringify(e));return this}}),b.extend(b.Element,{remember:function(t,e){if("object"==typeof arguments[0])for(var e in t)this.remember(e,t[e]);else{if(1==arguments.length)return this.memory()[t];this.memory()[t]=e}return this},forget:function(){if(0==arguments.length)this._memory={};else for(var t=arguments.length-1;t>=0;t--)delete this.memory()[arguments[t]];return this},memory:function(){return this._memory||(this._memory={})}}),b.get=function(t){var i=e.getElementById(v(t)||t);return b.adopt(i)},b.select=function(t,i){return new b.Set(b.utils.map((i||e).querySelectorAll(t),function(t){return b.adopt(t)}))},b.extend(b.Parent,{select:function(t){return b.select(t,this.node)}});var k="abcdef".split("");if("function"!=typeof t.CustomEvent){var S=function(t,i){i=i||{bubbles:!1,cancelable:!1,detail:void 0};var n=e.createEvent("CustomEvent");return n.initCustomEvent(t,i.bubbles,i.cancelable,i.detail),n};S.prototype=t.Event.prototype,b.CustomEvent=S}else b.CustomEvent=t.CustomEvent;return function(e){for(var i=0,n=["moz","webkit"],r=0;r<n.length&&!t.requestAnimationFrame;++r)e.requestAnimationFrame=e[n[r]+"RequestAnimationFrame"],e.cancelAnimationFrame=e[n[r]+"CancelAnimationFrame"]||e[n[r]+"CancelRequestAnimationFrame"];e.requestAnimationFrame=e.requestAnimationFrame||function(t){var n=(new Date).getTime(),r=Math.max(0,16-(n-i)),s=e.setTimeout(function(){t(n+r)},r);return i=n+r,s},e.cancelAnimationFrame=e.cancelAnimationFrame||e.clearTimeout}(t),b});;







function MenuItemClass(menuItemJSON) {
this.menuItemJSON = menuItemJSON;
}
MenuItemClass.prototype.findMenu = function (menuid) {
var menuItemJSON = this.menuItemJSON;
var menuItemId = menuItemJSON.id;
if (menuItemId == menuid)
{
return menuItemJSON;
}
var children = menuItemJSON.children;
if ( !children )
{
return null;
}
for (var i = 0; i < children.length; i++) {
var childItem = children[i];
var childID = childItem.id;
if ( menuid == childID )
{
return childItem;
}
if ( childItem.children )
{
var childObj = new MenuItemClass(childItem);
var targetMenu = childObj.findMenu(menuid);
if (targetMenu)
{
return targetMenu;
}
}
}
return null
}
MenuItemClass.prototype.getLeftMostPageJSON = function () {
var menuItemJSON = this.menuItemJSON;
var menuItemId = menuItemJSON;
var children = menuItemJSON.children;
if ( !children )
{
return menuItemJSON;
}
var leftMostSon = children[0];
var menuObj = new MenuItemClass(leftMostSon);
return menuObj.getLeftMostPageJSON();
}
function MenuTreeClass(menuTreeJSON)
{
this.menuTreeJSON = menuTreeJSON
}
MenuTreeClass.prototype.findMenu = function(menuid) {
var menuTreeJSON = this.menuTreeJSON
for (var i = 0; i < menuTreeJSON.length; i++) {
var menu1table = menuTreeJSON[i];
var menu1Obj = new MenuItemClass(menu1table);
var targetMenu = menu1Obj.findMenu(menuid);
if ( targetMenu )
{
return targetMenu;
}
}
return null
};
function GetLeftMostPageID(menuid)
{
var menuTable = menuTreeObj.findMenu(menuid);
var menuObj = new MenuItemClass(menuTable);
var pageJSON = menuObj.getLeftMostPageJSON();
return pageJSON.id;
}
function Class3MenuShow(selectPageID, selectSupId, selectMidId, selectThdId)
{
if ( selectThdId == "" )
{
$("#class3Menu").css("display", "none");
return;
}
var class2MenuNode = menuTreeObj.findMenu(selectMidId);
var class3MenuJSON = class2MenuNode.children;
var class3MenuContent = "";
for (var index in class3MenuJSON)
{
var menu = class3MenuJSON[index]
var class3MenuID = menu.id
var class3MenuName = menu.name
if ( class3MenuID == selectThdId )
{
AEleMenu3Class = "AEleMenu3Selected";
}
else
{
AEleMenu3Class = "AEleMenu3";
}
class3MenuContent = class3MenuContent
+ "<li class='item-menu'><a class='" + AEleMenu3Class + "'"
+ "MenuClass='3'"
+ "id='"+ class3MenuID + "'"
+ "MenuPage='"+ GetLeftMostPageID(class3MenuID) +"'"
+ "href='#" + class3MenuID + "'><span class='arrow-right-small'></span>"
+ class3MenuName
+ "</a></li>";
}
$("#class3MenuMainContent ul").html(class3MenuContent);
$("#class3MenuMainContent ul li a").click(function(){
var MenuOBJ = $(this);
if ( !checkDisClickAttr(MenuOBJ) )
{
return;
}
AjaxQuery_ClassMenuClick(MenuOBJ);
});
}
function Class2MenuShow(selectPageID, selectSupId, selectMidId, selectThdId)
{
if ( selectMidId == "" )
{
return;
}
var class1MenuNode = menuTreeObj.findMenu(selectSupId);
var class2MenuJSON = class1MenuNode.children;
var class2MenuContent = "<ul class='holder-sub-menu'>";
var class2MenuClass = "";
var have3menu = false;
for (var index in class2MenuJSON)
{
var menu = class2MenuJSON[index]
var class2MenuID = menu.id
var class2MenuName = menu.name
if ( class2MenuID == selectMidId )
{
if(selectThdId != "")
{
have3menu = true;
}
}
var class2MenuNode = menuTreeObj.findMenu(class2MenuID);
var class3MenuJSON = class2MenuNode.children;
var class3MenuContent = "";
if ( !class3MenuJSON )
{
have3menu = false;
}
else
{
have3menu = true;
class3MenuContent = "<ul class='holder-sub-menu sub'>";
for (var index in class3MenuJSON)
{
var menu3 = class3MenuJSON[index]
var class3MenuID = menu3.id
var class3MenuName = menu3.name
class3MenuContent = class3MenuContent
+ "<li class='item-menu'><a class='MenuPage' "
+ "MenuClass='3' "
+ "id='"+ class3MenuID + "' "
+ "MenuPage='"+ GetLeftMostPageID(class3MenuID) +"' ><span class='arrow-right-small'></span>"
+ class3MenuName
+ "</a>";
}
class3MenuContent = class3MenuContent + "</ul>";
}
if(have3menu == true)
{
class2MenuClass = "<li class='item-menu'><input class='sub-menu-controler' id='menu-firewall' type='checkbox' name='menu-controler-sub-seguranca'>"
+ "<label for='menu-"+ class2MenuID + "' menuclass='2' "
+ "id='" + class2MenuID + "' "
+ "menupage='" + GetLeftMostPageID(class2MenuID)
+ "' title='" + class2MenuName + "' >"
+ class2MenuName
+ "<span class='holder-state'><span class='plus'></span><span class='minus'></span></span></label>"
}
else
{
class2MenuClass = "<li class='item-menu'><a href='javascript:void(0);' class='MenuPage' "
+ "MenuClass='2' "
+ "id='"+ class2MenuID + "' "
+ "MenuPage='"+ GetLeftMostPageID(class2MenuID)
+ "' title='" + class2MenuName
+ "'>"
+ class2MenuName
+ "</a>";
}
class2MenuContent = class2MenuContent
+ class2MenuClass
+ class3MenuContent
+ "</li>";
}
class2MenuContent = class2MenuContent + "</ul>"
$("#class2Menu").html(class2MenuContent);
$("#class2Menu a").click(function(){
$("#main-menu").prop("checked", false);
var wholeMenuObj = $(".wrapper-menu");
$(".sub-menu-controler", wholeMenuObj).prop("checked", false);
var MenuOBJ = $(this);
var parentsObj = MenuOBJ.parents(".item-menu");
$(".sub-menu-controler", parentsObj).prop("checked", true);
if ( !checkDisClickAttr(MenuOBJ) )
{
return;
}
AjaxQuery_ClassMenuClick(MenuOBJ);
});
}
function Class1MenuShow(selectPageID, selectSupId)
{
var FirstMenuContent = "";
var SupClass = "";
var SupLiID = "";
var FirstOne = "yes";
for (var index in menuTreeJSON)
{
var menu = menuTreeJSON[index]
var supId = menu.id
var supName = menu.name
if ( supId == selectSupId )
{
liClass = "nav-item menu-item menu-active menu-font-center";
aCladd = "nav-link";
}
else
{
liClass = "nav-item menu-item menu-font-center";
aCladd = "nav-link text-light";
}
if ( FirstOne == "yes" )
{
SupLiID = "homeLi";
FirstOne = "no";
}
else
{
SupLiID = "";
}
FirstMenuContent = FirstMenuContent
+ "<li id=\"" + SupLiID + "\" class=\"" + liClass + "\">"
+ "<a href=\"javascript:void(0);\" class=\"" + aCladd
+ "\" "
+ "style=\"width:" + aWidth +"px;padding:0.5rem 0rem\" "
+ "MenuClass='1' "
+ "id='"+ supId + "' "
+ "MenuPage='"+ GetLeftMostPageID(supId) +"'"
+ ">"
+ supName
+ "</a></li>";
}
FirstMenuContent = FirstMenuContent + "</ul>";
$("#trueNavigator").html(FirstMenuContent);
$("#trueNavigator li a").click(function(){
var MenuOBJ = $(this);
if ( !checkDisClickAttr(MenuOBJ) )
{
return;
}
AjaxQuery_ClassMenuClick(MenuOBJ);
});
}
function CreateMenu()
{
var FirstMenuContent = "";
for (var index in menuTreeJSON)
{
var menu = menuTreeJSON[index];
var supId = menu.id;
var supName = menu.name;
var class2MenuJSON = menuTreeJSON[index].children;
FirstMenuContent = FirstMenuContent + "<li class='item-menu'>";
if( !class2MenuJSON )
{
FirstMenuContent = FirstMenuContent
+ "<a href='javascript:void(0);' class='MenuPage' menuclass='1' "
+ "id='"+ supId + "' "
+ "MenuPage='"+ GetLeftMostPageID(supId) +"'"
+ " title='" + supName +"'>"
+ supName
+ "</a>";
}
else
{
FirstMenuContent = FirstMenuContent
+ "<input class='sub-menu-controler' id='menu-" + supId + "' type='checkbox' name='menu-controler-menu'>"
+ "<label for='menu-" + supId + "'>" + supName + "<span class='arrow-right'></span><span class='arrow-down'></span></label>";
var class2MenuContent = "<ul class='holder-sub-menu'>";
var class2MenuClass = "";
var have3menu = false;
for (var index in class2MenuJSON)
{
var menu = class2MenuJSON[index];
var class2MenuID = menu.id;
var class2MenuName = menu.name;
var class2MenuNode = menuTreeObj.findMenu(class2MenuID);
var class3MenuJSON = class2MenuNode.children;
var class3MenuContent = "";
if ( !class3MenuJSON )
{
have3menu = false;
}
else
{
have3menu = true;
class3MenuContent = "<ul class='holder-sub-menu sub'>";
for (var index in class3MenuJSON)
{
var menu3 = class3MenuJSON[index]
var class3MenuID = menu3.id
var class3MenuName = menu3.name
class3MenuContent = class3MenuContent
+ "<li class='item-menu'><a class='MenuPage' "
+ "MenuClass='3' "
+ "id='"+ class3MenuID + "' "
+ "MenuPage='"+ GetLeftMostPageID(class3MenuID) +"' ><span class='arrow-right-small'></span>"
+ class3MenuName
+ "</a>";
}
class3MenuContent = class3MenuContent + "</ul>";
}
if(have3menu == true)
{
class2MenuClass = "<li class='item-menu'><input class='sub-menu-controler' id='menu-" + class2MenuID + "' type='checkbox' name='menu-controler-sub-seguranca'>"
+ "<label for='menu-"+ class2MenuID + "' menuclass='2' "
+ "id='" + class2MenuID + "' "
+ "menupage='" + GetLeftMostPageID(class2MenuID)
+ "' title='" + class2MenuName + "' >"
+ class2MenuName
+ "<span class='holder-state'><span class='plus'>&#xe908;</span><span class='minus'>&#xe909;</span></span></label>"
}
else
{
class2MenuClass = "<li class='item-menu'><a href='javascript:void(0);' class='MenuPage' "
+ "MenuClass='2' "
+ "id='"+ class2MenuID + "' "
+ "MenuPage='"+ GetLeftMostPageID(class2MenuID)
+ "' title='" + class2MenuName
+ "'>"
+ class2MenuName
+ "</a>";
}
class2MenuContent = class2MenuContent
+ class2MenuClass
+ class3MenuContent
+ "</li>";
}
class2MenuContent = class2MenuContent + "</ul>";
FirstMenuContent = FirstMenuContent + class2MenuContent;
}
FirstMenuContent = FirstMenuContent + "</li>";
}
FirstMenuContent = FirstMenuContent
+ "<li class='item-menu'><a id='LogOffLnk'onclick='LogOff()'> Sair</a></li>";
$(".holder-menu").append(FirstMenuContent);
$(".holder-menu li a[class='MenuPage']").click(function(){
if ($(this).attr("id")=="quicksetup"){
$(".wrapper-menu").hide();
$("#qlogout").show();
$("#Qstate").show();
$("#Qquickset").hide();
}else{
$(".wrapper-menu").show();
$("#qlogout").hide();
$("#Qstate").hide();
$("#Qquickset").show();
}
$("#main-menu").prop("checked", false);
var wholeMenuObj = $(".wrapper-menu");
$(".sub-menu-controler", wholeMenuObj).prop("checked", false);
var MenuOBJ = $(this);
var parentsObj = MenuOBJ.parents(".item-menu");
parentsObj.each(function(){
var itemObj = $(this);
var inputObj = itemObj.children("input");
if (inputObj.length > 0)
{
inputObj.prop("checked", true);
}
});
if ( !checkDisClickAttr(MenuOBJ) )
{
return;
}
AjaxQuery_ClassMenuClick(MenuOBJ);
});
}
function checkDisClickAttr(obj)
{
if ("off" == obj.attr("EnableClick"))
{
return false;
}
handleDisClickAttr("off");
return true;
}
function handleDisClickAttr(ret)
{
var selectSupId = $("#_NowSupIdInfo",_MenuInfo).text();
var selectMidId = $("#_NowMidIdInfo",_MenuInfo).text();
var selectThdId = $("#_NowThdIdInfo",_MenuInfo).text();
if(selectThdId)
{
var objs = [$("#" + selectSupId),$("#" + selectMidId),$("#" + selectThdId)];
}
else
{
if(selectMidId)
{
var objs = [$("#" + selectSupId),$("#" + selectMidId)];
}
else
{
var objs = [$("#" + selectSupId)];
}
}
for (var i = 0; i < objs.length; i++)
{
if (objs[i].length > 0)
{
objs[i].attr("EnableClick", ret);
}
}
}
function AjaxPageGet(PageName, MenuClass)
{
var pageContainer = $("#commPageContainer");
pageContainer.succfunction = function(html){
pageContainer.html(html);
$(document).scrollTop(0);
handleDisClickAttr("on");
};
pageContainer.errorfunction = function(){
consoleLog("page get fail");
showWaitTip(false);
pageContainer.html("Pedido da página falhou, por favor tente novamente!");
handleDisClickAttr("on");
};
showWaitTip(true);
pageContainer.dataTransfer( PageName, "GET", pageContainer.succfunction,
pageContainer.errorfunction, false,
undefined, 'html'
);
}
function AjaxQuery_ClassMenuClick(MenuOBJ)
{
var MenuClass = MenuOBJ.attr("MenuClass");
var page = MenuOBJ.attr("MenuPage");
var pageFile = "/?_type=menuView&_tag="
+ page + "&Menu3Location=0";
AjaxPageGet(pageFile, MenuClass);
}
function openLink(pageurl)
{
var PageName = "/?_type=menuView&_tag=" + pageurl;
AjaxPageGet(PageName, 1);
}
function MenuShow(Menuclass, selectPageID, selectSupId, selectMidId, selectThdId)
{
CreateMenu();
}
function FakeClass1MenuShow()
{
$(".wrapper-menu").hide();
}
function showWaitTip(show, TipMsg, StopTag)
{
var TipMsgTmp = TipMsg;
if( show )
{
$("#blackMask,#tipLayer,#confirmBtnArea").css("display", "block");
if (TipMsgTmp == undefined || TipMsgTmp == "")
{
$("#waitingImgArea").css("display", "none");
if(true==StopTag)
{
$("#confirmStop").css("display", "block");
$("#confirmCancel,#confirmOK").css("display", "none");
}
else
{
$("#confirmStop").css("display", "none");
$("#confirmCancel,#confirmOK").css("display", "block");
}
}
else
{
$("#confirmLayer, #waitingImgArea").css("display", "block");
$("#confirmMsg p").text(TipMsgTmp);
if(true==StopTag)
{
$("#confirmStop").css("display", "block");
$("#confirmCancel,#confirmOK").css("display", "none");
}
else
{
$("#confirmCancel,#confirmOK,#confirmStop").css("display", "none");
}
}
$('#confirmLayer :button:visible:first').focus();
$("#page_container").bind("keyup", function(event){
if (event.which == 9) {
$('#confirmLayer :button:visible:first').focus();
}
});
reposition_box("tipLayer");
}
else
{
$("#blackMask, #tipLayer, #confirmLayer").css("display", "none");
$("#confirmCancel, #confirmOK, #confirmStop, #confirmCancel").removeAttr("tabindex");
$("#page_container").unbind("keyup");
}
}
function IniConfirm(msg)
{
showWaitTip(true);
var confirmLayerOBJ = $("#confirmLayer");
$("#confirmCancel, #confirmOK, #confirmStop, #confirmCancel").attr("tabindex", "1");
confirmLayerOBJ.css("display", "block");
$("#confirmMsg p",confirmLayerOBJ).text(msg);
$("#confirmCancel",confirmLayerOBJ).unbind( "click" );
$("#confirmOK",confirmLayerOBJ).unbind( "click" );
$("#confirmStop",confirmLayerOBJ).unbind( "click" );
$("#confirmCancel",confirmLayerOBJ).bind("click", function(event){
showWaitTip(false);
});
$('#confirmLayer :button:visible:first').focus();
return confirmLayerOBJ;
}
function IniTip(msg, infoType)
{
showWaitTip(true);
var confirmLayerOBJ = $("#confirmLayer");
$("#confirmCancel",confirmLayerOBJ).css("display", "none");
confirmLayerOBJ.css("display", "block");
if (infoType == "err")
{
$("#confirmMsg",confirmLayerOBJ).css("background", 'url("../img/err_m.png") no-repeat 20px 50%');
}
else if (infoType == "succ")
{
$("#confirmMsg",confirmLayerOBJ).css("background", 'url("../img/succ_m.png") no-repeat 20px 50%');
}
else
{
$("#confirmMsg",confirmLayerOBJ).css("background", 'url("../img/info_m.png") no-repeat 20px 50%');
}
$("#confirmMsg p",confirmLayerOBJ).text(msg);
$("#confirmCancel",confirmLayerOBJ).unbind( "click" );
$("#confirmOK",confirmLayerOBJ).unbind( "click" );
$("#confirmStop",confirmLayerOBJ).unbind( "click" );
$("#confirmOK",confirmLayerOBJ).bind("click", function(event){
showWaitTip(false);
$("#confirmMsg",confirmLayerOBJ).css("background", 'url("../img/info_m.png") no-repeat 20px 50%');
});
$("#confirmOK",confirmLayerOBJ).focus();
return confirmLayerOBJ;
}
function getStyle(obj,attr)
{
if (obj.currentStyle)
{
return obj.currentStyle[attr];
}
else
{
return document.defaultView.getComputedStyle(obj,null)[attr];
}
}
function reposition_box(divId)
{
var box=document.getElementById(divId);
if (null!=box)
{
var boxObj = $("#"+divId);
var winH = $(window).height();
var winW = $(window).width();
var divH = boxObj.height();
var divW = boxObj.width();
var h = (winH-divH)/2;
h = (h > 0) ? h : 5;
var w = (winW-divW)/2;
w = (w > 0) ? w : 5;
boxObj.css({top:h, left:w});
if ( divH > winH || divW > winW)
{
boxObj.css("position", "absolute");
}
else
{
boxObj.css("position", "fixed");
}
}
}
function keyBoardClick(obj) {
obj.off('keydown.eventEnter');
obj.on('keydown.eventEnter', function(event) {
var thisOBJ = $(this);
if (event.key === 'Enter' || event.key === ' '
|| event.code == 'Enter' || event.code == 'Space'
|| event.keyCode === 13 || event.keyCode === 32) {
event.preventDefault();
thisOBJ.click();
}
});
}
function getFocusToClick(querySelector, template) {
var focusableElements = $(querySelector, template);
focusableElements.each(function() {
keyBoardClick($(this));
});
}
function setARIAAttr(obj, attrname, attrvalue) {
if (attrvalue == undefined) {
obj.attr(attrname, attrname);
} else {
obj.attr(attrname, attrvalue);
}
if (attrname == "link") {
obj.attr("href", "#");
}
}
$.validator.setDefaults({
errorPlacement: function (error, element) {
var tipHTML = "<div class=\"errorLabelWraper\"></div>";
var tipObj = $(tipHTML);
error.appendTo(tipObj);
var rowObj = element.closest(".f-row");
if ( rowObj.length == 0 )
{
consoleLog("element id=["+element.attr("id")+"] is not in row div.");
return ;
}
var rowWidth = rowObj.width();
var usedWidth = 0;
var rightObj = undefined;
rowObj.children().each(function(){
if (!($(this).hasClass("_LuQUID_AccessDeviceList")||
$(this).hasClass("clear"))){
usedWidth += $(this).outerWidth(true);
}
if ($(this).hasClass("f-wrap")){
rightObj = $(this);
}
});
var errWidth = rowWidth - usedWidth;
if (rightObj != undefined)
{
tipObj.insertAfter(rightObj);
}
else
{
tipObj.appendTo(rowObj);
}
},
onkeyup: function(element, event) {
var excludedKeys = [
16, 17, 18, 20, 35, 36, 37,
38, 39, 40, 45, 144, 225
];
if (event.which === 9 && this.elementValue(element) === "" || $.inArray(event.keyCode, excludedKeys) !== -1 ) {
return;
} else if (element.name in this.submitted || element.name in this.invalid || element === this.lastActive) {
this.element(element);
}
}
});
jQuery.extend(jQuery.validator.messages, {
required: "Este campo é obrigatório. ",
remote: "Por favor corrigir esse campo. ",
email: "Por favor insira um endereço de e-mail válido. ",
url: "Por favor, insira um URL válido. ",
date: "Por favor insira uma data válida. ",
dateISO: "Por favor, indique uma data válida (ISO). ",
number: "Por favor insira um número válido. ",
digits: "Digite um número inteiro. ",
creditcard: "Por favor digite um número de cartão de crédito válido. ",
equalTo: "Por favor entre com o mesmo valor novamente. ",
maxlength: jQuery.validator.format("Por favor, indique não mais do que {0} caracteres. "),
minlength: jQuery.validator.format("Por favor, insira pelo menos {0} caracteres. "),
rangelength: jQuery.validator.format("Por favor insira um valor com {0} ~ {1} caracteres. "),
range: jQuery.validator.format("Por favor insira um valor entre {0} e {1}. "),
max: jQuery.validator.format("Por favor insira um valor menor ou igual a {0}. "),
min: jQuery.validator.format("Por favor insira um valor maior ou igual a {0}. ")
});
function AsciiPasswordCheck(Key)
{
for (var j = 0 ;j < Key.length; j++)
{
var ch = Key.charCodeAt(j);
if(ch == 9)
{
return false;
}
}
return true;
}
function AsciiCheck(Key)
{
for (var j = 0 ;j < Key.length; j++)
{
var ch = Key.charCodeAt(j);
if(ch<32 || ch>126)
{
return false;
}
}
return true;
}
function AsciiCheckWithLen(Key, LenLimit)
{
if (Key.length != LenLimit)
{
return false;
}
if ( false == AsciiCheck(Key) )
{
return false;
}
return true;
}
function HexCheck(Key)
{
for (var j = 0 ;j < Key.length; j++)
{
var ch = Key.charCodeAt(j);
if (!((ch >= 65 && ch <= 70)
||(ch >= 97 && ch <= 102)
||(ch >= 48 && ch <= 57)))
{
return false;
}
}
return true;
}
function HexCheckWithLen(Key, LenLimit)
{
if (Key.length != LenLimit)
{
return false;
}
if ( false == HexCheck(Key) )
{
return false;
}
return true;
}
function checkIPv4Addr(ipaddr)
{
var re = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
if(re.test(ipaddr) == true)
{
var parts = ipaddr.split(".");
for(var i=0; i<parts.length; i++)
{
if(parts[i].indexOf("0") == 0 && parts[i].length > 1)
return false;
if (parseInt((parts[i]),10) > 255 || parseInt((parts[i]),10) < 0)
{
return false;
}
}
return true;
}
return false;
}
function checkMacAddr(macaddr)
{
var regSingleByte = new RegExp(":","g");
var regexp = /^([A-Fa-f0-9]{2}-){5}[A-Fa-f0-9]{2}$/;
macaddr = macaddr.replace(regSingleByte,"-");
if (!regexp.test(macaddr)) {
return false;
}
return true;
}
jQuery.validator.addMethod(
"macAddr",
function(value, element, params) {
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if(checkMacAddr(value) == true)
{
return true;
}
return false;
},
"Insira um endereço MAC válido. "
);
jQuery.validator.addMethod(
"IPv4Addr",
function(value, element, params) {
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if(checkIPv4Addr(value) == true)
{
return true;
}
return false;
},
"Insira um endereço IPv4 válido. "
);
jQuery.validator.addMethod(
"IPv6Addr",
function(value, element, params) {
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if (value.match("[^0-9a-fA-F:.]") != null)
return false;
addrParts = value.split(':');
Doublecolon = value.split('::');
ipv4Parts = value.split('.');
if(addrParts.length<3||addrParts.length>8)
{
return false;
}
else if(Doublecolon.length==1&&ipv4Parts.length==1&&addrParts.length!=8)
{
return false;
}
else if(Doublecolon.length==1&&ipv4Parts.length>1&&addrParts.length!=6)
{
return false;
}
else if(Doublecolon.length>1&&ipv4Parts.length>1&&addrParts.length>6)
{
return false;
}
else if(Doublecolon.length>2||value.split(':::').length>1)
{
return false;
}
else
{
if(addrParts[0]==""&&addrParts[1]!="")
{
return false;
}
for(var i=0;i<addrParts.length;i++)
{
if(i==addrParts.length-1&&addrParts[i]==""&&addrParts[i-1]!="")
{
return false;
}
if(addrParts[i].length>4 && addrParts[i].split('.').length<2)
{
return false;
}
}
}
var pos = value.lastIndexOf(":");
var ipv4Parts = value.split('.');
if(ipv4Parts.length>1)
{
var ipv4=value.substring(pos+1,value.length);
if( false == checkIPv4Addr(ipv4) )
{
return false;
}
}
return true;
},
"Insira um endereço IPv6 válido. "
);
jQuery.validator.addMethod(
"DomainName",
function(value, element, params) {
if ( this.optional(element) )
{
return "dependency-mismatch";
}
var len = value.length;
var firstChar = value.substr(0,1);
var lastChar = value.substr(len-1,1);
var maxlen = 64;
if(len>64||len<1)
{
return false;
}
if (value.match("[^0-9a-zA-Z.-]") != null)
{
return false;
}
if(firstChar.match("[^0-9a-zA-Z]") != null)
{
return false;
}
if(lastChar.match("[^0-9a-zA-Z]") != null)
{
return false;
}
var pos = value.lastIndexOf(".");
if(pos == -1)
{
var str = value;
var templen = value.length;
for(var i=0;i<len;i++)
{
var tempvalue = str.substring(i,i+1);
if(isNaN(parseInt(tempvalue)))
{
return true;
}
}
return false;
}
else
{
var str = value.substr(pos+1);
var tmplen = value.length - (pos + 1);
for(var i=0;i<tmplen;i++)
{
var tmpvalue = str.substring(i,i+1);
if(isNaN(parseInt(tmpvalue)))
{
return true;
}
}
return false;
}
},
"Por favor insira um nome de domínio válido. "
);
jQuery.validator.addMethod(
"HostName",
function(value, element, params) {
if ( this.optional(element) )
{
return "dependency-mismatch";
}
var len = value.length;
var firstChar = value.substr(0,1);
var lastChar = value.substr(len-1,1);
if (value.match("[^0-9a-zA-Z.-]") != null)
{
return false;
}
if(firstChar.match("[^0-9a-zA-Z]") != null)
{
return false;
}
if(lastChar.match("[^0-9a-zA-Z]") != null)
{
return false;
}
var pos = value.lastIndexOf(".");
if(pos == -1)
{
var str = value;
var templen = value.length;
for(var i=0;i<len;i++)
{
var tempvalue = str.substring(i,i+1);
if(isNaN(parseInt(tempvalue)))
{
return true;
}
}
return false;
}
else
{
var str = value.substr(pos+1);
var tmplen = value.length - (pos + 1);
for(var i=0;i<tmplen;i++)
{
var tmpvalue = str.substring(i,i+1);
if(isNaN(parseInt(tmpvalue)))
{
return true;
}
}
return false;
}
},
"Por favor insira um nome de host válido. "
);
jQuery.validator.addMethod(
"url",
function(value, element, params) {
if ( this.optional(element) )
{
return "dependency-mismatch";
}
var len = value.length;
if( (len < 1) || (len > 256) )
{
return false;
}
if (value.match("[^0-9a-zA-Z.:;,!@%#?_/&=+*'$()\\[\\]-]") != null)
{
return false;
}
return true;
},
"Por favor, insira um URL válido. "
);
jQuery.validator.addMethod(
"PasswordASCII",
function(value, element, params)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if (value == "						")
{
return true;
}
if ( false == AsciiPasswordCheck(value) )
{
params = 0;
return false;
}
if ( false == AsciiCheck(value) )
{
params = 1;
return false;
}
return true;
},
function(param, element)
{
var error = ["O formato da senha está errada. Por favor, digite novamente. ", "Por favor, indique apenas caracteres ASCII. "];
var value = $(element).val();
var ret = 0;
if ( false == AsciiPasswordCheck(value) )
{
ret = 0;
}
else if( false == AsciiCheck(value) )
{
ret = 1;
}
else
{
}
if ( ret <= error.length )
{
return error[ret];
}
}
);
jQuery.validator.addMethod(
"ASCII",
function(value, element, params)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if ( false == AsciiCheck(value) )
{
return false;
}
return true;
},
"Por favor, indique apenas caracteres ASCII. "
);
jQuery.validator.addMethod(
"utf8",
function(value, element, params)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
return true;
},
"Por favor, indique apenas caracteres ASCII. "
);
jQuery.validator.addMethod(
"WEPKey128Bit",
function(value, element, params)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
var AsciiLenLimit = 13;
var HexLenLimit = 26;
if ( AsciiCheckWithLen(value, AsciiLenLimit) == false
&& HexCheckWithLen(value, HexLenLimit) == false )
{
return false;
}
return true;
},
"Por favor insira 13 caracteres ASCII ou 26 dígitos hexadecimais. "
);
jQuery.validator.addMethod(
"WEPAsciiOrHexLen",
function(value, element, params)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
var AsciiLenLimit = 5;
var HexLenLimit = 10;
var AsciiLenLimit13 = 13;
var HexLenLimit26 =26;
if (AsciiCheckWithLen(value, AsciiLenLimit) == false
&& HexCheckWithLen(value, HexLenLimit) == false
&& AsciiCheckWithLen(value, AsciiLenLimit13) == false
&& HexCheckWithLen(value, HexLenLimit26) == false)
{
return false;
}
return true;
},
"Por favor, digite 5 ou 13 caracteres ASCII, ou digite 10 ou 26 dígitos hexadecimais. "
);
jQuery.validator.addMethod(
"HEX",
function(value, element, params)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if ( HexCheck(value) == false )
{
return false;
}
return true;
},
"Introduza apenas caracteres hexadecimais. "
);
jQuery.validator.addMethod(
"fixedlength",
function(value, element, param)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if (value.length != param)
{
return false;
}
return true;
},
jQuery.validator.format("Por favor, indique {0} caracteres. ")
);
jQuery.validator.addMethod(
"fixedValue",
function(value, element, param)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if (value != param)
{
return false;
}
return true;
},
jQuery.validator.format("O único valor permitido é {0}.")
);
function hexCompare(hexNum, hexRefer)
{
var num = parseInt(hexNum, 16);
var refer = parseInt(hexRefer, 16);
if (num < refer)
{
return -1;
}
else if (num > refer)
{
return 1;
}
else
{
return 0;
}
}
jQuery.validator.addMethod(
"hexRange",
function(value, element, params)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if (typeof(params[0]) == "object")
{
for (var i=0; i<params.length; i++)
{
var range = params[i];
if (typeof(range) == "object")
{
if (hexCompare(value, range[0]) != -1 && hexCompare(value, range[1]) != 1 )
{
return true;
}
}
}
}
else
{
if (hexCompare(value, params[0]) != -1 && hexCompare(value, params[1]) != 1 )
{
return true;
}
}
return false;
},
function(params, element){
var rangesStr = "";
if (typeof(params[0]) == "object")
{
var rangesLen = params.length;
for (var i=0; i<rangesLen; i++)
{
var range = params[i];
if (hexCompare(range[0], range[1]) != 0)
{
rangesStr += range[0] + "~" + range[1];
}
else
{
rangesStr += range[0];
}
if ( i < rangesLen-1 )
{
rangesStr += ", ";
}
}
}
else
{
rangesStr = params[0] + "~" + params[1];
}
return $.validator.format("Por favor insira um valor hexadecimal em intervalos de {0}. ", rangesStr);
}
);
jQuery.validator.addMethod(
"ranges",
function(value, element, param)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
var rangesLen = param.length;
for (var i=0; i<rangesLen; i++)
{
var range = param[i];
if ( typeof range === 'number' )
{
if ( value == range )
{
return true;
}
}
else
{
if ( value >= range[0] && value <= range[1] )
{
return true;
}
}
}
return false;
},
function(param, element){
var rangesStr = "";
var rangesLen = param.length;
for (var i=0; i<rangesLen; i++)
{
var range = param[i];
if ( typeof range === 'number' )
{
rangesStr += range;
}
else
{
rangesStr += range[0] + "~" + range[1];
}
if ( i < rangesLen-1 )
{
rangesStr += ",";
}
}
return $.validator.format("Por favor insira um valor em intervalos de {0}. ", rangesStr);
}
);
jQuery.validator.addMethod(
"integer",
function(value, element, params)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
return /^-?\d+$/.test(value);
},
"Digite um número inteiro. "
);
jQuery.validator.addMethod(
"concurrence",
function(value, element, param)
{
if (1 > param.length)
{
return true;
}
var obj = get_element_obj($(element), param[0]);
if (obj.is(":hidden"))
{
return true;
}
if ("" == value && "" == obj.val())
{
return true;
}
if ("" != value && "" != obj.val())
{
return true;
}
return false;
},
"Por favor coloque prefixo válido. "
);
function get_element_obj(obj, id)
{
var instTplt = obj.closest("[id^=template_]");
var elementID = obj.attr("id");
var arr = elementID.split(':');
var strId = id;
if (arr.length > 1)
{
var exNum = arr[arr.length-1];
strId = id + ":" + exNum;
}
return $("[id='"+strId+"']", instTplt);
};
function test_greatThan(obj, value, param, type)
{
if ("errstring" == type )
{
var tempstring = {
"1" : param[2].separate ? "Por favor, indique um valor superior a \"{0}\". " : "Por favor insira um valor maior do que o anterior. " ,
"2" : param[2].separate ? "Por favor insira um valor não inferior a \"{0}\". " : "Por favor insira um valor não inferior ao primeiro. " ,
"3" : param[2].separate ? "Assegure-se de que a diferença com o primeiro não seja maior que {1}. " : "Assegure-se de que a diferença com o primeiro não seja maior que {1}. "
};
return $.validator.format(tempstring[param[2].ret], param[2].idtext, param[2].discrepantMode);
}
else
{
var tmpvalue = obj.val();
var ret = true;
if (param[2].equal)
{
ret = Number(value) >= Number(tmpvalue);
if (!ret)
{
param[2].ret = "2";
return false;
}
}
else
{
ret = Number(value) > Number(tmpvalue);
if (!ret)
{
param[2].ret = "1";
return false;
}
}
if (param[2].discrepantMode)
{
ret = Number(value) - Number(tmpvalue) <= Number(param[2].discrepantMode);
if (!ret)
{
param[2].ret = "3";
return false;
}
}
obj.parent().next().children().hide();
return true;
}
};
function test_lessThan(obj, value, param, type)
{
if ("errstring" == type )
{
var tempstring = {
"1" : param[2].separate ? "Por favor insira um valor inferior a \"{0}\". " : "Por favor insira um valor menor do que o último. " ,
"2" : param[2].separate ? "Por favor insira um valor não superior a \"{0}\". " : "Por favor insira um valor não superior ao último. " ,
"3" : param[2].separate ? "Assegure-se de que a diferença com o primeiro não seja maior que {1}. " : "Assegure-se de que a diferença com o primeiro não seja maior que {1}. "
};
return $.validator.format(tempstring[param[2].ret], param[2].idtext, param[2].discrepantMode);
}
else
{
var tmpvalue = obj.val();
var ret = true;
if (param[2].equal)
{
ret = Number(value) <= Number(tmpvalue);
if (!ret)
{
param[2].ret = "2";
return false;
}
}
else
{
ret = Number(value) < Number(tmpvalue);
if (!ret)
{
param[2].ret = "1";
return false;
}
}
if (param[2].discrepantMode)
{
ret = Number(tmpvalue) - Number(value) <= Number(param[2].discrepantMode)
if (!ret)
{
param[2].ret = "3";
return false;
}
}
obj.parent().next().children().hide();
return true;
}
};
jQuery.validator.addMethod(
"extremumRange",
function(value, element, param)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if (2 > param.length)
{
return true;
}
var obj = get_element_obj($(element), param[1]);
if (3 > param.length)
{
param[2] = {};
}
param[2]["idtext"] = obj.parent().prev().text();
if (obj.is(":hidden") || "" == obj.val())
{
return true;
}
var selectMode = {
"greatThan" : test_greatThan,
"lessThan" : test_lessThan
};
return selectMode[param[0]](obj, value, param);
},
function(param,element)
{
var selectMode = {
"greatThan" : test_greatThan,
"lessThan" : test_lessThan
};
return selectMode[param[0]]("", "", param, "errstring");
}
);
function range_greatThan(obj, value, param, type)
{
if ("errstring" == type )
{
var tempstring = {
"1" : param[2].separate ? "Por favor, indique um valor superior a \"{0}\". " : ( param[2].objPosition =="first" ? "Por favor insira um valor maior do que o anterior. " : "Por favor insira um valor maior do que o último." ),
"2" : param[2].separate ? "Por favor insira um valor não inferior a \"{0}\". " : ( param[2].objPosition =="first" ? "Por favor insira um valor não inferior ao primeiro. " : "Por favor insira um valor não inferior ao último. " ) ,
"3" : param[2].separate ? "Por favor, assegure a diferença com \"{0}\" não maior que {1}. " : ( param[2].objPosition =="first" ? "Assegure-se de que a diferença com o primeiro não seja maior que {1}. " : "Assegure-se de que a diferença com o primeiro não seja maior que {1}. ")
};
return $.validator.format(tempstring[param[2].ret], param[2].idtext, param[2].discrepantMode);
}
else
{
obj.parent().next().children().hide();
var tmpvalue = obj.val();
var ret = true;
if (param[2].equal)
{
ret = Number(value) >= Number(tmpvalue);
if (!ret)
{
param[2].ret = "2";
return false;
}
}
else
{
ret = Number(value) > Number(tmpvalue);
if (!ret)
{
param[2].ret = "1";
return false;
}
}
if (param[2].discrepantMode)
{
ret = Number(value) - Number(tmpvalue) <= Number(param[2].discrepantMode);
if (!ret)
{
param[2].ret = "3";
return false;
}
}
return true;
}
};
function range_lessThan(obj, value, param, type)
{
if ("errstring" == type )
{
var tempstring = {
"1" : param[2].separate ? "Por favor insira um valor inferior a \"{0}\". " : ( param[2].objPosition == "first" ? "Por favor insira um valor menor do que o anterior. " : "Por favor insira um valor menor do que o último. " ),
"2" : param[2].separate ? "Por favor insira um valor não superior a \"{0}\". " : ( param[2].objPosition == "first" ? "Por favor insira um valor não superior ao primeiro." : "Por favor insira um valor não superior ao último. " ),
"3" : param[2].separate ? "Por favor, assegure a diferença com \"{0}\" não maior que {1}. " : ( param[2].objPosition == "first" ? "Assegure-se de que a diferença com o primeiro não seja maior que {1}. " : "Assegure-se de que a diferença com o primeiro não seja maior que {1}. " )
};
return $.validator.format(tempstring[param[2].ret], param[2].idtext, param[2].discrepantMode);
}
else
{
obj.parent().next().children().hide();
var tmpvalue = obj.val();
var ret = true;
if (param[2].equal)
{
ret = Number(value) <= Number(tmpvalue);
if (!ret)
{
param[2].ret = "2";
return false;
}
}
else
{
ret = Number(value) < Number(tmpvalue);
if (!ret)
{
param[2].ret = "1";
return false;
}
}
if (param[2].discrepantMode)
{
ret = Number(tmpvalue) - Number(value) <= Number(param[2].discrepantMode)
if (!ret)
{
param[2].ret = "3";
return false;
}
}
return true;
}
};
jQuery.validator.addMethod(
"compareRange",
function(value, element, param)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
if (2 > param.length)
{
return true;
}
var obj = get_element_obj($(element), param[1]);
if (3 > param.length)
{
param[2] = {};
}
param[2]["idtext"] = obj.parent().prev().text();
var selectMode = {
"greatThan" : range_greatThan,
"lessThan" : range_lessThan
};
return selectMode[param[0]](obj, value, param);
},
function(param,element)
{
var selectMode = {
"greatThan" : range_greatThan,
"lessThan" : range_lessThan
};
return selectMode[param[0]]("", "", param, "errstring");
}
);
jQuery.validator.addMethod(
"banValue",
function(value, element, param)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
var paramLen = param.length;
for (var i = 0;i < paramLen;i++)
{
var range = param[i];
if (typeof range === 'string' )
{
if (value == range)
{
return false;
}
}
else
{
if (value >= range[0] && value <= range[1])
{
return false;
}
}
}
return true;
},
function(param, element){
var rangesStr = "";
var paramLen = param.length;
for (var i=0; i<paramLen; i++)
{
var paraVal = param[i];
if ( "object" === typeof paraVal )
{
rangesStr += paraVal[0] + "~" + paraVal[1];
}
else
{
rangesStr += paraVal;
}
if ( i < paramLen-1 )
{
rangesStr += ", ";
}
}
if (paramLen > 1)
{
return $.validator.format("Por favor, garantir a entrada não nas faixas de \"{0}\". ", rangesStr);
}
else
{
return $.validator.format("Por favor, garantir a entrada não é igual a \"{0}\". ", rangesStr);
}
}
);
jQuery.validator.addClassRules({
ipSepCheck: {
"required": true,
"integer": true,
"range":[0,255]
},
macSepCheck:{
"required": true,
"HEX": true,
"fixedlength": 2
}
});
function compareIPv4(firstIP, secondIP)
{
var fIP;
var sIP;
fIP = firstIP.split(".");
sIP = secondIP.split(".");
for (var i = 0; i < 4; i++)
{
if (fIP[i] != "" && sIP[i] != "")
{
fIP[i] = parseInt(fIP[i],10);
sIP[i] = parseInt(sIP[i],10);
}
if (fIP[i] > sIP[i])
{
return 1;
}
else if (fIP[i] < sIP[i])
{
return -1;
}
}
return 0;
}
function checkWholeIPv4(k, v, ipValue)
{
var vLen = v.length;
var retMsg = "";
for (var j = 0; j < vLen; j++)
{
if (retMsg != "")
{
retMsg += ", ";
}
var range = v[j];
if (typeof range === 'string')
{
retMsg += range;
}
else
{
retMsg += range[0]+" ~ "+range[1];
}
}
if (k == "banValue")
{
retMsg = "Não é permitido introduzir o seguinte valor (es): {0}. ".format(retMsg);
for (var i = 0; i < vLen; i++)
{
var range = v[i];
if (typeof range === 'string')
{
if (ipValue == range)
{
return [false, k, retMsg];
}
}
else
{
if ("-1" != compareIPv4(ipValue, range[0]) &&
"1" != compareIPv4(ipValue, range[1]))
{
return [false, k, retMsg];
}
}
}
}
else if (k == "allowRange")
{
retMsg = "Entrada inválida. Por favor, certifique-se de que a entrada esteja no seguinte intervalo: {0}. ".format(retMsg);
for (var i = 0; i < vLen; i++)
{
var range = v[i];
if ("-1" != compareIPv4(ipValue, range[0]) &&
"1" != compareIPv4(ipValue, range[1]))
{
return [true, "", ""];
}
}
return [false, k, retMsg];
}
else if (k == "notLessThan")
{
}
else if (k == "notMoreThan")
{
}
else
{
}
return [true, "", ""];
}
function checkWholeMac(k, v, macValue)
{
var vLen = v.length;
var retMsg = "";
for (var j = 0; j < vLen; j++)
{
if (retMsg != "")
{
retMsg += ", ";
}
var range = v[j];
if (typeof range === 'string')
{
retMsg += range;
}
else
{
retMsg += range[0]+" ~ "+range[1];
}
}
if (k == "banValue")
{
retMsg = "Não é permitido introduzir o seguinte valor (es): {0}. ".format(retMsg);
for (var i = 0; i < vLen; i++)
{
var range = v[i];
if (typeof range === 'string')
{
if (macValue.toLowerCase() == range.toLowerCase())
{
return [false, k, retMsg];
}
}
}
}
else
{
}
return [true, "", ""];
}
function getMsgofWholeMACIPCheck(checkRetArray, ruleObj, checkValue, checkParaName)
{
var errMsg = "";
switch (checkRetArray[1])
{
case "banValue":
{
if (ruleObj.messages.banValue != undefined)
{
errMsg = ruleObj.messages.banValue;
}
else
{
if (checkParaName != "")
{
errMsg = checkParaName + checkRetArray[2];
}
else
{
errMsg = "A operação atual é inválida, por favor, verifique os parâmetros de configuração."+"["+"Erro:"+checkValue+"]";
}
}
break;
}
case "allowRange":
{
if (ruleObj.messages.allowRange != undefined)
{
errMsg = ruleObj.messages.allowRange;
}
else
{
if (checkParaName != "")
{
errMsg = checkParaName + checkRetArray[2];
}
else
{
errMsg = "A operação atual é inválida, por favor, verifique os parâmetros de configuração."+"["+"Erro:"+checkValue+"]";
}
}
break;
}
default:
{
errMsg = "error msg undefined!"
}
}
return errMsg;
}
jQuery.validator.addMethod(
"utf8LengthRange",
function(value, element, param)
{
if ( this.optional(element) )
{
return "dependency-mismatch";
}
var valLength = value.length;
var param1 = param[0];
var param2 = param[1];
if (param2 < 3)
{
alert("utf8LengthRange is invalid!["+param2+"<"+3 +"]");
}
else
{
param1 = Math.ceil(parseInt(param[0])/ 3);
param2 = Math.floor(parseInt(param[1]) / 3);
if (param1 < param2)
{
if (valLength >= param1 && valLength <= param2 )
{
return true;
}
}
else if (param1 == param2)
{
if (valLength == param2)
{
return true;
}
}
else
{
alert("utf8LengthRange ["+param1+","+param2+"] is invalid!");
}
}
return false;
},
function(param, element){
var lengthStr = "";
var param1 = param[0];
var param2 = param[1];
if (param2 < 3)
{
lengthStr = " Range Error!!!!!![param2<WEB_UTF8_REALBYTE]";
}
else
{
param1 = Math.ceil(parseInt(param[0])/ 3);
param2 = Math.floor(parseInt(param[1]) / 3);
if (param1 < param2)
{
lengthStr = param1 + " ~ " + param2;
}
else if (param1 == param2)
{
lengthStr = param2;
}
else
{
lengthStr = " Range Error!!!!!!["+param1+","+param2+"]";
}
}
return $.validator.format("Por favor insira um valor com {0} caracteres.", lengthStr);
}
);

(function(){
$(document).ready(function(){
var curv = 163;
if (curv == "65")
$("#languageSwitch").hide();
});
})();


var menuTreeJSON = [{"id":"status","name":"Estado"},{"id":"wlan","name":"Wi-Fi"},{"id":"mgrAndDiag","name":"Gestão"}];
var menuTreeObj = new MenuTreeClass(menuTreeJSON);
var _sessionTmpToken = "";


if(top != self)
{
document.getElementsByTagName("body")[0].style.display = 'none';
top.location = self.location;
}
function LogOff()
{
showWaitTip(true);
$.post( "/?_type=loginData&_tag=logout_entry", {IF_LogOff:1, _sessionTOKEN:_sessionTmpToken}, undefined, "json" )
.done(function( data ) {
if ( data.need_refresh )
{
top.location.href = top.location.href;
}
else
{
alert("Esta página expirou, por favor, atualize e tente novamente. ");
showWaitTip(false);
}
});
}
function LogUser()
{
openLink("accountMgr" + "&Menu3Location=0");
}



var loginLockInterval = null;
var editableInputs;
var dftFcsTaget;
var IsAllowedSubmit = true;
var IPAccess = "";
function createTimeCountDownMessage(lockingTime, promptMsg)
{
if((promptMsg != null && promptMsg.length > 0) || lockingTime > 0 )
{

var timeOutHint = promptMsg.concat("Por favor, tente novamente após {1} segundos. ");
$("#login_error_waittime").text(timeOutHint.format(3,lockingTime)).show();
}
else
{
$("#login_error_waittime").hide();
}
}
function timer(seconds, promptMsg) {
window.setTimeout(function() {
editableInputs.removeAttr("disabled");
if(dftFcsTaget){
dftFcsTaget.focus();
}
$("#LoginId").removeAttr("disabled").removeClass("disableBtn");
$("#login_error").hide();
$("#login_error_waittime").hide().text("");
if (loginLockInterval) {
window.clearInterval(loginLockInterval);
consoleLog("timeout to clearInterval!!!");
}
}, seconds * 1000);
loginLockInterval = window.setInterval((function(sec, msg){
return function () {
if (sec > 0){
sec--;
}
createTimeCountDownMessage(sec, msg);
}
})(seconds, promptMsg), 1000);
}
function showTimeCountDown(lockingTime, promptMsg)
{
if(lockingTime > 0)
{
createTimeCountDownMessage(lockingTime, promptMsg);
$("#LoginId").attr("disabled","true").addClass("disableBtn");
editableInputs.attr("disabled","true");
timer(lockingTime, promptMsg);
}
}
function DisplayLoginErrorTip(loginData)
{
var loginErrMsg = loginData.loginErrMsg;
var lockingTime = loginData.lockingTime;
var promptMsg = loginData.promptMsg;
lockingTime = parseInt(lockingTime);
if ( IsBrowserSupportCookie() == false )
{
$("#login_error").show();
$("#login_error_span").text("A funcionalidade de cookies do seu navegador está desativada, por favor, ligue-o antes de fazer login.");
}
else if(loginErrMsg.length > 0 || promptMsg.length > 0)
{
$("#login_error").show();
if(loginErrMsg.length > 0)
{
$("#login_error_span").text(loginErrMsg).show();
}
else
{
$("#login_error_span").hide();
}
if (lockingTime > 0 || promptMsg.length > 0)
{
showTimeCountDown(lockingTime, promptMsg);
}
}
else
{
$("#login_error").hide();
}
}
function g_loginToken(xml)
{
var xmlObj = $(xml).text();
var Password =$("#Frm_Password").val();
var SHA256Password =sha256(Password+xmlObj);
var postData = {};
postData["action"] = "login";
postData["Password"] = SHA256Password;
postData["Username"] = $("#Frm_Username").val();
postData["_sessionTOKEN"] = $("#_sessionTOKEN").val();
Password = undefined;
SHA256Password = undefined;
$.post( "/?_type=loginData&_tag=login_entry", postData, undefined, "json" )
.done(function( data ) {
$("#_sessionTOKEN").val(data.sess_token);
if ( data.login_need_refresh )
{
top.location.href = top.location.href;
}
else
{
DisplayLoginErrorTip(data);
}
});
postData = undefined;
}
var throttle = function (fn, delay, atleast) {
var timer = null, previous = null;
return function () {
var context = this, args = arguments, now = +new Date();
if (!previous) {previous = now;}
if (now - previous > atleast) {
fn.apply(context, args);
previous = now;
} else {
clearTimeout(timer);
timer = setTimeout(function() {
fn.apply(context, args);
}, delay);
}
}
};
$(document).ready(function(){
var loginForm = $(".loginInstCfgArea");
editableInputs = $("input",loginForm).not(":disabled").not("[readonly=readonly]");
$.getJSON("/?_type=loginData&_tag=login_entry")
.done(function( json ) {
$("#_sessionTOKEN").val(json.sess_token);
DisplayLoginErrorTip(json);
})
.fail(function( jqxhr, textStatus, error ) {
var err = textStatus + ", " + error;
consoleLog( "Request Failed: " + err );
});
editableInputs.each(function(){
if ($(this).val() == "") {
$(this).focus();
dftFcsTaget = $(this);
return false;
}
});
$("#LoginId").bind("click", throttle(function(){
if ( true == IsAllowedSubmit )
{
var loadAllowAddr = "/?_type=loginData&_tag=login_token";
$(this).dataTransfer(loadAllowAddr, "GET", g_loginToken, undefined, false);
}
}, 300, 300));
editableInputs.keydown(function(event){
if(event.keyCode==13){
event.preventDefault();
event.stopPropagation();
$("#LoginId").click();
}
});
});
var ssidConf = {};
var commConf = {};
var lanConf = {};

commConf = JSON.parse('{"ShowFakeClass1Menu":true,"redAuthentication":false,"miniolt":"RoomPONInfo_002","pdtVer":{"SoftwareVer":"show","WEBTitle":"show"},"broadwiseTopo":false,"QosMenu":false,"PortForwarding":[],"fwPortServHidden":"","ValidateCode":false,"TopoV2Layer":"3","pon":{"snPwdCheck":"PasswordASCII","loidPwdCheck":"PasswordASCII"},"elementControl":[],"webEnable":true,"errTipWarp":"","setEncode":true,"passLength":8,"template":"","devInfo":{"SN":"OUI+SN"},"serviceCtl":[],"ChgpwdStrong":false,"IntegCheck":true,"DHCPpage":"whole","timeArea":"","passCanSee":"","loginErrCustom":"login_029","language":[],"getEncode":true,"diagnose":{"ping":0,"trace":0,"speedtest":0,"simulate":0},"wizard":[],"oneWholePage":[]}');
if (!commConf.dataSave)
{
commConf.dataSave = 2000;
}
lanConf = JSON.parse('[]');
String.prototype.format = function(args) {
var result = this;
if (arguments.length > 0)
{
for (var i = 0; i < arguments.length; i++)
{
if (arguments[i] != undefined) {
var reg = new RegExp("({[" + i + "]})", "g");
result = result.replace(reg, arguments[i]);
}
}
}
return result;
};
function showOrHideRowDiv()
{
if (arguments.length < 2)
{
return;
}
var action = arguments[0];
for(var i = 1; i < arguments.length; i++)
{
var subWidget = arguments[i].find("*[id!='']")
if ( action == "show" )
{
arguments[i].showIt(true);
subWidget.removeClass("PostIgnore");
}
else
{
arguments[i].showIt(false);
subWidget.addClass("PostIgnore");
}
}
}
function colonStripping(str)
{
var colonLocation = str.indexOf(":");
if ( colonLocation != -1 )
{
return str.substring(0, colonLocation);
}
return str;
}
function colonStrippingLast(str)
{
var colonLocation = str.lastIndexOf(":");
if ( colonLocation != -1 )
{
return str.substring(0, colonLocation);
}
return str;
}
function randomNum(n){
var t='';
for(var i=0;i<n;i++)
{
t+=Math.floor(Math.random()*10);
}
return t;
}
function checkPassStrong(sz)
{
if(/[a-z]/.test(sz) && /[A-Z]/.test(sz) && /[0-9]/.test(sz) && (sz.length >= 8))
{
return true;
}
return false;
}
function asyEncode(srcStr)
{
var pubKey = "-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwlo/vZBnSJ2MyJ0dbNcw\nDvzPqBN+O/BPvLX93GIJVSZmquJHD9X6Xn6VYeM9mRKzjEbXPlv73Dj/gjjtNj9j\nTq2QVyW2Sd4ZkY9e3h1ALCCCfkbjnmSqedyrcvXriTeW+J65jhBje6lTJbafmC5q\nbGiItjt0OeOkT+Vb4S7hYPSWIjeYYBh+7Y/fg25Rt2a+RgC8dahvJ3ttB1LHXADr\noCm6q7G+lpbRAlpC8jjc0rZdS0c6HcBoYgzW8vxjj2fTuFy3CZZTrpPyTv/C8K6B\nhjTnjRe6ocgFVyQ0RIYfx2hxSJcuauR57OzfMzlgFQv3RAXguDZtuVUFLO2sAiwL\nELph3Acfy9Eh58SHcswZvsOSXY0JNb0XeRM9gxpntLRfM6TB7f9hYtYTDw5oKdyN\nBY+nnEa/IpBUjndGDrSs3Z4BxRbYcJEwkKQZkvw/5TpQYbkD6sTRVSlZPaXSjeCl\n0hsLCttqwJqRZcjbWXrINBYFw8PYE14Xr9BCyPgqocdQh7FgvasVgG6u5mLR1PBZ\no4EFF/LdY0yvMG5rl9egBk1XD/UMayhRtmSQEUzYt3eEWLBbqJB6MbVJ2ygcv5EL\nReDY0SWXw1PIEbHeP51A/MyB6kwSgZwdoQW3JiaPnGHMaE0NqfAYPNiGJLMsmvT/\nrNUI/8iSCW+WvSzx9tByUxsCAwEAAQ==\n-----END PUBLIC KEY-----";
var encrypt = new JSEncrypt();
encrypt.setPublicKey(pubKey);
var encrypted = encrypt.encrypt(srcStr);
var dstStr = encrypted.toString();
if(dstStr.length == 0 || dstStr == "false")
{
console.log("encrypt key fail!");
dstStr = "";
}
return dstStr;
}
function encodeKey(key,iv)
{
var kv = key + "+" + iv;
return asyEncode(kv);
}
function encodeParaValue(src,key,iv)
{
if(src.length > 0)
{
var bKey = CryptoJS.SHA256(key);
var bIv = CryptoJS.SHA256(iv);
var encrypted =CryptoJS.AES.encrypt(src,bKey,
{
iv:bIv,
mode:CryptoJS.mode.CBC,
padding:CryptoJS.pad.ZeroPadding
});
var dst = encrypted.toString();
if(dst != "" && dst != "failed")
{
return dst;
}
}
return src;
}
function decodeParaValue(src,key,iv)
{
if(src.length > 0)
{
var bKey = CryptoJS.SHA256(key);
var bIv = CryptoJS.SHA256(iv);
var decrypted =CryptoJS.AES.decrypt(src,bKey,
{
iv:bIv,
mode:CryptoJS.mode.CBC,
padding:CryptoJS.pad.ZeroPadding
});
var dst = decrypted.toString(CryptoJS.enc.Utf8);
if(dst != "" && dst != "failed")
{
return dst;
}
}
return src;
}
function getDecodeValue(data)
{
var key = _sessionTmpToken;
var iv = key.split("").reverse().join("");
return decodeParaValue(data,key,iv);
}
jQuery.fn.showIt = function(show) {
if (show)
{
$(this).css("display", "");
}
else
{
$(this).css("display", "none");
}
};
jQuery.fn.disableIt = function(disable) {
if (disable)
{
$(this).attr("disabled", "disabled");
$(this).addClass("PostIgnore");
}
else if( undefined == $(this).attr("hideattr") )
{
$(this).prop("disabled", "");
$(this).removeClass("PostIgnore");
}
};
jQuery.fn.disableButton = function(disable) {
if (disable)
{
$(this).addClass("disableBtn");
}
else if( undefined == $(this).attr("hideattr"))
{
$(this).removeClass("disableBtn");
}
};
function GetSuffixedIDorName(oldValue, suffix, splitter, forParaName)
{
var newValue = "";
if ( forParaName == true )
{
oldValue = oldValue.split(":");
oldValue[0] += splitter + suffix;
newValue = oldValue.join(":");
}
else
{
newValue = oldValue + splitter + suffix;
}
return newValue;
}
jQuery.fn.cloneWithSuffix = function(suffix, splitter, forParaName) {
var source = $(this);
var clone = source.clone(true);
clone.attr("id", clone.attr("id")+"_"+suffix);
if ( undefined == splitter )
{
splitter = ":";
}
if ( undefined == forParaName )
{
forParaName = false;
}
var idElems = clone.find("*[id!='']");
idElems.each(function(){
var idEle = $(this);
var oldID = idEle.attr("id");
if (oldID != undefined)
{
var newID = GetSuffixedIDorName(oldID, suffix, splitter, forParaName);
idEle.attr("id", newID);
}
var oldName = idEle.attr("name");
if (oldName != undefined)
{
var newName = GetSuffixedIDorName(oldName, suffix, splitter, forParaName);
idEle.attr("name", newName);
}
});
labelForElems = clone.find("label");
labelForElems.each(function(){
var labelForEle = $(this);
var oldFor = labelForEle.attr("for");
if (oldFor != undefined)
{
var newFor = GetSuffixedIDorName(oldFor, suffix, splitter, forParaName);
labelForEle.attr("for", newFor);
}
});
clone.trigger("applyPromptCheckJSON", [clone]);
return clone;
};
function initial_sceneTip()
{
$(".sceneTip_container").each(function(){
$(this).hide();
});
$(".sceneTipLink").each(function(){
var sceneTipLinkContent = $(this).children();
sceneTipLinkContent.unbind( "click" );
sceneTipLinkContent.click(function(event){
event.preventDefault();
$(this).parent().next().slideToggle("normal");
});
});
$(".sceneTip_close").each(function(){
var sceneTip_closeLink = $(this).children();
sceneTip_closeLink.unbind( "click" );
sceneTip_closeLink.click(function(){
$(this).parent().parent().slideUp("normal");
});
});
}
function succHintShow(template)
{
var PostFeedbackOBJ = $(".succHint",template);
PostFeedbackOBJ.fadeIn(1000);
window.setTimeout(
function() {
PostFeedbackOBJ.fadeOut(1000);
PostFeedbackOBJ.hide();
},
commConf.dataSave
);
}
jQuery.fn.dataTransfer = function(URL, transferType, success_func, error_func, IfShowWaitTip, async, dataType){
if ( !URL || URL == "" )
{
consoleLog("[dataTransfer]URL is illegal!");
return;
}
var IfShowWaitTipTmp = IfShowWaitTip;
if ( IfShowWaitTipTmp == undefined )
{
IfShowWaitTipTmp = true;
}
var asyncTemp = async;
if ( asyncTemp == undefined )
{
asyncTemp = true;
}
if ( IfShowWaitTipTmp == true )
{
showWaitTip(true);
}
var Head = $(this);
$.ajax({
url:URL,
type: transferType,
timeout: 30000,
async: asyncTemp,
cache:false,
error: function(){
if ($.isFunction(error_func))
{
error_func();
}
else
{
if (Head != undefined)
{
var ajaxTransferFailHint = "O servidor não está disponível agora. Atualize a página para recarregar. ";
var externErrorHint = $(".externErrorHint",Head);
if ( externErrorHint != undefined )
{
$("span",externErrorHint).text(ajaxTransferFailHint);
externErrorHint.showIt(true);
}
}
showWaitTip(false);
}
},
success: function(data){
success_func(data);
if ( IfShowWaitTipTmp == true )
{
showWaitTip(false);
}
}
});
};
function HTMLEnCode(str)
{
var s = "";
if (typeof(str) != "string")
{
return str;
}
if(str.length == 0)
{
return "";
}
s = str.replace(/&/g, "&#38;");
s = s.replace(/</g, "&#60;");
s = s.replace(/>/g, "&#62;");
s = s.replace(/ /g, "&#32;");
s = s.replace(/\'/g, "&#39;");
s = s.replace(/\"/g, "&#34;");
return s;
}
function addSlash(srcStr)
{
var str = "";
var ch = "";
if (typeof(srcStr) != "string")
{
return srcStr;
}
for(var i = 0; i < srcStr.length; i++)
{
ch = srcStr.substr(i, 1);
if( "\\" == ch )
{
ch = "\\\\";
}
else if( "\'" == ch )
{
ch = "\\\'";
}
else if( "\"" == ch )
{
ch = "\\\"";
}
str = str + ch;
}
return str;
}
function SetSelectValue(SelectElem, data)
{
$("option[class='_optExpHandle']", SelectElem).remove();
var findOption = 0;
$("option", SelectElem).removeAttr("selected");
$("option", SelectElem).each(function(){
var OptionObj = $(this);
if ( OptionObj.val() == data )
{
findOption = 1
return false;
}
});
if ( findOption == 0 )
{
SelectElem.append("<option value='"+ HTMLEnCode(data)
+ "' title='--Desconhecido--' class='_optExpHandle'>"
+ "--Desconhecido--" + "</option>");
}
SelectElem.val(data);
}
jQuery.fn.fillDataByType = function(data){
var Elems = $(this);
if (Elems.is("input"))
{
switch (Elems.attr("type"))
{
case "hidden":
{
if( commConf.getEncode && Elems.attr("encode") == "1")
{
data = getDecodeValue(data);
}
Elems.val(data);
if (Elems.attr("_LuQUID_splitMACID") != undefined)
{
var splitMACID = Elems.attr("_LuQUID_splitMACID");
Elems.FillIPorMacDataBySplit(splitMACID, ":", 6);
}
else if (Elems.attr("_LuQUID_splitIPID") != undefined)
{
var splitIPID = Elems.attr("_LuQUID_splitIPID");
Elems.FillIPorMacDataBySplit(splitIPID, ".", 4);
}
break;
}
case "text":
case "password":
{
if( commConf.getEncode && Elems.attr("encode") == "1")
{
data = getDecodeValue(data);
}
Elems.val(data);
if (typeof(Elems.attr("title")) != "undefined")
{
Elems.attr("title", data);
}
break;
}
case "checkbox":
{
if( 1 == data )
{
Elems.prop("checked", true);
}
else
{
Elems.prop("checked", false);
}
Elems.val(data);
break;
}
default:
{
break;
}
}
}
else if (Elems.is("span"))
{
if( commConf.getEncode && Elems.attr("encode") == "1")
{
data = getDecodeValue(data);
}
Elems.text(data);
if (typeof(Elems.attr("title")) != "undefined")
{
Elems.attr("title", data);
}
}
else if (Elems.is("a"))
{
Elems.text(data);
Elems.attr("href",data);
}
else if (Elems.is("select"))
{
SetSelectValue(Elems, data);
}
else if (Elems.is("textarea"))
{
Elems.val(data);
}
else if (Elems.is("label"))
{
Elems.text(data);
}
else if (Elems.is("div"))
{
var radioObj = $("input[type=radio]", Elems);
radioObj.each(function(){
var thisObj = $(this);
if (thisObj.val() == data)
{
thisObj.prop("checked", true);
}
else
{
thisObj.prop("checked", false);
}
});
}
else if (Elems.is("td"))
{
if( commConf.getEncode && Elems.attr("encode") == "1")
{
data = getDecodeValue(data);
}
Elems.text(data);
if (typeof(Elems.attr("title")) != "undefined")
{
Elems.attr("title", data);
}
}
else
{
}
};
function fillEncodeAttr(data, OBJIDs, Clone)
{
if ($.isPlainObject(data))
{
$.each(OBJIDs,function(i,obj){
if(data[obj] != undefined && data[obj]["encode"] != undefined)
{
var encodePara= data[obj]["encode"].split(",");
for(var i in encodePara)
{
$("input[id^="+encodePara[i]+"]", Clone).attr("encode","1");
}
}
});
}
else
{
$(data).find("encode").each(function(){
var encodePara= $(this).text().split(",");
for(var i in encodePara)
{
$("input[id^="+encodePara[i]+"]", Clone).attr("encode","1");
}
});
}
}
function fillDataWithXML(data, OBJIDs, Clone, suffix, splitter)
{
for (var i=0; i<OBJIDs.length; i++)
{
var OBJID = OBJIDs[i];
var OBJIDSplit = OBJID.split(":");
var OBJIDIndex = 0;
var isSplitterExist = 0;
if ( OBJIDSplit.length == 2 )
{
OBJID = OBJIDSplit[0];
OBJIDIndex = parseInt(OBJIDSplit[1]);
isSplitterExist = 1;
}
var OBJs = $(data).find(OBJID);
if ( OBJs.length == 0 )
{
continue;
}
var OBJ;
if ( OBJIDIndex < OBJs.length )
{
OBJ = OBJs.get(OBJIDIndex);
}
else
{
continue;
}
var instances;
if ( 1 == isSplitterExist )
{
instances = $("Instance", OBJ);
}
else
{
instances = $("Instance", OBJs);
}
if ( instances.length <= suffix
|| suffix < 0 )
{
consoleLog("suffix off normal upper!!");
continue;
}
var InstOBJ = instances.eq(suffix);
InstOBJ.find("ParaName").each(function(){
var ParaName = $(this).text();
var ParaValue = $(this).next().text();
var Elems = $("[id^='"+ParaName+splitter+"']", Clone);
if ( Elems.length == 0 )
{
Elems = $("[id='"+ParaName+"']", Clone);
}
if ( Elems.length > 0 )
{
if ( Elems.length > 1 )
{
consoleLog("this ele id is duplicate[" +Elems.attr("id")+ "]");
}
Elems.fillDataByType(ParaValue);
}
else
{
if ( "_InstID" != ParaName )
{
consoleLog("XML ParaName("+ParaName+") cannot map to HTML "
+ "by fillDataByType, so it may be useless, "
+ "web security require deleting it!");
}
}
});
}
}
function fillDataWithJSON(data, OBJIDs, Clone, suffix, splitter)
{
for (var i=0; i<OBJIDs.length; i++)
{
var OBJID = OBJIDs[i];
var OBJIDSplit = OBJID.split(":");
var OBJIDIndex = 0;
var isSplitterExist = 0;
if ( OBJIDSplit.length == 2 )
{
OBJID = OBJIDSplit[0];
isSplitterExist = 1;
}
var OBJs = $(data).find(OBJID);
if ( data[OBJID] == undefined )
{
continue;
}
var instances = data[OBJID]["Instance"];
if ( instances.length <= suffix
|| suffix < 0 )
{
consoleLog("suffix off normal upper!!");
continue;
}
var InstOBJ = instances[suffix];
for (var key in InstOBJ)
{
var ParaName = key;
var ParaValue = InstOBJ[key];
var Elems = $("[id^='"+ParaName+splitter+"']", Clone);
if ( Elems.length == 0 )
{
Elems = $("[id='"+ParaName+"']", Clone);
}
if ( Elems.length > 0 )
{
if ( Elems.length > 1 )
{
consoleLog("this ele id is duplicate[" +Elems.attr("id")+ "]");
}
Elems.fillDataByType(ParaValue);
}
else
{
if ( "_InstID" != ParaName )
{
consoleLog("json ParaName("+ParaName+") cannot map to HTML "
+ "by fillDataByType, so it may be useless, "
+ "web security require deleting it!");
}
}
}
}
}
function fillData(data, OBJIDs, Clone, suffix, splitter)
{
if ($.isPlainObject(data))
{
fillDataWithJSON(data, OBJIDs, Clone, suffix, splitter);
}
else
{
fillDataWithXML(data, OBJIDs, Clone, suffix, splitter);
}
}
jQuery.fn.fillDataByOBJID = function(data, OBJIDs, Clone, suffix, splitter){
if ( undefined == splitter )
{
splitter = ":";
}
fillEncodeAttr(data, OBJIDs, Clone);
fillData(data, OBJIDs, Clone, suffix, splitter);
$(".SpecialPassword", Clone).each(function(i){
$(this).val("						");
});
};
jQuery.fn.InstantializeForTemplateBox = function(data, OBJIDs, container){
for (var i=0; i<OBJIDs.length; i++)
{
var OBJID = OBJIDs[i];
var OBJs = $(data).find(OBJID);
if ( OBJs.length == 0 )
{
continue;
}
var ruleTemplate = $("[id='"+OBJID+"']._LuQuid_TempalteBox", container);
if( ruleTemplate.length == 0 )
{
continue;
}
$("[id^='"+OBJID+"_']._LuQuid_TempalteBox", container).remove();
var subWidget = ruleTemplate.find("*[id!='']");
subWidget.removeClass("PostIgnore");
var instances = $("Instance", OBJs);
var ruleNum = instances.length;
for (var i=0; i<ruleNum; i++)
{
var clone = ruleTemplate.cloneWithSuffix(i, "_", true);
ruleTemplate.before(clone);
var DataOBJID = [OBJID];
clone.fillDataByOBJID(data, DataOBJID, clone, i, "_");
clone.showIt(true);
}
$("[id='"+OBJID+"._OBJ_InstNUM']", container).val(ruleNum);
var templateInstID = $("[id='"+OBJID+"._OBJ_InstID']", container);
templateInstID.addClass("PostIgnore");
subWidget.addClass("PostIgnore");
}
};
jQuery.fn.FillDataOnlyForTemplateBox = function(data, OBJIDs, container){
for (var i=0; i<OBJIDs.length; i++)
{
var OBJID = OBJIDs[i];
var OBJs = $(data).find(OBJID);
if ( OBJs.length == 0 )
{
continue;
}
var ruleTemplate = $("[id='"+OBJID+"']._LuQuid_TempalteBox", container);
if( ruleTemplate.length == 0 )
{
continue;
}
$("[id^='"+OBJID+"_']._LuQuid_TempalteBox", container).each(function(){
var instObj = $(this);
var instId = instObj.find("[id^='"+OBJID+"._OBJ_InstID']").val();
var index = -1;
var instances = $("Instance", OBJs);
var ruleNum = instances.length;
for (var i=0; i<ruleNum; i++)
{
var instIdName = OBJID+"._OBJ_InstID";
var ToOperParaArray = {};
ToOperParaArray[instIdName] = {
ValueOrigin: ""
};
xmlParaInInstOperate(data, OBJID, i, ToOperParaArray);
var ruleInstId = ToOperParaArray[instIdName].ValueOrigin;
if ( instId == ruleInstId )
{
index = i;
break;
}
}
if ( index > -1 )
{
var DataOBJID = [OBJID];
instObj.fillDataByOBJID(data, DataOBJID, instObj, index, "_");
}
else
{
consoleLog("instId("+instId+") cannot match xml instance");
}
});
}
};
jQuery.fn.createPageDataByClone = function(RuleNum,DataOBJID,data,fillDataByCustom){
var Head = $(this);
var HeadID = Head.attr("id");
var TemplateOBJ = $("#template_"+HeadID , Head);
$("#_InstNum", Head).val(RuleNum);
for (var i=0; i<RuleNum; i++)
{
var clone = TemplateOBJ.cloneWithSuffix(i);
TemplateOBJ.before(clone);
clone.fillDataByOBJID(data ,DataOBJID, clone, i);
if ( $.isFunction(fillDataByCustom) )
{
fillDataByCustom(i,clone);
}
else
{
clone.trigger("fillDataByCustom",[i,clone]);
}
clone.showIt(true);
}
};
jQuery.fn.hasError = function(data, location){
var ContentContainer = $(this);
var cmapiErrorContainer;
var ErrorString = "";
var ErrorParam = "";
if ($.isPlainObject(data))
{
if (data.IF_ERRORSTR == undefined || data.IF_ERRORPARAM == undefined)
{
consoleLog("[hasError:]json cannot find IF_ERRORSTR or IF_ERRORPARAM");
return 1;
}
ErrorString = data.IF_ERRORSTR;
ErrorParam = data.IF_ERRORPARAM;
}
else
{
if ($("IF_ERRORSTR", $(data)).length <= 0 || $("IF_ERRORPARAM", $(data)).length <= 0)
{
consoleLog("[hasError:]xml cannot find IF_ERRORSTR or IF_ERRORPARAM");
return 1;
}
ErrorString = $("IF_ERRORSTR", $(data)).text();
ErrorParam = $("IF_ERRORPARAM", $(data)).text();
}
if (!location)
{
location = "errorHint";
}
if (location == "externErrorHint")
{
cmapiErrorContainer = $(".externErrorHint",ContentContainer);
}
else
{
cmapiErrorContainer = $("."+location,ContentContainer);
}
if ( ErrorString == "SUCC" )
{
cmapiErrorContainer.showIt(false);
return 0;
}
else if ( ErrorString == "SessionTimeout" )
{
top.location.href = top.location.href;
return 1;
}
else
{
var cmapiErrorContainerHtml = "";
var paraString = "";
if ( ErrorParam != "SUCC")
{
var LabelFindResult = 0;
ErrorString = "Operação atual é inválido, verifique se {0} é legal. "
var paraLabel = ContentContainer.find("label[for^='"+ErrorParam+"\\:']");
if ( paraLabel.length <= 0 )
{
paraLabel = ContentContainer.find("label[for='"+ErrorParam+"']");
}
if ( paraLabel.length > 0 )
{
paraLabel.each(function(){
var labelTmp = $(this);
if ( !labelTmp.hasClass("error"))
{
paraString = labelTmp.text();
LabelFindResult = 1;
return false;
}
});
}
if ( LabelFindResult == 0 )
{
ErrorString = "A operação atual é inválida, por favor, verifique os parâmetros de configuração.";
}
cmapiErrorContainerHtml = ErrorString.format(paraString);
}
else
{
if ( "FAIL" == ErrorString
|| "Operação atual é inválido, verifique se {0} é legal. " == ErrorString )
{
ErrorString = "A operação atual é inválida, por favor, verifique os parâmetros de configuração.";
}
cmapiErrorContainerHtml = ErrorString;
}
$("span",cmapiErrorContainer).text(cmapiErrorContainerHtml);
cmapiErrorContainer.showIt(true);
return 1;
}
};
jQuery.fn.ShouldPostIgnore = function(){
if($(this).hasClass("PostIgnore"))
{
return true;
}
return false;
};
jQuery.fn.InitialPostData = function(actionType){
var AND = "&";
var template = $(this);
var PostData = "IF_ACTION=" + actionType;
var cryptoKey = randomNum(16);
var cryptoIv = randomNum(16);
var needEncode = false;
var formInputContent = template.find("input,select,textarea");
formInputContent.each(function(key){
var Elems = $(this);
if ( Elems.ShouldPostIgnore() )
{
if ( Elems.attr("encode") == "1" )
{
needEncode = true;
}
return true;
}
var ElemsID = Elems.attr("id");
if (typeof(ElemsID) != "string") {
return true;
}
if ( Elems.attr("type") == "radio" )
{
if ( Elems.is(':checked') )
{
ElemsID = Elems.attr("name");
}
else
{
return true;
}
}
var ElemsMainID = colonStripping(ElemsID);
var ElemsValue = "";
if ( Elems.is("input") )
{
switch (Elems.attr("type"))
{
case "hidden":
{
if (Elems.attr("_LuQUID_splitMACID") != undefined)
{
var splitMACID = Elems.attr("_LuQUID_splitMACID");
Elems.FillIPorMacDataCombination(splitMACID, ":", 6);
}
else if (Elems.attr("_LuQUID_splitIPID") != undefined)
{
var splitIPID = Elems.attr("_LuQUID_splitIPID");
Elems.FillIPorMacDataCombination(splitIPID, ".", 4);
}
ElemsValue = Elems.val();
if(commConf.setEncode && Elems.attr("encode") == "1")
{
ElemsValue = encodeParaValue(ElemsValue,cryptoKey,cryptoIv);
needEncode = true;
}
break;
}
case "text":
case "password":
case "radio":
{
ElemsValue = Elems.val();
if(commConf.setEncode && Elems.attr("encode") == "1")
{
ElemsValue = encodeParaValue(ElemsValue,cryptoKey,cryptoIv);
needEncode = true;
}
break;
}
case "checkbox":
{
if( Elems.is(':checked'))
{
ElemsValue = 1;
}
else
{
ElemsValue = 0;
}
break;
}
default:
{
break;
}
}
}
else if ( Elems.is("select") )
{
ElemsValue = Elems.val();
}
else if( Elems.is("textarea") && Elems.attr("needPost") == "needPost" )
{
ElemsValue = Elems.val();
}
else
{
consoleLog("when create post data, find not support elements type!!");
}
var NameValueJson = {
"ElemsMainID": ElemsMainID,
"ElemsValue": ElemsValue
};
template.trigger("PostDataChangeByCustom",[NameValueJson,template]);
var RealElemsValue = encodeURIComponent(NameValueJson.ElemsValue);
PostData += AND + ElemsMainID + "=" + RealElemsValue;
});
if(needEncode)
{
PostData += AND + "encode=" + encodeURIComponent(encodeKey(cryptoKey,cryptoIv));
}
return PostData;
};
function RefreshClickHandle(Head)
{
$(".Btn_refresh", Head).each(function(){
$(this).unbind("click");
$(this).bind("click", function(){
var buttonOBJ = $(this);
if (buttonOBJ.hasClass("disableBtn")
||buttonOBJ.hasClass("disableLongBtn"))
{
return;
}
var HeadID = Head.attr("id");
Head.find("[id^='template_"+HeadID+"_']").each(function(){
$(this).remove();
});
var ServerAddr = $("address span", Head).text();
Head.dataTransfer(ServerAddr,
"GET",
Head.succfunction,
Head.failfunction,
undefined,
true);
});
})
}
function initialStatusArea(Head)
{
if ( 0 == $("._LuQUID_STATUS_OBJID", Head).length )
{
return;
}
var OBJID = [];
var OBJDOMs = $("._LuQUID_STATUS_OBJID>li", Head);
OBJDOMs.each(function(){
var identity = $(this).text();
OBJID.push(identity);
})
var isMultiInst = $(".maxInstNum", Head).val();
var ServerAddr = $("address span", Head).text();
Head.succfunction = function(data){
if (Head.hasError(data,"externErrorHint") == 0)
{
Head.trigger("changeXMLDataBeforeFillData", [data]);
var XMLOBJ = $(data).find(OBJID[0]);
var RuleNum = $("Instance", XMLOBJ).length;
if (RuleNum == 0)
{
$(".noDataHint",Head).showIt(true);
$(".form_content",Head).showIt(false);
}
else
{
$(".noDataHint",Head).showIt(false);
$(".form_content",Head).showIt(true);
if (isMultiInst == 0)
{
Head.fillDataByOBJID(data ,OBJID, Head, 0);
Head.trigger("fillDataByCustom",[0, Head]);
var template = $("[id^='template_']", Head);
template.trigger("fillDataByCustom",[0, template]);
template.showIt(true);
}
else
{
Head.fillDataByCustom = undefined;
Head.createPageDataByClone(RuleNum, OBJID, data,
Head.fillDataByCustom);
}
colorTblRow(".colorTbl", "even", Head);
}
}
};
RefreshClickHandle(Head);
if ( $(".collapBarWithDataTrans",Head).length <= 0 )
{
Head.dataTransfer(ServerAddr,
"GET",
Head.succfunction);
}
else
{
initial_collapBarWithDataTrans(Head);
}
}
function initial_special_password(Head)
{
$(".SpecialPassword", Head).each(function(){
$(this).mouseup( function(){
if(this.focused){
this.focused=false;
return false;
}
});
});
$(".SpecialPassword", Head).each(function(){
$(this).focus( function(){
this.select();
this.focused=true;
});
});
}
function initial_button(buttonType, Head, IfShowWaitTip)
{
if ( !Head )
{
consoleLog("incoming para:Head is not defined!");
return;
}
var buttonClass = "";
var eventHandler = "";
if ( buttonType == "Apply" )
{
buttonClass = "Btn_apply";
eventHandler = "fillDataByApplyResult";
}
else if ( buttonType == "Cancel" )
{
buttonClass = "Btn_cancel";
eventHandler = "fillDataByCancelResult";
}
else if ( buttonType == "Delete" )
{
buttonClass = "Btn_delete";
eventHandler = "fillDataByDeleteResult";
}
else
{
}
$("."+buttonClass, Head).each(function(){
$(this).unbind("click");
$(this).bind("click",function(event){
var buttonOBJ = $(this);
if (buttonOBJ.hasClass("disableBtn")
||buttonOBJ.hasClass("disableLongBtn"))
{
return;
}
var Head = buttonOBJ.parents(".HeadDIV");
var template = buttonOBJ.parents("[id^='template']");
var ActionBeforePostResult = {result: "Process"};
if ( buttonType == "Apply" )
{
var formOBJ = $(".form_content", template);
if ( formOBJ.length > 0 && false == formOBJ.valid() )
{
return;
}
else
{
var formObj = $(".form_content", template);
var txtInputObjs = $("input[type='text']", formObj);
txtInputObjs.each(function(){
var obj = $(this);
var rules = obj.rules();
if (rules.integer)
{
var intStr = obj.val();
var sign, digits;
if ( intStr.charAt(0) == '-' )
{
sign = "-";
digits = intStr.substring(1);
}
else
{
sign = "";
digits = intStr;
}
while(digits.charAt(0) == '0' && digits.length > 1)
{
digits = digits.substring(1);
}
intStr = sign + digits;
obj.val(intStr);
}
});
}
var IPMACCheckResult = {result: "checkOK"};
template.trigger("wholeIPorMACCheck",[template,IPMACCheckResult]);
if (IPMACCheckResult.result != "checkOK")
{
return;
}
}
template.trigger("ActionBeforePostByCustom",[template,ActionBeforePostResult]);
if (ActionBeforePostResult.result != "Process")
{
return;
}
var ThisInstID = $("[id^='_InstID']",template).val();
if ( ThisInstID == undefined )
{
var luquidObjUl = $("._LuQUID_CONFIG_OBJID", Head);
var objId = $("li", luquidObjUl).eq(0).text();
var instId = objId + "\\._OBJ_InstID";
ThisInstID = $("[id^='"+ instId +"']",template).val();
}
if ( ThisInstID == -1
&& (buttonType == "Cancel" || buttonType == "Delete") )
{
template.remove();
return;
}
var ServerAddr = $("address span", Head).text();
var IfShowWaitTipTmp = IfShowWaitTip;
if ( IfShowWaitTipTmp == undefined )
{
IfShowWaitTipTmp = true;
}
dataPost(buttonType, eventHandler, ServerAddr, template, undefined, IfShowWaitTipTmp);
});
});
}
function dataPost(actionType, PostSuccHandler, ServerAddr, template, PostData, IfShowWaitTip, asyncFlag)
{
var IfShowWaitTipTmp = IfShowWaitTip;
if ( IfShowWaitTipTmp == undefined )
{
IfShowWaitTipTmp = true;
}
if (asyncFlag == undefined)
{
asyncFlag = true;
}
var PostDataTmp = "";
if (PostData == undefined)
{
template.trigger("hiddenValueChangeByCustom",[template, actionType]);
PostDataTmp = template.InitialPostData(actionType);
}
else
{
PostDataTmp = PostData;
}
PostDataTmp += "&_sessionTOKEN="+_sessionTmpToken;
var procData = true;
if (PostDataTmp.indexOf("%20") >= 0)
{
procData = false;
}
var selfHeader = {};
if (commConf.IntegCheck)
{
var degistStr = sha256(PostDataTmp);
selfHeader["Check"] = asyEncode(degistStr);
}
if ( IfShowWaitTipTmp == true )
{
showWaitTip(true);
}
$.ajax({
url:ServerAddr,
type: 'POST',
data: PostDataTmp,
headers: selfHeader,
processData: procData,
async: asyncFlag,
timeout: 30000,
cache:false,
error: function(){
var ajaxPostFailHint = "O servidor não está disponível agora. Atualize a página para recarregar. ";
var errorContainer = $(".errorHint",template);
var changeArea = $(".ChangeArea",template);
var collapsibleInst = $(".collapsibleInst",template);
if ( errorContainer != undefined )
{
$("span", errorContainer).text(ajaxPostFailHint);
errorContainer.showIt(true);
if ( changeArea != undefined )
{
changeArea.showIt(true);
}
if ( collapsibleInst != undefined )
{
collapsibleInst.addClass("instNameExp");
}
template.showIt(true);
}
showWaitTip(false);
},
success: function(data){
_LuQUID_setTemplateDefEvents(template, PostSuccHandler);
template.trigger(PostSuccHandler,[data,template]);
if (template.hasError(data,"_noExist") == 0)
{
$(".SpecialPassword", template).each(function(i){
$(this).val("						");
});
}
var formObj = $(".form_content", template);
var errObjs = $(".errorLabelWraper > .error", formObj);
errObjs.attr("style", "display:none");
if ( IfShowWaitTipTmp == true )
{
showWaitTip(false);
}
}
});
}
function homedeletedataPost(actionType, PostSuccHandler, ServerAddr, template, PostData, IfShowWaitTip, asyncFlag)
{
var IfShowWaitTipTmp = IfShowWaitTip;
if ( IfShowWaitTipTmp == undefined )
{
IfShowWaitTipTmp = true;
}
if (asyncFlag == undefined)
{
asyncFlag = true;
}
var deleteid = $("[id^='Delete']",template).attr('id');
var idArr = deleteid.split(":");
var tmpinsid = idArr[idArr.length - 1];
var insid = parseInt(tmpinsid, 10) + 1;
var PostDataTmp = "IF_ACTION=" + actionType + "&" +"_InstID=" + parseInt(insid, 10);
if (typeof(_sessionTmpToken) != "undefined")
{
PostDataTmp += "&_sessionTOKEN="+_sessionTmpToken;
}
if ( IfShowWaitTipTmp == true )
{
showWaitTip(true);
}
$.ajax({
url:ServerAddr,
type: 'POST',
data: PostDataTmp,
async: asyncFlag,
timeout: 30000,
cache:false,
error: function(){
var ajaxPostFailHint = "O servidor não está disponível agora. Atualize a página para recarregar. ";
var homeWrapperObj = template.parent("[id^='homeWrapper']");
var errorContainertmp = $(".lanErr",homeWrapperObj);
var errorContainer = $(".errorHint",errorContainertmp);
if ( errorContainer != undefined )
{
$("span", errorContainer).text(ajaxPostFailHint);
errorContainer.showIt(true);
template.showIt(true);
}
showWaitTip(false);
},
success: function(data){
template.trigger(PostSuccHandler);
if ( IfShowWaitTipTmp == true )
{
showWaitTip(false);
}
}
});
}
function focusAndSelectInput(jqObj)
{
var disValue = jqObj.attr("disabled");
if (disValue != "disabled" && disValue != true)
{
jqObj.focus();
jqObj.select();
}
}
function FocusAutoJump(obj,value,e)
{
var objJQ = $(obj);
var prevOBJ = objJQ.prev("input");
var nextOBJ = objJQ.next("input");
var valLen = value.length;
var keynum;
if (window.event)
{
keynum = e.keyCode;
}
else if (e.which)
{
keynum = e.which;
}
var temp = value.substring(valLen-1, valLen);
if ("." == temp && objJQ.hasClass("ip") && 0 != valLen)
{
objJQ.val(value.substring(0, valLen-1))
if ("." != value)
{
focusAndSelectInput(nextOBJ);
}
}
if (valLen == obj.maxLength)
{
if (nextOBJ.length <= 0)
{
return;
}
if (9 != keynum && 16 != keynum && 35 != keynum && 36 != keynum &&
37 != keynum && 38 != keynum && 39 != keynum && 40 != keynum &&
46 != keynum && 8 != keynum && objJQ.valid() == 1)
{
focusAndSelectInput(nextOBJ);
}
}
else if (valLen == 0 && 37 == keynum)
{
if (prevOBJ.length <= 0)
{
return;
}
focusAndSelectInput(prevOBJ);
}
else
{
return;
}
}
function autoJumpBack(obj,value,e)
{
var objJQ = $(obj);
var prevOBJ = objJQ.prev("input");
var nextOBJ = objJQ.next("input");
var valLen = value.length;
var keynum;
if (window.event)
{
keynum = e.keyCode;
}
else if (e.which)
{
keynum = e.which;
}
if (8 == keynum && valLen == 0)
{
if (prevOBJ.length <= 0)
{
return;
}
focusAndSelectInput(prevOBJ);
}
}
jQuery.fn.FillIPorMacDataBySplit = function(subid,Delimiter,length) {
var IPOBJ = $(this);
if ( IPOBJ.length == 0 )
{
return;
}
var containerOBJ = IPOBJ.parents("[id^='template_']");
var value = IPOBJ.val();
if ( !value )
{
return;
}
var temp= value.split(Delimiter);
if (length != temp.length)
{
return;
}
for(var i=0; i<length; i++)
{
var fillOBJ = $("[id^='"+subid+i+"']",containerOBJ);
fillOBJ.val(temp[i]);
}
};
jQuery.fn.FillIPorMacDataCombination = function(subid,Delimiter,length) {
var IPOBJ = $(this);
if ( IPOBJ.length == 0 )
{
return;
}
var containerOBJ = IPOBJ.parents("[id^='template_']");
var temp = "";
for(var i=0; i<length; i++)
{
var tempObj = $("[id^='"+subid+i+"']",containerOBJ);
if(0!=i)
{
temp += Delimiter;
}
var tempValue = tempObj.val();
if ( !tempValue )
{
tempValue = "";
}
temp += tempValue;
tempObj.addClass("PostIgnore");
}
IPOBJ.val(temp);
return temp;
};
jQuery.fn.checkIPorMACbyApply = function(checkIPorMACObj, template, IPMACCheckResult){
var breakFlag = 0;
$.each(checkIPorMACObj, function(key, value){
if (breakFlag != 0)
{
return false;
}
if ($("[id^='sub_"+key+"']",template).is(":visible") != true)
{
return true;
}
var labelId = value.labelId;
var paraName = "";
var paraNameObj = template.find("label[for^='"+labelId+"\\:']");
if ( paraNameObj.length <= 0 )
{
paraNameObj = template.find("label[for='"+labelId+"']");
}
if ( paraNameObj.length > 0 )
{
paraNameObj.each(function(){
var labelTmp = $(this);
if (labelTmp.hasClass("error"))
{
return true;
}
paraName = labelTmp.text();
return false;
});
}
var elementType = value.eleType;
if (elementType == "IP")
{
var IPObj = $("[id^='"+key+"']",template);
IPObj.FillIPorMacDataCombination("sub_"+key, ".", 4);
var ipValue = IPObj.val();
if (value.rules != undefined)
{
$.each(value.rules, function(k, v){
var ipRet = checkWholeIPv4(k, v, ipValue, template);
if (ipRet[0] == false)
{
var errMsg = getMsgofWholeMACIPCheck(ipRet, value, ipValue, paraName);
$(".errorHint",template).show();
$(".errorHint span",template).text(errMsg);
IPMACCheckResult.result = "checkFail";
breakFlag = 1;
return false;
}
else
{
$(".errorHint",template).hide();
}
});
}
}
else if (elementType == "MAC")
{
var MACObj = $("[id^='"+key+"']",template);
MACObj.FillIPorMacDataCombination("sub_"+key, ":", 6);
var macValue = MACObj.val();
if (value.rules != undefined)
{
$.each(value.rules, function(k, v){
var macRet = checkWholeMac(k, v, macValue);
if (macRet[0] == false)
{
var errMsg = getMsgofWholeMACIPCheck(macRet, value, macValue, paraName);
$(".errorHint",template).show();
$(".errorHint span",template).text(errMsg);
IPMACCheckResult.result = "checkFail";
breakFlag = 1;
return false;
}
else
{
$(".errorHint",template).hide();
}
});
}
}
else
{
consoleLog("ElementType +'"+elementType+"' is not supported now!")
}
});
};
jQuery.fn.setPromptCheckJSON = function(checkJSONTempObj, template){
var templateID = template.attr("id");
var instIndex = templateID.match(/\d+$/);
var suffix = "";
var modifierName = "common/" + templateID.replace(/(^template_)|(_\d)/gm,"") + "/CheckJSON";
var CheckData = {};
CheckData.checkJSONTempObj = checkJSONTempObj;
CheckData.template = template;
$.callModifier(modifierName, CheckData);
if ( instIndex )
{
suffix = ":"+instIndex;
}
var checkJSONInstObj = {"groups":{}, "rules":{}, "messages":{}};
if ( checkJSONTempObj.groups != undefined )
{
$.each(checkJSONTempObj.groups, function(key, value) {
var valJSONStr = value;
var idArr = value.split(" ");
var newIdArr = [];
var j = 0;
for ( var i=0; i<idArr.length; i++ )
{
if (idArr[i] == "") {
continue;
}
newIdArr[j] = idArr[i] + suffix;
j++;
}
valJSONStr = newIdArr.join(" ");
var parameterJSON = eval("({'"+key+suffix+"':'" + valJSONStr + "'})");
$.extend(checkJSONInstObj.groups, parameterJSON);
});
}
if ( checkJSONTempObj.rules != undefined )
{
$.each(checkJSONTempObj.rules, function(key, value) {
var parameterJSON = {};
parameterJSON[key + suffix] = value;
$.extend(checkJSONInstObj.rules, parameterJSON);
});
}
if ( checkJSONTempObj.messages != undefined )
{
$.each(checkJSONTempObj.messages, function(key, value) {
var parameterJSON = {};
parameterJSON[key + suffix] = value;
$.extend(checkJSONInstObj.messages, parameterJSON);
});
}
var instForm = template.find("form");
instForm.validate(checkJSONInstObj);
};
function consoleLog(para)
{
if (typeof window.console == "undefined") {
window.console = {log: function() {}};
}
window.console.log( para );
}
function getInstIndexByPath(data, OBJID, path)
{
var instIndex = -1;
if ($.isPlainObject(data))
{
var instances = data[OBJID]["Instance"];
$.each(instances,function(i,v){
var inst = v;
if(inst["_InstID"] != undefined && inst["_InstID"] == path)
{
instIndex = i;
}
});
}
else
{
var OBJ = $(data).find(OBJID);
var instances = $("Instance", OBJ);
instances.each(function(i){
var inst = $(this);
inst.find("ParaName").each(function(){
var ParaName = $(this).text();
var ParaValue = $(this).next().text();
if ( ParaName.match(/^_InstID/) != null
&& ParaValue == path )
{
instIndex = i;
}
});
});
}
return instIndex;
}
function xmlParaInInstOperate(data, OBJVal, InstIndex, ToOperParaArray)
{
if ($.isPlainObject(data))
{
var instances = data[OBJVal]["Instance"];
var inst = instances[InstIndex];
for (var tmp in ToOperParaArray)
{
if(inst[tmp] != undefined)
{
ToOperParaArray[tmp].ValueOrigin = inst[tmp];
if (ToOperParaArray[tmp].setAction)
{
ToOperParaArray[tmp].setAction(inst, null, inst[tmp]);
}
}
}
}
else
{
var OBJ = $(OBJVal, $(data));
var inst = $("Instance", OBJ).eq(InstIndex);
inst.find("ParaName").each(function(){
var ParaSelf = $(this);
var ParaValSelf = $(this).next();
var ParaName = ParaSelf.text();
var ParaValue = ParaValSelf.text();
for (var tmp in ToOperParaArray)
{
if( tmp == ParaName )
{
ToOperParaArray[tmp].ValueOrigin = ParaValue;
if (ToOperParaArray[tmp].setAction)
{
ToOperParaArray[tmp].setAction(ParaSelf, ParaValSelf, ParaValue);
}
}
}
});
}
}
function getParaValueInXML(data, OBJID, InstIndex, paraNameIn)
{
var paraValueOut = "N/A";
if ($.isPlainObject(data))
{
var instances = data[OBJID]["Instance"];
var inst = instances[InstIndex];
if(inst[paraNameIn] != undefined)
{
paraValueOut = inst[paraNameIn];
if(commConf.getEncode && data[OBJID]["encode"] != undefined && data[OBJID]["encode"].indexOf(paraNameIn) != -1)
{
paraValueOut = getDecodeValue(paraValueOut);
}
}
}
else
{
var OBJ = $(data).find(OBJID);
var instances = $("Instance", OBJ);
var inst = instances.eq(InstIndex);
inst.find("ParaName").each(function(){
var ParaName = $(this).text();
var ParaValue = $(this).next().text();
if ( ParaName == paraNameIn )
{
paraValueOut = ParaValue;
$(data).find("encode").each(function(){
if(commConf.getEncode && $(this).text().indexOf(paraNameIn) != -1)
{
paraValueOut = getDecodeValue(paraValueOut);
return false;
}
});
return false;
}
});
}
return paraValueOut;
}
function colorTblRow(tblClass, rowAttr, Head)
{
$(tblClass+" .colorTblRow", Head).each(function(){
var thisRow = $(this);
thisRow.removeClass("colorRow");
});
var shouldPainted = true;
if ( rowAttr == "even" )
{
shouldPainted = true;
}
else
{
shouldPainted = false;
}
var allRows = $(tblClass+" .colorTblRow", Head);
allRows.each(function(){
var thisRow = $(this);
if ( thisRow.css("display") != "none" )
{
if ( true == shouldPainted )
{
thisRow.addClass("colorRow");
shouldPainted = false;
}
else
{
shouldPainted = true;
}
}
});
}
function reformString(inStr, splitNum)
{
var strLen = inStr.length;
var outStr = "";
var arr = [];
var start = 0;
var end = 0;
if (strLen > 4)
{
var flag = strLen % splitNum;
if (flag != 0)
{
end = flag;
}
else
{
end = start + splitNum;
}
for (var i=0; end <= strLen; i++)
{
arr[i] = inStr.slice(start, end);
start = end;
end = start + splitNum;
}
for (var j = 0; j < arr.length; j++)
{
outStr = outStr + arr[j] + " ";
}
outStr = outStr.slice(0, (outStr.length-1));
}
if (outStr == "")
{
outStr = inStr;
}
return outStr;
}
function sec2HrMinSec(sec)
{
if (sec == "")
{
consoleLog("[sec2HrMinSec]sec is empty, please check if it's ok?! ");
}
var s, m, h;
s = parseInt(sec % 60);
m = parseInt(sec / 60, 10) % 60;
h = parseInt(sec / 3600, 10);
return (h + " h " + m + " min " + s + " s");
}
jQuery.fn.collapsibleInstTitleChange = function(referenceID) {
var ContainerOBJ = $(this);
var NameValue = "";
var nameSrcObj = $("[id^='"+referenceID+":']",ContainerOBJ);
var eleType = nameSrcObj[0].type;
if (eleType == "select-one") {
NameValue = $("option:selected", nameSrcObj).text();
}else {
NameValue = nameSrcObj.val();
}
var instNameObj = $(".collapsibleInst",ContainerOBJ);
instNameObj.text(NameValue);
instNameObj.attr("title", NameValue);
};
function initialCtrlAllLink(containerOBJ)
{
var AllObj = $(".AllOn, .AllOff",containerOBJ);
AllObj.unbind("click");
AllObj.click(function(event){
var AllCtlItme = $(this);
var Head = AllCtlItme.parents(".HeadDIV");
var Template = AllCtlItme.parents("[id^='template_']");
var needCheck = 1;
var EleSelectValue;
if ( AllCtlItme.hasClass("AllOn") )
{
needCheck = 1;
EleSelectValue = 1;
}
else if ( AllCtlItme.hasClass("AllOff") )
{
needCheck = 0;
EleSelectValue = 0;
}
else
{
}
if ( AllCtlItme.attr("EleSelectValue") )
{
EleSelectValue = AllCtlItme.attr("EleSelectValue");
}
$(":radio",Template).each(function(){
var RadioOBJ = $(this);
if ( RadioOBJ.val() == EleSelectValue )
{
RadioOBJ.prop("checked", true);
}
else
{
RadioOBJ.prop("checked", false);
}
});
$(":checkbox",Template).each(function(){
var CheckboxOBJ = $(this);
if ( needCheck == 1)
{
CheckboxOBJ.prop("checked", true);
}
else
{
CheckboxOBJ.prop("checked", false);
}
});
});
}
function ActionByApplyResult(data, template, TitleValueReferID)
{
var isError = template.hasError(data);
if (isError == 0)
{
$("span.__CheckPwdStrength",template).remove();
succHintShow(template);
if ($.isPlainObject(data))
{
if(data["_InstID"] != undefined)
{
$("[id^='_InstID']",template).val(data["_InstID"]);
}
}
else
{
var _InstIDOBJ = $(data).find("_InstID");
if (_InstIDOBJ.length > 0)
{
$("[id^='_InstID']",template).val(_InstIDOBJ.text());
}
}
var headObj = template.parents(".HeadDIV");
var luquidObjUl = $("._LuQUID_CONFIG_OBJID", headObj);
$("li", luquidObjUl).each(function(){
var objId = $(this).text();
var ruleTemplate = $("[id='"+objId+"']._LuQuid_TempalteBox", template);
if( ruleTemplate.length > 0 )
{
return true;
}
var instIdSelector = objId + "\\._OBJ_InstID";
var instIDTag = $(data).find(instIdSelector);
if (instIDTag.length == 0)
{
return true;
}
$("[id^='"+ instIdSelector +"']",template).val(instIDTag.text());
});
if ( TitleValueReferID != undefined )
{
template.collapsibleInstTitleChange(TitleValueReferID);
}
$("textarea[_readonlycanberm]",template).attr("readonly","readonly");
$("input[type!=button][_readonlycanberm],select[_readonlycanberm]",template).attr("disabled","disabled")
.addClass("readonlyInputBg");
$(".Button[_readonlycanberm]",template).attr("disabled","disabled").addClass("disableBtn");
$(".longBtn[_readonlycanberm]",template).attr("disabled","disabled").addClass("disableLongBtn");
}
return isError;
}
function ActionByCancelResult(data, template, OBJIDForFillData, TitleValueReferID)
{
var isError = template.hasError(data);
if ( isError == 0 )
{
$("span.__CheckPwdStrength",template).remove();
template.fillDataByOBJID(data, OBJIDForFillData, template, 0);
template.FillDataOnlyForTemplateBox(data, OBJIDForFillData, template);
if ( TitleValueReferID != undefined )
{
template.collapsibleInstTitleChange(TitleValueReferID);
}
}
else
{
$(".ChangeArea",template).showIt(true);
$(".collapsibleInst",template).addClass("instNameExp");
}
return isError;
}
function addInst(Head, InstNumOBJ)
{
var HeadID = Head.attr("id");
var templateOBJ = $("#template_"+HeadID);
var suffix = InstNumOBJ.val();
var clone = templateOBJ.cloneWithSuffix(suffix);
if(!$("[_readonlycanberm]",clone).attr("hideattr"))
$("[_readonlycanberm]",clone).removeAttr("disabled readonly")
.removeClass("readonlyInputBg disableBtn disableLongBtn");
templateOBJ.before(clone);
InstNumOBJ.val(parseInt(suffix)+1);
templateOBJ.trigger("ActionBeforeAddInst",[clone]);
clone.showIt(true);
$(".collapsibleInst",clone).addClass("instNameExp");
$(".ChangeArea",clone).showIt(true);
}
function IfCreateInstChk(Head, InstNumOBJ, AddInstLink)
{
var ExistInst = 0;
$("[id^='template_']",Head).each(function(){
if ($(this).css("display") == "block")
{
ExistInst = 1;
return false;
}
});
if ( ExistInst == 0
&& AddInstLink.length > 0 )
{
return true;
}
return false;
}
function collapBarAction(collapBar)
{
var Head = collapBar.parents(".HeadDIV");
var HeadID = Head.attr("id");
var containerMainID = HeadID + "_container";
var UnderControlContainer = $("#"+containerMainID, Head);
var template = collapBar.parents("[id^='template_']");
var selector = "[id^='"+ containerMainID +"']";
var containerInTemp = $(selector, template);
var containerLen = containerInTemp.length;
if ( containerLen > 0 )
{
UnderControlContainer = containerInTemp;
}
if ( UnderControlContainer.is(":visible") )
{
UnderControlContainer.showIt(false);
collapBar.removeClass("collapsibleBarExp");
}
else
{
UnderControlContainer.showIt(true);
collapBar.addClass("collapsibleBarExp");
}
var InstNumOBJ = $("#_InstNum",Head);
var AddInstLink = Head.find(".addInst");
if ( IfCreateInstChk(Head, InstNumOBJ, AddInstLink) )
{
addInst(Head, InstNumOBJ);
}
}
function initial_collapBarWithDataTrans(Head)
{
var UnderControlContainer = $("#"+ Head.attr("id") +"_container");
UnderControlContainer.hide();
$(".collapBarWithDataTrans",Head).click(function(event){
event.preventDefault();
var collapBar = $(this);
if ( $("#DataHasBeenGot",Head).val() == 0 )
{
showWaitTip(true);
setTimeout(function(){
var ServerAddr = $("address span", Head).text();
Head.dataTransfer(ServerAddr,
"GET",
Head.succfunction,
undefined,
undefined,
false
);
$("#DataHasBeenGot",Head).val(1);
collapBarAction(collapBar);
}, 2);
}
else
{
collapBarAction(collapBar);
}
});
}
function initial_CollapsibleBar()
{
$(".collapsibleBar").each(function(){
var HeadID = $(this).parents(".HeadDIV").attr("id");
var UnderControlContainer = $("#"+ HeadID +"_container");
UnderControlContainer.hide();
});
$(".collapsibleBar").each(function(){
var collapsibleBar = $(this);
collapsibleBar.click(function(event){
event.preventDefault();
var collapBar = $(this);
collapBarAction(collapBar);
});
});
}
function initial_addInstLink()
{
$(".addInst").each(function(event){
var addInstOBJ = $(this);
addInstOBJ.unbind("click");
addInstOBJ.click(function(event){
var Head = $(this).parents(".HeadDIV");
var InstNumOBJ = $("#_InstNum",Head);
addInst(Head, InstNumOBJ);
});
});
}
function _LuQUID_template_ApplyDefEventFunc(event, data, template)
{
return ActionByApplyResult(data, template);
}
function _LuQUID_template_CancelDefEventFunc(event, data, template)
{
var OBJID = [];
var Head = template.parents(".HeadDIV");
var OBJDOMs = $("._LuQUID_CONFIG_OBJID>li", Head);
OBJDOMs.each(function(){
var identity = $(this).text();
OBJID.push(identity);
})
ActionByCancelResult(data, template, OBJID);
template.trigger("fillDataByCustom",[0, template, data]);
}
function _LuQUID_template_DeleteDefEventFunc(event, data, template)
{
if ( template.hasError(data) == 0 )
{
template.remove();
}
else
{
$(".ChangeArea",template).showIt(true);
}
}
function _LuQUID_template_InstSwitchDefEventFunc(event, data, template)
{
if ( template.hasError(data) == 0 )
{
return;
}
$(".ChangeArea",template).showIt(true);
$(".collapsibleInst",template).addClass("instNameExp");
}
var _LuQUID_template_DefEventFuncMap = {
"fillDataByApplyResult" : _LuQUID_template_ApplyDefEventFunc,
"fillDataByCancelResult" : _LuQUID_template_CancelDefEventFunc,
"fillDataByDeleteResult" : _LuQUID_template_DeleteDefEventFunc,
"fillDataByInstSwitchResult" : _LuQUID_template_InstSwitchDefEventFunc
};
function _LuQUID_setTemplateDefEvents(template, PostSuccHandler)
{
var LuquidObj = $(template).parent().find("address").find("[class^='_LuQUID_']");
if( LuquidObj.length == 0 )
{
return;
}
var events = template.data("events");
if( events && events[PostSuccHandler] )
{
return ;
}
var eventFunc = _LuQUID_template_DefEventFuncMap[PostSuccHandler];
if ( eventFunc )
{
template.bind(PostSuccHandler, eventFunc);
}
}
function initialConfigArea(Head)
{
if ( 0 == $("._LuQUID_CONFIG_OBJID", Head).length )
{
return;
}
var OBJID = [];
var OBJDOMs = $("._LuQUID_CONFIG_OBJID>li", Head);
OBJDOMs.each(function(){
var identity = $(this).text();
OBJID.push(identity);
});
var isMultiInst = $(".maxInstNum", Head).val();
consoleLog("isMultiInst="+isMultiInst);
Head.succfunction = function(data){
Head.hasError(data, "externErrorHint");
{
Head.trigger("changeXMLDataBeforeFillData", [data]);
var XMLOBJ = $(data).find(OBJID[0]);
var RuleNum = $("Instance", XMLOBJ).length;
if (isMultiInst == 0)
{
Head.fillDataByOBJID(data, OBJID, Head, 0);
Head.InstantializeForTemplateBox(data, OBJID, Head);
var template = $("[id^='template_']", Head);
template.trigger("fillDataByCustom",[0, template]);
template.showIt(true);
}
else
{
Head.fillDataByCustom = undefined;
Head.createPageDataByClone(RuleNum, OBJID, data,
Head.fillDataByCustom);
}
}
};
if ( $(".collapBarWithDataTrans",Head).length <= 0 )
{
Head.dataTransfer(ServerAddr,
"GET",
Head.succfunction);
}
else
{
initial_collapBarWithDataTrans(Head);
}
}
function initial_QueryAccessDeviceLink()
{
var linkSelector = "._LuQUID_SelAccessDevice";
var selDevLinks = $(linkSelector);
if ( selDevLinks.length == 0 )
{
return;
}
selDevLinks.each(function(){
var selDevLink = $(this);
selDevLink.css("display", "block");
var rowObj = selDevLink.parents(".f-row").eq(0);
rowObj.append("<div class='clear'></div>");
var macID = rowObj.find(".mac").eq(0).attr("id");
var macIDStriped = macID;
var paraID = macIDStriped.match(/^sub_(.+)\d$/)[1];
var headID = selDevLink.parents(".HeadDIV").attr("id");
var suffix = ":"+paraID+":"+headID;
var devListHTML = ''
+ '<div class="LuQUID-AccessDeviceInfo" name="_LuQUID_AccessDeviceInfo'+suffix+'" style="display:none;">'
+ '<input type="hidden" class="PostIgnore" id="_LuQUID_InstNum'+suffix+'" value="0">'
+ '<p id="_LuQUID_NoAccessDev'+suffix+'">Actualmente não há dispositivos associados.</p>'
+ '<p id="_LuQUID_template_AccessDeviceInfo'+suffix+'" style="display:none">'
+ '<label class="cfgLabel">&nbsp;</label>'
+ '<input type="hidden" class="PostIgnore" id="_LuQUID_HostName'+suffix+'" value="">'
+ '<input type="hidden" class="PostIgnore" id="_LuQUID_IPAddress'+suffix+'" value="">'
+ '<input type="hidden" class="PostIgnore" id="_LuQUID_MACAddress'+suffix+'" value="">'
+ '<input type="radio" class="PostIgnore" id="_LuQUID_AccessDeviceRadio'+suffix+'" name="_LuQUID_AccessDeviceRadio'+suffix+'" value=""/>'
+ '<label for="_LuQUID_AccessDeviceRadio'+suffix+'" style="font-size:15px">'
+ 'Nome de anfitrião: [<span id="_LuQUID_StrHostName'+suffix+'">Desconhecido</span>]'
+ '-Endereço MAC: [<span id="_LuQUID_StrMACAddress'+suffix+'"></span>]'
+ '</label>'
+ '</p>'
+ '<a class="_LuQUID_HideAccessDevice">Ocultar</a>'
+ '</div>';
var macObj = rowObj.find(".f-wrap");
var devListObj = $(devListHTML).insertAfter(macObj);
var labelObj = selDevLink.parent().prev();
var labelWidth = labelObj.css("width");
devListObj.css("margin-left", labelWidth);
});
var devRadios = $("input[name^='_LuQUID_AccessDeviceRadio']");
devRadios.click(function(event){
var devRadio = $(this);
var templateSelector = "[id^='_LuQUID_template_AccessDeviceInfo']";
var templateDev = devRadio.parents(templateSelector);
var devListObj = devRadio.parents("[name^='_LuQUID_AccessDeviceInfo']");
var rowObj = devRadio.parents(".f-row").eq(0);
var deviceRadioSelector = "input[name^='_LuQUID_AccessDeviceRadio']";
$(deviceRadioSelector, devListObj).prop("checked", false);
devRadio.prop("checked", true);
var devMACObj = $("[id^='_LuQUID_MACAddress']", templateDev);
var macID = rowObj.find(".mac").eq(0).attr("id");
var macIDStriped = colonStrippingLast(macID);
var subID = macIDStriped.match(/^(sub_.+)\d$/)[1];
devMACObj.FillIPorMacDataBySplit(subID, ":", 6);
var lastSubMAC = rowObj.find(".mac").last();
lastSubMAC.focus().blur();
});
var hideDevLinks = $("._LuQUID_HideAccessDevice");
hideDevLinks.unbind("click");
hideDevLinks.click(function(event){
event.preventDefault();
var devListObj = $(this).parents("[name^='_LuQUID_AccessDeviceInfo']");
devListObj.hide();
});
selDevLinks.unbind("click");
selDevLinks.click(function(event){
event.preventDefault();
var selDevLink = $(this);
var rowObj = selDevLink.parents(".f-row");
var devListObj = rowObj.find("[name^='_LuQUID_AccessDeviceInfo']");
if (devListObj.is(":visible"))
{
devListObj.hide();
return;
}
var InstNumBefore = $("[id^='_LuQUID_InstNum']", devListObj).val();
for ( var i=0; i<InstNumBefore; i++ )
{
var selector = "[id$='_"+i+"']"
+"[id^='_LuQUID_template_AccessDeviceInfo']";
$(selector, devListObj).remove();
}
devListObj.AccessDeviceXMLDealWith = function(data){
devListObj.hasError(data,"externErrorHint");
var ACCESSDEVRuleOBJ = $(data).find("OBJ_ACCESSDEV_ID");
var RuleNum = $("Instance", ACCESSDEVRuleOBJ).length;
var OBJID = ["OBJ_ACCESSDEV_ID"];
var templateSelector = "[id^='_LuQUID_template_AccessDeviceInfo']";
var TemplateOBJ = $(templateSelector, devListObj);
$("[id^='_LuQUID_InstNum']", devListObj).val(RuleNum);
var NoAccessDevObj = $("[id^='_LuQUID_NoAccessDev']", devListObj);
if (RuleNum == 0 )
{
NoAccessDevObj.show();
}
else
{
NoAccessDevObj.hide();
}
for (var i=0; i<RuleNum; i++)
{
var clone = TemplateOBJ.cloneWithSuffix(i);
TemplateOBJ.before(clone);
clone.fillDataByOBJID(data, OBJID, clone, i);
var HostNameStr = $("[id^='_LuQUID_HostName']", clone).val();
var IPAddress = $("[id^='_LuQUID_IPAddress']", clone).val();
var MACAddress = $("[id^='_LuQUID_MACAddress']", clone).val();
if (HostNameStr == "")
{
if (IPAddress != "")
{
HostNameStr = "PC" + IPAddress;
}
else if (MACAddress != "")
{
HostNameStr = "PC" + MACAddress
}
else
{
HostNameStr = "Desconhecido";
}
}
$("[id^='_LuQUID_StrHostName']", clone).text(HostNameStr);
var MACAddress = $("[id^='_LuQUID_MACAddress']", clone).val();
$("[id^='_LuQUID_StrMACAddress']", clone).text(MACAddress);
clone.show();
}
devListObj.show();
};
var accessMode = selDevLink.attr("_LuQUID_Access_Mode")
var AccessModeSet =
[
"ETH",
"WLAN",
"ALL"
];
if ( -1 == $.inArray(accessMode, AccessModeSet) )
{
var devTypeList = AccessModeSet.join("/")
consoleLog("_LuQUID_Access_Mode must be set as one of "+devTypeList);
return ;
}
var ServerAddr = "/?_type=hiddenData&_tag=accessdev_data&";
ServerAddr += "DeveiceType="+accessMode;
showWaitTip(true);
devListObj.dataTransfer(ServerAddr,
"GET",
devListObj.AccessDeviceXMLDealWith,
undefined,
undefined,
false);
});
}
function InitTimeOption(start,end,ele,step, ctrlClass)
{
var realNum = (end - start)/step;
for(var i=0; i<realNum; i++)
{
var tmp = i*step+start;
var tmpText = tmp;
if ( tmp < 10 )
{
tmpText = '0'+tmpText;
}
if (i == realNum-1
&&( ctrlClass == "group_HourEnd" || ctrlClass == "group_MinuteEnd" ) )
{
ele.append("<option value='"+tmp+"' selected='selected'>"+ tmpText +"</option>");
}
else
{
ele.append("<option value='"+tmp+"'>"+ tmpText +"</option>");
}
}
}
function initial_TimeCtl()
{
var TimeCtl = $("._LuQUID_TimeCtl");
if ( TimeCtl.length <= 0 )
{
return;
}
var timeArr = {
"group_HourStart" : [0, 24],
"group_MinuteStart" : [0, 60],
"group_HourEnd" : [0, 24],
"group_MinuteEnd" : [0, 60]
};
for (var tmp in timeArr)
{
var timeEle = $("."+ tmp, TimeCtl);
var start = timeArr[tmp][0];
var end = timeArr[tmp][1];
InitTimeOption(start, end, timeEle, 1, tmp);
}
}
function Second2DHMS(num)
{
var s = num % 60;
num = parseInt(num/60);
var m = num % 60;
num = parseInt(num/60);
var h = num % 24;
num = parseInt(num/24);
var d = num;
return {
day: d,
hour: h,
minute: m,
second: s
}
}
function InitSelectByIntRange(selectObj, min, max)
{
selectObj.empty();
var domCache = [];
for (var i = min; i <= max; i++)
{
domCache.push("<option title='" +i+ "' value='" +i+ "'>"+i+"</option>");
}
selectObj.append(domCache.join());
}
function SetCookie(name,value)
{
var Days = 30;
var exp = new Date();
exp.setTime(exp.getTime() + Days*24*60*60*1000);
document.cookie = name + "="+ escape (value)
+ ";expires=" + exp.toGMTString();
}
function getCookie(name)
{
var arr = document.cookie.match(new RegExp("(^| )"+name+"=([^;]*)(;|$)"));
if(arr != null)
{
return unescape(arr[2]);
}
return null;
}
function delCookie(name)
{
var exp = new Date();
exp.setTime(exp.getTime() - 1);
var cval = getCookie(name);
if( cval!=null )
{
document.cookie= name + "="+cval+";expires="+exp.toGMTString();
}
}
function IsBrowserSupportCookie()
{
var support = false;
SetCookie('cookie_test','1');
var cookie_test = getCookie('cookie_test');
if( '1' == cookie_test)
{
support = true;
}
delCookie('cookie_test');
return support;
}
(function () {
var setTimeout_context_binding = function (vCallback, nDelay ) {
var oThis = this, aArgs = Array.prototype.slice.call(arguments, 2);
return window.setTimeout(vCallback instanceof Function ? function () {
vCallback.apply(oThis, aArgs);
} : vCallback, nDelay);
};
var setInterval_context_binding = function(vCallback, nDelay ) {
var oThis = this, aArgs = Array.prototype.slice.call(arguments, 2);
return window.setInterval(vCallback instanceof Function ? function() {
vCallback.apply(oThis, aArgs);
} : vCallback, nDelay);
};
var timer = function(fnAlarm, options)
{
this.fnAlarm_inner = undefined;
this.timeout = undefined;
this.interval = undefined;
this.contextDom = undefined;
this.timerHandle;
if ( fnAlarm )
{
this.fnAlarm_inner = fnAlarm;
}
else
{
return;
}
if ( options )
{
if ( options.timeout )
{
this.timeout = options.timeout;
}
if ( options.interval )
{
this.interval = options.interval;
}
if ( options.contextDom )
{
this.contextDom = options.contextDom;
}
}
if ( !(this.timeout || options.interval) )
{
return;
}
};
timer.prototype.start = function(){
var context_binding_timer = undefined;
var time_value = undefined;
if ( this.timeout )
{
context_binding_timer = setTimeout_context_binding;
time_value = this.timeout;
}
else if ( this.interval )
{
context_binding_timer = setInterval_context_binding;
time_value = this.interval;
}
else
{
return;
}
this.timerHandle = context_binding_timer.call(this, function(){
if ( this.contextDom && !document.body.contains(this.contextDom) )
{
this.stop();
return;
}
this.fnAlarm_inner.call(this);
}, time_value);
};
timer.prototype.stop = function(){
if ( this.timeout ) {
clearTimeout(this.timerHandle)
} else {
clearInterval(this.timerHandle)
}
delete this.timerHandle;
};
timer.prototype.getTimerID = function(){
return this.timerHandle;
};
window.ContextBindingTimer = timer;
})();
(function ($) {
var o = $({});
var modifier = $({});
$.subscribe = function () {
o.on.apply(o, arguments);
};
$.unsubscribe = function () {
o.off.apply(o, arguments);
};
$.publish = function () {
o.trigger.apply(o, arguments);
};
$.addModifier = function(modifierName,callFunc){
modifier[modifierName] = callFunc;
};
$.callModifier = function(modifierName,data){
if(modifier[modifierName] == undefined){
return;
}
var callFunc = modifier[modifierName];
callFunc(data);
};
} (jQuery));
function timeTranslate(timeString)
{
var timetempstr = timeString;
if( timeString != "" )
{
var dayTranslat = {
"Sun" : "Dom",
"Mon" : "Seg",
"Tue" : "Ter",
"Wed" : "Qua",
"Thu" : "Qui",
"Fri" : "Sex",
"Sat" : "Sab"
};
var MonTranslat = {
"Jan" : "Jan",
"Feb" : "Fev",
"Mar" : "Mar",
"Apr" : "Abr",
"May" : "Mai",
"Jun" : "Jun",
"Jul" : "Jul",
"Aug" : "Ago",
"Sep" : "Set",
"Oct" : "Out",
"Nov" : "Nov",
"Dec" : "Dez"
};
var timeArry = timeString.split(",");
if(timeArry.length > 1)
{
var datstr = timeArry[0];
var monstr = timeArry[1];
timeArry[0] = dayTranslat[datstr];
timeArry[1] = MonTranslat[monstr];
}
timetempstr = timeArry.join(",");
}
return timetempstr;
}
function g_ApplyPopUp(template)
{
$(".Btn_apply", template).unbind('click').bind('click', function(event){
var templateObj = $(this).parents("[id^='template']");
var EncryptionTypeVal = $("[id^='EncryptionType']", templateObj).val();
var passVal = $("[id^='KeyPassphrase']:not(.PostIgnore)",templateObj).val();
var rePass = $("[id^='ConfKeyPassphrase']:visible",templateObj);
var rePassVal = rePass.val();
if(rePass.length>0 && passVal!=rePassVal){
return false;
}
var IsStrongPass = getPwdLevelCustom(passVal,"",10);
if (( false == IsStrongPass) && (EncryptionTypeVal !="No Security")){
var msg = "Falha! É necessário uma senha forte, que deve conter pelo menos 1 letra maiúscula, 1 letra minúscula e 1 número. A senha deve ter mais de 10 dígitos.";
var confirmLayerOBJ = IniConfirm(msg);
$("#confirmCancel",confirmLayerOBJ).css( "display","none" );
$("#confirmOK",confirmLayerOBJ).val("Voltar");
$("#confirmOK",confirmLayerOBJ).unbind("click").focus();
$("#confirmOK",confirmLayerOBJ).bind("click", templateObj, function(event){
showWaitTip(false);
});
}
else{
var Head = templateObj.parents(".HeadDIV");
var ServerAddr = $("address span", Head).text();
dataPost("Apply", "fillDataByApplyResult", ServerAddr, templateObj, undefined, true);
}
});
}
function random_PWD(tempObj,passLength,passTip){
var str = "qWwRrTtYyUupAafGgHhJjKkZzXxCcVvNnMm124789";
var UPstr = "WRTYUAGHJKZXCVNM";
var LWstr = "qwrtyupafghjkzxcvnm";
var Nstr = "124789";
var strlen = str.length;
var rand = "";
var pwd = [];
rand = Math.floor(Math.random()*16);
pwd[0] = UPstr[rand];
rand = Math.floor(Math.random()*19);
pwd[1] = LWstr[rand];
rand = Math.floor(Math.random()*6);
pwd[2] = Nstr[rand];
for(var i=3;i<passLength;i++){
rand = Math.floor(Math.random()*strlen);
pwd[i] = str[rand];
}
passTip += pwd.join("");
return passTip;
}
function getPwdLevelCustom(value, relVal, Longth)
{
var PwdTypeNum = 0;
if( (/[0-9]+/).test(value) )
PwdTypeNum++;
if( (/[a-z]+/).test(value) )
PwdTypeNum++;
if( (/[A-Z]+/).test(value) )
PwdTypeNum++;
if(PwdTypeNum<3)
return false;
if (value.length < Longth)
{
return false;
}
return true;
}
function getPwdLevel(val, relVal, Longth)
{
if (val.length < Longth)
{
return false;
}
if ( !(/[0-9]+/).test(val) ||
!(/[a-zA-Z]+/).test(val) ||
!(/[!"#$%&'()*+,-./:;<=>?@\[\\\]^_`{|}~]+/).test(val) )
{
return false;
}
if (val == relVal || val == relVal.split("").reverse().join(""))
{
return false;
}
return true;
}
function CheckPwdStrengthClass(pwdId, relativeId, templateId, customRuleFunc, customTip, minLongth){
this.pwdObj = $("[id^="+pwdId+"]", $("#"+templateId));
this.checkStrength = function(o, v){
var r = {
txt: "Fraco",
aClass: "redFont"
};
if (typeof(customRuleFunc) == "function"){
return customRuleFunc(o,v);
}
var myTplt = o.closest("[id^=template_]");
var relVal = $("[id^="+relativeId+"]", myTplt).val();
var Longth = 10;
if (typeof(minLongth) == "number") {
Longth = minLongth;
}
var strongPwd = getPwdLevelCustom(v, relVal, Longth);
if (strongPwd) {
r.txt = "";
}
return r;
};
this.showResult = function(o, r){
var inputParent = o.parent();
inputParent.find(".__CheckPwdStrength").remove();
if (r.txt != "") {
inputParent.append("<span class='__CheckPwdStrength "+r.aClass+"'>"+r.txt+"</span>");
}
};
this.showTip = function(o){
var tipF = "Uma senha forte deve coincidir com estas regras: <br/> 1. Ela deve ter pelo menos {0} caracteres. <br/> 2. Deve ser composto por dígitos, alfabeto e símbolos especiais. <br/> 3. Ele não deve ter relação contexto com o nome de utilizador, tal como o mesmo ou inversa. ";
tipF="É necessário uma senha forte e deve conter as seguintes regras:<br/>1. A senha deve ter pelo menos 10 caracteres.<br/>2. Deve conter pelo menos 1 letra maiúscula, 1 letra minúscula e 1 número.<br/>3. Não deve ter correlação com o nome de usúario.";
if (typeof(customTip) == "string") {
tipF = customTip;
}
var tip = "";
if(typeof(minLongth) == "number") {
tip = tipF.format(minLongth);
}
else {
tip = tipF.format(8);
}
if (tip.length > 0){
var area = o.closest(".formTbl");
if (area.find(".__CheckPwdStrengthTip").length < 1) {
area.prepend("<div class='staticInfoHint __CheckPwdStrengthTip'><p>"+tip+"</p></div>");
}
}
$("#dynamicTip").remove();
o.trigger("focus.dTip");
};
var theCPSObj = this;
this.pwdObj.bind("keyup.pwdStrength", function(){
var v = $(this).val();
var r = theCPSObj.checkStrength($(this), v);
theCPSObj.showResult($(this), r);
}).bind("focus.pwdStrength", function(){
theCPSObj.showTip($(this));
});
}
function wlanDisableControl(funcID){
if(ssidConf.disable != undefined){
if(ssidConf.disable == "all" || ssidConf.disable.indexOf(funcID) != -1){
var Head = $("#"+funcID);
Head.find("input[id!=''],select[id!='']").attr("disabled","disabled");
Head.find(".Button").addClass("disableBtn");
Head.find(".instDelete,.instNew").off("click");
}
}
}
function speed_change_auto(accessType, speeddata) {
var speeddata = parseInt(speeddata);
if (accessType === 'wlan') {
if (speeddata < 1000) {
speeddata = Number(speeddata).toFixed(0) + 'bps ';
} else if (speeddata >= 1000 && speeddata < 1000000) {
speeddata = Number(speeddata / 1000).toFixed(0) + 'Kbps ';
} else if (speeddata >= 1000000 && speeddata < 1000000000) {
speeddata = Number(speeddata / 1000 / 1000).toFixed(0) + 'Mbps ';
} else if (speeddata >= 1000000000) {
speeddata = Number(speeddata / 1000 / 1000 / 1000).toFixed(0) + 'Gbps ';
}
} else if (accessType === 'eth') {
var tmp = speeddata/1000;
if (tmp < 1000) {
tmp = tmp + 'bps ';
} else if (tmp >= 1000 && tmp < 1000000) {
tmp = Number(tmp / 1000).toFixed(0) + 'Kbps ';
} else if (tmp >= 1000000) {
tmp = Number(tmp / 1000 / 1000).toFixed(0) + 'Mbps ';
}
speeddata = tmp;
}
return speeddata;
}
function bps_speed_change_auto(speeddata) {
var speeddata = parseInt(speeddata);
if (speeddata < 1000) {
speeddata = Number(speeddata).toFixed(0) + 'bps ';
} else if (speeddata >= 1000 && speeddata < 1000000) {
speeddata = Number(speeddata / 1000).toFixed(0) + 'Kbps ';
} else if (speeddata >= 1000000) {
speeddata = Number(speeddata / 1000 / 1000).toFixed(0) + 'Mbps ';
}
return speeddata;
}
function disable_all_templte(templateId) {
templateId = "#" + templateId;
$(templateId).find("input,select").disableIt(true);
$(templateId).find(".Btn_cancel,.Btn_apply").disableButton(true);
}
function g_WlanCountryCodeOptionAdd(template)
{
var countryCodeOBJ = $("#CountryCode", template);

var countryCodeEx = "";
var countryCodeTitle = "";
var modiferMode = "";
if(countryCodeEx == "")
{
return;
}
if(modiferMode == "add")
{
var optionStr = "<option value ='"+countryCodeEx+"' title='"+countryCodeTitle+"'>"+countryCodeTitle+"</option>";
countryCodeOBJ.append(optionStr);
}
else if (modiferMode == "replace")
{
$("option",countryCodeOBJ).each(function(index,item){
if(this.value == countryCodeEx )
{
this.title = countryCodeTitle;
this.text = countryCodeTitle;
return false;
}
else if(this.title == countryCodeTitle)
{
this.value = countryCodeEx;
return false;
}
});
}
}
function groupBtnChange(template)
{
}
function initial_CheckBox()
{
}



$(document).ready(function(){
initial_sceneTip();
initial_CollapsibleBar();
initial_addInstLink();
initial_CheckBox();
initial_QueryAccessDeviceLink();
initial_TimeCtl();
$(".HeadDIV").each(function(){
var Head = $(this);
var HeadID = Head.attr("id");
var template = $("#template_"+HeadID,Head);
var formOBJ = $("form",Head);
if ( ! formOBJ.attr("onsubmit") )
{
formOBJ.attr("onsubmit", "return false;");
}
var stopFormAutoSubmitStr = "<input type='text' id='_stopFormAutoSubmit'"
+" value='' class='PostIgnore'"
+" style='display:none;'>";
formOBJ.prepend(stopFormAutoSubmitStr);
initial_button("Apply", Head);
initial_button("Cancel", Head);
initial_button("Delete", Head);
initialCtrlAllLink(Head);
initial_special_password(Head);
var collapsibleInstObj = $(".collapsibleInst",template);
collapsibleInstObj.unbind("click");
collapsibleInstObj.click(function(event){
var collapsibleInst = $(this);
var template = collapsibleInst.parents("[id^='template_']");
var ChangeArea = $(".ChangeArea",template);
if ( ChangeArea.is(":hidden") )
{
ChangeArea.show();
collapsibleInst.addClass("instNameExp");
groupBtnChange(ChangeArea);
ChangeArea.attr("aria-live","polite");
}
else
{
ChangeArea.hide();
collapsibleInst.removeClass("instNameExp");
ChangeArea.attr("aria-live","off");
$(".Btn_cancel",ChangeArea).click();
}
});
$(".utf8Compatible", template).each(function(){
var thisObj = $(this);
var dTip = thisObj.text();
var dTipArr = dTip.split("");
var firstNum = "";
var secNum = "";
var firstNumStart = "";
var firstNumEnd = "";
var secNumStart = "";
var secNumEnd = "";
var Nums = 0;
var newTip = "";
dTipArr = $.grep(dTipArr, function(n,i){
return n != " ";
});
dTip = dTipArr.join("");
for(var i=0; i<dTipArr.length; i++)
{
if (Nums > 2)
{
thisObj.remove();
break;
}
if (isNaN(dTipArr[i]) == false)
{
if (firstNumStart == "")
{
firstNumStart = i;
firstNumEnd = parseInt(i)+1;
Nums += 1;
}
else
{
if (secNumStart == "")
{
if (firstNumEnd == i)
{
firstNumEnd = parseInt(i)+1;
}
else
{
secNumStart = i;
secNumEnd = parseInt(i)+1;
Nums += 1;
}
}
else
{
if (secNumEnd == i)
{
secNumEnd = parseInt(i)+1;
}
else
{
Nums = 3;
}
}
}
}
}
if (firstNumStart != "" && secNumStart != "")
{
firstNum = dTip.slice(firstNumStart, firstNumEnd);
secNum = dTip.slice(secNumStart, secNumEnd);
newTip = dTip.slice(0, firstNumStart)+" ";
if (parseInt(secNum) < 3)
{
var prevObjId = thisObj.prev().attr("id");
alert("Element[id='"+prevObjId+"']'s length range ["+ firstNum+","+secNum+"] will be invalid after utf-8 transforming!");
}
else
{
firstNum = Math.ceil(parseInt(firstNum) / 3);
secNum = Math.floor(parseInt(secNum) / 3);
if (firstNum < secNum)
{
firstNum=reformString(firstNum.toString(), 3);
secNum=reformString(secNum.toString(), 3);
newTip += firstNum + " ~ " + secNum;;
}
else if (firstNum == secNum)
{
secNum=reformString(secNum.toString(), 3);
newTip += secNum;
}
else
{
var prevObjId = thisObj.prev().attr("id");
alert("Element[id='"+prevObjId+"']'s length range ["+firstNum+","+secNum+"] is invalid after utf-8 transforming!");
}
}
}
else
{
thisObj.remove();
}
if (newTip != "")
{
thisObj.text(newTip);
}
});
template.on("focus.dTip","input[type='text'],input[type='password']", function(){
var thisObj = $(this);
if (thisObj.attr("readonly")) {
return;
}
var msg = thisObj.next("span").not(".__CheckPwdStrength").text();
if (msg != "")
{
var pos = thisObj.offset();
var objWidth = thisObj.width();
var dhtml = "<div id='dynamicTip'><div id='dTip_l'></div>"
+ "<div id='dTip_m'>"
+ msg
+ "</div><div id='dTip_r'></div></div>";
var dtObj = $(dhtml).css({top:(pos.top-33)+'px',left:(pos.left+objWidth+8)+'px'});
dtObj.appendTo('body').fadeIn(400);
thisObj.bind("blur.dTip",function(){
dtObj.remove();
});
}
var fObj = $(":focus");
var tObj = $("#dynamicTip");
if ( (tObj.length > 0) && (fObj.attr("id") != thisObj.attr("id")) )
{
tObj.remove();
}
});
$("input.ip,input.mac", template).each(function(){
var InputOBJ = $(this);
InputOBJ.unbind("keydown");
InputOBJ.unbind("keyup");
InputOBJ.keydown(function(event){
autoJumpBack(this,this.value,event);
});
InputOBJ.keyup(function(event){
FocusAutoJump(this,this.value,event);
});
});
$(".instSwitch input",template).each(function(){
var InputOBJ = $(this);
if (InputOBJ.attr("type") == "radio")
{
InputOBJ.unbind("change");
InputOBJ.change(function(event){
var template = $(this).parents("[id^='template_']");
var ChangeArea = $(".ChangeArea",template);
var _InstIDName = "_InstID";
var _InstIDValue = template.find("[id^='_InstID']").val();
var luquidObjUl = $("._LuQUID_CONFIG_OBJID", Head);
var objId = $("li", luquidObjUl).eq(0).text();
if ( _InstIDValue == undefined )
{
var instId = objId + "\\._OBJ_InstID";
_InstIDValue = $("[id^='"+ instId +"']",template).val();
_InstIDName = objId + "._OBJ_InstID";
}
if ( ChangeArea.is(":hidden")
&& _InstIDValue != "-1" )
{
var ServerAddr = template.parents(".HeadDIV").find("address span").text();
var instSwitchName = colonStripping(InputOBJ.attr("name"));
var instSwitchValue = InputOBJ.val();
var PostData = "IF_ACTION=Apply"+"&"
+ instSwitchName+"="+instSwitchValue+"&"
+ _InstIDName+"=" + _InstIDValue;
var actionType = "InstSwitch";
var PostSuccHandler = "fillDataByInstSwitchResult";
dataPost(actionType, PostSuccHandler, ServerAddr, template, PostData);
}
});
}
});
template.unbind("fillDataByInstSwitchResult");
template.bind("fillDataByInstSwitchResult", function(event,xml, template){
if ( template.hasError(xml) == 0 )
{
return;
}
$(".ChangeArea",template).showIt(true);
$(".collapsibleInst",template).addClass("instNameExp");
});
template.unbind("fillDataByDeleteResult");
template.bind("fillDataByDeleteResult", function(event,xml, template){
if ( template.hasError(xml) == 0 )
{
template.remove();
}
else
{
$(".ChangeArea",template).showIt(true);
}
});
initialStatusArea(Head);
initialConfigArea(Head);
});
$("[id^='AreaHideAttr']").each(function(){
var HideAttr = $(this);
var HeadID = $(this).next().next().attr("id") || $(this).next().attr("id");
var template = $("#template_"+HeadID);
if (HideAttr.html() == 4){
template.find("*").attr("disabled",true).attr("hideattr",true);
$("[class^='Button']", template).addClass("disableBtn");
$("[class^='longBtn']", template).addClass("disableBtn");
$("[class^='instDelete Btn_delete']").remove();
$("[class^='addInstBar AddContentContainer']").remove();
$("[id^='Btn_cancel_'],[id^='Btn_apply_']", template).unbind();
$("[class^='Button Btn_refresh']").removeClass("disableBtn").attr("disabled",false);
}
});
});


function LanguageSwitch(nowLanguage, nowStatus)
{
var changeLanguage = "";
if ( "English" == nowLanguage)
{
changeLanguage = "Portuguese";
}
else
{
changeLanguage = "English";
}
showWaitTip(true);
if (nowStatus == "showloginPage")
{
_sessionTmpToken = $("#_sessionTOKEN").val();
}
$.post( "/?_type=hiddenData&_tag=switchlang_entry", {IF_LanguageSwitch:changeLanguage, _sessionTOKEN:_sessionTmpToken}, undefined, "json" )
.done(function( data ) {
if ( data.need_refresh )
{
top.location.href = top.location.href;
}
else
{
alert("Esta página expirou, por favor, atualize e tente novamente. ");
showWaitTip(false);
}
});
}
var UpdateTimeTimerID;
function UpdateCurrTime()
{
var CurrTimeObj = $("#_DevCurrTime");
var CurrTimeDiv = $("#timeArea");
CurrTimeObj.succfunction = function(xml){
if (CurrTimeDiv.hasError(xml,"_noExist") == 0)
{
var currTimeByXML = "";
$(xml).find('ParaName').each(function(){
var tmp = $(this);
if ( tmp.text() == "CurrentLocalTime" )
{
currTimeByXML = tmp.next().text();
return false;
}
});
if(typeof(customTimeStyle) == "function")
{
customTimeStyle(CurrTimeObj, currTimeByXML, "template");
}
else
{
var timeStr = timeTranslate(currTimeByXML);
if ( currTimeByXML != "")
{
var SecTimeLocation = currTimeByXML.lastIndexOf(":");
var currTimeNotSec = currTimeByXML.substring(0, SecTimeLocation);
CurrTimeObj.text(currTimeNotSec);
}
}
}
};
CurrTimeObj.failfunction = function(xml){
};
CurrTimeObj.dataTransfer("/?_type=hiddenData&_tag=sntp_data",
"GET",
CurrTimeObj.succfunction,
CurrTimeObj.failfunction,
false);
UpdateTimeTimerID = setTimeout("UpdateCurrTime()", 30*1000);
}
$(document).ready(function(){
var NowNextpage = $("#_NextPageInfo").text();
if(NowNextpage==""){
$("#Qquickset,#Qstate").remove();
}
else if(NowNextpage=="quicksetup"){
$(".wrapper-menu").hide();
$("#qlogout").show();
}
else{
$("#Qstate").hide();
$("#Qquickset").show();
}
if("ONLINE" == "OFFLINE"){
$("#Tstatus").removeClass("success").addClass("error");
}else{
$("#Tstatus").removeClass("error").addClass("success");
}
var TxMax = parseFloat("5");
var TxMin = parseFloat("0.5");
var RxMax = parseFloat("-8");
var RxMin = parseFloat("-27");
if(parseFloat("2.3658") >= TxMin && parseFloat("2.3658") <= TxMax){
$("#TTX").removeClass("error").addClass("success");
}else{
$("#TTX").removeClass("success").addClass("error");
}
if(parseFloat("-16.6354") >= RxMin && parseFloat("-16.6354") <= RxMax){
$("#TRX").removeClass("error").addClass("success");
}else{
$("#TRX").removeClass("success").addClass("error");
}
if("Ativo" == "Deavtive"){
$("#TwlanStat").removeClass("success").addClass("error");
}else{
$("#TwlanStat").removeClass("error").addClass("success");
}
if("100.95.39.42" == ""){
$("#TIPv4").removeClass("success").addClass("error");
}else{
$("#TIPv4").removeClass("error").addClass("success");
}
if("fe80::da9a:dff:fea5:1da8" == "" || "fe80::da9a:dff:fea5:1da8" == "::"){
$("#Tv6LLA").removeClass("success").addClass("error");
}else{
$("#Tv6LLA").removeClass("error").addClass("success");
}
if(("2804:14c:48::194b" == ""||"2804:14c:48::194b" == "::") && ("::" == ""||"::" == "::") && ("::" == ""||"::" == "::")){
$("#Tv6GUA").removeClass("success").addClass("error");
}else{
$("#Tv6GUA").removeClass("error").addClass("success");
}
if("INACTIVE" == "INACTIVE"){
$("#TLine1").removeClass("success").addClass("error");
}else{
$("#TLine1").removeClass("error").addClass("success");
}
if("1" == "2"){
if("" == "INACTIVE"){
$("#TLine2").removeClass("success").addClass("error");
}else{
$("#TLine2").removeClass("error").addClass("success");
}
}
$("#Qstate").unbind("click").bind("click", function(){
openLink("statusMgr");
$(".wrapper-menu").show();
$("#qlogout").hide();
$("#Qstate").hide();
$("#Qquickset").show();
});
$("#Qquickset").unbind("click").bind("click", function(){
openLink("quicksetup");
$(".wrapper-menu").hide();
$("#qlogout").show();
$("#Qstate").show();
$("#Qquickset").hide();
});

FakeClass1MenuShow();

clearTimeout(UpdateTimeTimerID);
var NowStatus = "\x73\x68\x6f\x77\x6c\x6f\x67\x69\x6e\x50\x61\x67\x65";
var IsShowTimeZone = {
'showloginPage' : false,
'showWizardPage' : true,
'showCommonPage' : true
};
if ( !IsShowTimeZone[NowStatus] )
{
$("#timeArea").hide();
}
else
{
$("#timeArea").show();
UpdateCurrTime();
}
var IsShowlogOff = {
'showloginPage' : false,
'showWizardPage' : false,
'showCommonPage' : true
};
if ( !IsShowlogOff[NowStatus] )
{
$("#logOff").hide();
}
var languageButContent = "\x50\x6f\x72\x74\x75\x67\x75\x65\x73\x65";
var languageOBJ = $("#languageSwitch");
var languageModifyOBJ = $("#LanguageModify",languageOBJ);
if ( languageButContent == "English" )
{
languageModifyOBJ.addClass("icon-Pt").removeClass("icon-En");
}
else if ( languageButContent == "Portuguese" )
{
languageModifyOBJ.addClass("icon-En").removeClass("icon-Pt");
}
else
{
}
languageModifyOBJ.click(function(){
var LanguageNow = "\x50\x6f\x72\x74\x75\x67\x75\x65\x73\x65";
LanguageSwitch(LanguageNow, NowStatus);
});
try{
if((templateModify!=undefined) && (typeof(templateModify)=="function")){
templateModify();
}
}catch(e){
}
});
window.onresize = function()
{
if ($("#tipLayer").css("display") != "none")
{
reposition_box("tipLayer");
consoleLog("window reseze!");
}
}
