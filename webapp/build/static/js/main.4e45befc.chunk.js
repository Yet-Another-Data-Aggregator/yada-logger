(this.webpackJsonpwebapp=this.webpackJsonpwebapp||[]).push([[0],{37:function(e,n,t){},39:function(e,n,t){},45:function(e,n,t){"use strict";t.r(n);var c=t(0),r=t.n(c),s=t(13),a=t.n(s),o=(t(37),t(12)),i=t.n(o),l=t(16),u=(t(39),t(29)),j=t(68),f=t(63),d=t(69),h=t(64),b=t(65),p=t(66),x=t(67),O=t(5);function g(){var e=Object(c.useState)([]),n=Object(u.a)(e,2),t=n[0],r=n[1];return Object(O.jsxs)(h.a,{children:[Object(O.jsx)(b.a,{className:"w-1/2 border",children:function(e){return console.log(e),e&&e.length>0?Object(O.jsx)("div",{children:e.map((function(e,n){return Object(O.jsxs)(j.a,{className:"border",children:[Object(O.jsx)(f.a,{children:Object(O.jsx)(x.a,{})}),Object(O.jsx)(d.a,{className:"flex justify-center",primary:e.ssid})]},n)}))}):Object(O.jsx)("div",{children:Object(O.jsx)(j.a,{className:"border",children:Object(O.jsx)(d.a,{className:"flex justify-center",primary:"Didn't find any networks."})})})}(t)}),Object(O.jsx)(p.a,{onClick:function(){fetch("/ping").then(function(){var e=Object(l.a)(i.a.mark((function e(n){var t;return i.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,n.json();case 2:t=e.sent,alert(t.data),console.log(t.data);case 5:case"end":return e.stop()}}),e)})));return function(n){return e.apply(this,arguments)}}()).catch((function(e){console.log("Something went wrong: "+e)}))},children:"Ping"}),Object(O.jsx)(p.a,{onClick:function(){fetch("/rescan_wifi").then(function(){var e=Object(l.a)(i.a.mark((function e(n){var c;return i.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,n.json();case 2:c=e.sent,r(c.scan_results),console.log("Success Getting Wifi Networks"),console.log(c),console.log(t),console.log(c.scan_results);case 8:case"end":return e.stop()}}),e)})));return function(n){return e.apply(this,arguments)}}()).catch((function(e){console.log("ERROR:"+e)}))},children:"Refresh"})]})}var m=function(){return Object(O.jsx)("div",{className:"App",children:Object(O.jsx)(g,{})})},w=function(e){e&&e instanceof Function&&t.e(3).then(t.bind(null,70)).then((function(n){var t=n.getCLS,c=n.getFID,r=n.getFCP,s=n.getLCP,a=n.getTTFB;t(e),c(e),r(e),s(e),a(e)}))};a.a.render(Object(O.jsx)(r.a.StrictMode,{children:Object(O.jsx)(m,{})}),document.getElementById("root")),w()}},[[45,1,2]]]);
//# sourceMappingURL=main.4e45befc.chunk.js.map