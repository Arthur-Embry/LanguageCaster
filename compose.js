/*    <script src="lib/src-min-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
    <script src="lib/src-min-noconflict/ext-language_tools.js"></script>
    <script src="lib/base64.js"></script>
    <script src="x86Reference/ref.js"></script>
    <script src="https://togetherjs.com/togetherjs-min.js"></script>
    <script defer src="//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular.min.js"></script>
    <script defer src="//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-animate.min.js"></script>
    <script defer src="//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-aria.min.js"></script>
    <script defer src="//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-messages.min.js"></script>
    <script defer src="//ajax.googleapis.com/ajax/libs/angular_material/1.1.0-rc2/angular-material.min.js"></script>
    <script defer src="config.js"></script>
    <script defer src="v2.js"></script>
    <script defer src="examples.js"></script>
    <script src="injection.js"></script> */
/*load the scripts*/

function loadScript(url)
{    
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    head.appendChild(script);
}
function loadDeferedScript(url)
{    
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.defer = true;
    script.src = url;
    head.appendChild(script);
}
loadScript("lib/src-min-noconflict/ace.js");
loadScript("lib/src-min-noconflict/ext-language_tools.js");
loadScript("lib/base64.js");
loadScript("x86Reference/ref.js");
loadScript("https://togetherjs.com/togetherjs-min.js");
loadDeferedScript("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular.min.js");
loadDeferedScript("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-animate.min.js");
loadDeferedScript("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-aria.min.js");
loadDeferedScript("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-messages.min.js");
loadDeferedScript("//ajax.googleapis.com/ajax/libs/angular_material/1.1.0-rc2/angular-material.min.js");
loadDeferedScript("config.js");
loadDeferedScript("v2.js");
loadDeferedScript("examples.js");
//append a div to the head
var div = document.createElement("div");
div.id = "injected";
div.style = "position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); z-index: 9999;";
document.head.appendChild(div);
div.innerHTML=`
<div style="display: none;" ng-app="WasmExplorerApp" ng-cloak layout="column" ng-controller="WasmExplorerAppCtrl as vm">
<md-button ng-click="vm.share($event)" id="execute_script" class="md-raised" style="margin-left: -3px; width: 100%">Create a Persistent Link</md-button>
<div flex id="sourceCodeContainer"></div>
<div id="wastCodeContainer" flex></div>
<div flex id="assemblyCodeContainer"></div>
<div flex id="llvmAssemblyCodeContainer"></div>
<div style="height: 200px" id="consoleContainer" ng-show="vm.showConsole"></div>
<a id="downloadLink" href="" download="test.wasm" data-uncompiled="test"></a>
</div>
`
function checkLoaded() {
    return document.readyState === "complete" || document.readyState === "interactive";
}
async function _base64ToArrayBuffer(base64) {
    var binary_string = window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}
async function cpp(code){
while(!checkLoaded()){
    await new Promise(r => setTimeout(r, 100));
}
wasm = await fetch(await uri_cpp(code));
base64=wasm.url.split(",")[1]
buffer = await _base64ToArrayBuffer(base64)
module = await WebAssembly.compile(buffer)
instance = await new WebAssembly.Instance(module)
return instance;
}
async function uri_cpp(code){
    document.querySelector("#downloadLink").setAttribute("data-uncompiled",code)
    document.querySelector("#execute_script").click();
    for(let i=0;i<100;i++){
      if(document.getElementById('downloadLink').href == document.location) {
          await new Promise(r => setTimeout(r, 100));
        } else {
          cache=document.getElementById("downloadLink").href
          document.getElementById('downloadLink').href = document.location;
          return cache;
        }
    }

}
