(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[8],{QZxW:function(e,t,a){},f0pd:function(e,t,a){"use strict";a.r(t);a("g9YV");var n=a("wCAj"),r=(a("+L6B"),a("2/Rp")),c=(a("miYZ"),a("tsqr")),l=a("KQm4"),i=a("ODXe"),u=a("q1tI"),m=a.n(u),s=a("o0o1"),o=a.n(s),p=a("HaE+"),f=a("t3Un");function d(){return x.apply(this,arguments)}function x(){return x=Object(p["a"])(o.a.mark((function e(){return o.a.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.abrupt("return",Object(f["a"])("/api/sns/v1/lit/experiment/all_experiments",{method:"GET",params:{}}));case 1:case"end":return e.stop()}}),e)}))),x.apply(this,arguments)}function E(e){return b.apply(this,arguments)}function b(){return b=Object(p["a"])(o.a.mark((function e(t){return o.a.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.abrupt("return",Object(f["a"])("/api/sns/v1/lit/experiment/get_experiments",{method:"GET",params:{exp_name:t.exp_name}}));case 1:case"end":return e.stop()}}),e)}))),b.apply(this,arguments)}function y(e){return v.apply(this,arguments)}function v(){return v=Object(p["a"])(o.a.mark((function e(t){return o.a.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.abrupt("return",Object(f["a"])("/api/sns/v1/lit/experiment/set_experiments?exp_name=".concat(t.exp_name),{method:"POST",data:t.data}));case 1:case"end":return e.stop()}}),e)}))),v.apply(this,arguments)}a("14J3");var h=a("BMrR"),_=(a("giR+"),a("fyUT")),w=(a("jCWc"),a("kPKH")),k=(a("y8nQ"),a("Vl3Y")),O=(a("5NDa"),a("5rEg")),j=(a("iB5I"),a("wlus")),I=a("xvlK"),C=[{required:!0}],g=function(e){var t=Object(u["useRef"])(),a=e.name,n=function(e){var t={},n=0;e.experiments.forEach((function(e){t[e.exp_name]=Number(e.exp_value),n+=t[e.exp_name]})),n>100?c["a"].error("\u6bd4\u4f8b\u8bbe\u7f6e\u9519\u8bef"):y({exp_name:a,data:{value_buckets:t}}).then((function(e){e.success&&c["a"].success("\u66f4\u65b0\u6210\u529f")}))};return Object(u["useEffect"])((function(){E({exp_name:a}).then((function(e){e.success&&t.current.setFieldsValue({experiments:e.data.map((function(e){return{exp_name:e[0],exp_value:e[1]}}))})}))}),[]),m.a.createElement(k["a"],{ref:t,onFinish:n,className:"my-form"},m.a.createElement(k["a"].List,{name:"experiments"},(function(e,t){var a=t.add,n=t.remove;return m.a.createElement("div",null,e.map((function(e,t){return m.a.createElement(h["a"],{key:e.key},m.a.createElement(w["a"],null,m.a.createElement(k["a"].Item,{name:[e.name,"exp_name"],fieldKey:[e.fieldKey,"exp_name"],rules:C},m.a.createElement(O["a"],{placeholder:"\u5b9e\u9a8c\u540d\u79f0"}))),m.a.createElement(w["a"],null,m.a.createElement(k["a"].Item,{name:[e.name,"exp_value"],fieldKey:[e.fieldKey,"exp_value"],rules:C,style:{marginLeft:10}},m.a.createElement(_["a"],{min:0,max:100,placeholder:"\u5b9e\u9a8c\u6bd4\u4f8b"}))),m.a.createElement(w["a"],{flex:"none"},m.a.createElement(j["a"],{style:{marginLeft:10},className:"dynamic-delete-button",onClick:function(){n(e.name)}})))})),m.a.createElement(k["a"].Item,null,m.a.createElement(r["a"],{type:"dashed",onClick:function(){a()},style:{width:"20%"}},m.a.createElement(I["a"],null)," \u589e\u52a0\u5b9e\u9a8c")))})),m.a.createElement(k["a"].Item,null,m.a.createElement(r["a"],{type:"primary",htmlType:"submit"},"Submit")))},K=g,R=(a("2qtc"),a("kLXV")),T=(a("QZxW"),function(e){var t=e.visible,a=e.onCreate,n=e.onCancel,r=k["a"].useForm(),c=Object(i["a"])(r,1),l=c[0];return m.a.createElement(R["a"],{visible:t,title:"\u65b0\u589e\u5b9e\u9a8c",okText:"Create",cancelText:"Cancel",onCancel:n,onOk:function(){l.validateFields().then((function(e){l.resetFields(),a(e)})).catch((function(e){console.log("Validate Failed:",e)}))}},m.a.createElement(k["a"],{form:l,layout:"vertical",name:"form_in_modal",initialValues:{modifier:"public"}},m.a.createElement(k["a"].Item,{name:"exp_name",label:"\u5b9e\u9a8c\u540d\u79f0",rules:[{required:!0,message:"Please input the title of collection!"}]},m.a.createElement(O["a"],null)),m.a.createElement(k["a"].Item,{name:"exp_desc",label:"\u5b9e\u9a8c\u63cf\u8ff0"},m.a.createElement(O["a"],{type:"textarea"}))))}),F=T,V=[{title:"\u5b9e\u9a8c\u540d\u5b57",dataIndex:"name",key:"name"},{title:"\u65e5\u671f",dataIndex:"time",key:"time"},{title:"\u5b9e\u9a8c\u5185\u5bb9",dataIndex:"desc",key:"desc"},{title:"Action",dataIndex:"",key:"x",render:function(){return m.a.createElement("a",null,"\u5220\u9664")}}];function q(e){var t=Object(u["useState"])([]),a=Object(i["a"])(t,2),s=a[0],o=a[1],p=Object(u["useState"])(!1),f=Object(i["a"])(p,2),x=f[0],E=f[1];Object(u["useEffect"])((function(){d().then((function(e){e.success&&o(e.data.exp_names.map((function(e){return{name:e,time:"--",desc:"--"}})))}))}),[]);var b=function(e){console.log("Received values of form: ",e),E(!1),y({exp_name:e.exp_name,data:{value_buckets:{default:100}}}).then((function(t){t.success&&(o([].concat(Object(l["a"])(s),[{name:e.exp_name,time:"--",desc:"--"}])),c["a"].success("\u521b\u5efa\u6210\u529f"))}))};return m.a.createElement("div",null,m.a.createElement(r["a"],{type:"primary",onClick:function(){E(!0)},style:{marginBottom:10}},"\u65b0\u589e\u5b9e\u9a8c"),m.a.createElement(F,{visible:x,onCreate:b,onCancel:function(){E(!1)}}),m.a.createElement(n["a"],{columns:V,expandable:{expandedRowRender:function(e){return m.a.createElement(K,{name:e.name})},rowExpandable:function(){return!0}},rowKey:"name",dataSource:s}))}t["default"]=q},iB5I:function(e,t,a){}}]);