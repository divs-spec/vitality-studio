// preload placeholder - expose safe APIs later
const { contextBridge } = require('electron')

contextBridge.exposeInMainWorld('vitality', {
  // future: add ipc methods here
})
