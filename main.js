const { app, BrowserWindow, Tray, protocol, screen } = require("electron");
const path = require("path");

let mainWindow;
let tray;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 600,
    show: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
    },
  });

  mainWindow.loadFile(path.join(__dirname, "bartools.html"));

  const { width } = screen.getPrimaryDisplay().workAreaSize;
  const x = width - (mainWindow.getBounds().width - 20);
  const y = 0;
  mainWindow.setPosition(x, y);
  mainWindow.webContents.openDevTools();


  mainWindow.on("close", function (event) {
    if (app.quitting) {
      mainWindow = null;
    } else {
      event.preventDefault();
      mainWindow.hide();
    }
  });

  mainWindow.on("activate", () => {
    if (mainWindow === null) {
      createWindow();
    } else {
      mainWindow.show();
    }
  });

  mainWindow.once("ready-to-show", () => {
    // Agregar el ícono a la barra de notificaciones
    const iconPath = path.join(__dirname, "icon_bartool.png"); // Reemplaza 'path-to-your-icon.png' con la ruta a tu icono
    tray = new Tray(iconPath);
    tray.setToolTip("GPT CLI");

    // Maneja el evento click para mostrar el microfono
    tray.on("click", () => {
      mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
    });

    // Manejar doble clic en el ícono para mostrar/ocultar la ventana
    tray.on("double-click", () => {});
  });
}

app.on("ready", () => {
  createWindow();

  // Configuración para ocultar la aplicación en el dock en macOS
  if (process.platform === "darwin") {
    app.dock.hide();

    protocol.registerFileProtocol("app", (request, callback) => {
      const url = request.url.replace("app://", "");
      callback({ path: path.normalize(`${__dirname}/${url}`) });
    });

    app.setAsDefaultProtocolClient("app");
  }
});

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.exit();
});

app.on("activate", function () {
  if (mainWindow === null) createWindow();
});

// Manejar el evento 'before-quit' para limpiar la bandeja
app.on("before-quit", () => {
  tray.destroy();
});
