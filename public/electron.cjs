const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const fs = require('fs');
const csv = require('csv-parser');
const { wake } = require('wake_on_lan');

function createWindow() {
  // Create the browser window
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.cjs')
    },
    icon: path.join(__dirname, 'icon.png') // Optional: add an icon
  });

  // Load the app
  mainWindow.loadURL(
    isDev
      ? 'http://localhost:5173'
      : `file://${path.join(__dirname, '../build/index.html')}`
  );

  // Open DevTools in development
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  // Set Content Security Policy for security
  mainWindow.webContents.session.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': ["default-src 'self' 'unsafe-inline' 'unsafe-eval' data: http: https:"]
      }
    });
  });
}

// Create window when app is ready
app.whenReady().then(createWindow);

// Quit when all windows are closed
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

// IPC handlers
ipcMain.handle('read-csv', async () => {
  try {
    const csvPath = path.join(process.cwd(), 'list.csv');
    const results = [];
    
    return new Promise((resolve, reject) => {
      fs.createReadStream(csvPath)
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => resolve(results))
        .on('error', (error) => reject(error));
    });
  } catch (error) {
    console.error('Error reading CSV:', error);
    throw error;
  }
});

ipcMain.handle('wake-pc', async (event, macAddress) => {
  try {
    await wake(macAddress, {
      address: '192.168.0.255',
      port: 9
    });
    console.log(`Magic packet sent to ${macAddress}`);
    return { success: true };
  } catch (error) {
    console.error(`Error sending magic packet to ${macAddress}:`, error);
    throw error;
  }
}); 