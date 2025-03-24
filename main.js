const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { exec } = require('child_process');
const WebSocket = require('ws');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

//backend
ipcMain.on('run-script', (event, arg) => {
    const pythonScriptPath = path.join(__dirname, 'python_backend', 'process_csv.py');
    exec(`python "${pythonScriptPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
    });
});

//websocket
const wss = new WebSocket.Server({ port: 8000 });

wss.on('connection', ws => {
    ws.on('message', message => {
        console.log(`Received message: ${message}`);
        mainWindow.webContents.send('update-block-status', message);
    });
});
