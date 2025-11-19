let syncInProgress = false;

// Objeto global para controlar las cards por empleado
const asistenciaHoy = {};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Renderiza todas las cards de asistencia
function renderAsistenciaHoy(empleados) {
    const contenedor = document.getElementById("asistencia-hoy-list");
    if (!contenedor) return;

    empleados.forEach(emp => {
        // Si la card ya existe, actualizamos
        if (asistenciaHoy[emp.employee_id]) {
            const card = asistenciaHoy[emp.employee_id];
            card.querySelector('.entrada').textContent = emp.entrada || '— Sin registro —';
            card.querySelector('.salida').textContent = emp.salida || '— Sin registro —';
        } else {
            // Crear nueva card
            const div = document.createElement('div');
            div.classList.add('card', 'mb-2');
            div.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">${emp.nombre} ${emp.apellido}</h5>
                    <p class="card-text">
                        <strong>DNI:</strong> ${emp.dni || "N/A"} <br>
                        <strong>Cargo:</strong> ${emp.cargo || "N/A"} <br>
                        <strong>Entrada:</strong> <span class="entrada">${emp.entrada || '— Sin registro —'}</span> <br>
                        <strong>Salida:</strong> <span class="salida">${emp.salida || '— Sin registro —'}</span>
                    </p>
                </div>
            `;
            contenedor.appendChild(div);
            asistenciaHoy[emp.employee_id] = div;
        }
    });
}

// Carga la asistencia del día desde la API
async function cargarAsistenciaHoy() {
    try {
        const response = await fetch('/api/asistencia-hoy/');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (data.exito && Array.isArray(data.empleados)) {
            renderAsistenciaHoy(data.empleados);
        }
    } catch (error) {
        console.error("[v0] Error cargando asistencia:", error);
    }
}

// Sincroniza los datos desde ZKTeco
async function sincronizar() {
    if (syncInProgress) return;
    syncInProgress = true;

    console.log("[v0] Iniciando sincronización...");
    try {
        const response = await fetch('/api/sync_zkteco/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const txt = await response.text().catch(() => '');
            console.error(`[v0] Error HTTP ${response.status}:`, txt || '(sin cuerpo)');
            return;
        }

        const data = await response.json();
        console.log("[v0] Respuesta de sincronización:", data);

        if (data.exito && Array.isArray(data.empleados)) {
            renderAsistenciaHoy(data.empleados);
        }

    } catch (error) {
        console.error("[v0] Error en sincronizar():", error);
    } finally {
        syncInProgress = false;
    }
}

window.addEventListener('load', () => {
    cargarAsistenciaHoy();

    const syncBtn = document.getElementById('syncBtn');
    if (syncBtn) syncBtn.addEventListener('click', sincronizar);
});