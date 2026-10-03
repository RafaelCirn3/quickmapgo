const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const {randomUUID}=require('node:crypto');

test('mapa envia um evento por gesto, bloqueia enquanto aguarda e permite repetir ponto',()=>{
  const html=fs.readFileSync('src/quickmapgo/ui/map/index.html','utf8');
  const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
  const messages=[], listeners={}, handlers={};
  const parent={postMessage:message=>messages.push(message)};
  const elements={map:{classList:{toggle(){}}},notice:{}};
  const map={setView(){return this;},removeLayer(){},invalidateSize(){},
    on(name,callback){handlers[name]=callback;}};
  const L={map:()=>map,tileLayer:()=>({addTo(){return this;},on(){}}),
    circleMarker:()=>({addTo(){return this;},bindTooltip(){}})};
  const context={parent,crypto:{randomUUID},L,setTimeout:callback=>callback(),
    document:{getElementById:id=>elements[id],createElement:()=>({})},
    window:{addEventListener:(name,callback)=>{listeners[name]=callback;}}};
  vm.createContext(context);vm.runInContext(script,context);context.startMap();
  const click=()=>handlers.click({latlng:{lat:-7,lng:-34}});
  const render=args=>listeners.message({source:parent,data:{type:'streamlit:render',args}});
  const events=()=>messages.filter(message=>message.type==='streamlit:setComponentValue');
  click();assert.equal(events().length,0);
  render({connected:true});click();click();assert.equal(events().length,1);
  const first=events()[0].value;
  assert.equal(first.latitude,-7);assert.equal(first.longitude,-34);
  render({connected:true,consumed_event:first.event_id});
  click();assert.equal(events().length,2);
  assert.notEqual(events()[1].value.event_id,first.event_id);
});
