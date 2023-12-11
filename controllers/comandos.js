const path = require("path");
const dbPath = path.join(__dirname, "./libs/console/0x0000000A12FDFD.db");
const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database(dbPath);
const { spawn } = require("child_process");

let start_services = null;

function toToast(mensaje){
  var myToastEl = document.getElementById('toastalarm')
  var myToastElText = document.getElementById('textalarm')
  myToastElText.innerHTML = mensaje
  myToastEl.classList.add("show")
}
function closeToast(){
  var myToastEl = document.getElementById('toastalarm')
  var myToastElText = document.getElementById('textalarm')
  myToastElText.innerHTML = ""
  myToastEl.classList.remove("show")
}

function iniciarServicios() {
  // Detener el proceso si ya está en ejecución
  if (start_services) {
    start_services.kill();
    toToast("La actualización del estado de los comandos puede tardar. Si desea hacerlo inmediato se recomienda cerrar la app")
  }

  // Iniciar el proceso nuevamente
  start_services = spawn("python3", ["./libs/console/init.py"]);

  start_services.stdout.on("data", (data) => {
    console.log("Servicios iniciados");
  });

  start_services.stderr.on("data", (data) => {
    console.log(data);
  });

  start_services.on("close", (code) => {
    console.log(code);
  });

  start_services.on("exit", (code, signal) => {
    if(!code && !signal){
      console.log("Actualizado");
    }
  });
}

iniciarServicios();

function cerrarTodosLosModales() {
  // Obtener todos los modales abiertos
  var modalesAbiertos = document.querySelectorAll(".modal.show");

  // Cerrar cada modal usando el método modal de Bootstrap
  modalesAbiertos.forEach(function (modal_) {
    var modalInstance = bootstrap.Modal.getInstance(modal_);

    if (modalInstance) {
      modalInstance.hide();
    }
  });
}

function crearNuevoComandos() {
  const nombre = document.getElementById("nombre").value;
  const comando = document.getElementById("comando").value;
  const estado = 1;

  if (nombre && comando !== null) {
    db.run(
      "INSERT INTO comandos (nombre, comando, estado) VALUES (?, ?, ?)",
      [nombre, comando, estado],
      (err) => {
        if (err) {
          console.error(err);
        } else {
          renderTableComandos(); // Actualizar la tabla después de crear
          document.getElementById("crearModal").classList.remove("show"); // Cerrar modal
        }
      }
    );
  }
}

function guardarEdicionComandos() {
  const id = document.getElementById("editId").value;
  const nombre = document.getElementById("editNombre").value;
  const comando = document.getElementById("editComando").value;
  const estado = document.getElementById("editEstado").value;

  if (id && nombre && comando && estado !== null) {
    db.run(
      "UPDATE comandos SET nombre=?, comando=?, estado=? WHERE id=?",
      [nombre, comando, estado, id],
      (err) => {
        if (err) {
          console.error(err);
        } else {
          renderTableComandos(); // Actualizar la tabla después de editar
          cerrarTodosLosModales();
          iniciarServicios();
        }
      }
    );
  }
}

function traerHistorial() {
  cerrarTodosLosModales();
  const id = document.getElementById("editId").value;
  const historyautomat = document.getElementById("historyautomat");
  historyautomat.value = "";
  db.all("SELECT * FROM respuestas WHERE id_comando = " + id, (err, rows) => {
    if (err) {
      console.error(err);
      return;
    }

    rows.forEach((row) => {
      historyautomat.value += `\n\nConsola:\n${row.consulta}\nRespuesta automatica:\n${row.respuesta}`;
    });
  });
}

function finalizarAutomatizacion() {
  let automatconsole = document.getElementById("automatconsole");
  let automatresponse = document.getElementById("automatresponse");
  let automatbutton = document.getElementById("automatbutton");
  const advertencyautomat = document.getElementById("advertencyautomat");
  const formautomat = document.getElementById("formautomat");
  advertencyautomat.classList.remove("d-none");
  formautomat.classList.add("d-none");
  automatconsole.value = "";
  automatresponse.value = "";
  automatresponse.disabled = true;
  automatbutton.disabled = true;
  iniciarServicios();
  cerrarTodosLosModales();
}

function automatizarRespuestas() {
  const advertencyautomat = document.getElementById("advertencyautomat");
  const formautomat = document.getElementById("formautomat");
  let automatconsole = document.getElementById("automatconsole");
  let automatresponse = document.getElementById("automatresponse");
  let automatbutton = document.getElementById("automatbutton");

  automatbutton.innerHTML =
    'Esperando consola <div class="spinner-border" style="width: 12px; height: 12px" role="status"><span class="visually-hidden">Loading...</span></div>';
  advertencyautomat.classList.add("d-none");
  formautomat.classList.remove("d-none");

  const id = document.getElementById("editId").value;
  const nombre = document.getElementById("editNombre").value;
  const comando = document.getElementById("editComando").value;
  const estado = document.getElementById("editEstado").value;

  if (id && nombre && comando && estado !== null) {
    start_service_automatizar = spawn("python3", [
      "./libs/console/automatizar.py",
      "-idcommand",
      id,
    ]);

    start_service_automatizar.stdout.on("data", (data) => {
      automatresponse.value = "";
      let string_data = `${data}`;
      if (!automatconsole.value.includes(string_data) && string_data != "[3J[H[2J") {
        automatconsole.value += `${string_data}\n`;
        automatconsole.scrollTop = automatconsole.scrollHeight;
        automatresponse.disabled = false;
        automatbutton.disabled = false;
        automatbutton.innerHTML = "Responder";

        automatbutton.addEventListener("click", function () {
          automatresponse.disabled = true;
          automatbutton.disabled = true;
          if (automatresponse.value.length) {
            start_service_automatizar.stdin.write(automatresponse.value + "\n");
          } else {
            start_service_automatizar.stdin.write("\n");
          }
        });
      }
    });

    start_service_automatizar.stderr.on("data", (data) => {
      console.log(data);
    });

    start_service_automatizar.on("close", (code) => {
      console.log(code);
    });
  }
}

function renderTableComandos() {
  const table = document
    .getElementById("comandosTable")
    .getElementsByTagName("tbody")[0];
  table.innerHTML = ""; // Limpiar el cuerpo de la tabla

  db.all("SELECT * FROM comandos", (err, rows) => {
    if (err) {
      console.error(err);
      return;
    }

    rows.forEach((row) => {
      const rowHtml = `
              <tr>
                  <td>${row.id}</td>
                  <td>${row.nombre}</td>
                  <td class="text-truncate" style="max-width: 220px">${
                    row.comando
                  }</td>
                  <td>${row.estado ? "Activo" : "Deshabilitado"}</td>
                  <td class="row">
                      <div class="col-6">
                        <button class="btn btn-primary btn-sm w-100" data-bs-toggle="modal" data-bs-target="#editarModal" onclick="editRow(${
                          row.id
                        }, '${row.nombre}', '${row.comando}', ${row.estado})">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                          </svg>
                        </button>
                      </div>
                      <div class="col-6">
                        <button class="btn btn-danger btn-sm w-100" onclick="deleteRow(${
                          row.id
                        })">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                          </svg>
                        </button>
                      </div>
                  </td>
              </tr>
          `;
      table.innerHTML += rowHtml;
    });
  });
}

function editRow(id, nombre, comando, estado) {
  // Llena el formulario de edición con los datos actuales
  document.getElementById("editId").value = id;
  document.getElementById("editNombre").value = nombre;
  document.getElementById("editComando").value = comando;
  document.getElementById("editEstado").value = estado;
}

function deleteRow(id) {
  const confirmDelete = confirm(
    "¿Está seguro de que desea eliminar este registro?"
  );

  if (confirmDelete) {
    db.run("DELETE FROM comandos WHERE id=?", [id], (err) => {
      if (err) {
        console.error(err);
      } else {
        renderTableComandos(); // Actualizar la tabla después de eliminar
      }
    });
  }
}
